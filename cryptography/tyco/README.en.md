# Tyco (Cryptography)

[日本語](README.ja.md)

The [official Tyco archive](https://ctf.hiddeninvestigations.net/challenges?challenge=2914b4ef-91ea-4270-8965-2d224b7788e0) had SHA-256 `f88f50cb0857595fce5457bc73d756215326093d6a1a478ae552d58460dc99f2`. Our final official record marks this challenge solved.

## Related-message RSA

`chall.py` publishes an RSA modulus `N`, exponent `e`, known difference `d`, and two ciphertexts `t1 = r^e mod N` and `t2 = (r+d)^e mod N`. Both polynomials `f(x)=x^e−t1` and `g(x)=(x+d)^e−t2` therefore share the factor `x−r` over `Z/NZ`. The Franklin–Reiter related-message attack computes their polynomial gcd without factoring `N`.

Using PARI/GP for polynomial arithmetic modulo `N`, the gcd was linear. Its root gave `r`. We checked both `pow(r,e,N)==t1` and `pow(r+d,e,N)==t2` before interpreting `r` as big-endian UTF-8. The result was `hiCTF{your_ai_slop_bores_me}`. This is a local algebraic solve backed by both ciphertext equations and the official solved record.
