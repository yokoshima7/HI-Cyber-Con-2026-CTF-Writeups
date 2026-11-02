# Ghost in the Wire（Forensics）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=618323b5-0af7-493c-b35c-7c61c3dc7a0f) · ReFlection、Agentic AI部門

配布ZIPのSHA-256は `392084661bebf2a86f4194056436ddb2b78917577bc259cc07e1210f007c563c` です。PCAPにはEthernet/IPv4/ICMPフレームが30件あります。`192.168.1.100` から `10.0.0.5` への4件はノイズで、残る26件は `10.13.37.1` から `10.13.37.2` へのecho requestです。

送信元・宛先・ICMP echo request（`icmp.type == 8`）で絞り、ICMP sequence番号の1から26まで順に、各パケットの1バイトのペイロードを連結します。

```text
hiCTF{1cmp_3xf1l_d3t3ct3d}
```

並び順はsequence番号で決まるので、キャプチャ順に依存しません。フラグ文字列は対象パケットから直接復元したもので、ReFlectionの大会終了時の公開解答済み一覧にも本問が含まれます。
