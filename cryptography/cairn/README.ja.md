# Cairn（暗号）

[English](README.en.md)

ReFlection が Agentic AI 部門で解いた問題です。[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=cd968c16-2c61-4d27-a215-af9dd1bb34c1)には `challenge.json` と歩行規則があり、配布 ZIP の SHA-256 は `9f8f036fbb3a25341dc58602c9d8c340c786f1ba882095c45bac69b785796f21` でした。

## 解法

フラグの暗号鍵は、`GF(p²)` 上の **1,048,576 段の逐次歩行**の終点から作られます。`p = 2²⁵⁶ − 2³² − 977`、点 `a+bi` は `(a,b)` で表し、`i² = −1` です。各段 `t` では `LE32(a) || LE32(b) || BE8(t) || salt` を SHA-256 でハッシュします。先頭バイトで `ℓ ∈ {2,3,5,7}` に対応する配布多項式 `Φ_ℓ` を選び、次のバイトで根を選びます。`Φ_ℓ` の各変数の次数は `ℓ+1` です。重根を除いた後の根を、正規化した `(a,b)` の辞書順に並べてから添字を適用する必要があります。

Python と PARI/GP で有限体の根を計算し、`f / gcd(f,f')` で重根を除去、根の個数を確認し、1,000 段ごとに再開用チェックポイントを保存しました。初段と最初の 1,000 段は独立に照合しています。最後に `SHA256(LE32(a_T) || LE32(b_T) || "IsogenyLabyrinth")` を鍵として AES-256-GCM を認証復号しました。256 ビット整数を含むので、数値を丸める通常の JavaScript JSON パーサーは使えません。

認証タグが一致し、`hiCTF{w41k_th3_sup3rs1n9u14r_l46yr1ntH}` を得ました。公式画面でも `Flag correct!` と `Challenge solved!` を確認しています。近道は確認できず、規則どおりの歩行を完走した解法です。
