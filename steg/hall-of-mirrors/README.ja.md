# Hall of Mirrors

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=94f0bbb8-c6c1-491b-b576-90309bbf01d3)

運営が追加したarchivist datasheetが解法の鍵だった。そこには、WAVのインターリーブされた16ビットサンプルをSplitMix64で選ぶ方法、1ビットあたり2回の乱数、MIRRORS1フレームとCRC32が書かれていた。

スペクトログラムから最初に読んだ鍵は誤っていた。64ビットのフレームマジック全体を検証条件にして少数の桁の修正を調べると、**9C4F1E7A3B50D682** が唯一一致した。この鍵で6,266バイトのMVM1イメージを取り出せ、保存CRC32と計算CRC32はともに **e2046fb1** だった。

MVM1仮想機械は64 KiBのHarvard型メモリ、16本の64ビットレジスタ、分岐、自己書換え命令を持つ。20,395回の命令取得の後、MIRRORS1で始まる5,083バイトを出力した。中身はsecp256k1のパラメータ、48件のECDSA署名、暗号化されたデータ。署名の保存順を **(z, r, s)** と読むと48件すべてが検証に通り、他の5通りは一件も通らなかった。

各nonceの上位12ビットがゼロという制約を使い、32署名から格子で秘密鍵を回復した。公開鍵との一致と48件すべてのnonce上限を確かめ、datasheetのKDFとストリーム暗号で復号した。

Flag: **hiCTF{h1dd3n_numb3r_l4ttice_le4k}**

公式のチーム解答一覧にも受理が記録されている。再現には公式WAVとdatasheet、Python、格子計算用のfpylllが必要。大きなWAVはここに再配布しない。

AIエージェントを使って搬送路、VM、署名を独立に点検した。CRC、署名48/48件、公開鍵一致、nonce制約、公式受理記録が判断の根拠である。
