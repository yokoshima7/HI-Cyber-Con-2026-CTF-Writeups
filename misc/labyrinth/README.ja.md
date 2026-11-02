# Labyrinth

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=8d5871ff-b72f-49a5-9bdc-235d11dddd42)

フレーム形式のTCPパズルを解いた後、毎回変化する迷路を探索する問題。各フレームは **4c 42 59 7f**、1バイトのopcode、2バイトのビッグエンディアン長、payloadで構成される。平文の挨拶は通らない。

1. 空payloadのHELLO（01）を送り、応答の8バイトnonceをPROBE（10）へ渡す。
2. PROBEには変換の入出力例と4バイトの課題がある。変換はバイト列を逆順にし、各バイトをセッション固有のmaskとXORする。ゼロ入力の例からmaskを読み、変換結果をANSWER（30）で返す。
3. 迷路の各部屋は座標、扉のbitmask、flags、2バイトのtokenを返す。MOVE（20）はN/E/S/Wの方向1バイトと現在の部屋のtokenを要求する。探索しながら部屋と辺を記録する。
4. 封印された門で02を送ると、入口からの**最短経路**を求められる。記録したグラフを幅優先探索し、方向バイト列をANSWER（30）で送る。

サービスが **hiCTF{l34rn3d_th3_t0ngu3_w4lk3d_th3_l4byr1nth_528f336956}** を返した。公式問題画面の解答済み表示と最終チーム一覧でも確認した。

光る場所やopcode 40から返る **hiCTF{not_the_exit}** は意図的なデコイ。迷路とtokenはセッションごとに変わるため、固定ルートを一般解にしない。AIエージェントでプロトコルを整理し、自チームのインスタンスで確認した。
