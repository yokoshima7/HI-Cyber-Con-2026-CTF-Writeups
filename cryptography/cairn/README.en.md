# Cairn (Cryptography)

[日本語](README.ja.md)

We solved this challenge in the Agentic AI division. The [official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=cd968c16-2c61-4d27-a215-af9dd1bb34c1) supplied `challenge.json` and a precise walk specification; the archive SHA-256 was `9f8f036fbb3a25341dc58602c9d8c340c786f1ba882095c45bac69b785796f21`.

## Idea

The flag is encrypted under a key derived from the last point of a **sequential 1,048,576-step walk** in `GF(p²)`, where `p = 2²⁵⁶ − 2³² − 977`. Each point is represented as `(a,b)` for `a + bi`, with `i² = −1`. At step `t`, hash `LE32(a) || LE32(b) || BE8(t) || salt`. The first digest byte selects one of the provided modular polynomials `Φ_ℓ` for `ℓ ∈ {2,3,5,7}`; the second selects a root of its squarefree specialization. Each `Φ_ℓ` has degree `ℓ+1` in either variable. Roots must be sorted by the canonical unsigned pair `(a,b)` before indexing.

Our Python solver used PARI/GP to compute finite-field roots. It removed repeated factors with `f / gcd(f,f')`, checked the root count, serialized coefficients exactly, and checkpointed every 1,000 steps. The first step and first 1,000 steps were independently checked. After the complete walk, it derived `SHA256(LE32(a_T) || LE32(b_T) || "IsogenyLabyrinth")` and authenticated the provided AES-256-GCM ciphertext. Ordinary JavaScript JSON parsing would round the 256-bit integers, so arbitrary-precision parsing is essential.

The GCM tag verified and produced `hiCTF{w41k_th3_sup3rs1n9u14r_l46yr1ntH}`. The official challenge UI also displayed `Flag correct!` and `Challenge solved!`. No shortcut was established; this was a checkpointed computation of the specified walk.
