# Obfuscated Flow（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=bbb7442a-7577-430e-a10e-e17dffffe581) · 配布ZIPのSHA-256: `ddaca1f93d3f748482982814ed307b58f9fba73e6298bb4551594a2b344a2d30`

ELFが受け入れる40バイトのパスキーが、フラグの中身である。検証器は連続する8バイトずつを別々の数学的条件で調べるため、各部分を独立に逆算した。復元した4バイト整数はリトルエンディアンの印字可能ASCIIに絞る。

最初の部分は `2^31-1` 上の積と二次式から復元する。2番目は楕円曲線上の `T = P + [1337]Q` を逆にたどり、3番目はbaby-step/giant-stepで離散対数を求める。4番目は `0xfffffffb` 上の連立一次式を解き、5番目は和と積から得た候補を2個の素数条件で選ぶ。得られる断片は `m4th_c0n`、`tr0l_fl0`、`w_3ll1pt`、`1c_dlog_`、`4f7b2c9e`。

結合結果は `hiCTF{m4th_c0ntr0l_fl0w_3ll1pt1c_dlog_4f7b2c9e}`。元のx86-64バイナリへ入力すると `ACCESS GRANTED` と同じフラグを表示し、公式問題画面でも受理された。
