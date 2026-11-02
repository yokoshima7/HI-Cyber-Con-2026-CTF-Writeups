# Snapfile (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=f00787dd-0538-47c9-8431-1499eed7d3d0) · Download SHA-256: `33ba2e74970adb7f6f25c9b6a85eae326b2e7b5724c09e71fad6ed7a28f51eb6`

The archive supplies one stripped x86-64 Crystal executable, `snaptool`, and no example `.snap` file. Static analysis of its parser showed that a valid file is exactly 104 bytes. Its first 40 bytes contain `SNAP`, version `0x0002`, type `0x03`, marker `SNAP-LNG`, and six big-endian 32-bit descriptor values: `0x28, 0x10, 0x38, 0x20, 0x58, 0x08`. We left the next 56 bytes at zero and computed the eight-byte big-endian trailer checksum over offsets `0x08..0x5f`:

```python
s = 0x1357BDF02468ACE1
for byte in data[8:0x60]:
    t = ((s + byte) * 0xD1B54A32D192ED03) & 0xFFFFFFFFFFFFFFFF
    s = t ^ (t >> 29)
data[0x60:0x68] = (s ^ 0x58).to_bytes(8, 'big')
```

With zero data, the trailer is `fd47ab989124f3f2`. The binary hashes the fixed 40-byte header, concatenates `SHA256(header_hash || counter_be32)` for counters 0 and 1, and XORs the first 46 bytes with its embedded ciphertext. The plaintext's SHA-256 matches the second embedded digest.

The resulting flag is `hiCTF{r3c0nstruct3d_th3_sn4pf1l3_by73_by_by73}`. An unmodified `snaptool` accepted the constructed 104-byte file and printed that flag; the official site then displayed `Flag correct!` and `Challenge solved!`.
