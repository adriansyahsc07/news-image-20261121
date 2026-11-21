#!/usr/bin/env python3
"""Entry point for the News Image 21 Nov 2026 submission.

Runs fully offline and deterministically: builds the 1024x1024 PNG
infographic of the day's six biggest stories (see gen_image.py) and
writes it to /output/entry.png. Two runs produce byte-identical files.
"""

import os

import gen_image

OUTPUT_PATH = "/output/entry.png"


def main():
    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    gen_image.write_entry(OUTPUT_PATH)


if __name__ == "__main__":
    main()
