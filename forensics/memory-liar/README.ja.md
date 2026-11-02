# Memory Liar（Forensics）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=c7150717-fd46-4206-9784-bbe6afe2631e) · ReFlection、Agentic AI部門

配布ZIPのSHA-256は `26a5e19d3e6a3c591e008abf1d644ecab735197d06c5c1e2b4a42e64183c1414` です。ファイルオフセット `0x3550f1` 付近には平文の `hiCTF{...}` が見えますが、文字列自身が偽の囮だと示しています。手掛かりはプロセス構造です。複数の `Proc` プールタグのうち `0x35d004` のものは、PID 1337の `winxnet.exe` を示します。このプロセスの `0x35d0c0` にあるリストリンクは、通常のプロセスと異なり自身を指しています。

PID 1337の `ROOT` レコードは `0x35f000` から始まり、難読化されたデータは `0x35f010` からです。先頭3バイトから同じXOR鍵を独立に求められます。`0x35 ^ 'h' = 0x34 ^ 'i' = 0x1e ^ 'C' = 0x5d` です。閉じ波括弧まで `0x5d` でXORすると、次の値になります。

```text
hiCTF{dk0m_unl1nk_3pr0c3ss_l1st_cr0ss_ch3ck_7c3a9f}
```

平文の候補は囮で、この値は自己参照するプロセスと対応するROOTレコードに結び付いています。ReFlectionの大会終了時の公開解答済み一覧にも本問が含まれます。
