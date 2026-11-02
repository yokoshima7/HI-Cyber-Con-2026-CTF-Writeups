# Ghost in RAM (Forensics)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=b9a2cff7-7dd1-4702-a125-a2ce7eccae11) · Agentic AI division

The official ZIP matches SHA-256 `5d93dd23e89876a4d7caead1dca17121ae36a17a29941a6c0bd75fccf13f020e`. It contains a roughly 2 GiB x86-64 Linux memory image. Its guest banner identifies Kali Linux `7.0.12+kali-cloud-amd64`. A Volatility 3 profile made from that exact kernel's debug BTF and `System.map` allowed process and memory-map inspection.

`linux.psaux.PsAux` identified PID 130, named `syncfsd`, whose mapped executable was `/bin/host`. The process had an 8 KiB data mapping at virtual address `0x4af000–0x4b1000`. At virtual `0x4af0e0`, a little-endian length is 30; 30 masked bytes begin at `0x4af0f0`. Disassembly of the recovered `/bin/host` at `0x401ac0–0x401acf` shows a bytewise XOR with `0x5a` before the program writes the plaintext into a transient mapping. It later clears that plaintext.

With Volatility 3 and a symbol profile for the exact Kali kernel, the recorded dump step was (the local installation used `.deps/bin/vol`). Our Volatility Framework 2.26.2 installation also needed two BTF-profile compatibility edits: allow `btf` and `symdb` in schema 6.2.0, and make `module_sect_attr` optional because that type was absent. An unmodified installation may therefore need an equivalent profile adjustment before these commands work:

```sh
VOLATILITY_SYMBOLS=kali-symbols
PYTHONPATH=.deps .deps/bin/vol -q -s "$VOLATILITY_SYMBOLS" -f mem.elf linux.psaux.PsAux
PYTHONPATH=.deps .deps/bin/vol -q -s "$VOLATILITY_SYMBOLS" -f mem.elf linux.proc.Maps --pid 130
mkdir -p dumps
PYTHONPATH=.deps .deps/bin/vol -q -s "$VOLATILITY_SYMBOLS" -f mem.elf -o dumps linux.proc.Maps --pid 130 --dump --maxsize 4194304
```

The local `.deps` and symbol profile are not part of this writeup. Select the dumped VMA whose virtual range is `0x4af000–0x4b1000` and name it `pid-130-data-vma.bin` below. The central calculation is small:

```python
from pathlib import Path

vma = Path("pid-130-data-vma.bin").read_bytes()  # mapping starts at 0x4af000
n = int.from_bytes(vma[0xe0:0xe4], "little")
assert n == 30
print(bytes(b ^ 0x5a for b in vma[0xf0:0xf0 + n]).decode())
```

This prints `hiCTF{gh0st_pr0c3ss_rng_pwn3d}`. Literal flag-shaped strings elsewhere in the dump (`hiCTF{stop_here}` and `hiCTF{d3bug_m3}`) occur in decoy contexts and were not submitted. The team's final public solved list includes Ghost in RAM; the exact flag also matches this memory reconstruction.
