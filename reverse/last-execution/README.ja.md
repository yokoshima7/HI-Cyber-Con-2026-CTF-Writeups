# Last Execution（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=da8426d4-3f64-4cd1-9747-ed4cd3ad6480)

配布イメージには `EXE-9` インタープリタの説明がある。しかし `PRIMER` はエンコード時のトレースと3か所で食い違う。トレースと独立したself-testのSHA-256から、初期ページ回転は17、dispatchは `pc >> 3`、テーブル行の漸化式は `i * 13` と特定できた。この設定でself-testのダイジェストを再現した。

`EXEC_LIMIT` は20,015,998,343,868回という反復回数を指定する。機械状態は786,432回ごとに繰り返すため、完全な周期分の寄与を計算し、残りだけをエミュレートした。短縮版を使う前に、1回と1,000回の実行について、レジスタとsegment chainの全状態が素朴な実行と一致することを確認した。

最終状態のR2は、配布された `TELEMETRY` の `FF975FD2B1F14576` ではなく `FF975FD2B1F15576`。配布値では意図的な `TEST_SEAL_2` の偽フラグしか開けない。計算した真の状態から鍵を作ると、`WILL_SEAL` が正しいPKCS#7 paddingで開き、`hiCTF{3x3c_9_r3m3mb3rs_4ll_but_th3_l4st_h4lt_l13s}` を得る。公式サイトで受理され、最終解答済み一覧にも含まれる。
