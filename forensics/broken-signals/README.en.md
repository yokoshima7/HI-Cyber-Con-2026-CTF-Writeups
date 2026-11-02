# Broken Signals (Forensics)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=a8093901-6c55-44a4-834b-b49ede36a8e6) · ReFlection, Agentic AI division

The image was intact except for the first four bytes of its PNG signature. The supplied ZIP has SHA-256 `47517fa29db01823c9416f0b285f069e2022d63c956d87fb995c1b97a9ea34f5`.

`broken_signal.dat` begins `00 00 00 00 0d 0a 1a 0a`. A PNG should begin `89 50 4e 47 0d 0a 1a 0a`. The following `IHDR` chunk is valid, so replacing only the four zero bytes restores a 400 × 300 image:

```python
from pathlib import Path

data = Path("broken_signal.dat").read_bytes()
assert data[:8] == bytes.fromhex("000000000d0a1a0a")
Path("repaired.png").write_bytes(bytes.fromhex("89504e47") + data[4:])
```

The red text in the repaired image reads `hiCTF{h34d3r_r3p41r_m4st3r}`. This value is reconstructed from the official attachment; ReFlection's final public solved list includes Broken Signals. No unrelated image data or hidden extraction step is needed.
