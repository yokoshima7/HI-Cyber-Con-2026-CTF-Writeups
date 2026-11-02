# Forgotten Secrets

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=a6e70ac6-77ea-4adc-aada-3b1cd0a325a6)

The recovered memory-like binary does not contain the flag in plaintext. Search for the literal eight-byte ASCII marker **DEADBEEF** (not the four hex bytes `de ad be ef`), take the next 27 bytes, and require the literal ASCII marker **CAFEBABE** immediately afterward. The retained solver found 22 such records, all with the same 27-byte payload.

XOR each payload byte with **0x42**. The repeated, transformed record becomes:

Flag: **hiCTF{m3m0ry_dump_d1g_d33p}**

The repeated payload is a useful integrity check: the solver asserts both the record count and equality of all 22 copies before decoding. The official team snapshot lists this challenge as solved. Official ZIP SHA-256: **bfde7ee94bc2841f3c9fc6275e6f005256df9d1a77363f291ec8adc90929840a**.

This writeup was reconstructed from our retained 13-line solver. We did not retain a separate exploration log, so it describes the verified extraction, not a detailed search history.
