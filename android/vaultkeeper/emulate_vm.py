#!/usr/bin/env python3
"""Emulate the native VaultKeeper bytecode that constructs its final XOR mask."""

import ctypes
import hashlib
from pathlib import Path

from cell_mixer import k1, rol32, ror32

ROOT = Path(__file__).resolve().parent
PROGRAM = (ROOT / "vm-program.bin").read_bytes()
VAULT = (ROOT / "assets/vault.bin").read_bytes()
seed = hashlib.sha256(VAULT + b"VK-SEED-v1").digest()
cell_data = b"".join(hashlib.sha256(seed + i.to_bytes(4, "little")).digest()
                     for i in range(16))
CELLS = k1([int.from_bytes(cell_data[i:i+4], "little")
            for i in range(0, 512, 4)])

hot = ctypes.CDLL(str(ROOT / "vm_hot.dylib")).vm_hot
hot.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
hot.restype = None

registers = (ctypes.c_uint32 * 8)()
scratch = bytearray(512)
pc = 0
steps = 0
condition = 0


def imm16(offset):
    return int.from_bytes(PROGRAM[offset:offset + 2], "little")


def imm32(offset):
    return int.from_bytes(PROGRAM[offset:offset + 4], "little")


def getword(offset):
    return int.from_bytes(scratch[offset:offset + 4], "little")


def putword(offset, value):
    scratch[offset:offset + 4] = (value & 0xFFFFFFFF).to_bytes(4, "little")


while pc < len(PROGRAM):
    opcode = PROGRAM[pc]
    steps += 1
    if pc == 0x0F:
        assert PROGRAM[pc:pc + 16] == bytes.fromhex("19000102190102001902000118070f00")
        assert registers[7] == 100_000_000
        hot(registers, registers[7])
        registers[7] = 0
        pc = 0x1F
        print("Hot loop r0..r2:", *(f"{registers[i]:08x}" for i in range(3)))
        continue
    if opcode == 0:
        pc += 1
    elif opcode == 1:
        registers[PROGRAM[pc + 1] & 7] = imm32(pc + 2)
        pc += 6
    elif opcode == 2:
        registers[PROGRAM[pc + 1] & 7] = getword(imm16(pc + 2) & 0x1FC)
        pc += 4
    elif opcode == 3:
        putword(imm16(pc + 2) & 0x1FC, registers[PROGRAM[pc + 1] & 7])
        pc += 4
    elif opcode == 4:
        registers[PROGRAM[pc + 1] & 7] = scratch[imm16(pc + 2) & 0x1FF]
        pc += 4
    elif opcode == 5:
        scratch[imm16(pc + 2) & 0x1FF] = registers[PROGRAM[pc + 1] & 7] & 0xFF
        pc += 4
    elif 6 <= opcode <= 16:
        d, s = PROGRAM[pc + 1] & 7, PROGRAM[pc + 2] & 7
        a, b = registers[d], registers[s]
        if opcode == 6:
            result = b
        elif opcode == 7:
            result = a + b
        elif opcode == 8:
            result = a - b
        elif opcode == 9:
            result = a * b
        elif opcode == 10:
            result = a ^ b
        elif opcode == 11:
            result = a & b
        elif opcode == 12:
            result = a | b
        elif opcode == 13:
            result = a << (b & 31)
        elif opcode == 14:
            result = a >> (b & 31)
        elif opcode == 15:
            result = rol32(a, b)
        else:
            result = ror32(a, b)
        registers[d] = result & 0xFFFFFFFF
        pc += 3
    elif opcode == 17:
        registers[PROGRAM[pc + 1] & 7] = CELLS[PROGRAM[pc + 2] & 127]
        pc += 3
    elif opcode == 18:
        pc = imm16(pc + 1)
    elif opcode == 19:
        pc = (imm16(pc + 2) if registers[PROGRAM[pc + 1] & 7] != 0
              else pc + 4)
    elif opcode == 20:
        condition = int(registers[PROGRAM[pc + 1] & 7]
                        == registers[PROGRAM[pc + 2] & 7])
        pc += 3
    elif opcode == 21:
        pc = imm16(pc + 1) if condition else pc + 3
    elif opcode == 24:
        d = PROGRAM[pc + 1] & 7
        registers[d] = (registers[d] - 1) & 0xFFFFFFFF
        pc = (imm16(pc + 2) if registers[d] != 0 else pc + 4)
    elif opcode == 25:
        d, s, t = (PROGRAM[pc + i] & 7 for i in (1, 2, 3))
        registers[d] = rol32(registers[d] + registers[s], 7) ^ rol32(registers[t], 27)
        pc += 4
    elif opcode == 28:
        d, s = PROGRAM[pc + 1] & 7, PROGRAM[pc + 2] & 7
        registers[d] = getword((registers[s] & 127) * 4)
        pc += 3
    elif opcode == 29:
        d, s = PROGRAM[pc + 1] & 7, PROGRAM[pc + 2] & 7
        putword((registers[d] & 127) * 4, registers[s])
        pc += 3
    elif opcode == 27:
        print("VM halt: success, pc", hex(pc), "interpreter dispatches", steps)
        break
    else:
        raise NotImplementedError(f"VM opcode {opcode} at {pc:#x}")
else:
    raise RuntimeError("VM ended without halt")

output = bytes(scratch[:64])
(ROOT / "vm-output.bin").write_bytes(output)
print("VM output 64 bytes:", output.hex())
