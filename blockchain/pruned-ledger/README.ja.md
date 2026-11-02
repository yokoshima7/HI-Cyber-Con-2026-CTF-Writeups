# Pruned Ledger（ブロックチェーン）

[English](README.en.md)

署名済み取引アーカイブから[このオフライン問題](https://ctf.hiddeninvestigations.net/challenges?challenge=be13630e-cdb5-4dbb-ae6b-954cc51edf08)を解きました。ZIP の SHA-256 は `aefb1f1300ca8758ba53fa17ae485a06ed1d48afd5bca941c305a23210dc78fd` です。復元したフラグは公式画面で受理されました。

## 最終ストレージだけでなく履歴を追う

署名済み legacy 取引を復号し、送信者とコントラクト作成アドレスを復元します。ケースタグ `0xca5ef11e` を持つ 4 個の `Relay` 作成取引からコンストラクタの `nextHop` をたどると `Ledger` に到達し、そのコンストラクタの参照値は `pruned_storage` です。

重要なのは `prune()` 時点で残る値ではなく、**`seal()` の前に最後に成功した `configure()`** の `record` で、これは `calldata` です。`seal()` の引数を `keccak256(SEAL_DOMAIN || ledgerAddress || recordAtSeal)` で XOR 解除すると `never`。記録済みの誤った `unlock()` 呼び出しの caller を使い、コンストラクタのマスク済み note を `keccak256(NOTE_DOMAIN || ledgerAddress || caller)` で戻すと `forgets` です。4 語を順番に組み合わせると `hiCTF{pruned_storage_calldata_never_forgets}` になります。

solver は取引署名、Relay の鎖、ソースが定めるマスク式を検証します。アーカイブ全体の Anvil 再生は行っていません。ソースに基づく復元と公式受理が結果の根拠です。
