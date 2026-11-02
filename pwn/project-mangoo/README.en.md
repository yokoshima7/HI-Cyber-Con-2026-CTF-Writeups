# Project Mangoo — a negative channel index led to a deeper stack pivot

Category: Pwn. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=8dfee4d3-d2b5-4d3a-ac10-9d62abdf1be9) · [日本語](README.ja.md)

The supplied Windows x86-64 PE ran behind a TLS menu. Its 32-byte session challenge looked like authentication, but static analysis of the binary showed a reversible byte transformation. For byte position `i`, the required token was:

```text
token[i] = ROL8(challenge[i], 3) XOR ((0x11 * i) & 0xff) XOR 0x6a
```

After authentication, `Query Channel` treated its number as a signed 16-bit value and rejected only numbers above 15. Negative indices therefore reached entries before the intended table. Querying `-3` disclosed a code pointer at PE RVA `0x1550`, `-1` a pointer to the root-key string, and `0` the telemetry heap pointer. Subtracting `0x1550` from the first pointer gave the image base for this process.

`Ingest Telemetry Stream` copied attacker-supplied bytes into that heap. `Sync Channel` had the same missing lower-bound check: index `-2` invoked a function pointer taken from telemetry heap offset `+0x10`. The payload placed these binary-relative gadgets and data into one approximately 8 KiB stream:

| Step | PE RVA | Effect |
| --- | --- | --- |
| First pivot | `0x16d0` | Move `rsp` to the telemetry heap |
| Deeper pivot | `0x19000` | `pop rsp; ret` to `heap+0x2000` |
| Argument | `0xbd60` | `pop rcx; ret` with the leaked root-key pointer |
| Output | `0x18348` | Call the imported `puts` thunk |
| Finish | `0xbd61`, `0x183e0` | Align and exit |

An initial direct `puts` call near `heap+0x18` crashed. Pivoting again to `heap+0x2000` left enough stack room for the call. A single telemetry write and `Sync Channel -2` then printed `hiCTF{n0_g4dg3ts_n0_sh3llc0d3_jusT_p1v0t_d33p3r_952b589bc3}` on the team's instance. The official UI accepted it, and Project Mangoo appears in ReFlection's final public solved set.

Official ZIP SHA-256: `6ec89ce54df8cfca960ef028270e674688a0fa10633e9ffa10d48c4558e91a3f`. The shipped `MANGOO_ROOT_KEY=hiCTF{fake_flag_for_local_testing}` is a local fixture. The offsets above were verified in the supplied PE; a local Wine execution was not performed for this solve.
