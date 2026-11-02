# Standing Order (Blockchain)

[日本語](README.ja.md)

We solved the [official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=4b0623b2-54b1-412a-8407-cc469bf7f490) on our isolated private chain. The challenge archive SHA-256 was `1d8cc1775f249e3ad8c8d1afc3ebff3e065e7dc238384152ba84992d7c51d823`.

## Reuse the voucher before it is marked used

`Setup` funds `Disbursement` with 20 ETH and gives the player a committee-signed voucher for 1 ETH. The signed digest covers only `(amount, nonce)`: it does not bind a recipient or distinguish `acknowledge()` from `disburse()`. In the vulnerable `disburse()` path, the ETH transfer to the recipient happens **before** the voucher's used bit is set. `acknowledge()` sets its bit first, which makes the order difference clear.

We deployed a receiving contract and called `disburse()` with the legitimate voucher. Its `receive()` callback called `disburse()` again while the used bit remained false and the reserve held at least 1 ETH. Twenty nested calls paid the 20 ETH reserve. After the deepest callback, the stack unwound and marked the voucher used. We neither recovered the committee key nor forged a signature.

The transaction succeeded with 20 `Paid` events. A later read showed reserve 0, voucher used, and `Setup.isSolved() == true`. The checker returned `hiCTF{one_sig_two_paths_then_the_l00p_f4222d7e32}` and the official UI showed `Flag correct!` and `Challenge solved!`.
