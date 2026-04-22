"""Derive a stable kebab-case slug from a paper filename.

Rules (see spec § "Per-Tick Workflow" step 4):
  - Strip the final extension.
  - Lowercase.
  - Replace runs of non-letter/non-digit characters with a single '-'.
  - Trim leading and trailing '-'.
  - Raise ValueError if the result is empty.
"""

from __future__ import annotations

import os
import re
import sys


_NON_ALNUM_RUN = re.compile(r"[^0-9a-zÀ-ɏͰ-῿Ⰰ-퟿]+", re.UNICODE)


def derive_slug(filename: str) -> str:
    stem, _ext = os.path.splitext(filename)
    lowered = stem.lower()
    replaced = _NON_ALNUM_RUN.sub("-", lowered)
    trimmed = replaced.strip("-")
    if not trimmed:
        raise ValueError(f"cannot derive slug from filename: {filename!r}")
    return trimmed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: derive_slug.py <filename>", file=sys.stderr)
        sys.exit(2)
    print(derive_slug(sys.argv[1]))
