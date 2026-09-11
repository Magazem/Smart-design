#!/usr/bin/env python3
"""Build the distributable skill ZIP. Stdlib only. Used by CI and dev alike.

Usage:
    python3 build_zip.py                    # real build - fails if data/schema-manifest.json is missing/invalid
    python3 build_zip.py --allow-empty-data  # dev build - skips the data-validation gate, tags the filename -dev

This is the single place that knows how to turn the skill source tree into
the ZIP claude.ai actually accepts, so CI (.github/workflows/release.yml) and
a developer's local machine cannot drift into building it two different ways.
CI never passes --allow-empty-data - a tag build with no valid schema-manifest.json
is exactly the "no artifact on bad data" failure release.yml is designed to produce
(research/11-upstream-releases.md §5's upstream failure mode: a broken release
shipping anyway because nothing gated it).

STEPS, IN ORDER:
  1. Validate: run validate_data.py's own `validate()` function against
     data/ (not a subprocess - imported directly, so a failure here is a
     real Python exception path, not a shelled-out exit-code guess). Skipped
     entirely under --allow-empty-data.
  2. Read VERSION (a single line in <skill-dir>/VERSION).
  3. Stamp `<!-- version: X (generated at build - do not edit) -->` as the
     first line of SKILL.md's body, immediately after the closing `---` of
     the YAML frontmatter (never before it - claude.ai requires SKILL.md to
     start with `---`), idempotently - a second build run replaces the
     previous stamp rather than stacking another one on top.
  4. Zip <skill-dir>/ with the skill folder itself as the ZIP root (the
     claude.ai upload rule - see research/04-packaging.md §1.3: the archive's
     root must be exactly one directory, matching the skill's own name, with
     SKILL.md directly inside it). Arcnames are always constructed with
     `.as_posix()`, never the OS path separator, so a Windows build never
     emits a backslash into the archive - zipfile doesn't do this
     automatically if you pass a bare Path/str, which is why this is
     explicit rather than assumed. Every text member's line endings are
     normalised to LF on the way into the archive, regardless of the
     working copy's own line endings (this repo's checkout is CRLF).
  5. Exclude: any path component named `__pycache__` or `tests`, any file
     named `.gitkeep`, any installed-brand state under `data/brand/`
     (a brand overlay dir `data/brand/<slug>/...`, or `active.json` -
     both are a user's own data and must never ship inside the public ZIP;
     `data/brand/`'s own documentation, README.md, still ships), and
     anything matched by <skill-dir>/../.gitignore's patterns (a small
     subset of real gitignore semantics - directory-name patterns ending
     in `/` and `*.ext`-style suffix globs via `fnmatch`; good enough for
     this project's own 3-line .gitignore, not a general gitignore
     parser).
  6. Refuse to build if any file under the skill directory is a symlink -
     this project's own design principle (research/04-packaging.md §3: "no
     symlinks in our repo") is enforced here mechanically, not left as a
     convention someone can forget.
  7. Write to <skill-dir>/../dist/<skill-name>-<version>.zip (creating
     dist/ if needed) and print the member list, file count, and total size.
  8. Print a constraint-check summary: ZIP root shape, SKILL.md
     name/description presence and description length against the
     1,024-character upload limit (research/04-packaging.md §1.2,
     confirmed by direct test - see references/activation.md), and the
     symlink check's result. This is intentionally printed on every build,
     not just this task's one-off report, so drift shows up immediately.
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_ROOT = SKILL_DIR.parent

EXCLUDED_DIR_NAMES = {"__pycache__", "tests", ".pytest_cache"}
EXCLUDED_FILE_NAMES = {".gitkeep"}

_VERSION_STAMP_RE = re.compile(r"^<!--\s*version:.*-->\s*\n?", re.IGNORECASE | re.MULTILINE)
_FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def load_gitignore_patterns(repo_root: Path) -> list[str]:
    gi = repo_root / ".gitignore"
    if not gi.is_file():
        return []
    patterns = []
    for line in gi.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


#: data/brand/'s own top-level files that are documentation, not user brand
#: state, and so are the only things under data/brand/ that still ship.
BRAND_DIR_DOC_FILES = {"README.md", ".gitkeep"}


def is_brand_overlay_path(rel_path: Path) -> bool:
    """True for anything under data/brand/ that is a user's brand state
    rather than this directory's own documentation: a specific brand's
    overlay dir (data/brand/<slug>/...) or data/brand/active.json (which
    brand is installed). Either must never ship inside the public skill
    ZIP - that would leak one user's brand identity/data to every other
    user who installs the skill.
    """
    parts = rel_path.parts
    if len(parts) < 2 or parts[0] != "data" or parts[1] != "brand":
        return False
    if len(parts) > 3:
        return True  # data/brand/<slug>/...
    return rel_path.name not in BRAND_DIR_DOC_FILES


def is_excluded(rel_path: Path, gitignore_patterns: list[str]) -> bool:
    if rel_path.name in EXCLUDED_FILE_NAMES:
        return True
    if any(part in EXCLUDED_DIR_NAMES for part in rel_path.parts[:-1]):
        return True
    if is_brand_overlay_path(rel_path):
        return True
    posix = rel_path.as_posix()
    for pattern in gitignore_patterns:
        if pattern.endswith("/"):
            dir_name = pattern.rstrip("/")
            if dir_name in rel_path.parts[:-1]:
                return True
        elif fnmatch.fnmatch(posix, pattern) or fnmatch.fnmatch(rel_path.name, pattern):
            return True
    return False


def check_no_symlinks(skill_dir: Path) -> list[Path]:
    return [p for p in skill_dir.rglob("*") if p.is_symlink()]


def normalize_newlines(data: bytes) -> bytes:
    """Rewrite CRLF/CR to LF for text members. Binary (non-UTF-8) content is
    passed through untouched - a Windows checkout of this repo is CRLF, but
    the archive claude.ai receives must be LF regardless of that checkout.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def stamp_version(skill_dir: Path, version: str) -> None:
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    content = _VERSION_STAMP_RE.sub("", content, count=1)
    match = _FRONTMATTER_RE.match(content)
    if not match:
        raise SystemExit("SKILL.md must start with YAML frontmatter (---) - stamp aborted")
    stamp = f"<!-- version: {version} (generated at build - do not edit) -->\n"
    insert_at = match.end()
    content = content[:insert_at] + stamp + content[insert_at:]
    skill_md.write_text(content, encoding="utf-8", newline="\n")


def read_description_length(skill_dir: Path) -> tuple[str | None, int]:
    """Return (description_text, length) parsed from SKILL.md frontmatter, best-effort."""
    content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r'^description:\s*"(.*)"\s*$', content, re.MULTILINE)
    if not m:
        return None, 0
    return m.group(1), len(m.group(1))


def collect_members(skill_dir: Path, gitignore_patterns: list[str]) -> list[Path]:
    members = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(skill_dir)
        if is_excluded(rel, gitignore_patterns):
            continue
        members.append(path)
    return members


def build(skill_dir: Path, dist_dir: Path, allow_empty_data: bool) -> Path:
    if not allow_empty_data:
        sys.path.insert(0, str(skill_dir / "scripts"))
        import validate_data  # local import: only needed on the real-build path

        data_dir = skill_dir / "data"
        ok, problem_lines, summary = validate_data.validate(data_dir)
        for line in problem_lines:
            print(line)
        if not ok:
            print(f"\n{len(problem_lines)} problem(s) found - build aborted (no artifact on bad data)")
            raise SystemExit(1)
        print(summary)

    symlinks = check_no_symlinks(skill_dir)
    if symlinks:
        for s in symlinks:
            print(f"ERROR: symlink found (not allowed): {s}")
        raise SystemExit(1)

    version = (skill_dir / "VERSION").read_text(encoding="utf-8").strip()
    stamp_version(skill_dir, version)

    filename_version = version
    if allow_empty_data and "dev" not in version.lower():
        filename_version = f"{version}-dev"

    gitignore_patterns = load_gitignore_patterns(skill_dir.parent)
    members = collect_members(skill_dir, gitignore_patterns)

    dist_dir.mkdir(parents=True, exist_ok=True)
    root_name = skill_dir.name
    out_path = dist_dir / f"{root_name}-{filename_version}.zip"

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in members:
            arcname = f"{root_name}/{path.relative_to(skill_dir).as_posix()}"
            info = zipfile.ZipInfo.from_file(path, arcname)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, normalize_newlines(path.read_bytes()))

    return out_path


def report(out_path: Path, skill_dir: Path) -> None:
    with zipfile.ZipFile(out_path) as zf:
        names = zf.namelist()
        total_uncompressed = sum(i.file_size for i in zf.infolist())

    print(f"\n--- {out_path.name} ---")
    for n in names:
        print(f"  {n}")
    print(f"\nfiles: {len(names)}")
    print(f"zip size on disk: {out_path.stat().st_size} bytes")
    print(f"uncompressed content size: {total_uncompressed} bytes")

    roots = {n.split("/", 1)[0] for n in names}
    print("\n--- constraint check ---")
    print(f"ZIP root: {sorted(roots)} ({'OK - exactly one' if len(roots) == 1 else 'FAIL - must be exactly one'})")
    has_backslash = any("\\" in n for n in names)
    print(f"backslashes in any archive path: {has_backslash} ({'FAIL' if has_backslash else 'OK'})")
    skill_md_present = any(n.endswith("SKILL.md") for n in names)
    print(f"SKILL.md present: {skill_md_present} ({'OK' if skill_md_present else 'FAIL'})")

    desc, desc_len = read_description_length(skill_dir)
    if desc is None:
        print("description: NOT FOUND in SKILL.md frontmatter (FAIL)")
    else:
        status = "OK" if desc_len < 1024 else "FAIL (>= 1024)"
        print(f"description length: {desc_len} characters ({status}, limit is under 1024, confirmed)")

    symlinks = check_no_symlinks(skill_dir)
    print(f"symlinks under skill dir: {len(symlinks)} ({'OK' if not symlinks else 'FAIL'})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--allow-empty-data", action="store_true",
        help="dev build only: skip the validate_data.py gate, tag the output filename -dev. CI never passes this.",
    )
    parser.add_argument("--skill-dir", default=str(SKILL_DIR), help="path to the skill folder (default: auto-detected)")
    parser.add_argument("--dist-dir", default=None, help="output directory (default: <skill-dir>/../dist)")
    args = parser.parse_args(argv)

    skill_dir = Path(args.skill_dir).resolve()
    dist_dir = Path(args.dist_dir).resolve() if args.dist_dir else skill_dir.parent / "dist"

    out_path = build(skill_dir, dist_dir, args.allow_empty_data)
    report(out_path, skill_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
