# Quiet Upgrade (Blockchain)

[日本語](README.ja.md)

The [official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=ef7c21c7-ee4c-440e-8355-0dea1db2e75d) archive had SHA-256 `e9d1567aa232756d02f5d0f0b2852f2236bf9e351098532da6300582c1ccfb87`. We solved our isolated team chain and submitted the accepted flag.

## Storage collision and proxy upgrade

`SettlementProxy.admin` sits in storage slot 0. `SettlementV1.branchOperator` also sits in slot 0 when V1 runs by `delegatecall` through the proxy. `registerBranch(player)` has no registrar check and writes to `branchOperator`, thereby changing the proxy admin to the player. The new admin can call `upgradeTo()`.

The upgrade guard only checks the candidate implementation's `proxiableSlot()` value. We supplied an implementation returning the expected `keccak256(abi.encodePacked(keccak256("quiet-upgrade.proxiable"), proxy))` and adding `drain()`. Called through the proxy, `drain()` executes in the proxy's context. `Treasury.release()` therefore sees `msg.sender == proxy`, satisfying its caller check and moving the reserve to the player.

A local test with the supplied contracts set `Setup.isSolved()` to true; the official team instance independently showed an empty reserve and true solved state. Its checker returned `hiCTF{sl0t0_c0llision_then_a_qu1et_upgrade_90dc819530}`, which the official challenge UI accepted. The exploit concerns the challenge's delegatecall storage layout, not a real public chain.
