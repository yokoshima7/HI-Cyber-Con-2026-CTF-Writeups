# Hollow Reserve (Blockchain)

[日本語](README.ja.md)

This was solved on ReFlection's isolated [challenge instance](https://ctf.hiddeninvestigations.net/challenges?challenge=bb99717c-d62a-4b9f-b0a4-017e257d8765). The objective was to reduce the reserve vault below its threshold.

## Oracle manipulation in one transaction

The lending facility values collateral by asking an oracle that simply reads `spotPrice()` from a shallow token pool. Initially the pool held 1,000 COL and 100,000 RSV, valuing one COL at 100 RSV. We deposited the player's 100 COL into an attack contract and borrowed 4,000,000 RSV from the challenge's zero-fee flash lender. During the flash-loan callback, swapping those RSV into the shallow pool pushed the reported price to roughly 167,608 RSV/COL. The facility then accepted 100 COL as collateral for a 9,100,000 RSV loan, still within its 75% limit under the manipulated price.

The attack swapped the newly acquired COL back, repaid the flash loan, and kept the borrowed RSV. After the transaction, the vault held 900,000 of its initial 10,000,000 RSV, `Setup.isSolved()` returned true, and the challenge checker returned `hiCTF{th1n_p00l_was_the_r3al_0racle}`. The official submission was accepted. The decisive flaw is using a manipulable instantaneous spot price for the credit decision.
