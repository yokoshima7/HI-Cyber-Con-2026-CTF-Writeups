# Echoes of a Forgotten Canvas

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=d5dffde1-b0d3-4b45-b2c9-6f9c7f5e76db)

The image has three successive carriers: a damaged PNG, an encrypted ZIP appended after its IEND chunk, and a JPEG with steghide data and a false height. We joined a prefix visible in the PNG to a suffix hidden below the JPEG's declared boundary.

1. The PNG declares 4000 × 4000 pixels, but its IHDR CRC and decompressed IDAT length establish a height of 4500. Correcting that height reveals the alpha-channel text **hiCTF{mu1t!14y3r3d_** near the bottom right. The two similar glyphs are both digit 1.
2. Bytes after IEND form a ZipCrypto archive. Password **dreamcatcher** decrypts its carrier.jpg. A bounded dictionary search found the password; full ZIP decompression and the JPEG signature confirmed it.
3. The poem in carrier.jpg includes “profound”. Steghide with passphrase **profound** extracts finall.jpg.
4. finall.jpg declares height 647 in its SOF0 marker, although its scan contains additional rows. Setting the height to 800 exposes **st3g0o_ju5t_l0v333}** in a gray strip. Joining the two fragments gives the flag.

Flag: **hiCTF{mu1t!14y3r3d_st3g0o_ju5t_l0v333}**

The local analysis records the byte offsets, hashes, and negative password checks. The official team result includes this challenge as solved. The challenge ZIP and derived images are linked through the official challenge rather than mirrored here.

AI agents helped inspect the PNG and archive layers and correct an early 1/l transcription error. The decisive checks were the PNG CRC and IDAT length, successful ZIP and steghide extraction, visible JPEG suffix, and official solve record.
