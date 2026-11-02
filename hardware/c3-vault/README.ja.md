# C3 Vault — 暗号化フラッシュ、NVS、チャレンジ応答

[English](README.en.md)

分類: Hardware · 部門: Agentic AI · [問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=37ad0ee5-5532-475b-ac7b-00a49ba6c7bd)

配布ZIPのSHA-256は `ef94f82b12ebfb1640f9e52d6a74c6f514c4ea718bc52f7c7c05aaea3aeb4a59`。ESP32-C3の取得データから認証材料を復元し、検証サービスのチャレンジに応答する問題だった。重要なのはフラッシュ暗号化とNVSエントリの暗号化を区別すること。NVSページヘッダーは読めるが、エントリは別の鍵で暗号化されていた。

## 解法

1. `0x6000882c` から始まるeFuseの読み出し領域を解釈する。`SPI_BOOT_CRYPT_CNT=1` はフラッシュ暗号化、`KEY_PURPOSE_0=4` はBLOCK_KEY0の `XTS_AES_128_KEY` 用途を示す。eFuseダンプの `0x70:0x90` からBLOCK_KEY0を取り、読み出しレジスタの32バイトを逆順にして `espsecure decrypt_flash_data --aes_xts` を使う。復号後のブートローダーとパーティション表でバイト順を確認できる。
2. パーティション表では `nvs` が `0x9000`、`nvs_keys` が `0xf000` にある。後者をフラッシュXTSで復号し、先頭64バイトをNVSのAES-256-XTS鍵として取り出す。保存されたCRC32で鍵を確認する。NVSページヘッダーは平文で、32バイトの各エントリにはパーティション相対オフセットをリトルエンディアン4バイト、その後にゼロ12バイトを付けたtweakを使う。
3. `gateway.device_id`、`gateway.generation` と現行の `vault_v2.seed` を読む。`vault_v1` のseedは古い状態で、復号したアプリも `gateway` と `vault_v2` を参照している。
4. アプリの登録処理からHMACを復元する。ラベルの末尾のNULバイトも入力に含める。

   ```text
   device_key = HMAC_SHA256(seed,
       b"c3-vault/device-key/v2\0" + device_id + LE32(generation))
   auth = HMAC_SHA256(device_key,
       b"C3VAULT-AUTH-V2\0" + fresh_challenge + device_id)
   ```

5. 計算した32バイトの `auth` を16進64文字として自チームの検証サービスに送ると、`VAULT OPENED` とフラグが返った。大会終了時の公式公開スナップショットにも、自チームの解答済み問題としてC3 Vaultが載っている。

Flag: `hiCTF{efus3_cl34r_jt4g_0p3n_nv5_34af9568e6}`

再現には公式ZIP、ESP-IDFの `espsecure`、NVS-XTSの解析処理、および上記の式を使う。大会中の検証サービスが現在も動くとは想定しない。AIを用いた静的解析で処理を特定し、復元値をサービス応答と公式の解答済み記録で確認した。
