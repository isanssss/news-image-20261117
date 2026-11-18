#!/usr/bin/env python3
"""Entry program for the make.fun competition news-image-20261117,
"Sum up 17 November's world news in one image".

The repository holds the finished front page as entry.png; this program
copies it to the output directory. Standard library only, no network,
and the copy is byte for byte, so the program's two runs in the grading
sandbox write identical bytes.
"""

import os
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # Copy the bytes themselves, nothing else: the two grading runs then
    # write files identical to the repository's entry.png and to each
    # other, whatever the filesystem does with metadata.
    (out_dir / "entry.png").write_bytes(source.read_bytes())


if __name__ == "__main__":
    main()
