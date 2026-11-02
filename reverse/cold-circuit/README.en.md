# Cold Circuit (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=928427a9-59bb-4675-a771-f736940ac853) · Download SHA-256: `cd9e56173d294497a6e07d560db89c46abe359a702b40be1165332cb9adb4c1c`

The stripped x86-64 checker requires `hiCTF{` plus 32 hexadecimal characters and `}`. It decodes those characters to 16 bytes and transforms them through 20 rounds: add a 16-byte round key modulo 256, apply a bijective byte substitution table, then permute the positions. The final state is compared with a fixed 16-byte target.

Because the substitution table is a permutation of all 256 byte values and the position table is a permutation of 0–15, every round is reversible. Starting at the embedded target, we processed rounds 19 down to 0: undo the position permutation, apply the inverse substitution table, and subtract the round key modulo 256. A separate forward replay reached the target again.

This gives the 16 input bytes `6e305f6a7461675f6e65656465642121` (ASCII `n0_jtag_needed!!`) and flag `hiCTF{6e305f6a7461675f6e65656465642121}`. The unmodified checker printed `Access granted.` and exited successfully. The official UI then displayed `Flag correct!` and `Challenge solved!`.
