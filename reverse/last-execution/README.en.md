# Last Execution (Reverse Engineering)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=da8426d4-3f64-4cd1-9747-ed4cd3ad6480)

The supplied image describes an `EXE-9` interpreter. Its `PRIMER` disagrees with encode-time traces in three places. The traces and a standalone self-test SHA-256 commitment select initial page rotation 17, dispatch by `pc >> 3`, and table-row recurrence `i * 13`. Those settings reproduce the self-test commitment; following the prose alone does not.

`EXEC_LIMIT` asks for 20,015,998,343,868 iterations. The machine's state repeats every 786,432 iterations, so we computed the contribution of complete cycles and emulated only the remainder. Runs of one and 1,000 iterations matched a naive emulator across registers and segment chaining before using the cycle shortcut for the full limit.

The final state differs from the supplied `TELEMETRY` in register R2: actual `FF975FD2B1F15576`, reported `FF975FD2B1F14576`. The reported state opens only the deliberate `TEST_SEAL_2` decoy. Deriving the key from the emulated state opens `WILL_SEAL` with valid PKCS#7 padding and yields `hiCTF{3x3c_9_r3m3mb3rs_4ll_but_th3_l4st_h4lt_l13s}`. The official site accepted the flag, and Last Execution is in the team's final solved set.
