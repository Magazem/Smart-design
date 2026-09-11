#!/usr/bin/env python3
"""Merge a brand kit into the base skill package. Stdlib only.

Usage (the only argument a non-technical user's Claude needs to supply):

    python3 merge_brand_kit.py <brand-kit.zip>

The base is auto-detected: when this script runs as part of an active,
mounted skill (the normal case inside claude.ai), it locates and zips up the
skill's own live directory to use as the base - the user does not need to
attach the base skill zip at all, only their saved brand kit. Pass
-b/--base <path> to override with an explicit base zip instead (e.g. after
downloading a new release, if auto-detection ever fails, or for local
testing outside a mounted skill).

<brand-kit.zip> accepts a bare filename (e.g. "my-brand-kit.zip") in addition
to a full path: if the given path does not exist as-is, its basename is
looked up under the uploads directory (see UPLOADS DIRECTORY below) before
giving up. This matches how claude.ai actually places chat attachments: they
land at a fixed path, not in this script's working directory, and a
non-technical user's Claude will typically only know the attachment's
filename. The same lookup applies to an explicit -b/--base path.

Produces "<base-stem>-<slug>.zip" in the outputs directory (see OUTPUTS
DIRECTORY below), or use -o/--output to name and place it explicitly. Add
--dry-run to validate and print what would happen without writing anything.

BASE AUTO-DETECTION: this script lives at
<skill-root>/scripts/merge_brand_kit.py, so its own file location's
grandparent directory IS the live skill root, wherever the platform mounted
it - this has been observed in the wild under paths like
/mnt/skills/public/<name>/, /mnt/skills/examples/<name>/, and
/mnt/skills/plugins/<name>/, and the exact tier a custom-uploaded skill lands
under has not been confirmed, which is exactly why this does not hardcode any
of those paths. If that heuristic doesn't find a directory containing
SKILL.md (e.g. this file was copied elsewhere before being run), it falls
back to globbing /mnt/skills/*/SKILL.md and /mnt/skills/*/*/SKILL.md and
using whichever one's own YAML frontmatter declares
`name: document-design-intelligence` - NOT whichever directory happens to be
named "document-design-intelligence". Confirmed in the field: claude.ai
renames a custom skill's mounted directory to its own display-name/slug at
upload time (one observed mount: our ZIP's root "document-design-intelligence"
landed at /mnt/skills/plugins/document-library), so the fallback cannot key
on the folder name - only SKILL.md's own frontmatter still says who it is.
Override with the DDI_SKILL_DIR environment variable to point at a specific
directory directly (used by this project's own tests; leave unset in normal
use).

UPLOADS DIRECTORY: chat attachments in claude.ai's code-execution container
are placed at /mnt/user-data/uploads/<filename> - a fixed, read-only mount,
not this script's current working directory. Override with the DDI_UPLOADS_DIR
environment variable (used by this project's own tests to simulate that mount
in a temp directory; leave unset in normal use).

OUTPUTS DIRECTORY: files placed at /mnt/user-data/outputs/ are what the user
can actually download from the chat. This script writes its result there by
default so the user gets a downloadable file with no extra step. Override
with the DDI_OUTPUTS_DIR environment variable (same purpose as above - testing
only). This script never writes into the uploads directory itself, and refuses
with a clear error if -o/--output is pointed there, since that mount is
read-only in the real container and writing there would silently fail (or
silently succeed somewhere the user still can't reach) in a way that would be
confusing to debug.

WHAT THIS DOES NOT DO: it does not know or check CSV column names, primary
keys, or row-level "Brand Scope" values - that depends on the document
library's table schema (research/09-library-schema.md), which does not exist
yet in this scaffolding. This script only merges *files*: it drops the brand
kit's allowed files into data/brand/<slug>/ inside a copy of the base and
refuses if that would silently overwrite something already there. Row-level
key-collision checking is the resolver's job, once it exists.

BRAND KIT CONTRACT (see data/brand/README.md):
  A brand kit zip may contain, at its root, only:
    - brand.md          (required - see below)
    - data/<name>.csv    (zero or more, one path segment under data/)
    - assets/...         (zero or more, any depth)
  Anything else causes the whole kit to be refused before any file is written.

  brand.md must contain a line of the form "slug: <value>" (case-insensitive
  key, scanned anywhere in the file - this is a plain "key: value" convention,
  not YAML, so no extra dependency is needed). <value> must match
  ^[a-z0-9-]+$; it becomes the destination directory name
  (data/brand/<slug>/) inside the merged package.

SECURITY: both the base and the brand kit are extracted with a zip-slip guard
- every member's resolved destination path is checked to stay inside the
intended directory before anything is written, and the brand slug is
validated against ^[a-z0-9-]+$ before it is ever joined into a filesystem
path. Treat any zip a user attaches as untrusted input.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
DATA_CSV_RE = re.compile(r"^data/[^/]+\.csv$")

DEFAULT_UPLOADS_DIR = "/mnt/user-data/uploads"
DEFAULT_OUTPUTS_DIR = "/mnt/user-data/outputs"
SKILL_NAME = "document-design-intelligence"

# NOT keyed on a folder named after the skill: claude.ai renames a custom
# skill's mounted directory to its own display-name/slug at upload time
# (observed in the field: our ZIP's root "document-design-intelligence"
# mounted at /mnt/skills/plugins/document-library - a name we don't control
# and can't predict). These patterns instead glob for any SKILL.md at the
# tiers observed in the wild, and _skill_md_declares_name below checks each
# candidate's own frontmatter `name:` field - the one place the skill's real
# identity survives a rename.
MOUNT_GLOB_PATTERNS = (
    "/mnt/skills/*/SKILL.md",
    "/mnt/skills/*/*/SKILL.md",
)


def _skill_md_declares_name(skill_md_path: Path, expected_name: str) -> bool:
    """True if skill_md_path's YAML frontmatter has `name: <expected_name>`.

    Deliberately does not use a YAML parser (stdlib-only, and this only
    needs one scalar field): finds the first line that is exactly `---`,
    then scans until the next `---` line for a `name: ...` line.
    """
    try:
        lines = skill_md_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return False
    start = next((i for i, line in enumerate(lines) if line.strip() == "---"), None)
    if start is None:
        return False
    for line in lines[start + 1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^name:\s*(.+?)\s*$", line)
        if match:
            return match.group(1) == expected_name
    return False


class KitError(ValueError):
    """A problem with the base or the brand kit that should abort the merge."""


def uploads_dir() -> Path:
    return Path(os.environ.get("DDI_UPLOADS_DIR", DEFAULT_UPLOADS_DIR))


def outputs_dir() -> Path:
    return Path(os.environ.get("DDI_OUTPUTS_DIR", DEFAULT_OUTPUTS_DIR))


def find_mounted_skill_dir() -> Path | None:
    """Locate the currently-active skill's own root directory, or None.

    Checked in order: an explicit DDI_SKILL_DIR override (testing only), this
    script's own file location (correct by construction whenever the skill is
    actually mounted and running, regardless of which tier it's mounted
    under), then a glob fallback across the tiers observed in the wild.
    """
    override = os.environ.get("DDI_SKILL_DIR")
    if override:
        candidate = Path(override)
        if (candidate / "SKILL.md").is_file():
            return candidate
        return None

    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "SKILL.md").is_file():
        return candidate

    for pattern in MOUNT_GLOB_PATTERNS:
        for hit in sorted(glob.glob(pattern)):
            hit_path = Path(hit)
            if _skill_md_declares_name(hit_path, SKILL_NAME):
                return hit_path.parent

    return None


def zip_dir_as_base(skill_dir: Path) -> Path:
    """Zip a live, mounted skill directory into a temp file to use as the base.

    The result's root is skill_dir's own name (e.g.
    "document-design-intelligence"), matching the single-top-level-directory
    convention get_zip_root_dir()/plan_merge() expect below - this makes an
    auto-detected live directory and an explicitly-supplied release zip
    interchangeable inputs to the same merge logic. Caller is responsible for
    deleting the returned path once done with it.
    """
    fd, tmp_path = tempfile.mkstemp(suffix=".zip", prefix="ddi-base-")
    os.close(fd)
    out_path = Path(tmp_path)
    root_name = skill_dir.name
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_file():
                arcname = f"{root_name}/{path.relative_to(skill_dir).as_posix()}"
                zf.write(path, arcname)
    return out_path


def resolve_input_path(given: str, uploads: Path) -> Path:
    """Resolve a user-given path or bare filename to a real file.

    Tries the path as given first (so absolute/relative paths still work for
    local testing), then falls back to <uploads>/<basename of given> - the
    shape a claude.ai chat attachment actually has. Raises KitError if
    neither exists.
    """
    direct = Path(given)
    if direct.is_file():
        return direct
    candidate = uploads / direct.name
    if candidate.is_file():
        return candidate
    raise KitError(f"file not found: {given!r} (also checked {candidate})")


def resolve_output_path(explicit: str | None, outputs: Path, uploads: Path, default_name: str) -> Path:
    """Resolve where to write the merged zip.

    If the caller gave -o/--output explicitly, use it - unless it resolves
    inside the read-only uploads mount, which is refused outright rather than
    attempted (that mount cannot be written to in the real container, and
    failing loudly here is clearer than a confusing write error later, or a
    silent write somewhere the user can't retrieve it from).

    Otherwise, default to <outputs>/<default_name> so the result lands
    somewhere the user can actually download it without being told to look
    for it.
    """
    if explicit:
        out = Path(explicit)
        try:
            out.resolve().relative_to(uploads.resolve())
        except ValueError:
            pass  # not under the uploads mount - fine
        else:
            raise KitError(f"refusing to write into the read-only uploads directory: {out}")
        return out
    outputs.mkdir(parents=True, exist_ok=True)
    return outputs / default_name


def _normalize(name: str) -> str:
    return name.replace("\\", "/")


def _reject_unsafe_name(name: str) -> None:
    if not name:
        raise KitError("archive contains an empty entry name")
    if name.startswith("/") or name.startswith("\\"):
        raise KitError(f"unsafe absolute path in archive: {name!r}")
    if re.match(r"^[A-Za-z]:", name):
        raise KitError(f"unsafe path with drive letter in archive: {name!r}")
    if "\\" in name:
        raise KitError(f"unsafe path (backslash) in archive: {name!r}")
    parts = name.split("/")
    if any(p in ("", ".", "..") for p in parts[:-1]) or parts[-1] in (".", ".."):
        raise KitError(f"unsafe path (traversal segment) in archive: {name!r}")


def safe_join(dest_dir: Path, member_name: str) -> Path:
    """Resolve member_name under dest_dir, refusing any zip-slip escape."""
    name = _normalize(member_name)
    _reject_unsafe_name(name)
    dest_root = dest_dir.resolve()
    target = (dest_root / name).resolve()
    try:
        target.relative_to(dest_root)
    except ValueError:
        raise KitError(f"zip-slip attempt blocked: {member_name!r} escapes target directory")
    return target


def get_zip_root_dir(zf: zipfile.ZipFile) -> str:
    """Return the single top-level directory name in a zip, or raise."""
    roots: set[str] = set()
    for name in zf.namelist():
        norm = _normalize(name)
        _reject_unsafe_name(norm)
        roots.add(norm.split("/", 1)[0])
    if len(roots) != 1:
        raise KitError(
            f"base does not have exactly one top-level directory (found: {sorted(roots)})"
        )
    return roots.pop()


def classify_member(name: str) -> str:
    """Return 'dir' | 'brand-md' | 'data-csv' | 'assets', or raise KitError."""
    norm = _normalize(name)
    _reject_unsafe_name(norm)
    if norm.endswith("/"):
        if norm in ("data/", "assets/") or norm.startswith("assets/"):
            return "dir"
        raise KitError(f"directory outside allowed set (data/, assets/): {name!r}")
    if norm == "brand.md":
        return "brand-md"
    if DATA_CSV_RE.fullmatch(norm):
        return "data-csv"
    if norm.startswith("assets/") and len(norm) > len("assets/"):
        return "assets"
    raise KitError(f"file outside allowed set (data/*.csv, brand.md, assets/): {name!r}")


def read_slug_from_brand_md(kit_zf: zipfile.ZipFile) -> str:
    try:
        raw = kit_zf.read("brand.md")
    except KeyError:
        raise KitError("brand kit is missing required brand.md")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise KitError(f"brand.md is not valid UTF-8: {exc}")

    slug = None
    for line in text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        if key.strip().lower() == "slug":
            slug = value.strip()
            break
    if not slug:
        raise KitError("brand.md must contain a 'slug: <value>' line")
    if not SLUG_RE.fullmatch(slug):
        raise KitError(f"invalid brand slug {slug!r} - must match ^[a-z0-9-]+$")
    return slug


def plan_merge(base_zip: Path, kit_zip: Path) -> tuple[str, str, dict[str, str]]:
    """Validate everything and compute the merge plan without writing anything.

    Returns (root_dir, slug, {kit_member_name: target_path_in_merged_zip}).
    Raises KitError on any problem.
    """
    if not zipfile.is_zipfile(base_zip):
        raise KitError(f"not a valid zip file: {base_zip}")
    if not zipfile.is_zipfile(kit_zip):
        raise KitError(f"not a valid zip file: {kit_zip}")

    with zipfile.ZipFile(base_zip) as base_zf, zipfile.ZipFile(kit_zip) as kit_zf:
        root = get_zip_root_dir(base_zf)
        base_names = {_normalize(n) for n in base_zf.namelist()}

        file_entries = []
        for info in kit_zf.infolist():
            name = _normalize(info.filename)
            category = classify_member(name)
            if category != "dir":
                file_entries.append((name, category))

        if not file_entries:
            raise KitError("brand kit contains no files")

        slug = read_slug_from_brand_md(kit_zf)

        target_map: dict[str, str] = {}
        for name, category in file_entries:
            if category == "brand-md":
                rel = f"data/brand/{slug}/brand.md"
            elif category == "data-csv":
                fname = name.split("/", 1)[1]
                rel = f"data/brand/{slug}/{fname}"
            else:  # assets
                rel = f"data/brand/{slug}/{name}"
            target_map[name] = f"{root}/{rel}"

        collisions = sorted(t for t in target_map.values() if t in base_names)
        if collisions:
            raise KitError(f"refusing to overwrite existing files in base: {collisions}")

        return root, slug, target_map


def safe_extract_all(zf: zipfile.ZipFile, dest_dir: Path) -> None:
    for info in zf.infolist():
        name = _normalize(info.filename)
        if name.endswith("/"):
            continue
        dest = safe_join(dest_dir, name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(info) as src, open(dest, "wb") as out:
            out.write(src.read())


def write_zip_from_dir(src_dir: Path, output_path: Path) -> None:
    entries = sorted(p for p in src_dir.rglob("*") if p.is_file())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in entries:
            zf.write(path, path.relative_to(src_dir).as_posix())


def do_merge(base_zip: Path, kit_zip: Path, target_map: dict[str, str], out_path: Path) -> None:
    """Write the merged package. Assumes plan_merge already validated everything."""
    with TemporaryDirectory() as tmp, zipfile.ZipFile(base_zip) as base_zf, zipfile.ZipFile(kit_zip) as kit_zf:
        merge_dir = Path(tmp) / "merged"
        merge_dir.mkdir()
        safe_extract_all(base_zf, merge_dir)
        for member_name, target_rel in target_map.items():
            dest = safe_join(merge_dir, target_rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(kit_zf.read(member_name))
        write_zip_from_dir(merge_dir, out_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("brand_kit_zip", help="path or attached filename of the brand-kit .zip")
    parser.add_argument(
        "-b", "--base", dest="base_zip", default=None,
        help="override: explicit base skill .zip (default: auto-detect the currently mounted skill)",
    )
    parser.add_argument("-o", "--output", default=None, help="output .zip path (default: outputs dir, <base>-<slug>.zip)")
    parser.add_argument("--dry-run", action="store_true", help="validate and report; write nothing")
    args = parser.parse_args(argv)

    uploads = uploads_dir()
    outputs = outputs_dir()
    temp_base_path: Path | None = None

    try:
        kit_zip = resolve_input_path(args.brand_kit_zip, uploads)

        if args.base_zip:
            base_zip = resolve_input_path(args.base_zip, uploads)
            base_stem = base_zip.stem
        else:
            skill_dir = find_mounted_skill_dir()
            if skill_dir is None:
                raise KitError(
                    "no --base given and no mounted skill directory found "
                    "(pass -b/--base <path> explicitly)"
                )
            temp_base_path = zip_dir_as_base(skill_dir)
            base_zip = temp_base_path
            base_stem = skill_dir.name  # not base_zip.stem - that's a random temp name

        # Slug is needed for the default output filename even on a dry run,
        # so plan first and resolve the output path with it in hand.
        _root, slug, target_map = plan_merge(base_zip, kit_zip)
        default_name = f"{base_stem}-{slug}.zip"
        out_path = resolve_output_path(args.output, outputs, uploads, default_name)

        summary = f"brand={slug} files={len(target_map)}"
        if args.dry_run:
            message = f"DRY-RUN OK: would merge ({summary}) -> {out_path}"
        else:
            do_merge(base_zip, kit_zip, target_map, out_path)
            message = f"OK: merged ({summary}) -> {out_path}"
    except KitError as exc:
        print(f"ERROR: {exc}")
        return 1
    except Exception as exc:  # last-resort guard so a bug never dumps a traceback into context
        print(f"ERROR: unexpected failure - {exc}")
        return 1
    finally:
        if temp_base_path is not None:
            temp_base_path.unlink(missing_ok=True)

    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
