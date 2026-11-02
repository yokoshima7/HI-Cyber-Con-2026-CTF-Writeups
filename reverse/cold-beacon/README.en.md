# Cold Beacon (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=3aef51b5-1216-4919-b80d-d49c9f358977) · Download SHA-256: `a01791f8259c7bcf1eb07f578abc686b2a4ab78d4fe410f565c74624e52610d8`

The stripped Nim executable asks for a 24-byte key. It checks the key with 23 table-driven expressions (XOR, addition, and multiplication over bytes) and three more byte relations. The checks can be modeled as 8-bit bit-vector constraints rather than brute-forcing printable strings.

We extracted the operation type, selected indexes, and target for each row from the ELF. In Z3, each key byte is printable (`0x20..0x7e`), and the arithmetic wraps at eight bits, as it does in the binary. The additional relations include `k[10] == 0xa8 - k[9]`, `k[20] == k[12] XOR k[4]`, and `k[12] + k[13] == 0xe3`.

Several keys can satisfy the visible constraints. For each model, we computed `seed = SHA256(key)`, made a stream of `SHA256(seed || counter_be32)` blocks, and XORed it with the embedded 47-byte ciphertext. The binary's embedded SHA-256 digest of the plaintext identifies the right model.

Result: `hiCTF{c0ld_b34c0n_cfg_uns34l3d_fr0m_th3_s4mpl3}`. The team's official end-of-event solved set includes Cold Beacon. The local solution also matched the embedded plaintext digest. The original solver used `z3-solver`; no challenge binary is mirrored here.
