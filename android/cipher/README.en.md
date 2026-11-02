# Cipher (Android)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=6bb49abf-0336-407d-ac25-74e5c87b63d3) · Download SHA-256: `d32ec3f2c705e1aefcba505d5f3af157680fe0bab50bc69418927c9298126745`

The APK distributes its logic over six DEX files and three small resources. The active path derives a 32-byte key with `PBKDF2WithHmacSHA256(password, salt, 32768)`, checks `HMAC-SHA256(key, "cipher-verifier-v3")[:16]` against a reconstructed anchor, and opens a `V1LT` version-3 vault. That vault has 64 indexed AES-GCM records. Each record uses a 12-byte nonce, a subkey from one-block HKDF-SHA256 with info `b"v1" + index`, and AAD `b"V1LT" + index`.

The apparently separate legacy classes expose a much smaller password search. `m4.bin` decodes to 256 eight-byte words. `SeedWindow` fixes the high seed bits at `764149760`, leaving `2^18` possibilities. Each candidate seeds Java `Random(seed XOR 7640891576956012809)`, chooses six words with `nextInt(256)`, then adds a two-digit suffix from `(nextInt(100) + 7 * bitCount(seed)) mod 100`.

We reproduced Java's 48-bit RNG and checked each candidate with the HMAC anchor before attempting vault decryption. Offset `258947` matched. All 64 GCM tags authenticated; record 47, “Archived security memo,” contained `hiCTF{cryptography_should_be_implemnetd_properly}`. The misspelling `implemnetd` belongs to the authenticated plaintext. The official UI displayed `Flag correct!` and `Challenge solved!`, and Cipher appears in the team's final solved set.
