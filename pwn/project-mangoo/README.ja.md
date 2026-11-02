# Project Mangoo — 負のチャネル番号から深いstack pivotへ

分類: Pwn。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=8dfee4d3-d2b5-4d3a-ac10-9d62abdf1be9) · [English](README.en.md)

配布されたWindows x86-64 PEはTLSのメニューサービスとして動く。32バイトのsession challengeは認証に見えるが、バイナリの静的解析で各バイトの可逆変換だと分かった。位置 `i` のtokenは次で求まる。

```text
token[i] = ROL8(challenge[i], 3) XOR ((0x11 * i) & 0xff) XOR 0x6a
```

認証後、`Query Channel` は番号を符号付き16ビット値として扱い、15を超える値しか拒否しない。そのため負数でテーブルの手前を参照できた。`-3` はPEのRVA `0x1550` にある関数へのポインタ、`-1` はroot key文字列へのポインタ、`0` はtelemetry heapへのポインタを漏らす。最初のポインタから `0x1550` を引けば、そのプロセスのimage baseになる。

`Ingest Telemetry Stream` は指定したバイト列をtelemetry heapへ書く。`Sync Channel` にも下限チェックがなく、`-2` でheapの `+0x10` から関数ポインタを取り出して呼ぶ。約8 KiBの一つのstreamに以下のガジェットとデータを配置した。

| 段階 | PE RVA | 動作 |
| --- | --- | --- |
| 1回目のpivot | `0x16d0` | `rsp` をtelemetry heapへ移す |
| 深いpivot | `0x19000` | `pop rsp; ret` で `heap+0x2000` へ移す |
| 引数設定 | `0xbd60` | `pop rcx; ret` で漏れたroot keyポインタを渡す |
| 出力 | `0x18348` | import済みの `puts` thunkを呼ぶ |
| 終了 | `0xbd61`, `0x183e0` | stackを整列して終了 |

最初に `heap+0x18` の近くから直接 `puts` を呼ぶとクラッシュした。`heap+0x2000` へ再度pivotすると、関数呼び出しに必要なstack余裕ができる。一度だけtelemetryを書いて `Sync Channel -2` を呼ぶと、自チームのインスタンスは `hiCTF{n0_g4dg3ts_n0_sh3llc0d3_jusT_p1v0t_d33p3r_952b589bc3}` を出力した。公式UIが受理し、最終公開解答一覧にもProject Mangooが載った。

公式ZIPのSHA-256は `6ec89ce54df8cfca960ef028270e674688a0fa10633e9ffa10d48c4558e91a3f`。配布物の `MANGOO_ROOT_KEY=hiCTF{fake_flag_for_local_testing}` はローカル用の値。上記offsetは配布PEで検証したが、この解法ではローカルWine実行は行っていない。
