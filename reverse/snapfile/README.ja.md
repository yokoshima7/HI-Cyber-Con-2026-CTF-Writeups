# Snapfile（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=f00787dd-0538-47c9-8431-1499eed7d3d0) · 配布ZIPのSHA-256: `33ba2e74970adb7f6f25c9b6a85eae326b2e7b5724c09e71fad6ed7a28f51eb6`

配布物はstrip済みx86-64 Crystal製 `snaptool` のみで、`.snap` の見本はない。パーサーを静的解析すると、有効なファイルはちょうど104バイト。先頭40バイトには `SNAP`、版 `0x0002`、種別 `0x03`、`SNAP-LNG`、ビッグエンディアン32ビットの記述子 `0x28, 0x10, 0x38, 0x20, 0x58, 0x08` が入る。続く56バイトをゼロにして、`0x08..0x5f` を対象とする末尾8バイトのビッグエンディアンchecksumを求めた。

```python
s = 0x1357BDF02468ACE1
for byte in data[8:0x60]:
    t = ((s + byte) * 0xD1B54A32D192ED03) & 0xFFFFFFFFFFFFFFFF
    s = t ^ (t >> 29)
data[0x60:0x68] = (s ^ 0x58).to_bytes(8, 'big')
```

データ部が全ゼロの場合、末尾は `fd47ab989124f3f2`。バイナリは固定40バイトのヘッダーをハッシュし、`SHA256(header_hash || counter_be32)` をカウンター0と1で連結したうちの46バイトを、埋め込み暗号文とXORする。復号文のSHA-256はもう一つの埋め込みダイジェストに一致した。

フラグは `hiCTF{r3c0nstruct3d_th3_sn4pf1l3_by73_by_by73}`。改変していない `snaptool` は生成した104バイトを受け入れて同じフラグを表示し、公式サイトでも `Flag correct!` と `Challenge solved!` を確認した。
