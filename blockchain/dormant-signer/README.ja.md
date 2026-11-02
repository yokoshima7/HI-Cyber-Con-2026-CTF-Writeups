# Dormant Signer（ブロックチェーン）

[English](README.en.md)

ReFlection は[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=c2a91af0-0164-4988-acff-92cc455c09c9)の署名済み取引アーカイブを解析しました。ZIP の SHA-256 は `9397090fc7419f8c581199533ee42ec3786e82ddcf0bd302f05c63d75542f957` です。

## 復元手順

対象は取引 52 で生成され、352 で破棄された本番用 `Authorizer` です。もう一方は sealed 状態で、設問の対象ではありません。380 個の署名済み legacy 取引を復号し、コントラクト作成アドレスを復元します。本番 signer は取引 137 と 234 の異なる要求ダイジェストに対して **同じ ECDSA の `r`** を使っていました。low-`s` と回復ビットから nonce の符号が逆であることを考慮して署名方程式を解き、秘密鍵を得ます。導出アドレスがコンストラクタの signer と一致することも確認します。

次にソースの規則を取引順に再生します。有効な `authorize` は 20 件で、署名者違い、重複、破棄後の呼び出しは累積ダイジェストに入れません。復元した鍵で指定された liveness ダイジェストに署名し、`final_seal`、`running_digest`、`escrow_mask` の XOR から escrow の平文を戻すと、`bytes32` にゼロ埋めされた `layout_undead_borrowed_betrays` になります。

受理フラグは `hiCTF{layout_undead_borrowed_betrays}`。取引ハッシュ、signer アドレス、ダイジェスト演算をローカルで確認し、公式の解答済み記録にも含まれています。完全な EVM 再生は行わず、取引とソース規則をオフラインで再生した点が再現上の留保です。
