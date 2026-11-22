"""Copy the repository-held news infographic to the output directory.

This program is the entrypoint for the news-image-20261121 entry. The
infographic itself (``entry.png``, a 1024x1024 summary of the news of
Saturday 21 November 2026) is stored in this repository next to this
script, and running the program simply copies that file into the
output directory chosen by the caller.

Only the Python standard library is used. That is deliberate: the
grader invokes the entrypoint as ``python3 -P -s main.py``, and under
those flags the script's own directory is not placed on ``sys.path``
(so importing a sibling module fails) and no user site-packages are
loaded (so third-party packages cannot be relied on). A copy built
purely on ``os``, ``shutil`` and ``pathlib`` runs the same way in that
sandbox as it does anywhere else.

The program is deterministic and fully offline: it reads one fixed
file from the repository and writes a byte-identical copy of it, so
repeated runs always produce exactly the same output.
"""

import os
import shutil
from pathlib import Path

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_DIR_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def source_image() -> Path:
    """Return the path of the infographic stored beside this script."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def output_directory() -> Path:
    """Return the directory the infographic should be copied into.

    The location comes from the ``MAKEFUN_OUTPUT_DIR`` environment
    variable when it is set to a non-empty value; surrounding
    whitespace is ignored. Otherwise the default ``/output``
    directory is used.
    """
    configured = os.environ.get(OUTPUT_DIR_ENV_VAR, "").strip()
    return Path(configured) if configured else Path(DEFAULT_OUTPUT_DIR)


def copy_infographic(source: Path, destination_dir: Path) -> Path:
    """Copy ``source`` into ``destination_dir`` and return the new path.

    The destination directory is created when needed. After copying,
    the size of the copy is checked against the original so a truncated
    or partial write is reported instead of silently accepted.
    """
    if not source.is_file():
        raise FileNotFoundError(
            f"infographic not found next to the entrypoint: {source}"
        )
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / IMAGE_NAME
    shutil.copyfile(source, destination)
    if destination.stat().st_size != source.stat().st_size:
        raise OSError(
            f"copy of {source} to {destination} is incomplete: "
            f"{destination.stat().st_size} bytes written, "
            f"expected {source.stat().st_size}"
        )
    return destination


def main() -> None:
    copy_infographic(source_image(), output_directory())


if __name__ == "__main__":
    main()
