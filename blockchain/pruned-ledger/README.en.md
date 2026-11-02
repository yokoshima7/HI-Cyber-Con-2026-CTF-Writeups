# Pruned Ledger (Blockchain)

[日本語](README.ja.md)

ReFlection solved this [offline blockchain challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=be13630e-cdb5-4dbb-ae6b-954cc51edf08) from the signed transaction archive (SHA-256 `aefb1f1300ca8758ba53fa17ae485a06ed1d48afd5bca941c305a23210dc78fd`). The official UI accepted the reconstructed flag.

## Trace the archived state, not only final storage

Decode the legacy signed transactions, recover their senders and creation addresses, and follow the four `Relay` creations tagged `0xca5ef11e`. Their constructor `nextHop` links lead to a `Ledger`. Its constructor case reference is `pruned_storage`.

The crucial record is the **last successful `configure()` before `seal()`**, not the later value visible at `prune()`: that record is `calldata`. The `seal()` transaction carries a masked entry. XOR it with `keccak256(SEAL_DOMAIN || ledgerAddress || recordAtSeal)` to get `never`. An observed wrong `unlock()` attempt exposes the caller needed to reverse the constructor's masked note with `keccak256(NOTE_DOMAIN || ledgerAddress || caller)`, yielding `forgets`. These four fields form `hiCTF{pruned_storage_calldata_never_forgets}`.

The solver verifies signed transactions, walks the relay chain, and applies the source-defined masks. We did not replay the entire archive in Anvil; source-level reconstruction and official acceptance are the evidence for this result.
