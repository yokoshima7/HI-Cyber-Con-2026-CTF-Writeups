# Just Give Me The Flag Man（暗号）

[English](README.en.md)

[公式配布物](https://ctf.hiddeninvestigations.net/challenges?challenge=0c29db29-bbf3-4dd1-b07a-6e5f05db558f)の SHA-256 は `47250d4a65be0eb4ff5e8b4c31ae2120f95bb086f301ebb2467f7640614952c0` です。ReFlection の提出は公式に受理されました。

## 復号の鎖

ファイルには 2 文字のトークンが 52 個あります。`u v w x y z` を順に 16 進数字の `f e d c b a` とみなし、各トークンの上位・下位ニブルを交換します。得られた ASCII85 の範囲にある 52 文字を**全体で反転**し、Adobe ASCII85 を復号して 41 文字にします。続いて ROT47、標準 basE91 を適用すると 33 バイトのフラグらしい中間結果が出ます。最後に英字だけ Atbash と ROT13 を重ねます。アルファベットの 0 始まり添字では `(12 − 添字) mod 26` です。数字と記号はそのままです。

取得したフラグは `hiCTF{sh1ft1ng_7hr0ugh_7h3_b4s3s}`。ASCII85 と basE91 は再符号化による一致も確認しました。`u..z` の 720 通りの割当てを調べると、ニブル交換後の印字可能性だけでは絞れず、後段の復号結果が重要です。公式の `Flag correct!` で全体を確認しました。
