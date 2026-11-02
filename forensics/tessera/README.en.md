# TESSERA (Forensics)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=b1002114-481d-4148-b857-416daa358c19) · Agentic AI division

The official ZIP has SHA-256 `18db37d7930dd005a409d96dee26de3de827c6a3296a3c45e7159dad6050c798`. Its 13,293 entries expand to roughly 3.2 GiB. The answer is split across an ETL message, a DPAPI LocalMachine vault, and an NTFS reparse attribute. Each stage points to the next.

1. In `Windows/System32/LogFiles/WMI/AuditDiagTrace.etl`, a UTF-16LE message at offset 8344 contains `PORT=\RPC Control\AepLocalEndpoint_Q8;HEX=...`. Hex-decode the following bytes and XOR with `0x5a`. The output begins `1ist-----hiCTF{alpc_p0rt_c0lloquy_` and names `TargetService:DiagTrackSvcAux`.
2. The offline `SYSTEM` hive key `ControlSet001\Services\DiagTrackSvcAux\Parameters` supplies the `ServiceVault` file path and Base64 `EntropyToken`. Extract `DPAPI_SYSTEM` using the `SYSTEM` and `SECURITY` hives, decrypt the matching `S-1-5-18` master key, and decrypt the 662-byte LocalMachine DPAPI blob with that entropy. Its JSON contains `FlagPart2`, an AES key, IV, and a `NodeHex` locator. The second flag part starts `s35s10n_z3r0_syst3npr0f1l3_`.
3. Hex-decoding `NodeHex` gives `ETLLocalStore`. MFT record 101281 for that node has a resident reparse attribute (`0xC0`) with tag `0xA0000028` and 48 encrypted bytes. Decrypt those bytes as AES-256-CBC with the key and IV from the vault JSON, then check and remove PKCS#7 padding. The final part is `r3p4r53_buff3r_vort3x}`.

Remove only the stage labels (`1ist-----`, `--s32nd--`, and `iiiiiiiiiii-3hird---`) and concatenate the three parts:

```text
hiCTF{alpc_p0rt_c0lloquy_s35s10n_z3r0_syst3npr0f1l3_r3p4r53_buff3r_vort3x}
```

The PowerShell operational EVTX includes a generator script that corroborates the construction, but the ETL, registry hives, vault, and MFT independently yield the flag. The team's final public solved list includes TESSERA; the local solver reproduced this exact value and the official UI was recorded as accepting it.
