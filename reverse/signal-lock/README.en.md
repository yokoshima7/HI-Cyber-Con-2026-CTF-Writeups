# Signal Lock (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=04a6db25-845e-4655-aa92-3e6288012f96) · Download SHA-256: `93651d91c60187eb03e2162653f627fb360425597eb0f61415c469abfaf9df99`

The archive contains a gzip-compressed Erlang BEAM module. We decompressed it, decoded OTP 26 bytecode, and traced `verify/1`: it requires an eight-byte token interpreted as an unsigned 64-bit integer. The transform is

```text
rotl64(((x XOR 0xa5a5a5a55a5a5a5a) * 0x9e3779b97f4a7c15) mod 2^64, 29)
  + 0x0123456789abcdef  (mod 2^64)
```

It must equal `0xafe7c5708f40ebc4`. Subtract the addend, rotate right by 29, multiply by the modular inverse of the odd multiplier, then XOR the constant. The result is token `g4m30v3r` (`67346d3330763372` in hex). An early transcription used the wrong XOR constant; this exact constant matters.

`unlock/1` hashes the 64-bit token plus big-endian 32-bit counters with SHA-256 and XORs the resulting bytes with a 48-byte embedded literal. OTP 26 execution of the unmodified module returned `hiCTF{b34m_byt3c0d3_n3v3r_l13s_s3ss10n_unl0ck3d}`. ReFlection's official solved set includes Signal Lock.
