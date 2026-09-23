#!/usr/bin/env python3
"""Zip the portable pack for a release: portable/*.md + LICENSE + NOTICE.md, LF-normalised.

Usage: python3 research/build-portable-zip.py <version> [--out-dir DIR]
Writes <out-dir>/ddi-portable-<version>.zip (default out-dir: portable-dist/ at the repo
root). Every member sits under a single `ddi-portable-<version>/` folder. Stdlib only;
member order and timestamps are fixed so the archive is reproducible. Fails if a
portable/*.md file is missing (run research/build-portable.py first).
"""
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skill" / "document-design-intelligence"
REQUIRED = ("AGENTS.md", "DDI-LIBRARY.md", "INSTALL.md")


def build(version, out_dir):
    members = [(REPO / "portable" / n, n) for n in REQUIRED]
    for path, _ in members:
        if not path.is_file():
            raise SystemExit(f"missing {path} -- run research/build-portable.py first")
    members += [(SKILL / "LICENSE", "LICENSE"), (SKILL / "NOTICE.md", "NOTICE.md")]
    root = f"ddi-portable-{version}"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{root}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, name in members:
            data = path.read_bytes().replace(b"\r\n", b"\n")
            info = zipfile.ZipInfo(f"{root}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)
    return target


def main(argv):
    args = list(argv)
    out_dir = REPO / "portable-dist"
    if "--out-dir" in args:
        i = args.index("--out-dir")
        out_dir = Path(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__)
        return 2
    print(build(args[0], out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
