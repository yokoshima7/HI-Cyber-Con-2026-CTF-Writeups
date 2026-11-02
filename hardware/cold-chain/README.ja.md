# Cold Chain — 再発するデフロスト設定を止める

[English](README.en.md)

分類: Hardware · チーム: ReFlection（Agentic AI）· [問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=fb980c53-cd11-4b3a-b397-613a63395f1d)

公式 `cold-chain.zip` のSHA-256は `6b11d090f36f12a2e1b4456b0d0aa84b0c20f855c8aef0d9cd63ab968bd48374`。ColdLinkの技術者用ツール、CLMP/1.1仕様、historianのサンプルが入っている。目標は6台の冷蔵ケースをすべて5°C未満に60秒間保つことだが、初期状態では全台が12°Cで `defrost` になっていた。

## 原因と修正

サンプルのhistorianには `macro_apply macro=M2 schedule=S9 detail=re-enabled_forced_defrost` が繰り返し現れ、S9を削除した後にも再設定されていた。手動でモードを変えるだけ、またはスケジュールを削除するだけでは維持できない。公式ツールの `auth_token(serial, nonce)` で自チームのコントローラーへ認証し、変更前に `CASES`、`SCHED LIST/GET`、`MACRO GET`、`STATUS` を確認した。

実際の状態は、S9が有効な `force_defrost`、M2が90秒ごとにS9を戻す `ensure_schedule` だった。通常冷却用のS1とS3はすでに有効。初期 `STATUS` もデフロスト設定、温度超過6台、再設定マクロを障害として示していた。

必要だった変更は次の2件。

```text
MACRO DISABLE M2
SCHED SET S9 action=noop enabled=0
```

M2とS9を読み直して変更を確認した後、S1/S3によって各ケースの温度が下がった。`CASES` で温度低下を追い、最終的に `STATUS` が `cases_cold=6/6 held=67s`、`compliant=1` とフラグを返した。6台とも約2.31〜2.33°Cでtripはなかった。同じフラグの公式問題画面での受理と、終了時の公開解答済み一覧も確認されている。

Flag: `hiCTF{cold_chain_restored_defrost_cleared_b2c2f403bb}`

新しいインスタンスで再現する場合は、先に実際のscheduleとmacroのIDを読む。M2/S9は今回観測した値である。AIを使ってhistorianとプロトコル仕様、稼働状態を突き合わせ、変更はすべてコントローラーの再読取で確認した。
