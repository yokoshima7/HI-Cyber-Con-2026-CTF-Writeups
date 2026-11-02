# Cipher（Android）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=6bb49abf-0336-407d-ac25-74e5c87b63d3) · 配布ZIPのSHA-256: `d32ec3f2c705e1aefcba505d5f3af157680fe0bab50bc69418927c9298126745`

APKの処理は6個のDEXと3個の小さなリソースに分散している。実際の解錠経路は `PBKDF2WithHmacSHA256(password, salt, 32768)` で32バイトの鍵を作り、`HMAC-SHA256(key, "cipher-verifier-v3")[:16]` を再構成したanchorと比較する。その後、64個のindexed recordを持つ `V1LT` version 3のvaultを開く。各レコードは12バイトnonce、`b"v1" + index` をinfoとするHKDF-SHA256のサブ鍵、`b"V1LT" + index` をAADとするAES-GCMで保護される。

別系統に見えるlegacy classが、狭いパスワード探索空間を示していた。`m4.bin` を復号すると8バイト語が256個得られる。`SeedWindow` はseedの上位を `764149760` に固定し、残りは `2^18` 通り。各候補はJavaの `Random(seed XOR 7640891576956012809)` で6語を `nextInt(256)` により選び、末尾2桁を `(nextInt(100) + 7 * bitCount(seed)) mod 100` で付ける。

Javaの48ビットRNGを再現し、各候補をまずHMAC anchorで検査した。一致したoffsetは `258947`。64件すべてのGCMタグが認証を通り、47番の “Archived security memo” に `hiCTF{cryptography_should_be_implemnetd_properly}` があった。`implemnetd` という綴りは認証済み平文の通り。公式画面の `Flag correct!` と `Challenge solved!`、チームの最終解答済み一覧でも確認した。
