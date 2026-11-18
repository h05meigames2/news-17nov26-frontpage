#!/usr/bin/env python3
"""Copy the pre-rendered front-page image to the output directory.

The entry image is drawn by gen_image.py (PIL, run at build time) and
stored in this repository as entry.png. The grading sandbox runs Python
3.13 with the standard library only, so this program does nothing but
copy that file to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
The copy is byte-for-byte, so repeated runs produce identical output.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
