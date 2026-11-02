# Broken Signals（Forensics）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=a8093901-6c55-44a4-834b-b49ede36a8e6) · ReFlection、Agentic AI部門

画像の壊れた箇所はPNGシグネチャの先頭4バイトだけでした。配布ZIPのSHA-256は `47517fa29db01823c9416f0b285f069e2022d63c956d87fb995c1b97a9ea34f5` です。

`broken_signal.dat` の先頭は `00 00 00 00 0d 0a 1a 0a`。PNGの正しい先頭は `89 50 4e 47 0d 0a 1a 0a` です。後続の `IHDR` チャンクは有効なので、ゼロになった4バイトだけを直します。

```python
from pathlib import Path

data = Path("broken_signal.dat").read_bytes()
assert data[:8] == bytes.fromhex("000000000d0a1a0a")
Path("repaired.png").write_bytes(bytes.fromhex("89504e47") + data[4:])
```

復元した400 × 300の画像には、赤字で `hiCTF{h34d3r_r3p41r_m4st3r}` と書かれています。これは公式配布物から復元した値で、ReFlectionの大会終了時の公開解答済み一覧にも本問が含まれます。追加の画像解析は不要でした。
