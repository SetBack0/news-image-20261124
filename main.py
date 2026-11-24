#!/usr/bin/env python3
"""Write the 24 Nov 2026 news poster to the make.fun output path.

Standard library only, no network, no randomness, no timestamps: the same
input always produces the same bytes.
"""

import hashlib
import os
import struct
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)
SOURCE = Path(__file__).resolve().parent / "entry.png"


class InvalidSource(Exception):
    """The source file is not the 1024x1024 PNG this entry ships."""


def ihdr_size(data: bytes) -> tuple[int, int]:
    """Return (width, height) from the IHDR chunk, or raise InvalidSource."""
    if not data.startswith(PNG_SIGNATURE):
        raise InvalidSource("missing PNG signature")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise InvalidSource("missing IHDR chunk")
    return struct.unpack(">II", data[16:24])


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    out_path = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"

    try:
        data = SOURCE.read_bytes()
        size = ihdr_size(data)
        if size != EXPECTED_SIZE:
            raise InvalidSource(f"expected 1024x1024, got {size[0]}x{size[1]}")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(data)
    except (OSError, InvalidSource) as exc:
        print(f"error: {exc}")
        return 1

    # Read the file back from disk: a short write or a full disk must not
    # silently ship a broken entry.
    try:
        written = out_path.read_bytes()
    except OSError as exc:
        print(f"error: cannot re-read {out_path}: {exc}")
        return 1

    if digest(written) != digest(data):
        out_path.unlink(missing_ok=True)
        print(f"error: copy verification failed, removed {out_path}")
        return 1

    print(f"wrote {out_path}")
    print(f"sha256 {digest(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
