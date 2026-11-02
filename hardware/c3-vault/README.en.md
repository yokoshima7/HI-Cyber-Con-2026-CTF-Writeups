# C3 Vault — encrypted flash, NVS, and challenge response

[日本語](README.ja.md)

Category: Hardware · Division: Agentic AI · [Challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=37ad0ee5-5532-475b-ac7b-00a49ba6c7bd)

The supplied ZIP has SHA-256 `ef94f82b12ebfb1640f9e52d6a74c6f514c4ea718bc52f7c7c05aaea3aeb4a59`. The task combined an ESP32-C3 acquisition with a live verifier. The central distinction was between flash encryption and NVS entry encryption: the NVS page headers were visible even though the entries were encrypted separately.

## Recovery

1. Decode the eFuse read-register window starting at `0x6000882c`. `SPI_BOOT_CRYPT_CNT=1` indicates flash encryption, and `KEY_PURPOSE_0=4` assigns BLOCK_KEY0 to `XTS_AES_128_KEY`. Extract BLOCK_KEY0 from offsets `0x70:0x90` in the eFuse dump, reverse the 32 read-register bytes, and use ESP-IDF's `espsecure decrypt_flash_data --aes_xts`. A valid ESP32-C3 bootloader and partition table check the byte order.
2. The partition table places `nvs` at flash offset `0x9000` and `nvs_keys` at `0xf000`. Decrypt the latter through flash XTS. Its first 64 bytes form the NVS AES-256-XTS key; the stored CRC32 validates that key. The NVS page headers themselves are plaintext. Decrypt each 32-byte entry using its partition-relative offset as the first four little-endian tweak bytes, followed by twelve zero bytes.
3. Read `gateway.device_id`, `gateway.generation`, and the current `vault_v2.seed`. The `vault_v1` seed is historical. This selection is supported by the decrypted application referring to the `gateway` and `vault_v2` namespaces.
4. Reverse the application's enrollment routine. The labels include their terminating NUL bytes, which matter to both HMACs:

   ```text
   device_key = HMAC_SHA256(seed,
       b"c3-vault/device-key/v2\0" + device_id + LE32(generation))
   auth = HMAC_SHA256(device_key,
       b"C3VAULT-AUTH-V2\0" + fresh_challenge + device_id)
   ```

5. Send the computed 32-byte `auth` as 64 hexadecimal characters to the team's verifier session. It returned `VAULT OPENED` and the flag. The final public team snapshot also lists C3 Vault as solved by our team.

Flag: `hiCTF{efus3_cl34r_jt4g_0p3n_nv5_34af9568e6}`

Reproduction requires the official ZIP, ESP-IDF's `espsecure`, an NVS-XTS parser, and the formulas above. The archived live verifier is not assumed to remain available. AI-assisted analysis was used to inspect the firmware and validate the cryptographic chain; the recovered values were checked against the verifier response and the official solved list.
