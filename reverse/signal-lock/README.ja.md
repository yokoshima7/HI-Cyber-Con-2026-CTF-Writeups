# Signal Lock（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=04a6db25-845e-4655-aa92-3e6288012f96) · 配布ZIPのSHA-256: `93651d91c60187eb03e2162653f627fb360425597eb0f61415c469abfaf9df99`

アーカイブにはgzip圧縮されたErlang BEAMモジュールが入っていた。展開してOTP 26のバイトコードを読み、`verify/1` を追うと、入力は符号なし64ビット整数として解釈される8バイトのトークンだった。変換は次の通り。

```text
rotl64(((x XOR 0xa5a5a5a55a5a5a5a) * 0x9e3779b97f4a7c15) mod 2^64, 29)
  + 0x0123456789abcdef  (mod 2^64)
```

結果は `0xafe7c5708f40ebc4` と一致しなければならない。加算値を引き、29ビット右回転し、奇数の乗数の逆元を掛け、最後にXOR定数を適用すると、トークンは `g4m30v3r`（16進数で `67346d3330763372`）となる。初回はXOR定数の転記ミスによって不正なトークンになったため、ここは特に注意した。

`unlock/1` は64ビットトークンと32ビットのビッグエンディアンのカウンターをSHA-256にかけ、得られたバイト列を埋め込みの48バイトとXORする。改変していないモジュールをOTP 26で実行すると `hiCTF{b34m_byt3c0d3_n3v3r_l13s_s3ss10n_unl0ck3d}` が返り、公式解答済み一覧にもSignal Lockが含まれる。
