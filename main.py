#!/usr/bin/env python3
"""Write the 24 Nov 2026 news poster to the make.fun output path.

Standard library only, no network, no randomness, no timestamps: the same
input always produces the same bytes.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)


def ihdr_size(data: bytes) -> tuple[int, int]:
    """Return (width, height) from the IHDR chunk, or raise ValueError."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("missing PNG signature")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    return struct.unpack(">II", data[16:24])


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        data = source.read_bytes()
        if ihdr_size(data) != EXPECTED_SIZE:
            raise ValueError("source is not 1024x1024")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "entry.png"
        out_path.write_bytes(data)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}")
        return 1

    # Read the file back from disk: a short write or a full disk must not
    # silently ship a broken entry.
    try:
        written = out_path.read_bytes()
    except OSError as exc:
        print(f"error: cannot re-read {out_path}: {exc}")
        return 1

    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        out_path.unlink(missing_ok=True)
        print(f"error: copy verification failed, removed {out_path}")
        return 1

    print(f"wrote {out_path}")
    print(f"sha256 {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
