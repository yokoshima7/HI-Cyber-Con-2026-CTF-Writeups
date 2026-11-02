# The Collector's Trail

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=15c57b89-a2b5-4bc8-9fa2-e292bd35b2a4)

This challenge combines six artwork images, museum catalogue records, hidden image fragments, two encrypted cabinets, a keyed pixel walk, and an authenticated final ciphertext. The ordering rule is the artists' birth years: Vermeer, Goya, Van Gogh, Klimt, Munch, Schiele.

| Artist | Fragment carrier in the unmodified supplied image | Eight data bytes – two checksum bytes (hex) |
| --- | --- | --- |
| Vermeer | Custom PNG coLl chunk | `be5f329a4841bece-ee99` |
| Goya | Base64 after PNG IEND | `b086be35786cac71-8ab3` |
| Van Gogh | RGB under a zero-alpha border | `c1d322deee71edf2-cfb8` |
| Klimt | Steghide in JPEG, using belvedere.at/912 | `07961017e80fb1e3-b14e` |
| Munch | Blue-channel LSB at every seventh row-major pixel | `7141415e3a146329-c2dc` |
| Schiele | First 176 PNG row-filter bytes: filter 1 → 0, filter 2 → 1 | `74718896e450c77c-e551` |

Each fragment encodes eight data bytes plus a two-byte checksum equal to the first two bytes of SHA-256 of those eight bytes. Concatenate the six data values in artist order. HKDF-SHA256 with salt **collector-v2:ossuary**, info **master**, and output length 32 produces the master key.

The catalogue locators are **mauritshuis.nl/670**, **museodelprado.es/P000749**, **moma.org/472.1941**, **belvedere.at/912**, **nasjonalmuseet.no/NG.M.00939**, **belvedere.at/3171**. Join them in this order with LF (`0x0a`) separators and no trailing LF. SHA-256 of those UTF-8 bytes is `40762afb7192c838fccba2284ebcb0b760da6a35698d4c6d0fb2da17088f46b1`; use the raw 32-byte digest as the salt for HKDF(master, info **zip**, length 16). The resulting password passes the encrypted cabinet's integrity test. The exact base domain belvedere.at matters: the collection subdomain gives the wrong password.

The cabinet's readme supplies HKDF(master, empty salt, info **stego**, length 32). Starting with counter zero, HMAC-SHA256 that key over each counter encoded as an unsigned eight-byte big-endian integer. Interpret the digest's first eight bytes as a big-endian integer and reduce it modulo the image's **6,220,800** row-major RGB byte positions. Skip repeated positions; take the least significant bit from each new position, in selection order. Assemble bits most significant first. The first four decoded bytes give a big-endian payload length of **451**, followed by that many payload bytes and a four-byte big-endian CRC32 of the payload. The checked payload names a [GitHub release](https://github.com/broski-creator/velarium-ossuary-ledger-7f3c2a/releases/tag/v1.0), its flag.enc asset, and a serial in the annotated tag. The asset SHA-256 matches the payload. HKDF(master, raw serial bytes, info **flag**, length 32) gives the AES-256-GCM key. Nonce is the asset's first 12 bytes; AAD is **collector-v2**. Authentication succeeds and yields:

Flag: **hiCTF{marble_sparrow_9eb44602eedb764aac082a3816b7d7cb}**

The official challenge page displayed the flag as correct, and the final team snapshot includes this solve. Original ZIP SHA-256: **b957032dc484894c3bfffc8fdecb5d6e269f2c24b5996422672fa45d6fe37f98**. AI agents helped enumerate and independently check the carriers; fragment checksums, cabinet integrity, payload CRC, asset digest, AES-GCM tag, and official acceptance anchor the result.
