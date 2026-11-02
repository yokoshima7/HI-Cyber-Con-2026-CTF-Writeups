# Labyrinth

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=8d5871ff-b72f-49a5-9bdc-235d11dddd42)

This is a framed TCP puzzle, followed by a randomized maze. Every frame starts with bytes **4c 42 59 7f**, a one-byte opcode, a two-byte big-endian payload length, and the payload. A plain text greeting does not work.

1. Send HELLO (opcode 01) with an empty payload and use the eight-byte nonce in the reply for PROBE (10).
2. PROBE supplies input/output examples and a four-byte challenge. The transform reverses the input bytes and XORs each with the session mask shown by the all-zero example. Send the transformed four bytes through ANSWER (30).
3. The server opens a maze. Each room gives coordinates, a door bitmask, flags, and a two-byte token. MOVE (20) takes a direction byte for N/E/S/W and that room's current token. Record the reachable graph while exploring.
4. On reaching the sealed gate, send stage query 02. It requests the **shortest route from the entrance**. Run breadth-first search over the recorded graph and send the route as raw direction bytes in ANSWER (30).

The service returned **hiCTF{l34rn3d_th3_t0ngu3_w4lk3d_th3_l4byr1nth_528f336956}**. The official challenge page then showed it solved, and the final team snapshot contains the challenge ID.

The glowing light and opcode 40 can return **hiCTF{not_the_exit}**, an intentional decoy. The route and tokens vary by session, so a hard-coded path is not a general solution. AI agents mapped the protocol and checked the result on our own team instance.
