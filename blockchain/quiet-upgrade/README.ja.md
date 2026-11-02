# Quiet Upgrade（ブロックチェーン）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=ef7c21c7-ee4c-440e-8355-0dea1db2e75d)の配布 ZIP の SHA-256 は `e9d1567aa232756d02f5d0f0b2852f2236bf9e351098532da6300582c1ccfb87` です。隔離された自チームのチェーンを解き、フラグは公式に受理されました。

## ストレージ衝突と proxy 更新

`SettlementProxy.admin` はストレージ slot 0 にあります。V1 が proxy から `delegatecall` で実行されると、`SettlementV1.branchOperator` も slot 0 を使います。登録権限の確認がない `registerBranch(player)` が `branchOperator` を書くと、実際には proxy の admin が player に変わります。これで `upgradeTo()` を呼べます。

更新時の検査は新実装の `proxiableSlot()` の戻り値だけです。期待値 `keccak256(abi.encodePacked(keccak256("quiet-upgrade.proxiable"), proxy))` を返し、`drain()` を持つ実装を用意しました。proxy 経由で `drain()` を呼ぶと proxy の文脈で動くため、`Treasury.release()` からは `msg.sender == proxy` に見え、準備金を player へ移せます。

配布コントラクトを使ったローカルテストで `Setup.isSolved()` が true になり、自チームの公式インスタンスでも準備金ゼロと true を確認しました。チェッカーは `hiCTF{sl0t0_c0llision_then_a_qu1et_upgrade_90dc819530}` を返し、公式画面でも受理されました。対象は問題の delegatecall ストレージ配置です。
