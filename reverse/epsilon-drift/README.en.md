# Epsilon Drift (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=61fa3c15-3a28-4a4e-903d-678d58706c88) · Download SHA-256: `993a5ed3ced717af48dedf7b18fd54396ba55e314ea4519613a96a9c6b05284f`

The checker interprets four 64-bit words as IEEE-754 doubles. The first two are pinned to `1.1` and `2.2` by mantissa and exponent checks; the third must be the **actual binary64 result** of adding them. It is important to pack the floating-point result back into its 64-bit representation instead of using a decimal approximation.

The fourth word is the trick. A floating-point comparison treats `+0.0` and `-0.0` as equal, but a later sign-bit test selects the successful branch only for `-0.0`, whose bits are `0x8000000000000000`. Concatenate the four words as little-endian bytes. SHA-256 of those 32 bytes seeds a counter-based SHA-256 stream; XOR the first 42 stream bytes with the ciphertext embedded in the ELF.

The output is `hiCTF{1eee754_s1gn3d_z3r0_1u1p_dr1ft_eps!}`. Its SHA-256 matches the checker's embedded 32-byte digest, and Epsilon Drift appears in the team's official solved set. This explanation and the digest check establish the chosen signed-zero path; merely entering positive zero would not do so.
