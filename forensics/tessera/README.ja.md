# TESSERA（Forensics）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=b1002114-481d-4148-b857-416daa358c19) · Agentic AI部門

公式配布ZIPのSHA-256は `18db37d7930dd005a409d96dee26de3de827c6a3296a3c45e7159dad6050c798` です。13,293件のファイルを展開すると約3.2 GiBになります。答えはETLメッセージ、DPAPI LocalMachineの保管ファイル、NTFSのreparse属性に分かれ、各段階が次の場所を指します。

1. `Windows/System32/LogFiles/WMI/AuditDiagTrace.etl` のオフセット8344に、`PORT=\RPC Control\AepLocalEndpoint_Q8;HEX=...` というUTF-16LEメッセージがあります。HEX以降をバイトに戻して `0x5a` でXORすると、`1ist-----hiCTF{alpc_p0rt_c0lloquy_` から始まる文字列と `TargetService:DiagTrackSvcAux` が出ます。
2. オフラインの `SYSTEM` ハイブの `ControlSet001\Services\DiagTrackSvcAux\Parameters` には、`ServiceVault` のパスとBase64の `EntropyToken` があります。`SYSTEM` と `SECURITY` ハイブから `DPAPI_SYSTEM` を取り出し、対応する `S-1-5-18` マスターキーを復号し、そのentropyで662バイトのLocalMachine DPAPI blobを開きます。JSONには `FlagPart2`、AES鍵、IV、`NodeHex` があり、第2断片の本文は `s35s10n_z3r0_syst3npr0f1l3_` です。
3. `NodeHex` をhexデコードすると `ETLLocalStore` になります。このノードのMFTレコード101281には、タグ `0xA0000028` の非常駐ではないreparse属性（`0xC0`）があり、暗号化された48バイトが入っています。JSON中の鍵とIVでAES-256-CBC復号し、PKCS#7 paddingを確認して除くと、第3断片 `r3p4r53_buff3r_vort3x}` が得られます。

`1ist-----`、`--s32nd--`、`iiiiiiiiiii-3hird---` の段階ラベルだけを除いて連結します。

```text
hiCTF{alpc_p0rt_c0lloquy_s35s10n_z3r0_syst3npr0f1l3_r3p4r53_buff3r_vort3x}
```

PowerShell operational EVTXには生成スクリプトも残っていますが、ETL、レジストリハイブ、vault、MFTから独立にこの値を復元できます。自チームの大会終了時の公開解答済み一覧にも本問が含まれ、ローカルのソルバーが同じ値を再現し、公式画面での受理も記録されています。
