#!/usr/bin/env python3
"""Recover VaultKeeper's 2048-byte bytecode from the APK asset and x86-64 JNI library."""

from hashlib import sha256
from pathlib import Path

from cell_mixer import k1, k2


ROOT = Path(__file__).resolve().parent
vault = (ROOT / "assets/vault.bin").read_bytes()
native = (ROOT / "lib/x86_64/libvaultnative.so").read_bytes()
assert len(vault) == 8192
assert len(native) >= 0x3220

# nv_seed makes one SHA-256 digest per 32-byte row, for 16 rows = 128 cells.
seed = sha256(vault + b"VK-SEED-v1").digest()
cell_bytes = b"".join(
    sha256(seed + row.to_bytes(4, "little")).digest() for row in range(16)
)
cells = k1([
    int.from_bytes(cell_bytes[offset:offset + 4], "little")
    for offset in range(0, 512, 4)
])

# 0x5f50 computes a 51-byte environment key, regardless of the random arm token.
self_hash = sha256(native[0x2220:0x3220]).digest()
first = sha256(self_hash + b"VK-SELFMIX-v1").digest()
second = sha256(first).digest()
environment = (first + second)[:51]

# nv_unseal produces a 2048-byte buffer from the cells, environment key, and
# encrypted read-only data. CellMixer.k2 then removes the final XOR layer.
pre_k2 = bytes(
    ((cells[(7 + 31 * index) & 127] >> ((8 * index) & 24)) & 255)
    ^ environment[index % 51]
    ^ native[0xF60 + index]
    ^ 0xA5
    for index in range(2048)
)
program = k2(pre_k2, cells)
output = ROOT / "vm-program.bin"
output.write_bytes(program)
print(f"{output}: {len(program)} bytes")
print(f"SHA-256: {sha256(program).hexdigest()}")
print(f"First 32 bytes: {program[:32].hex()}")
