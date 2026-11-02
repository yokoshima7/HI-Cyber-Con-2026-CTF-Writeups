# ChronoGrind（暗号）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=61784143-ff04-444c-868d-faa4c53939e5)の配布 ZIP の SHA-256 は `5a5316e688fdd9ee3ae30d85a5659a52d0a5c0adf74ac71ba95583467ac256b3` でした。提出した解答は公式に受理されています。

## 解法と検証

`state.dat` は各バイトを `0x4c` で XOR した `CGD1` レコード列です。復元すると、2048 ビットの法、241 進の種、**90 億回の逐次的な剰余平方**という条件が出ます。埋め込み SHA-256 でパラメータの読み取りを確認できます。最終状態を 256 バイトのビッグエンディアンで表し、SHA-256 から `flag.enc` の ChaCha20-Poly1305 鍵を作ります。

まず GMP で途中まで計算し、原子的に保存したチェックポイントから macOS 上の OpenSSL 3 Montgomery 演算へ引き継ぎました。同一チェックポイントからの 500 万段は GMP と OpenSSL で完全一致し、実データの 1,000 段遷移も Python で別途照合しました。最終チェックポイントは 90 億段到達を記録し、Poly1305 の認証付き復号で `hiCTF{n1c3_w0rk_n0w_t4k3_s0m3_r3$t}` を取得。公式画面の `Flag correct!` も確認しました。

この問題では逐次状態の正確な継承が核心です。認証タグと公式受理まで確認して、計算結果を解答と判断しました。
