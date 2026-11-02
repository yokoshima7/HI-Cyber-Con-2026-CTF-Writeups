# Log Jam（暗号）

[English](README.en.md)

[公式 Log Jam](https://ctf.hiddeninvestigations.net/challenges?challenge=4c01e897-f33f-45bd-8b00-249d493f6d8e) の配布 ZIP の SHA-256 は `25350191fa48891bf7ef70202a283fbbb9ea1d9c1c8904b5a5a4d09903fccfee` でした。ReFlection は最終公式解答済み一覧に含まれています。

## 復元

ZIP 内の `params.json` には、`h = g^x mod p` を満たす 16 進数の `p`, `g`, `h` と AES-GCM の nonce、暗号文、タグがあります。求めるのは離散対数 `x` です。PARI/GP の `znlog(Mod(h,p), Mod(g,p))` で `471774559909450042061` を得て、別途 `pow(g,x,p) == h` を確かめました。

鍵は `SHA256(str(x).encode())`、つまり **x の 10 進 ASCII 表記**をハッシュしたものです。整数のバイナリ表現ではありません。AES-GCM の `decrypt_and_verify` で認証タグを検証し、`hiCTF{W0W1_y0u_4ctu4a11y_s01v3d_1t_ju$t_L1k3_tH4t}` を得ました。認証済みの平文であり、公式のチーム解答済み記録にも載っています。

再現には配布 JSON の解析、PARI/GP による離散対数、べき乗関係の検査、上記の鍵導出と GCM タグ検証を順に行います。問題サービスへの接続は不要です。
