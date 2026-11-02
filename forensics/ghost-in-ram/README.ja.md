# Ghost in RAM（Forensics）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=b9a2cff7-7dd1-4702-a125-a2ce7eccae11) · ReFlection、Agentic AI部門

公式配布ZIPのSHA-256は `5d93dd23e89876a4d7caead1dca17121ae36a17a29941a6c0bd75fccf13f020e` です。中身は約2 GiBのx86-64 Linuxメモリイメージで、ゲストのバナーはKali Linux `7.0.12+kali-cloud-amd64` を示します。この正確なカーネルのデバッグ用BTFと `System.map` からVolatility 3のプロファイルを作り、プロセスとメモリマップを調べました。

`linux.psaux.PsAux` にはPID 130の `syncfsd` があり、対応する実行ファイルは `/bin/host` でした。そのデータ領域の8 KiBマッピングは仮想アドレス `0x4af000–0x4b1000` にあります。`0x4af0e0` にはリトルエンディアンの長さ30、`0x4af0f0` からは30バイトの難読化データがあります。復元した `/bin/host` の `0x401ac0–0x401acf` の命令は各バイトを `0x5a` でXORし、一時領域へ平文を書き込みます。プログラムは後でその平文を消去します。

対象KaliカーネルのシンボルプロファイルとVolatility 3を用意します。ローカルのVolatility Framework 2.26.2では、BTFプロファイルの互換性のため、schema 6.2.0で `btf` と `symdb` を許可し、このBTFにない `module_sect_attr` を任意にする2点の修正も必要でした。標準インストールでは同等の調整が必要な場合があります。ローカルでは `.deps/bin/vol` を使い、次のコマンドでダンプしました。

```sh
VOLATILITY_SYMBOLS=kali-symbols
PYTHONPATH=.deps .deps/bin/vol -q -s "$VOLATILITY_SYMBOLS" -f mem.elf linux.psaux.PsAux
PYTHONPATH=.deps .deps/bin/vol -q -s "$VOLATILITY_SYMBOLS" -f mem.elf linux.proc.Maps --pid 130
mkdir -p dumps
PYTHONPATH=.deps .deps/bin/vol -q -s "$VOLATILITY_SYMBOLS" -f mem.elf -o dumps linux.proc.Maps --pid 130 --dump --maxsize 4194304
```

ここで使った `.deps` とシンボルプロファイルは、このwriteupには含めていません。仮想アドレス範囲が `0x4af000–0x4b1000` のVMAダンプを選び、以下の例では `pid-130-data-vma.bin` とします。復号は次の通りです。

```python
from pathlib import Path

vma = Path("pid-130-data-vma.bin").read_bytes()  # 先頭仮想アドレス 0x4af000
n = int.from_bytes(vma[0xe0:0xe4], "little")
assert n == 30
print(bytes(b ^ 0x5a for b in vma[0xf0:0xf0 + n]).decode())
```

出力は `hiCTF{gh0st_pr0c3ss_rng_pwn3d}` です。メモリ中に平文で見える `hiCTF{stop_here}` と `hiCTF{d3bug_m3}` は囮の文脈にあり、提出していません。ReFlectionの大会終了時の公開解答済み一覧にも本問が含まれ、この値はメモリからの復元結果とも一致します。
