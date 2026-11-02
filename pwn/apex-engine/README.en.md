# Apex Engine — credit race followed by a path race

Category: Pwn. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=596582e4-cc87-4c51-9e76-8f4d2838af6b) · [日本語](README.ja.md)

The service began with 100 credits. Its asynchronous transfer workers checked the balance before their debits became visible to one another. Sending eight 100-credit transfers in a burst let every worker see the original 100. After all eight deductions, the unsigned 64-bit balance wrapped from `100 - 800` to `18446744073709550916`, enough to unlock the VIP operation.

VIP access opened an enclave file-stream feature. A slot could start with the harmless path `/tmp/preview.txt`. The stream worker validated that path, waited about 25 ms, and later opened the path from the same mutable slot. During the interval, the client changed slot 0 to `/flag`. The check and use therefore operated on different values.

The solve sequence was:

1. Burst eight transfers of 100 credits, then request the VIP upgrade.
2. Create enclave slot 0 with its default path.
3. Start streaming slot 0 and quickly edit its path to `/flag` during the worker's delay.
4. Read the stream output. A small bounded set of delays was tried because thread scheduling varies.

The distributed ELF was tested in an isolated local container: with a 2 ms edit delay the stream returned the local fixture flag. The same sequence against the team's challenge instance returned `hiCTF{t0ct0u_mult1thr34d_r4c3_c0nd1t10n_w1n_8d3f_0860951188}`. The official page displayed `Flag correct!`, and Apex Engine is present in ReFlection's final public solved set.

Official ZIP SHA-256: `aa932101aa0b92c17bcedd5bb76a6cf6fa3bd622f686ce9316b75fe5e4ef00a7`. The ZIP and instance are not mirrored here; the flow assumes the binary and service supplied by the challenge.
