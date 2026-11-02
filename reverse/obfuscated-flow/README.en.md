# Obfuscated Flow (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=bbb7442a-7577-430e-a10e-e17dffffe581) · Download SHA-256: `ddaca1f93d3f748482982814ed307b58f9fba73e6298bb4551594a2b344a2d30`

The flag's 40 inner bytes are the passkey accepted by the ELF. The validator checks five consecutive eight-byte pieces through different mathematical constraints, so we inverted each piece independently and restricted the recovered four-byte words to printable little-endian ASCII.

The first piece follows modular product and quadratic relations over `2^31-1`; the second comes from undoing an elliptic-curve relation `T = P + [1337]Q`; the third is recovered by baby-step/giant-step discrete logarithms; the fourth solves two modular linear equations over `0xfffffffb`; and the fifth uses modular sum/product roots, then filters with the two primality checks. The pieces are `m4th_c0n`, `tr0l_fl0`, `w_3ll1pt`, `1c_dlog_`, and `4f7b2c9e`.

Together they give `hiCTF{m4th_c0ntr0l_fl0w_3ll1pt1c_dlog_4f7b2c9e}`. The original x86-64 binary printed `ACCESS GRANTED` and the same flag for that input; the official challenge UI also accepted it.
