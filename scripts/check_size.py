#!/usr/bin/env python3
import hashlib
import pathlib
import sys

MAX_BYTES = 1_500_000_000

if len(sys.argv) != 2:
    print("usage: check_size.py MODEL.gguf", file=sys.stderr)
    raise SystemExit(2)
p = pathlib.Path(sys.argv[1])
if not p.is_file():
    print(f"ERROR: missing model: {p}", file=sys.stderr)
    raise SystemExit(2)
size = p.stat().st_size
sha = hashlib.sha256(p.read_bytes()).hexdigest()
print(f"path={p}")
print(f"bytes={size}")
print(f"MB_decimal={size/1_000_000:.3f}")
print(f"sha256={sha}")
if size >= MAX_BYTES:
    print(f"FAIL: {size} >= {MAX_BYTES} bytes", file=sys.stderr)
    raise SystemExit(1)
print("PASS: strictly below 1500 MB")
