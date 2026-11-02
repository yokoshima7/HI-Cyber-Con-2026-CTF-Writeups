# Entitlement（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=e06aac60-dd99-4331-bc41-99eea0a44ed7) · 配布ZIPのSHA-256: `d468c69996ba1e34344d616d3f0ccf1fb2de6367a498a0dda4be67041a8feca0`

x86-64 ELFはUPXで圧縮されていたが、3か所の `UPX!` マーカーが `HI4!` に変えられていた。元ファイルは残し、コピーを修復すると `upx -t` と `upx -d` で展開できた。検証は16桁16進数のserial、25桁16進数のactivation code、時間のかかるフラグ復号の3段階である。

serial検査のVMは入力を `GF(2^64)` の要素として扱う。還元多項式の下位64ビットは `0x2b395c2099596d9f`。VMは `(serial XOR 0xd1705c3b2e33689b)^13 XOR 0xba6b1f3cb925c25a` を計算する。逆算では、期待値 `0x30cefbec2e4bc466` と `0xba6b1f3cb925c25a` をまずXORし、体上で `13⁻¹ mod (2⁶⁴−1)` 乗してから、入力側の `0xd1705c3b2e33689b` をXORする。これでserialは `8f7db18bd70e193b` となり、復号したVMでも一致した。

activation codeは楕円曲線上の離散対数 `nP = Q` で判定される。この曲線は位数が基礎体の素数に等しい異常曲線（`#E(F_p)=p`）だった。p進持ち上げを使うSmart攻撃で `2977e17b118de75b3b4e921a4` を復元し、スカラー倍による `Q` との一致を確認した。

最後に、serialとactivationをリトルエンディアンで連結してハッシュから2048ビットの初期値を作り、**5億回の剰余平方**を行う。ELFのMontgomery演算が通常の剰余乗算と対応することを確認し、チェックポイント付きのGMP実装で計算を完了した。結果からSHA-256の鍵ストリームを作って64バイトを復号し、バイト和がELF内の `0x133d` と一致した。NUL埋めを除いた平文は `hiCTF{>o<_C0ngrats_Her3_1s_Y0ur_HI4_Subscript1on_^_^}`。自チームの公式解答済み一覧にも含まれる。

serialとactivationだけでは復号は完了せず、5億回の平方計算も必要である。
