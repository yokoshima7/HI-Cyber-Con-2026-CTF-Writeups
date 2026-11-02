# ChronoGrind (Cryptography)

[日本語](README.ja.md)

The [official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=61784143-ff04-444c-868d-faa4c53939e5) provided an archive with SHA-256 `5a5316e688fdd9ee3ae30d85a5659a52d0a5c0adf74ac71ba95583467ac256b3`. The team's submission was officially accepted.

## Idea and execution

`state.dat` is a `CGD1` record stream XORed bytewise with `0x4c`. Decoding it reveals a 2048-bit modulus, a base-241 seed, and a requirement for **9,000,000,000 sequential modular squarings**. An embedded SHA-256 checks the parsed parameters. The final 256-byte big-endian state is hashed to make the ChaCha20-Poly1305 key for `flag.enc`.

We first used a GMP worker with atomic checkpoints, then resumed the exact state on macOS using OpenSSL 3 Montgomery arithmetic. Five million iterations starting from the same checkpoint matched GMP and OpenSSL bit for bit. A separate Python check validated 1,000 real-state transitions. The final checkpoint recorded iteration 9,000,000,000; authenticated decryption then produced `hiCTF{n1c3_w0rk_n0w_t4k3_s0m3_r3$t}`. The official UI showed `Flag correct!`.

The point of the puzzle was preserving the exact sequential state. A plausible plaintext or unverified final iteration would not establish the answer; the checkpoint comparison, authenticated Poly1305 tag, and official acceptance did.
