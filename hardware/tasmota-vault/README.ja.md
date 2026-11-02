# Tasmota Vault — 現在のローテーションを特定して復号する

[English](README.en.md)

分類: Hardware · チーム: ReFlection（Agentic AI）· [問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=ceda2443-9f44-4e57-b25d-7db7307049fd)

取得した `tasmota_vault.zip` のSHA-256は `74e01ec638452b8674b70301a8270fe8607950737ca1c7a7dc3f5f62c03906ad`。ESP32のフラッシュとMQTT記録を組み合わせる問題で、保持された古いMQTTメッセージを現行のローテーションと誤認しやすい。

## 解法

1. フラッシュのパーティション表を読む。`0x3b0000` の区画には `spiffs` と記されているが、中身はLittleFSだった。`autoexec.be`、Berryバイトコード `vault.bec`、`vault/device.id`、`vault/keyring.bin`、`vault/sealed.bin` を抽出する。74バイトのsealedファイルのローカルSHA-256は `b6451db5cb534f3f082ab5d26ac60a08bf5b0929bf92c9b3742ede550f02d4c3`。
2. TCP再送を重複して数えず、MQTTのPUBLISHを再構成する。`VaultRotate` が2件あり、retainedのものは過去のepoch 7、後続のnon-retainedメッセージが現行の **epoch 8** とnonceを示す。
3. Berry/Tasmotaのバイト列と暗号APIの意味を確認しながら `vault.bec` を解析する。封印解除用の鍵は次の式で導出される。

   ```text
   HMAC_SHA256(keyring[epoch].key,
       b"tasmota-vault/unwrap/v2\0" + device.id + LE32(epoch) + nonce)
   ```

4. `sealed.bin` を12バイトのIV、暗号文、16バイトのAES-256-GCMタグとして読む。epoch 8の鍵ならタグ認証に成功し、フラグが得られる。epoch 7では認証に失敗するため、古いretainedメッセージを使っていないことも確認できる。

Flag: `hiCTF{b3rry_r0t4t10n_c94934d76344ab1151e03afd}`

GCMタグの認証はローカルの平文復元を裏付け、大会終了時の公式公開記録ではTasmota VaultがReFlectionの解答済みとして載っている。AIを用いてファイルシステムとバイトコードを解析し、GCM認証と古いepochでの失敗を照合した。元のファームウェア、PCAP、抽出した鍵はここには複製せず、公式配布物から再現する。
