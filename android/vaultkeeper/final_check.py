#!/usr/bin/env python3
"""Check VaultKeeper's final 51-byte candidate using the native SHA-256 tag."""

from hashlib import sha256
from pathlib import Path


root = Path(__file__).resolve().parent
native = (root / "lib/x86_64/libvaultnative.so").read_bytes()
vm_output = (root / "vm-output.bin").read_bytes()
assert len(vm_output) >= 51, "VM output must contain at least 51 bytes"

digest0 = sha256(native[0x2220:0x3220]).digest()
digest1 = sha256(digest0 + b"VK-SELFMIX-v1").digest()
digest2 = sha256(digest1).digest()
environment = (digest1 + digest2)[:51]

candidate = bytes(
    a ^ b ^ c ^ d
    for a, b, c, d in zip(
        native[0x1770:0x17A3],
        native[0x17B0:0x17E3],
        vm_output[:51],
        environment,
    )
)
tag = native[0x17E3:0x17EE]
expected = native[0x17F0:0x1800]
actual = sha256(tag + candidate).digest()[:16]
print("Candidate bytes:", candidate)
print("SHA-256 tag match:", actual == expected)
if actual != expected:
    print("Expected:", expected.hex(), "Actual:", actual.hex())
    raise SystemExit(1)
print("Candidate text:", candidate.decode("ascii"))
