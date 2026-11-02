# RESURRECTION (Operation Eclipse Void) — Forensics

[日本語](README.ja.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=ed0cc69e-48ea-49a0-bcda-1d538e752423) · Agentic AI division

The official ZIP has SHA-256 `46834f01b2a123bfdc10ec9d6d79a0d73347597922d282388bab0b9d399e0643`. It contains a sparse 1 GiB raw disk image. The primary MBR, GPT, and NTFS boot sector are zeroed, but the backup GPT at the final LBA and backup NTFS boot sector identify the partition beginning at LBA 32768 and its `$MFT` at LCN 85845. The backup GPT's partition-entry CRC field was overwritten; the actual partition-array CRC is `0x8f6e0090`.

Five fragments are encoded in different filesystem structures. Read the NTFS records after applying their update-sequence fixups, then recover the fragments in their labelled order:

| Part | Location | Extraction rule |
| --- | --- | --- |
| 1 | MFT record 179, `kbdusx.dll` | XOR its 42-byte PE overlay after file offset `0x400` with the four COFF timestamp bytes `80 85 ec 65`, repeating. |
| 2 | MFT record 111, `Confidential_Q3` | Read the 34 cluster counts in the nonresident `$DATA` runlist as ASCII byte values. |
| 3 | MFT record 181, `tx_journal.log` | In each 80-byte record, read the FILETIME at offset 32. An adjacent timestamp difference minus 10,000, plus 16, gives one character. |
| 4 | MFT record 193, `Security_Audit.evtx` | In the valid EVTX BinXML record, a count `0x21` at file offset `0x11c9` precedes 33 little-endian DWORD character codes beginning at `0x11cd`. |
| 5 | NTFS `$Bitmap` | Compare allocated clusters to all clusters mapped by MFT runlists. Exclude the backup boot sector; 40 orphan clusters remain. Their 39 adjacent LCN differences are ASCII codes. |

The unusual prefixes `f!r5t--`, `53c0nd--`, `th1jd--`, `f01_1rth--`, and `51f7h--` are ordinal labels stored in the evidence. Remove the labels and concatenate the five payloads. The result is:

```text
hiCTF{p3_0v3rl4y_71m3d473574mp_k3y_n7f5_runl157_cl5_g30m37ry_7r4ns4c710n_n4n0_f1l371m3_3v7x_b1n4ry_xml_70k3n5_b17m4p_orph4n_v01d_r35urr3c710n}
```

The important distinction is that the final fragment is encoded in the *positions* of allocated but unmapped clusters; reading those zero-filled clusters as file content gives nothing. The local decoder used bounded reads, with the largest individual read only 69,632 bytes. The team's final public solved list includes RESURRECTION, and the reconstructed flag matches the team's recorded accepted answer.
