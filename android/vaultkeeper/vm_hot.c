#include <stdint.h>

static inline uint32_t rol32(uint32_t value, unsigned bits) {
    return (value << bits) | (value >> (32 - bits));
}

/* The first bytecode loop executes exactly 100,000,000 rounds of op 25. */
void vm_hot(uint32_t registers[8], uint32_t rounds) {
    uint32_t a = registers[0], b = registers[1], c = registers[2];
    for (uint32_t i = 0; i < rounds; ++i) {
        a = rol32(a + b, 7) ^ rol32(c, 27);
        b = rol32(b + c, 7) ^ rol32(a, 27);
        c = rol32(c + a, 7) ^ rol32(b, 27);
    }
    registers[0] = a;
    registers[1] = b;
    registers[2] = c;
}
