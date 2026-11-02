# Dormant Signer (Blockchain)

[日本語](README.ja.md)

We solved the [official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=c2a91af0-0164-4988-acff-92cc455c09c9) from its signed transaction archive, SHA-256 `9397090fc7419f8c581199533ee42ec3786e82ddcf0bd302f05c63d75542f957`.

## Recovery

The target is the production `Authorizer` created in transaction 52 and destroyed in transaction 352, rather than the other, merely sealed Authorizer. Decode the 380 signed legacy transactions and reconstruct contract creation addresses. The production signer used the **same ECDSA `r` for two different request digests** in transactions 137 and 234. The low-`s` recovery bits indicate opposite nonce signs, so solving the pair of signature equations recovers the signing key. Derive its Ethereum address and compare it to the constructor signer before trusting it.

Replay the Authorizer's source-level rules in transaction order. Twenty `authorize` calls are valid; wrong-signer, duplicate, and post-destruction calls must not change the running digest. Sign the specified liveness digest with the recovered key. The contract's seal equations then give the escrow plaintext by XORing `final_seal`, `running_digest`, and `escrow_mask`. Its ASCII bytes spell `layout_undead_borrowed_betrays`, padded to `bytes32`.

The accepted flag is `hiCTF{layout_undead_borrowed_betrays}`. The local replay validated transaction hashes, recovered signer address, and digest arithmetic; the official solved set confirms the result. The archive was analyzed offline rather than replayed in a full EVM, which is the main reproduction limitation.
