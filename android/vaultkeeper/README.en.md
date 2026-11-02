# VaultKeeper (Android)

[日本語](README.ja.md) · [Overview](../../README.md)

[Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=2771edbb-c032-4c72-ab9e-343acfc0262b) · Download SHA-256: `7c0ccbd218561af27d1f51dcb18cf3ef5ab566e538788d88e285de1fb8d7aa10` · Extracted APK SHA-256: `400681608c68dd3613630f4dee34fd17dadad6f95bb3a3d7c6c7ca2112f59320`

The tempting `FlagRepository.getMasterKey()` string only helps `MainActivity` display a short vault ID. The claim path instead reads the 8,192-byte `assets/vault.bin`, calls native `nvSeed`, mixes 128 cells with `CellMixer.k1`, unseals a 2,048-byte program with `nvUnseal`, applies `CellMixer.k2`, executes the VM in `nvExec`, and validates 51 output bytes in `nvFinal`. The random gesture token gates the UI call sequence but is not needed to recover and emulate the static program. The UI's final alert also appears after an exception, so it is not proof of a successful claim.

The crucial correction in reconstructing `nvSeed` was to start with `seed = SHA256(vault.bin || b"VK-SEED-v1")`, then hash `seed || LE32(row)` once for each row from 0 through 15, retaining all 16 digests. Split those 512 bytes into 128 little-endian 32-bit cells. The supplied [cell_mixer.py](cell_mixer.py) and [derive_program.py](derive_program.py) reproduce the seed, unseal, and mixer chain. The recovered VM program has SHA-256 `ffd80cdd77c649e287672fab4ae72eaadb1ab242531e3440d9f4736ecca618ae`.

The VM begins with a 100,000,000-round register loop, which we accelerated with compiled C, then interprets 358 further instructions to the success halt at PC `0x58f`. XORing the first 51 output bytes with two native read-only arrays and the native self-mix hash yields `hiCTF{!!I_10v3_4ndr0!d_m4n_m4k!ng_th3m_f331_g0Od!!}`. Its `SHA256(b"VK-TAG-2026" + candidate)[:16]` is the embedded `62672db15a0b6a4793b351292f29a0b3`. The final official ReFlection solve roster includes VaultKeeper.

The five self-authored recovery files are [cell_mixer.py](cell_mixer.py), [derive_program.py](derive_program.py), [emulate_vm.py](emulate_vm.py), [final_check.py](final_check.py), and [vm_hot.c](vm_hot.c). The scripts use Python's standard library; the hot-loop helper needs a C compiler. They read, but do not execute, the APK's x86-64 native library.

## Reproduce on macOS

Download the official `VaultKeeper.zip` from the challenge link above. Use macOS with Python 3 and `clang` (Xcode Command Line Tools). Run the commands below **from this writeup directory**. They keep the official APK, its extracted files, the compiled helper, and generated VM data in a temporary working directory. Set `ZIP` to the **absolute** path of your downloaded archive. Check that the first two `shasum` outputs match the ZIP and APK hashes above before continuing.

```sh
ZIP="/absolute/path/to/VaultKeeper.zip"
WORK="$(mktemp -d)"
mkdir -p "$WORK/assets" "$WORK/lib/x86_64"
cp cell_mixer.py derive_program.py emulate_vm.py final_check.py vm_hot.c "$WORK/"
cd "$WORK"
shasum -a 256 "$ZIP"
unzip -p "$ZIP" VaultKeeper.apk > VaultKeeper.apk
shasum -a 256 VaultKeeper.apk
unzip -p VaultKeeper.apk assets/vault.bin > assets/vault.bin
unzip -p VaultKeeper.apk lib/x86_64/libvaultnative.so > lib/x86_64/libvaultnative.so
clang -O3 -dynamiclib -o vm_hot.dylib vm_hot.c
python3 derive_program.py
python3 emulate_vm.py
python3 final_check.py
```

Expect the program hash shown above, a VM success halt at PC `0x58f`, `SHA-256 tag match: True`, and the flag. [emulate_vm.py](emulate_vm.py) implements the opcodes exercised by this APK. Its `vm_hot.dylib` loader and the build command above are macOS-specific; other hosts need to adapt the shared-library build and loader name.
