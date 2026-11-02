# RESURRECTION (Operation Eclipse Void)（Forensics）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=ed0cc69e-48ea-49a0-bcda-1d538e752423) · ReFlection、Agentic AI部門

公式配布ZIPのSHA-256は `46834f01b2a123bfdc10ec9d6d79a0d73347597922d282388bab0b9d399e0643` です。中身はスパースな1 GiBのディスクイメージです。先頭のMBR、GPT、NTFSブートセクタはゼロ化されていますが、最終LBAのバックアップGPTとバックアップNTFSブートセクタから、パーティション開始がLBA 32768、`$MFT` がLCN 85845と分かります。バックアップGPTのパーティション配列CRC欄は改変されており、実際の配列CRCは `0x8f6e0090` です。

5つの断片が別々のファイルシステム構造に入っています。NTFSレコードの更新シーケンス修復を行ってから、各断片の序数ラベルに沿って復元します。

| 断片 | 場所 | 取り出し方 |
| --- | --- | --- |
| 1 | MFTレコード179、`kbdusx.dll` | ファイルオフセット `0x400` 以降の42バイトのPEオーバーレイを、COFFタイムスタンプの4バイト `80 85 ec 65` で繰り返しXORします。 |
| 2 | MFTレコード111、`Confidential_Q3` | 非常駐 `$DATA` のrunlistにある34個のクラスタ数をASCII値として読みます。 |
| 3 | MFTレコード181、`tx_journal.log` | 80バイト固定長レコードそれぞれのオフセット32のFILETIMEを読みます。隣接タイムスタンプの差から10,000を引き、16を足すと1文字になります。 |
| 4 | MFTレコード193、`Security_Audit.evtx` | 有効なEVTX BinXMLレコードで、ファイルオフセット `0x11c9` の個数 `0x21` に続く `0x11cd` からの33個のリトルエンディアンDWORDを文字コードとして読みます。 |
| 5 | NTFS `$Bitmap` | 割当済みクラスタとMFT runlistが参照する全クラスタを比較します。バックアップブートセクタを除くと孤立クラスタが40個残り、その隣接LCN差39個がASCII値になります。 |

`f!r5t--`、`53c0nd--`、`th1jd--`、`f01_1rth--`、`51f7h--` という少し変わった接頭辞は、証拠内に保存された序数ラベルです。ラベルのみを除いて5つの本文を連結すると、次の値になります。

```text
hiCTF{p3_0v3rl4y_71m3d473574mp_k3y_n7f5_runl157_cl5_g30m37ry_7r4ns4c710n_n4n0_f1l371m3_3v7x_b1n4ry_xml_70k3n5_b17m4p_orph4n_v01d_r35urr3c710n}
```

最後の断片は孤立クラスタの*中身*ではなく、その*配置*に埋め込まれています。クラスタ自体はゼロなので、ファイルとして読むだけでは見つかりません。ローカルの復元処理は読み取り量を制限し、最大の単一読み取りも69,632バイトでした。ReFlectionの大会終了時の公開解答済み一覧にも本問が含まれ、復元値は記録上の受理済み回答と一致します。
