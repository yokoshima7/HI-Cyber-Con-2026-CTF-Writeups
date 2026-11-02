# The Foxglove Trace

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=50ab1909-d636-4e0c-868f-49d7772834aa)

未完成の行動記録ツールから、メモ、信頼するWi-Fiアクセスポイントの重み、33行のスキャン結果、成功した一回の詳細ログが残されている。メモによると、歩いている時だけ電波強度を数え、信頼度で重み付けする。ログでは歩数差 **40** が静止、**41** が移動と判定されるので、この整数データでは **step_delta > 40** が条件となる。

aps.confに載るアクセスポイントだけについて、条件を満たす行の **signal × weight** を合計した。

| アクセスポイント | 採用行数 | スコア |
| --- | ---: | ---: |
| FoxgloveCoffee_Guest | 5 | 1,044 |
| CafeDelMundo | 3 | 364 |
| NETGEAR-8841 | 3 | 240 |
| HomePlex_5G | 1 | 174 |

自宅のルーターは一行ごとの電波が強いが、移動中の行はほぼ残らない。最大スコアの名前を表記そのままで提出する。

Flag: **hiCTF{FoxgloveCoffee_Guest}**

公式のチーム解答一覧に受理済みとして載る。元ZIPのSHA-256は **e76d9c898c069fa96e85d929009f3bd16e94a747940e90f7a23df2424ef3e5e4**。アクセスポイント名は配布された問題ファイルからのみ取得した。
