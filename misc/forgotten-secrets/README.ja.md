# Forgotten Secrets

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=a6e70ac6-77ea-4adc-aada-3b1cd0a325a6)

配布されたメモリダンプ風のバイナリにフラグは平文で入っていない。文字列 **DEADBEEF** を8バイトのASCIIマーカーとして探す（16進バイト列 `de ad be ef` ではない）。その直後の27バイトを取り、続けてASCII文字列 **CAFEBABE** があるレコードを探す。保存済みソルバーは22件を発見し、27バイトの本体はすべて同一だった。

各バイトを **0x42** とXORすると、次のフラグになる。

Flag: **hiCTF{m3m0ry_dump_d1g_d33p}**

ソルバーは復号前に22件という件数と内容の一致をassertするため、重複が整合性確認になる。公式のチーム解答一覧でも受理済み。公式ZIPのSHA-256は **bfde7ee94bc2841f3c9fc6275e6f005256df9d1a77363f291ec8adc90929840a**。

この文章は保存されていた13行のソルバーから再構成した。探索中の詳細ログは残っていないため、確認できる抽出手順を中心に記した。
