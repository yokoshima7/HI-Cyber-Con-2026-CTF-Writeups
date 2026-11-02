# Night Batch (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=9ee0bc40-5ee5-4db7-823e-360c6ed98db6) · Download SHA-256: `64ad99c6d690a7fac13b7d7cb56e2cc7c8553feceda2b503305dcb3ff6afcc9c`

The x86-64 ELF is a GnuCOBOL program that expects an 18-digit account key. It copies digits into packed-decimal fields, checks 22 expressions modulo 10, then compares one weighted integer sum directly with 94. The digit constraints mix linear, square, and pairwise-product terms.

To learn the expressions, we changed **only a copy** of the binary so its rejection branches would not abort measurement. Zero, single-digit, paired-digit, and random inputs supplied 214 observations of the packed-decimal values at each comparison. Polynomial fitting reproduced every expression, including 24 held-out random probes. We then constrained each digit to 0–9 in Z3 and solved the 23 equations. The resulting key was unique: `481702596318740925`.

Finally, the **unmodified** binary was run offline under x86-64 QEMU. The recovered key printed `hiCTF{c0b0l_p4ck3d_d3c1mal_n1ghtly_b4tch!}` and exited 0; a wrong key printed `account rejected`. The final official solved set includes Night Batch. The patched copy was used for observation, never as proof that the original checker accepts the key.
