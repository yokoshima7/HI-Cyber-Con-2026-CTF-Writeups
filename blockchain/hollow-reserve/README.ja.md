# Hollow Reserve（ブロックチェーン）

[English](README.en.md)

ReFlection の隔離された[問題インスタンス](https://ctf.hiddeninvestigations.net/challenges?challenge=bb99717c-d62a-4b9f-b0a4-017e257d8765)で解きました。目標は準備金 vault の残高を所定のしきい値より減らすことです。

## 1 取引内のオラクル操作

融資機構は担保を評価する際、浅いトークンプールの `spotPrice()` をそのまま読むオラクルを使っています。初期プールは 1,000 COL と 100,000 RSV で、1 COL は 100 RSV 相当でした。プレイヤーの 100 COL を攻撃コントラクトに預け、問題の手数料ゼロの flash lender から 4,000,000 RSV を借ります。コールバック内で RSV を浅いプールへ交換すると、表示価格は約 167,608 RSV/COL に上がります。この価格を参照した融資機構から、100 COL を担保に 9,100,000 RSV を借りられました。見かけ上は 75% の融資上限内です。

得た COL を RSV に戻して flash loan を返済し、融資分の RSV を残します。取引後、vault は当初 10,000,000 RSV から 900,000 RSV となり、`Setup.isSolved()` が true、チェッカーが `hiCTF{th1n_p00l_was_the_r3al_0racle}` を返しました。公式提出も受理されています。原因は操作可能な瞬間価格をそのまま信用判断に使ったことです。
