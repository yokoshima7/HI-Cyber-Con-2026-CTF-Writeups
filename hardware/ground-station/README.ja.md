# Ground Station — インターロックと信頼済みバックアップを修正する

[English](README.en.md)

分類: Hardware · 部門: Agentic AI · [問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=1cfece5d-3d61-4ed6-bd5b-5cebb48a1bd0)

公式 `ground-station.zip` のSHA-256は `21eecb59a1d0559081a7aaf53abc2e8187178dd4d667279906932dde4a574a19`。x86-64のファームウェア、保守クライアント、GSP/1.0の仕様書が入っている。燃料充填テストには技術者認証と安全かつ信頼済みのラダープログラムが必要だった。

## 認証

配布クライアントは技術者用の応答を計算しないため、ファームウェアを逆アセンブルした。鍵生成は `0x1f2e3d4c` を初期値とする32ビットLCGで、各段階で乗数 `0x19660d`、加数 `0x3c6ef35f` を使い、`((state >> 17) XOR (index * 0x5b)) & 0xff` を1バイトずつ出力する。得られた16バイト鍵をリトルエンディアン32ビットの4語 `a,b,c,d`、8バイトのセッションnonceを `n0,n1` とする。加算をすべて32ビットで折り返し、次を12ラウンド実行する。

```text
a = ROL(a + n0, 7)
b = ROL(b XOR a, 11)
c = ROL(c + b + n1, 17)
d = ROL(d XOR c, 19)
n0 = n0 + d + round * 0x9e3779b9
n1 = ROL(n1 XOR a, 13)
(a,b,c,d) = (b,c,d,a)
response = LE32(a XOR c) || LE32(b XOR d)
```

配布ELFの機械語をローカルで実行し、固定テストベクトルと追加の3 nonceで実装と一致することを確認してから、自チームのインスタンスへ `AUTH` した。

## 修正

仕様上 `INTERLOCK_OK` はタンク温度45°C以下、圧力100 kPa以下のときだけ成立する。`PROG LIST` と `BACKUP GET` を読むと、稼働中とバックアップの両方で温度条件だけが **145** になっていた。他のrungは仕様と一致した。watchdogが有効なため、稼働中プログラムだけ直してもテスト開始時に復元または拒否される。実施した操作は次のとおり。

```text
PROG SET INTERLOCK_OK (TANK_TEMP <= 45) AND (TANK_PSI <= 100)
BACKUP SAVE
BACKUP STATUS
WDOG STATUS
RUNTEST
```

修正したrungをバックアップへ保存すると、live、backup、trustedのchecksumが一致し、`arm_will_restore=0` になった。watchdogは有効のまま。1回の `RUNTEST` が `SUCCESS reason=fill_target_reached_scan_51` とフラグを返し、別の `STATUS` でも `solved=1` と同じフラグを確認した。公式問題画面でも受理された。

Flag: `hiCTF{ground_station_fueling_test_nominal_f43b56f7e6}`

ラダーの条件だけでなく、バックアップとwatchdogの整合性が解答の要点。AIを用いた逆解析で認証処理を特定し、機械語での照合、サービスの読み直し、公式受理で確認した。
