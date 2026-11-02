# The Inner Engine (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=f7603a79-8925-4e5e-8fb7-299a4205f836) · Download SHA-256: `8c20991917e05093d0c87268ae9563515cd33abc90dd36b916413b5667559f46`

The stripped Nim ELF runs a stack machine with five-byte instructions. We extracted its program from `.rodata`, identified the arithmetic, stack, memory, branch, and halt opcodes, and symbolically executed its success path. At 24 conditional checks, the VM branches to the fail instruction unless the predicate is true, so each success predicate becomes a Z3 constraint over the 24 printable key bytes.

One satisfying key is `L1c#N0d3_7mQ9f3a2b8c6d1e`. The VM checks by themselves admit other models. The success handler hashes the key, then hashes that digest with big-endian counters to produce 40 bytes of keystream. XOR with its embedded ciphertext yields `hiCTF{vm_byt3c0d3_1nn3r_3ng1n3_unw0und!}`. SHA-256 of this plaintext equals the binary's embedded expected digest `e4f870dad765bfab3d282870ec136b8f450dc8c606cd894b9ea78c91736a5272`.

The local work reproduced bytecode behavior and cryptographic checks; it did not execute this ELF on the macOS host. The final official solved set lists The Inner Engine for our team.
