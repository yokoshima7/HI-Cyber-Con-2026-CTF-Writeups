# Rocinate (Cryptography)

[日本語](README.ja.md)

This is [Rocinate](https://ctf.hiddeninvestigations.net/challenges?challenge=3fb2ceda-d5d3-4369-b887-2b18ff34a203), **not** the later unsolved “Rocinate Revenge.” The official ZIP SHA-256 was `2f7b41f0cf2d52ca975e05f69bfd99b311c65712dcb4c5b524431c4a1c36e41a`.

## Attack

`chall.py` uses Python's MT19937 `random` to generate 100 public exponents `Cs`. Each candidate generated during `randint(1,N)` consumes 64 consecutive 32-bit MT outputs; rejection sampling can consume additional candidates. The rejection-free run starting at `Cs[15]` exposes 624 outputs, apart from nine unknown low bits. We tried those 512 possibilities against later `Cs`, reconstructed the generator state, and reversed it to recover earlier random values `r` and `e`. The reconstructed public parameters `a` and `b` matched exactly.

Using `r`, recreate the affine LCG values `R_i`. Every published `T_i = R_i^e mod N` and `Z_i % R_i == 0` check passed. The quotients `Z_i/R_i` equal `s^Cs[i] mod N`; a Bézout combination of two coprime exponents recovers `s`. We validated it against all 100 quotients, then decoded `s` to `hiCTF{lmaoooo_w0t???y0u_d1d_17_??435p37++}`. The official UI displayed `Flag correct!` and `Challenge solved!`.

The full solver uses only Python's standard library and the extracted `chall.txt`. Its key test is the later-exponent check: the 512 state possibilities are not accepted merely because they fit the first observed block.
