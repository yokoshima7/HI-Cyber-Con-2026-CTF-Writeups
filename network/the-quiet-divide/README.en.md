# The Quiet Divide (Network)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=46aa0afb-e480-4614-8634-528586911f7d) · ReFlection, Agentic AI division

The supplied ZIP has SHA-256 `15c7f337f5eae52865fbece148237ca5f01b2f4fa703d64a54c4f35a7bb40225` and contains a 152,240,093-byte PCAP. The goal was to identify the authoritative production transfer among several plausible, authenticated archives. A valid decryption tag by itself was insufficient: all three archive candidates decrypted successfully.

## Build the evidence chain

1. Stream the PCAP and reassemble TCP directions, then pair HTTP requests and responses. The capture contains 110,248 packets over roughly 99 seconds and 185 HTTP transactions. Three `AVLT10` encrypted archive writes, in request streams 190, 204, and 222, are all accompanied by successful receipts. The batch finalization confirms storage, not which write controls the release.
2. Read the `ARCH-14` enrollment (stream 29). It identifies a production device in the `IDX-S9` shard. Reassemble four HTTP byte ranges of firmware v7.7.0 (streams 21, 23, 25, 27) and confirm SHA-256 `0835dfce789d002d55f3d20fe7f953a30da0adbef336a861839ce8f579958836`. The capture's `/v10/sdk` response specifies the binary layouts and key schedule used below.
3. Two HTTP escrow shares (streams 50 and 52) XOR to the production QUIC keylog. Verify each share against its receipt hash and the XOR result against the declared keylog hash. Decrypt the 1-RTT observation from `10.77.40.14` to `10.77.40.37`. It reports `ARCH-14`, sequence 848971, queue depth 31, load 8%, and the v7.7.0 firmware hash. Its canonical signed-object SHA-256 `60369e7f8427e6bc708a33afab217c9b42b64be3b43a7ef5ecc7396ba5a211eb` agrees with the ACK and status service. A separate recovery session is signed by `REC-14` in `dr-ops` and lies outside the `fleet-prod` release scope.
4. Validate the live `PLS2` frame (TCP stream 34 and UDP) with the SDK's CRC and state rules. It yields frame counter **10450910**, scheduler queue 23, load 71, and epoch `1793517529318` ms. The epoch matches the `ARCH-14` attestation.
5. Verify the five custody events in `/v8/audit`: epoch 732 ROOT, epoch 733 PREP/COMMIT, and epoch 734 PREP/COMMIT. Check their event hashes, parent links, and 15 Ed25519 committee signatures under the `MIRRORBREAK/CUSTODY/B1\0` domain. Each event has a three-key quorum including a chair. The terminal event hash is `b34dc728c1fa1525020b1969a8af2698b2bcd91a95d58b3e3b940de35deda6e1`. An independent W0 checkpoint (streams 172/188) freezes that epoch 734 COMMIT in `fleet-prod`; its canonical hash is `5e4f78ad0e23d862a60ef8fca9891b47997dc1936043dd13efe419beaf7b3c53`. Later epoch 735 replica records do not replace this witnessed release point. A v7.7.1 qualification report does not prove that firmware was deployed.

## Select and open the archive

Use the SDK layout and production evidence above to derive the `AVLT10` archive key from the final seal's salt. All three objects authenticate and decrypt to different SQLite databases. Inspect their `transfers`, `receipts`, and `fragments` tables. Only request stream **222**, transaction `6dd9ec588c9914ca95df44b2`, matches all of the following simultaneously: terminal custody hash, device nonce `12060f75d51d36eb9db836f46f49f575`, frame counter **10450910**, origin `OPS-17`, version 10, W0 checkpoint hash, codec observation, durable receipt, and four fragment digests plus their material commitment. Stream 190 has a different nonce; stream 204 has a different counter. Other rows in stream 222 fail a case, origin, checkpoint, or state check.

Unmask the four selected fragments, apply the SDK's `final_key` schedule using the production evidence and W0 checkpoint signature, and decrypt the final seal with AES-256-GCM and its specified AAD. The authenticated plaintext is:

```text
hiCTF{c8c46fdbd6e5e4eacabfba53a156ff9ab10567f2}
```

The official challenge UI displayed `Flag correct!` and `Challenge solved!` for this value, and ReFlection's final public solved list includes The Quiet Divide. The local solver reran after submission and found exactly one eligible transfer. Firmware, checkpoint, and seal contents were linked through captured hashes, the verified custody chain, and authenticated decryption; some separate signature domains outside the public SDK were not independently verified.
