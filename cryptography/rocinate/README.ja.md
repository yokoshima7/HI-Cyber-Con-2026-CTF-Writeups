# Rocinate（暗号）

[English](README.en.md)

対象は[この Rocinate](https://ctf.hiddeninvestigations.net/challenges?challenge=3fb2ceda-d5d3-4369-b887-2b18ff34a203)で、後から追加された未解答の「Rocinate Revenge」とは別問題です。公式 ZIP の SHA-256 は `2f7b41f0cf2d52ca975e05f69bfd99b311c65712dcb4c5b524431c4a1c36e41a` でした。

## 攻め方

`chall.py` は Python の MT19937 `random` で公開指数 `Cs` を 100 個作ります。`randint(1,N)` の候補生成1回で連続する32ビット出力を64個消費し、棄却があればさらに候補を生成します。`Cs[15]` からの棄却のない連続区間には、下位9ビットを除く624個の出力が現れます。欠けた9ビットの512通りを後続の `Cs` で検査して乱数状態を復元し、逆方向へたどって以前の `r` と `e` を取得しました。再計算した公開パラメータ `a`, `b` も一致します。

`r` から一次合同法の列 `R_i` を再生成すると、100 個すべての `T_i = R_i^e mod N` と `Z_i % R_i == 0` が成立しました。商 `Z_i/R_i` は `s^Cs[i] mod N` なので、互いに素な指数 2 個の Bézout 係数から `s` を回収し、全 100 個で照合しました。`s` を文字列に戻すと `hiCTF{lmaoooo_w0t???y0u_d1d_17_??435p37++}`。公式画面にも `Flag correct!` と `Challenge solved!` が表示されました。

再現用 solver は標準ライブラリと配布 `chall.txt` だけで動きます。最初の出力に合うだけで採用せず、後続の指数で乱数状態を検証するのが重要です。
