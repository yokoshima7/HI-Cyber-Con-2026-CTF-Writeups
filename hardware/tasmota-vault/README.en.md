# Tasmota Vault — identify the current rotation before unsealing

[日本語](README.ja.md)

Category: Hardware · Division: Agentic AI · [Challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=ceda2443-9f44-4e57-b25d-7db7307049fd)

Our downloaded `tasmota_vault.zip` has SHA-256 `74e01ec638452b8674b70301a8270fe8607950737ca1c7a7dc3f5f62c03906ad`. The task joins an ESP32 flash image to an MQTT capture. The main trap is using the retained MQTT rotation, which is older than the current command.

## Recovery

1. Read the flash partition table. The partition at `0x3b0000` is labelled `spiffs`, but its content is LittleFS. Extract `autoexec.be`, Berry bytecode `vault.bec`, and `vault/device.id`, `vault/keyring.bin`, `vault/sealed.bin`. The sealed file is 74 bytes; its local SHA-256 is `b6451db5cb534f3f082ab5d26ac60a08bf5b0929bf92c9b3742ede550f02d4c3`.
2. Reassemble MQTT PUBLISH payloads from the capture, ignoring the retransmitted TCP segment. Two `VaultRotate` messages appear. The retained message refers to epoch 7. The subsequent non-retained message refers to **epoch 8** and supplies its nonce; this is the current rotation.
3. Disassemble `vault.bec` against the Berry/Tasmota byte and crypto semantics. The unwrapping key is:

   ```text
   HMAC_SHA256(keyring[epoch].key,
       b"tasmota-vault/unwrap/v2\0" + device.id + LE32(epoch) + nonce)
   ```

4. Parse `sealed.bin` as a 12-byte IV, ciphertext, and 16-byte AES-256-GCM tag. The epoch 8 key authenticates the tag and reveals the flag. The epoch 7 key fails authentication, a useful check against the stale retained message.

Flag: `hiCTF{b3rry_r0t4t10n_c94934d76344ab1151e03afd}`

The authenticated GCM result establishes the plaintext locally; the contest close-time public snapshot separately records Tasmota Vault as solved by our team. AI assistance helped decode the filesystem and bytecode, while the GCM tag and stale-epoch failure checked the reconstructed algorithm. The original firmware, PCAP, and extracted keys are not mirrored here; use the official challenge files to reproduce the chain.
