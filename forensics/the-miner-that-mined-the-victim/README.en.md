# The Miner That Mined The Victim (Forensics)

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=dd259ba4-ec98-4470-99f2-869a8baaa688) · Agentic AI division

The challenge was a 14-question forensic quiz. The official ZIP has SHA-256 `5ac6011a696266ecaa40b9cb4948a247a6a3ca1ebe465cc60249c170d77d2182`. We inspected the provided Windows artifacts without running any executable from the archive. The questions had to be answered in order in one TLS session; the service returned `Correct!` for each and printed the actual challenge flag only after all 14.

| # | Accepted answer | Evidence in the attachment |
| --- | --- | --- |
| 1 | `Microsoft Windows NT 10.0.26200.0` | `ransomware_debug.log` OS banner. |
| 2 | `UTC-7, 420` | `SYSTEM` hive: `ControlSet001\Control\TimeZoneInformation\ActiveTimeBias=420`. |
| 3 | `https://limewire.com/d/Ak55K#Yrx3FgK3du` | Edge History `downloads.tab_url`. |
| 4 | `42d377fe-8948-4a32-809f-69a51e6dbcfa` | Edge History `downloads_url_chains` redirect URL's `downloadId`. |
| 5 | `2026-05-13 14:25:36 UTC` | Edge download end time, converted from Chromium microseconds since 1601-01-01 UTC. |
| 6 | `2026-05-13 14:26:55 UTC, 1` | `MINER.EXE-9A2B223D.pf`: last-run FILETIME and v31 Prefetch run count at raw offset 200. |
| 7 | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App\9.0.16\System.Security.Cryptography.dll, 2026-05-13 14:26:58 UTC` | Sysmon Event 7 image-load record. |
| 8 | `HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\DisableAntiSpyware` | Sysmon Event 13 registry write, DWORD 1. |
| 9 | `T1685` | The corresponding MITRE ATT&CK technique for disabling or modifying tools. |
| 10 | `hiCTF{finally_u_proved_ur_worthiness}` | Resident `$MFT` record 147927. This was a *quiz answer*, not the challenge flag. |
| 11 | `C:\Users\milon1\Downloads\miner, 2026-05-13 14:27:47 UTC` | Recycle Bin `$IGDL3PH` metadata in MFT record 1908. |
| 12 | `179623` | Deleted folder size in the same `$I` metadata. |
| 13 | `I will always be there for you bro!` | Sysmon Event 23 hash for `bar.txt` matched archived resident plaintext in MFT record 147908. |
| 14 | `help` | Sysmon Event 23 for `noting.txt` says it was shredded with pattern `0x706c6568`; little-endian bytes spell `help`. |

Two parsing details mattered. `Sysmon.evtx` advertised one active chunk, while relevant records were in inactive chunks; parsing all chunk slots yielded about 7,460 records. A Prefetch parser reported run count zero from offset 208, but the v31 file's raw count at offset 200 is one, which the quiz accepted.

The Q10 string looks like a final flag, but submitting it to the official challenge form returned an incorrect verdict. After all quiz answers, the service printed `hiCTF{c4r3ful_4b0ut_cr4ck3d_t001s_a18d7bbdf5}`. The official challenge UI then displayed `Challenge solved!`, and the team's final public solved list includes this challenge.
