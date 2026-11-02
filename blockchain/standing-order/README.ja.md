# Standing Order（ブロックチェーン）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=4b0623b2-54b1-412a-8407-cc469bf7f490)を隔離された自チームの private chain で解きました。配布 ZIP の SHA-256 は `1d8cc1775f249e3ad8c8d1afc3ebff3e065e7dc238384152ba84992d7c51d823` です。

## 使用済みになる前に voucher を再利用

`Setup` は `Disbursement` に 20 ETH を置き、プレイヤーに委員会署名付きの 1 ETH voucher を渡します。署名対象は `(amount, nonce)` のみで、受取人も `acknowledge()` と `disburse()` の区別も結び付けません。脆弱な `disburse()` では、受取人への ETH 送金が **voucher の使用済みビットを立てる前**に行われます。対照的に `acknowledge()` は先にビットを立てます。

受信コントラクトを配置し、正規 voucher で `disburse()` を呼びました。`receive()` コールバックから、まだビットが false で残高が 1 ETH 以上ある間、同じ `disburse()` を再入呼び出しします。20 回の入れ子呼び出しで 20 ETH が払い出され、最深部から戻ると使用済みになります。委員会の鍵回収や署名偽造は不要でした。

取引は成功し、`Paid` イベント 20 件、準備金ゼロ、voucher 使用済み、`Setup.isSolved() == true` を確認。チェッカーは `hiCTF{one_sig_two_paths_then_the_l00p_f4222d7e32}` を返し、公式画面の `Flag correct!` と `Challenge solved!` も確認しました。
