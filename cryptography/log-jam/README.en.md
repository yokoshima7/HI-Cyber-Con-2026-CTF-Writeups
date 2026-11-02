# Log Jam (Cryptography)

[日本語](README.ja.md)

The [official Log Jam challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=4c01e897-f33f-45bd-8b00-249d493f6d8e) supplied an archive with SHA-256 `25350191fa48891bf7ef70202a283fbbb9ea1d9c1c8904b5a5a4d09903fccfee`. ReFlection is in the final official solved set.

## Recovery

The archive contains `params.json`, with hexadecimal `p`, `g`, and `h` satisfying `h = g^x mod p`, plus an AES-GCM nonce, ciphertext, and tag. The task is to recover the discrete logarithm `x`. PARI/GP's `znlog(Mod(h,p), Mod(g,p))` returned `471774559909450042061`. We verified `pow(g,x,p) == h` independently.

The key is `SHA256(str(x).encode())`, meaning the **decimal ASCII representation** of `x`, not its binary integer encoding. AES-GCM `decrypt_and_verify` authenticated the ciphertext and produced `hiCTF{W0W1_y0u_4ctu4a11y_s01v3d_1t_ju$t_L1k3_tH4t}`. A successful tag check rules out an accidental plausible-looking plaintext; the official team solved record confirms acceptance.

To reproduce, parse the provided JSON, run `znlog` in PARI/GP, assert the modular equation, derive the key exactly as above, and verify the GCM tag. No challenge service interaction is required.
