# GhostBus — UART nonce unlocks a sealed SPI region

[日本語](README.ja.md)

Category: Hardware · Team: ReFlection (Agentic AI) · [Challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=b7d2e1fc-da43-4e73-975c-86cccad4d53e)

The official `ghost_bus.zip` SHA-256 is `8ffeac83846c1261595323f18fa701d940c702cc724c185e312cebdd72ef2676`. The useful evidence was split across a logic-analyzer capture, firmware, and a flash dump.

## Recovery

1. Parse each channel in `capture.csv` as `AA 55 LEN CMD PAYLOAD CRC16_LE`. Verify each CRC with CRC16-Modbus (initial value `0xffff`, reflected polynomial `0xa001`). Channel 0's final frame is a zero-length `0x10` command. Channel 1's `0x10` response contains the 16-byte nonce.
2. Disassemble `firmware.elf`. Its receive path hashes a 24-byte constant in the firmware followed by the response nonce with SHA-256, then uses the first 16 digest bytes as an AES-128 key. This order of concatenation matters.
3. The firmware reads 48 bytes of SPI NOR from offset `0x6a000`. It reverses the byte order inside each four-byte word before AES-CBC decryption. Use the UART nonce as the CBC IV.
4. Decrypt without automatic padding removal, then validate the seven trailing `0x07` bytes as PKCS#7. The remaining plaintext is the flag.

In pseudocode:

```python
key = sha256(firmware_constant_24 + uart_nonce).digest()[:16]
sealed = flash_dump[0x6a000:0x6a030]
ciphertext = b''.join(sealed[i:i+4][::-1] for i in range(0, 48, 4))
plaintext = AES_CBC_decrypt(key, uart_nonce, ciphertext)
assert plaintext.endswith(b'\x07' * 7)
```

Flag: `hiCTF{gh0st_bu5_uart_n0nc3_r3v3al_9c3f12}`

The local solver checks frame CRCs, padding, and flag shape. The contest close-time public snapshot lists GhostBus among ReFlection's solved challenges; the earlier local extraction note alone did not establish submission. AI-assisted reverse engineering helped correlate the three artifacts, and the deterministic decryption supplied an independent local check.
