# Hall of Mirrors

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=94f0bbb8-c6c1-491b-b576-90309bbf01d3)

The organizer's archivist datasheet was the turning point. It specifies a SplitMix64 sample selector over interleaved 16-bit WAV samples, two draws per bit, and a MIRRORS1 frame with CRC32.

Our first transcription of the spectrogram key failed. Searching small corrections against the full 64-bit frame magic found one three-nibble correction: **9C4F1E7A3B50D682**. That key extracts a 6,266-byte MVM1 image, whose stored and calculated CRC32 both equal **e2046fb1**.

The MVM1 virtual machine has 64 KiB Harvard memory, 16 64-bit registers, branch instructions, and self-modifying code. Its 20,395 instruction fetches emit 5,083 bytes beginning with MIRRORS1. The output contains secp256k1 parameters, 48 ECDSA signatures, and a sealed blob. Interpreting each tuple as stored **(z, r, s)** verifies all 48 signatures; the other five permutations verify none.

The top 12 bits of each nonce are zero. A lattice built from 32 signatures recovers the private key. The recovered public key matches the supplied point, and all 48 nonces satisfy the bound. The datasheet's KDF and stream cipher then unseal:

Flag: **hiCTF{h1dd3n_numb3r_l4ttice_le4k}**

The official team result lists Hall of Mirrors as solved. Reproduction requires the official WAV and datasheet, Python, and fpylll for the lattice step; the original large WAV is not mirrored here.

AI agents carried out independent carrier, VM, and signature checks. The CRC, 48/48 signature verification, key-to-public-point match, nonce bounds, and official solve record are the decisive evidence.
