# Night Batch（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=9ee0bc40-5ee5-4db7-823e-360c6ed98db6) · 配布ZIPのSHA-256: `64ad99c6d690a7fac13b7d7cb56e2cc7c8553feceda2b503305dcb3ff6afcc9c`

x86-64 ELFはGnuCOBOL製で、18桁の口座キーを要求する。各数字をpacked decimalにコピーし、22個の式を10を法として検査した後、最後の加重和を94と直接比較する。式には一次項、二乗項、2数字の積が混ざっている。

式を調べるため、**コピーしたバイナリだけ**の拒否分岐を無効化し、検査を途中で止めずに計測した。全ゼロ、単一数字、数字ペア、ランダム入力による214件の比較値を集め、多項式を当てはめた。24件の未使用ランダム入力でも全式が一致した。各数字を0～9に制限し、23本の式をZ3で解くと、唯一のキー `481702596318740925` を得た。

最後は**改変していない**ELFをオフラインのx86-64 QEMUで実行した。求めたキーで `hiCTF{c0b0l_p4ck3d_d3c1mal_n1ghtly_b4tch!}` を出して正常終了し、誤ったキーは `account rejected` になった。公式の最終解答済み一覧にもNight Batchがある。改変コピーは式の観測用であり、元の検証器に受理された根拠とは分けている。
