# Titan Relay — build a capsule that opens its own VM gate

Category: Pwn. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=e3ee5fb0-e4ec-4135-8751-128213da17cd) · [日本語](README.ja.md)

The Windows x86-64 Rust binary accepted a length and hex-encoded capsule. Before interpreting it as register-VM bytecode, it decoded byte `i` by XOR with `(0x71 + 0x3d*i) & 0xff`. The reverse-engineering task was to construct a VM program that would satisfy the host handler's gate and pass it a valid order structure.

The VM had eight 64-bit registers. Static disassembly placed its loop near image address `0x1400035a7` and its handler gate near `0x140003b26`. The useful instructions were:

| Opcode | Effect used in the solve |
| --- | --- |
| `0x21` | Load a pointer to an internal token area |
| `0x71` | Read the low and high cookie halves, and `cookie XOR handler_address` |
| `0x32` | Write a register's low 32 bits at a bounded signed VM offset |
| `0x51` | Invoke the handler with register 6 as the order pointer |

The allowed signed writes reached the gate fields at object offsets `+8` and `+16`. The capsule combined the two cookie halves, unmasked the handler address, and wrote both gate fields. It then built an order at VM allocation offset `+0x80` and its encoded path at `+0xa0`. The handler checked the cookie, two derived 32-bit values, the constant `11`, and the first 11 path bytes XORed with repeating cookie bytes. Those bytes decoded to the Wine path `Z:\flag.txt` plus a NUL; Wine's `Z:` mapping exposed `/flag.txt` to the Windows process.

The final VM program was 180 bytes before the per-index XOR encoding. Running the distributed PE under local Wine with a fixture `/flag.txt` returned the fixture flag. The team's service returned `hiCTF{ru5t_vm_g4te_and_h4ndler_ch41n_25d260a06b}` on three connections. The official challenge page displayed `Flag correct!` and `Challenge solved!`; Titan Relay is in ReFlection's final public solved set.

Official ZIP SHA-256: `7f8fe53c63aa1268d7fa06a44089caee87bc160097915ed217044262a2fd2f0e`. The capsule bytes were derived from the supplied binary. This explanation gives the field and opcode relationships; the raw challenge binary and temporary VM are not distributed here.
