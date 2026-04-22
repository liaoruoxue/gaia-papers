"""Derive a stable kebab-case slug from a paper filename.

Rules (see spec § "Per-Tick Workflow" step 4):
  - Strip the final extension.
  - Lowercase.
  - Keep any unicode character in general category Letter (L*) or Number (N*).
  - Replace runs of other characters with a single '-'.
  - Trim leading and trailing '-'.
  - Raise ValueError if the result is empty.
"""

from __future__ import annotations

import os
import sys
import unicodedata


def derive_slug(filename: str) -> str:
    stem, _ext = os.path.splitext(filename)
    lowered = stem.lower()

    out: list[str] = []
    prev_was_sep = False
    for ch in lowered:
        if unicodedata.category(ch)[0] in ("L", "N"):
            out.append(ch)
            prev_was_sep = False
        elif not prev_was_sep:
            out.append("-")
            prev_was_sep = True

    slug = "".join(out).strip("-")
    if not slug:
        raise ValueError(f"cannot derive slug from filename: {filename!r}")
    return slug


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: derive_slug.py <filename>", file=sys.stderr)
        sys.exit(2)
    print(derive_slug(sys.argv[1]))
