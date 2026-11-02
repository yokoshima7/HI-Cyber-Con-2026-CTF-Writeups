# Apex Engine — 残高競合の後にパスの競合を起こす

分類: Pwn。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=596582e4-cc87-4c51-9e76-8f4d2838af6b) · [English](README.en.md)

サービスは100クレジットから始まる。非同期の送金workerは、互いの引き落としが反映される前に残高を検査していた。100クレジットの送金を8件まとめて送ると、各workerが元の100を見て通過する。8件の処理後、符号なし64ビット残高は `100 - 800` から `18446744073709550916` にアンダーフローし、VIP機能を使える。

VIPではenclaveのファイルstreamを操作できた。slot 0の初期パスは無害な `/tmp/preview.txt`。stream workerはこのパスを検査し、約25 ms待ってから、同じ可変slot内のパスを開く。その間にslot 0を `/flag` へ変更すると、検査した値と実際に開く値が異なる。

解法の流れは次のとおり。

1. 100クレジットの送金を8件一気に投入し、VIPへupgradeする。
2. 初期パスでenclave slot 0を作る。
3. slot 0のstreamを開始し、workerの待ち時間内にパスを `/flag` へ変更する。
4. streamの出力を読む。threadのスケジュールが変わるため、少数の待ち時間だけ試した。

配布ELFを隔離したローカル環境で検証すると、編集まで2 msの場合にテスト用flagが返った。同じ手順を自チームの問題インスタンスで行い、`hiCTF{t0ct0u_mult1thr34d_r4c3_c0nd1t10n_w1n_8d3f_0860951188}` を取得した。公式画面に `Flag correct!` が表示され、最終公開解答一覧にもApex Engineが載った。

公式ZIPのSHA-256は `aa932101aa0b92c17bcedd5bb76a6cf6fa3bd622f686ce9316b75fe5e4ef00a7`。配布ZIPやインスタンスはここには複製せず、公式の配布物を使う。
