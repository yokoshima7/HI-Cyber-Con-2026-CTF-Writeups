# Cold Beacon（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=3aef51b5-1216-4919-b80d-d49c9f358977) · 配布ZIPのSHA-256: `a01791f8259c7bcf1eb07f578abc686b2a4ab78d4fe410f565c74624e52610d8`

strip済みのNim製ELFは24バイトの鍵を要求する。鍵には、テーブルで指定された23個のXOR・加算・乗算の検査と、追加の3個のバイト間条件がかかる。印字可能文字列を総当たりする代わりに、8ビットの制約として解いた。

ELFから各行の演算種別、参照位置、目標値を読み、鍵の各バイトを `0x20..0x7e` に制限した。計算はELFと同じ8ビットの折り返しを使う。追加条件には `k[10] == 0xa8 - k[9]`、`k[20] == k[12] XOR k[4]`、`k[12] + k[13] == 0xe3` がある。

これらの条件だけでは候補が複数残る。各候補について `seed = SHA256(key)` を求め、`SHA256(seed || counter_be32)` を連結した鍵ストリームで埋め込みの47バイトをXOR復号した。復号文のSHA-256がELF内の期待値に一致する候補を選ぶ。

結果は `hiCTF{c0ld_b34c0n_cfg_uns34l3d_fr0m_th3_s4mpl3}`。ローカルで埋め込みダイジェストと一致し、大会終了時のReFlectionの公式解答済み一覧にもCold Beaconが含まれる。使用したソルバーは `z3-solver` ベースで、問題バイナリはここには再配布しない。
