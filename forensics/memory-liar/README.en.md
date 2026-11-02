# Memory Liar (Forensics)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=c7150717-fd46-4206-9784-bbe6afe2631e) · Agentic AI division

The supplied ZIP has SHA-256 `26a5e19d3e6a3c591e008abf1d644ecab735197d06c5c1e2b4a42e64183c1414`. A visible `hiCTF{...}` string near file offset `0x3550f1` explicitly calls itself a fake decoy. The useful clue is structural: several process pool tags `Proc` occur in the memory image, and the one at `0x35d004` identifies `winxnet.exe`, PID 1337. Its process list links at `0x35d0c0` point back to itself, unlike the ordinary linked processes.

A `ROOT` record for PID 1337 begins at `0x35f000`. Its obfuscated bytes begin at `0x35f010`. The first three bytes imply the same XOR key independently: `0x35 ^ 'h' = 0x34 ^ 'i' = 0x1e ^ 'C' = 0x5d`. XOR the record with `0x5d` through the closing brace to recover:

```text
hiCTF{dk0m_unl1nk_3pr0c3ss_l1st_cr0ss_ch3ck_7c3a9f}
```

The decoy is a plain string; the answer is tied to the self-linked process and matching root record. The team's final public solved list includes Memory Liar. The exact flag above is the locally decoded value.
