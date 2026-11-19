#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to /output/entry.png.

The image is drawn by draw.py (run it first); this program only copies it,
so the submitted run is deterministic and needs no network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    print("copied entry.png to", out_dir)


if __name__ == "__main__":
    main()
