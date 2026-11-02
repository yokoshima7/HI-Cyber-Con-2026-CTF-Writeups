# Zanzibar Whisper

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=864156fe-12ef-45c3-9add-3fbc89ac8782)

The supplied ZIP contains a 1024 × 683 JPEG. There is no EXIF section or appended data after its JPEG end marker. The carrier is steghide, and the passphrase is empty.

To reproduce with the official extracted JPEG:

    steghide extract -sf zanzibar_whisper.jpg -p ''

The extracted 28-byte ASCII text contains the flag followed by a newline.

Flag: **hiCTF{sp1c3_1sl4nd_s3cr3ts}**

The ZIP SHA-256 is **48aedaaf1a363d859ceaece068354394edd6a8ff1ea7245af3fde395aa749a67**. The local extraction and the official team solved-set support the result. AI assistance was used for artifact triage; the extraction itself is deterministic.
