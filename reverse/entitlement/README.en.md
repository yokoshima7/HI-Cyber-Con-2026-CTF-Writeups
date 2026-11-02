# Entitlement (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=e06aac60-dd99-4331-bc41-99eea0a44ed7) · Download SHA-256: `d468c69996ba1e34344d616d3f0ccf1fb2de6367a498a0dda4be67041a8feca0`

The x86-64 ELF was packed with UPX, but three `UPX!` markers had been replaced with `HI4!`. Repairing a **copy** of the file allowed `upx -t` and `upx -d` to recover the executable. There are three gates: a 16-hex-digit serial, a 25-hex-digit activation code, and a time-consuming flag decryption.

The serial check interprets the input as an element of `GF(2^64)` (reduction polynomial low word `0x2b395c2099596d9f`). Its virtual machine computes `(serial XOR 0xd1705c3b2e33689b)^13 XOR 0xba6b1f3cb925c25a`. To invert the check, first XOR the expected value `0x30cefbec2e4bc466` with `0xba6b1f3cb925c25a`, raise that result to `13⁻¹ mod (2⁶⁴−1)` in the field, and finally XOR with `0xd1705c3b2e33689b`. This gives serial `8f7db18bd70e193b`; running the decoded VM confirms it.

The activation check is an elliptic-curve discrete logarithm `nP = Q`. The curve has order equal to its base-field prime (`#E(F_p)=p`), making it anomalous. A p-adic Smart attack recovers `2977e17b118de75b3b4e921a4`; scalar multiplication verifies that value against `Q`.

The final stage hashes the little-endian serial and activation bytes to form a 2048-bit starting value, then performs **500,000,000 modular squarings**. We verified that the binary's Montgomery operations correspond to ordinary modular multiplication, used a checkpointed GMP implementation to complete the squarings, and derived a SHA-256 keystream to decrypt 64 bytes. The byte-sum checksum equals the binary's `0x133d` constant. The plaintext, without NUL padding, is `hiCTF{>o<_C0ngrats_Her3_1s_Y0ur_HI4_Subscript1on_^_^}`. ReFlection's official solved set includes Entitlement.

The long squaring stage is part of the intended computation; the serial and activation alone do not produce the flag.
