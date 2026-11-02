# Echoes of a Forgotten Canvas

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=d5dffde1-b0d3-4b45-b2c9-6f9c7f5e76db)

破損したPNG、IENDの後ろに付いた暗号化ZIP、さらにsteghideと高さ偽装を施したJPEGの三層構造だった。PNGで前半、最後のJPEGで後半を回収して結合する。

1. PNGは4000 × 4000と宣言するが、IHDRのCRCとIDATの展開長から正しい高さは4500と分かる。高さを直すと、右下のアルファ領域に **hiCTF{mu1t!14y3r3d_** が見える。紛らわしい二文字は両方とも数字の1。
2. IEND以降のバイト列はZipCryptoのZIP。辞書候補から見つかった **dreamcatcher** でcarrier.jpgを展開でき、ZIPの完全展開とJPEGヘッダーで確認した。
3. JPEG内の詩にある “profound” をパスフレーズにしてsteghideからfinall.jpgを抽出する。
4. finall.jpgのSOF0は高さ647を宣言するが、画像データはその下にも続く。高さを800に変えると灰色の帯に **st3g0o_ju5t_l0v333}** が現れる。

Flag: **hiCTF{mu1t!14y3r3d_st3g0o_ju5t_l0v333}**

元の問題ファイルは[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=d5dffde1-b0d3-4b45-b2c9-6f9c7f5e76db)から取得する。チームの公式解答一覧にもこの問題が含まれる。

AIエージェントは各層の解析と、当初の1/lの読み違いの訂正に使用した。結論はCRC・展開長、ZIPとsteghideの展開成功、JPEGの可視文字、公式の解答記録で確認した。
