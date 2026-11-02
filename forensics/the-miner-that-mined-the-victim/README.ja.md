# The Miner That Mined The Victim（Forensics）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=dd259ba4-ec98-4470-99f2-869a8baaa688) · ReFlection、Agentic AI部門

14問に順番に答えるフォレンジッククイズです。公式配布ZIPのSHA-256は `5ac6011a696266ecaa40b9cb4948a247a6a3ca1ebe465cc60249c170d77d2182` でした。配布物の実行ファイルは起動せず、Windowsの記録類を調べました。TLS接続1回の中で14問すべてに答え、各回答に `Correct!`、最後に本当のフラグが返りました。

| 問 | 受理された回答 | 配布物中の根拠 |
| --- | --- | --- |
| 1 | `Microsoft Windows NT 10.0.26200.0` | `ransomware_debug.log` のOS表示。 |
| 2 | `UTC-7, 420` | `SYSTEM` ハイブの `ControlSet001\Control\TimeZoneInformation\ActiveTimeBias=420`。 |
| 3 | `https://limewire.com/d/Ak55K#Yrx3FgK3du` | Edge Historyの `downloads.tab_url`。 |
| 4 | `42d377fe-8948-4a32-809f-69a51e6dbcfa` | Edge Historyの `downloads_url_chains` にあるリダイレクトURLの `downloadId`。 |
| 5 | `2026-05-13 14:25:36 UTC` | Edgeのダウンロード終了時刻。1601-01-01 UTC起点のマイクロ秒を換算。 |
| 6 | `2026-05-13 14:26:55 UTC, 1` | `MINER.EXE-9A2B223D.pf` の最終実行FILETIMEと、v31 Prefetchの生データのオフセット200にある実行回数。 |
| 7 | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App\9.0.16\System.Security.Cryptography.dll, 2026-05-13 14:26:58 UTC` | Sysmon Event 7のDLLロード記録。 |
| 8 | `HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\DisableAntiSpyware` | Sysmon Event 13のレジストリ書き込み。DWORD値は1。 |
| 9 | `T1685` | ツールの無効化・変更に対応するMITRE ATT&CKの技法。 |
| 10 | `hiCTF{finally_u_proved_ur_worthiness}` | `$MFT` の常駐レコード147927。これは*クイズの回答*であり、問題の最終フラグではありません。 |
| 11 | `C:\Users\milon1\Downloads\miner, 2026-05-13 14:27:47 UTC` | MFTレコード1908のごみ箱 `$IGDL3PH` メタデータ。 |
| 12 | `179623` | 同じ `$I` メタデータにある削除フォルダのサイズ。 |
| 13 | `I will always be there for you bro!` | Sysmon Event 23の `bar.txt` のハッシュと、MFTレコード147908に残る常駐平文が一致。 |
| 14 | `help` | `noting.txt` のSysmon Event 23に消去パターン `0x706c6568`。リトルエンディアンで読むと `help`。 |

解析上の注意点は2つです。`Sysmon.evtx` のヘッダーはアクティブなチャンクを1個と示しますが、必要な記録は非アクティブなチャンクにもありました。全チャンクスロットを解析すると約7,460件の記録が得られます。また、あるPrefetchパーサーはオフセット208を実行回数としてゼロを返しましたが、このv31ファイルの生のオフセット200には1があり、クイズも1を受理しました。

10問目の文字列を公式のフラグ欄に入れたときは不正解でした。14問を正しく終えると、サービスが `hiCTF{c4r3ful_4b0ut_cr4ck3d_t001s_a18d7bbdf5}` を返しました。その後、公式問題画面の `Challenge solved!` とReFlectionの最終公開解答済み一覧でも受理を確認しています。
