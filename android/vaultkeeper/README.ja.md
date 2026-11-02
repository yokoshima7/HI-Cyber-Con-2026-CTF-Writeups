# VaultKeeper（Android）

[English](README.en.md) · [概要](../../README.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=2771edbb-c032-4c72-ab9e-343acfc0262b) · 配布ZIPのSHA-256: `7c0ccbd218561af27d1f51dcb18cf3ef5ab566e538788d88e285de1fb8d7aa10` · 展開後APKのSHA-256: `400681608c68dd3613630f4dee34fd17dadad6f95bb3a3d7c6c7ca2112f59320`

目立つ `FlagRepository.getMasterKey()` は `MainActivity` で短いvault IDを表示するための文字列で、flagを直接開かない。claimの経路は8,192バイトの `assets/vault.bin` を読み、nativeの `nvSeed`、128セルを混ぜる `CellMixer.k1`、2,048バイトのプログラムを開く `nvUnseal`、`CellMixer.k2`、VMを実行する `nvExec`、51バイトを検証する `nvFinal` と続く。ランダムなgesture tokenはUIの呼出順序を制限するが、静的なVMプログラムの回収とエミュレーションには不要である。UIの最終alertは例外後にも出るので、claim成功の根拠にはならない。

`nvSeed` の再現で重要だった修正は、まず `seed = SHA256(vault.bin || b"VK-SEED-v1")` を求め、行番号0～15のそれぞれについて `seed || LE32(row)` を1回ずつハッシュし、16個のダイジェストをすべて保存すること。得られた512バイトをリトルエンディアン32ビット値128個に分割する。[cell_mixer.py](cell_mixer.py) と [derive_program.py](derive_program.py) でseed、unseal、mixerの経路を再現できる。復元したVMプログラムのSHA-256は `ffd80cdd77c649e287672fab4ae72eaadb1ab242531e3440d9f4736ecca618ae`。

VM先頭の1億回のレジスタループはCで高速化し、残り358命令をPC `0x58f` の成功終了まで解釈した。出力の先頭51バイトをnativeの読み取り専用配列2つとself-mix hashでXORすると `hiCTF{!!I_10v3_4ndr0!d_m4n_m4k!ng_th3m_f331_g0Od!!}` となる。`SHA256(b"VK-TAG-2026" + candidate)[:16]` は埋め込み値 `62672db15a0b6a4793b351292f29a0b3` に一致する。大会終了時の自チームの公式解答済み一覧にもVaultKeeperが含まれる。

自作の復元コード5本は [cell_mixer.py](cell_mixer.py)、[derive_program.py](derive_program.py)、[emulate_vm.py](emulate_vm.py)、[final_check.py](final_check.py)、[vm_hot.c](vm_hot.c)。Python側は標準ライブラリのみを使い、1億回ループの補助コードにはCコンパイラが必要となる。APK内のx86-64 nativeライブラリは読み取るだけで、実行はしない。

## macOSで再現する

上の公式問題リンクから `VaultKeeper.zip` をダウンロードする。macOS、Python 3、`clang`（Xcode Command Line Tools）が必要。次のコマンドは**このwriteupのディレクトリから**実行する。APK、展開ファイル、コンパイルした補助コード、生成したVMデータは別の一時ディレクトリに置く。`ZIP` にはダウンロードしたZIPの**絶対パス**を設定する。先頭2回の `shasum` の結果が冒頭のZIPとAPKの値に一致することを確認してから続行する。

```sh
ZIP="/absolute/path/to/VaultKeeper.zip"
WORK="$(mktemp -d)"
mkdir -p "$WORK/assets" "$WORK/lib/x86_64"
cp cell_mixer.py derive_program.py emulate_vm.py final_check.py vm_hot.c "$WORK/"
cd "$WORK"
shasum -a 256 "$ZIP"
unzip -p "$ZIP" VaultKeeper.apk > VaultKeeper.apk
shasum -a 256 VaultKeeper.apk
unzip -p VaultKeeper.apk assets/vault.bin > assets/vault.bin
unzip -p VaultKeeper.apk lib/x86_64/libvaultnative.so > lib/x86_64/libvaultnative.so
clang -O3 -dynamiclib -o vm_hot.dylib vm_hot.c
python3 derive_program.py
python3 emulate_vm.py
python3 final_check.py
```

上記のVMプログラムのハッシュ、PC `0x58f` での成功終了、`SHA-256 tag match: True`、フラグが得られる。[emulate_vm.py](emulate_vm.py) はこのAPKで使われるopcodeを実装している。`vm_hot.dylib` の読み込みと上記ビルドコマンドはmacOS専用で、別のOSでは共有ライブラリのビルド方法と読み込むファイル名を変更する必要がある。
