# The Collector's Trail

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=15c57b89-a2b5-4bc8-9fa2-e292bd35b2a4)

6点の美術作品画像、博物館の所蔵記録、画像内の断片、暗号化された保管庫、鍵付きの画素選択、最後の認証付き暗号文をつなぐ問題。断片を並べる順序は画家の生年で、Vermeer、Goya、Van Gogh、Klimt、Munch、Schieleとなる。

| 画家 | 配布画像を変更せずに調べる場所 | 本体8バイト–チェックサム2バイト（hex） |
| --- | --- | --- |
| Vermeer | PNGの独自coLlチャンク | `be5f329a4841bece-ee99` |
| Goya | PNGのIEND後にあるBase64 | `b086be35786cac71-8ab3` |
| Van Gogh | アルファ0の縁の下にあるRGB | `c1d322deee71edf2-cfb8` |
| Klimt | JPEG内のsteghide。belvedere.at/912を使用 | `07961017e80fb1e3-b14e` |
| Munch | 行優先で7画素ごとの青チャネルLSB | `7141415e3a146329-c2dc` |
| Schiele | 先頭176行のPNGフィルタバイト。1を0、2を1と読む | `74718896e450c77c-e551` |

各断片は8バイトの本体と、SHA-256(本体)の先頭2バイトに等しいチェックサムを持つ。6個の本体を生年順に連結し、salt **collector-v2:ossuary**、info **master**、長さ32のHKDF-SHA256でmaster keyを得る。

正規化した所蔵番号は **mauritshuis.nl/670**、**museodelprado.es/P000749**、**moma.org/472.1941**、**belvedere.at/912**、**nasjonalmuseet.no/NG.M.00939**、**belvedere.at/3171**。この順にLF（`0x0a`）で区切り、末尾にはLFを付けず、UTF-8バイト列のSHA-256を取る。得られる `40762afb7192c838fccba2284ebcb0b760da6a35698d4c6d0fb2da17088f46b1` の生の32バイトをsaltとし、HKDF(master, info **zip**, 長さ16)で保管庫のパスワードを作る。保管庫の整合性検査に通った。Belvedereはコレクションのサブドメインではなく基底ドメインを使う必要がある。

保管庫のreadmeはHKDF(master, 空のsalt, info **stego**, 長さ32)を指示する。0から始めるカウンタを符号なし8バイトのビッグエンディアンで表し、この鍵でHMAC-SHA256を計算する。digestの先頭8バイトをビッグエンディアン整数と読み、画像を行優先に並べた **6,220,800** 個のRGBバイト位置で剰余を取る。既に選んだ位置は飛ばし、新しい位置の最下位ビットを選択順に集める。ビットは上位からバイトに組み、先頭4バイトをビッグエンディアンのpayload長 **451** と読む。その後ろの451バイトがpayload、続く4バイトがpayloadのビッグエンディアンCRC32で、検算に通った。payloadは[GitHubリリース](https://github.com/broski-creator/velarium-ossuary-ledger-7f3c2a/releases/tag/v1.0)、flag.enc、注釈付きタグ内のserialを示す。assetのSHA-256もpayloadと一致する。HKDF(master, serialの生バイト, info **flag**, 長さ32)をAES-256-GCMの鍵とし、assetの先頭12バイトをnonce、**collector-v2** をAADとして復号すると認証に成功する。

Flag: **hiCTF{marble_sparrow_9eb44602eedb764aac082a3816b7d7cb}**

公式問題画面で正解が表示され、最終チーム一覧にも含まれる。元ZIPのSHA-256は **b957032dc484894c3bfffc8fdecb5d6e269f2c24b5996422672fa45d6fe37f98**。AIエージェントで各搬送路を調査したが、断片のチェックサム、保管庫の整合性、payloadのCRC、assetのハッシュ、AES-GCMタグ、公式受理をそれぞれ確認した。
