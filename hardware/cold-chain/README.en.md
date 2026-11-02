# Cold Chain — remove the defrost rule that keeps coming back

[日本語](README.ja.md)

Category: Hardware · Team: ReFlection (Agentic AI) · [Challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=fb980c53-cd11-4b3a-b397-613a63395f1d)

The official `cold-chain.zip` SHA-256 is `6b11d090f36f12a2e1b4456b0d0aa84b0c20f855c8aef0d9cd63ab968bd48374`. It includes the ColdLink technician toolkit, CLMP/1.1 reference, and a historian sample. The task is to keep all six refrigerated cases below 5 °C for 60 seconds. The initial state instead held every case at 12 °C in `defrost`.

## Diagnosis and repair

The sample historian repeatedly records `macro_apply macro=M2 schedule=S9 detail=re-enabled_forced_defrost`, including after S9 was deleted. This made a one-time mode change or schedule deletion insufficient. We authenticated to our own controller using the toolkit's documented `auth_token(serial, nonce)` and read `CASES`, `SCHED LIST/GET`, `MACRO GET`, and `STATUS` before changing anything.

The live controller confirmed that S9 was an enabled `force_defrost` schedule, while M2 was an enabled 90-second `ensure_schedule` macro targeting S9. Normal cooling schedules S1 and S3 were already enabled. The initial `STATUS` named three blockers: an active forced-defrost schedule, six cases above 5 °C, and an enabled persistence macro.

The minimal repair was:

```text
MACRO DISABLE M2
SCHED SET S9 action=noop enabled=0
```

We read back M2 and S9 to verify both changes. S1 and S3 then cooled the cases without a manual override. `CASES` showed falling temperatures; a later `STATUS` showed `cases_cold=6/6 held=67s`, `compliant=1`, and the flag. At that point all cases were about 2.31–2.33 °C, with no trip. The official challenge UI accepted the same flag, and the final public solved list includes Cold Chain.

Flag: `hiCTF{cold_chain_restored_defrost_cleared_b2c2f403bb}`

For a fresh instance, read actual schedule and macro IDs before applying the sequence: the sample names are evidence for this run, not a universal assumption. This writeup documents our team's contest instance and its observed response. AI assistance was used to compare the historian, reference protocol, and live status, while each state change was verified through controller readback.
