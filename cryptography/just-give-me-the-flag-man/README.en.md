# Just Give Me The Flag Man (Cryptography)

[日本語](README.ja.md)

The [official archive](https://ctf.hiddeninvestigations.net/challenges?challenge=0c29db29-bbf3-4dd1-b07a-6e5f05db558f) has SHA-256 `47250d4a65be0eb4ff5e8b4c31ae2120f95bb086f301ebb2467f7640614952c0`. The team's answer was accepted.

## Decoding chain

The file has 52 two-character tokens. Map `u v w x y z` to hexadecimal `f e d c b a`, respectively, then swap the two nibbles of each token. The result is a 52-character ASCII85-range string. Reverse the **entire string** and Adobe ASCII85-decode it to 41 characters. Apply ROT47, then the standard basE91 decoder to get a 33-byte flag-shaped intermediate. Finally apply Atbash and ROT13 to each English letter, leaving digits and punctuation unchanged. For zero-based alphabet indices the combined final mapping is `(12 − index) mod 26`.

The recovered flag is `hiCTF{sh1ft1ng_7hr0ugh_7h3_b4s3s}`. We checked round trips for the ASCII85 and basE91 stages. A brute-force check of all 720 assignments of `u..z` to `a..f` showed that printability after the nibble swap alone was insufficient; the later layers isolate the readable branch. Official `Flag correct!` confirmed the chain.
