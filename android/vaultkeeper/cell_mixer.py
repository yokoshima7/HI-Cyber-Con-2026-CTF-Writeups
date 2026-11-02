"""Python translation of the two transformations in CellMixer.java."""

MASK = 0xFFFFFFFF
MUL_C = 0x85EBCA6B


def rol32(value, bits):
    bits &= 31
    value &= MASK
    return ((value << bits) | (value >> ((32 - bits) & 31))) & MASK


def ror32(value, bits):
    bits &= 31
    value &= MASK
    return ((value >> bits) | (value << ((32 - bits) & 31))) & MASK


def k1(cells):
    """Mutate and return the 128-element uint32 cell array."""
    assert len(cells) == 128
    for round_number in range(7):
        indices = range(128) if round_number % 2 == 0 else range(127, -1, -1)
        for index in indices:
            total = cells[index] + rol32(cells[(index - 1) & 127], 11)
            total += ror32(cells[(index + 1) & 127], 5)
            cells[index] = rol32(total * MUL_C, (round_number % 3) + 13)
    return cells


def k2(program, cells):
    """Return the CellMixer.k2 XOR of a program byte sequence."""
    assert len(cells) == 128
    result = bytearray(program)
    for index in range(len(result)):
        block, offset = divmod(index, 256)
        cell = cells[((offset * 7) + (block * 13)) & 127]
        key = ((cell >> ((offset & 3) * 8)) & 255) ^ ((block * 31 + offset) & 255)
        result[index] ^= key
    return bytes(result)
