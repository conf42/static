#!/usr/bin/env python3
"""Write WebP versions of headshots and podcast covers (conf42.com links to these).

  headshots/<name>.png -> headshots/webp/<name>.webp     500x400, ~16 KB (PNG ~50-250 KB)
                       -> headshots/webp/sm/<name>.webp  160 px, ~5 KB, for 44-60 px avatars
  podcasts/<name>.png  -> podcasts/webp/<name>.webp      800 px wide, ~30 KB (PNG ~2 MB)

The WebPs live in webp/ subfolders so headshots/ and podcasts/ list only the PNGs.

Only missing or outdated WebPs are written, so re-running is cheap. Runs in CI on every
push that touches headshots/ or podcasts/ (.github/workflows/webp.yml); conf42.com falls
back to the PNG (onerror) until the WebP exists.

PNGs given as arguments are always rewritten: a CI checkout gives every file the same
mtime, so a REPLACED headshot looks up to date there and would keep its old WebP. The
workflow passes the PNGs changed by the push.

    pip install Pillow && python3 make_webp.py [headshots/<name>.png ...]
"""
import sys
from pathlib import Path

from PIL import Image

JOBS = [
    # folder, output folder, max size, quality
    ("headshots", "headshots/webp", (500, 500), 80),
    ("headshots", "headshots/webp/sm", (160, 160), 75),
    ("podcasts", "podcasts/webp", (800, 800), 78),
]


def convert(src, dst, size, quality):
    img = Image.open(src)
    img.load()
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "transparency" in img.info or img.mode in ("LA", "PA") else "RGB")
    img.thumbnail(size, Image.LANCZOS)
    img.save(dst, "WEBP", quality=quality, method=4)


def main():
    force = {Path(a).as_posix() for a in sys.argv[1:]}
    written = 0
    for folder, out, size, quality in JOBS:
        Path(out).mkdir(parents=True, exist_ok=True)
        for src in sorted(Path(folder).glob("*.png")):
            dst = Path(out) / (src.stem + ".webp")
            if src.as_posix() not in force and dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                continue
            try:
                convert(src, dst, size, quality)
                written += 1
            except Exception as e:  # a broken upload shouldn't stop the rest
                print(f"WARNING {src}: {e}")
    print(f"Wrote {written} WebP files")


if __name__ == "__main__":
    main()
