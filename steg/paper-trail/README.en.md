# Paper Trail

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=7001419c-fba8-41f4-b3f0-f04068f0a7aa)

The answer is in invisible PDF text operations, not in the rendered page. Pages 3, 6, 9, and 12 append compressed content streams 179–182. They use text rendering mode 3 and TJ arrays containing empty strings and numeric operands.

In streams 179–181, take the longest TJ row, drop its first two numbers, and interpret the remaining 21, 21, and 22 numbers as bytes. This yields a 64-byte ciphertext. Stream 182 is cover noise.

The PDF trailer supplies two 16-byte ID values. Treat the first as an AES-128-CBC key and the second as the IV. Decryption yields the CTF1 magic, a two-byte big-endian length field with value 40, the 40-byte flag, and an eight-byte checksum. The checksum equals the first eight bytes of SHA-256 of the flag; PKCS#7 padding also validates.

Flag: **hiCTF{n3w_ar34_fOr_hid!ng_d4t4_n4m3d_TJ}**

The retained JavaScript solver reads the official PDF and reproduces these checks. The official team snapshot includes Paper Trail as solved. PDF SHA-256: **e334a7c9e078fd1ddc7ac73be1058fcac50a96c7aabb52b5492dd4d4a3974a60**.

AI assistance helped inspect PDF object structure. The byte count, AES framing, checksum, and official solve record validate the result.
