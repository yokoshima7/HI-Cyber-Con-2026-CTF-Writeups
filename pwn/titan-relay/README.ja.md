# Titan Relay — 自分のVM gateを開くcapsuleを組み立てる

分類: Pwn。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=e3ee5fb0-e4ec-4135-8751-128213da17cd) · [English](README.en.md)

Windows x86-64のRustバイナリは、長さと16進表記のcapsuleを受け取る。register VMのbytecodeとして解釈する前に、位置 `i` のバイトを `(0x71 + 0x3d*i) & 0xff` とXORして復号する。課題は、VMプログラムを組み立ててホスト側handlerのgateを通し、正しいorder構造体を渡すことだった。

VMには64ビットregisterが8個ある。静的解析ではloopがimage address `0x1400035a7` 付近、handler gateが `0x140003b26` 付近だった。使う命令は次のとおり。

| Opcode | 解法での役割 |
| --- | --- |
| `0x21` | 内部token領域へのポインタを読む |
| `0x71` | cookieの下位・上位32ビットと `cookie XOR handler_address` を読む |
| `0x32` | register下位32ビットを、許可された符号付きoffsetへ書く |
| `0x51` | register 6をorderポインタとしてhandlerを呼ぶ |

許可された符号付き書き込み範囲には、オブジェクトoffset `+8` と `+16` のgate値も含まれていた。capsuleはcookieの前後半を結合し、handler addressをXORから復元して、この2箇所を書き換える。その後VM確保領域の `+0x80` にorder、`+0xa0` に暗号化したpathを構成する。handlerはcookie、派生32ビット値2件、定数 `11`、cookieのバイトを繰り返しXORしたpath先頭11バイトを検査する。復号したpathはWine形式の `Z:\flag.txt` とNULで、Wineの `Z:` 対応から `/flag.txt` を読める。

インデックスごとのXORを適用する前のVMプログラムは180バイト。配布PEをローカルWineで動かし、テスト用 `/flag.txt` の内容が返ることを確認した。自チームのサービスは3接続で `hiCTF{ru5t_vm_g4te_and_h4ndler_ch41n_25d260a06b}` を返した。公式画面に `Flag correct!` と `Challenge solved!` が表示され、最終公開解答一覧にも載っている。

公式ZIPのSHA-256は `7f8fe53c63aa1268d7fa06a44089caee87bc160097915ed217044262a2fd2f0e`。capsuleは配布バイナリから導出した。ここではフィールドとopcodeの関係を説明し、問題バイナリや一時VMは配布しない。
