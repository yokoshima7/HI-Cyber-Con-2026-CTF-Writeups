# Warden's Maze

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=1a18e0db-e534-4694-b19c-c2307a094a7e)

The vault is surrounded by walls in an ordinary 24 × 21 maze. The bug is in the visibility renderer. It reads the tile to display from the correct map address but writes the visible copy to an address computed with a **signed eight-bit relative offset**.

At player position (4, 14), a six-tile-down sightline reads floor at map index 484. The correct offset is +144; narrowing it to signed eight bits changes it to **−112**. The write therefore lands at player index 340 − 112 = **228**, the top vault wall at (12, 9). The renderer has changed a wall into traversable floor.

The retained route reaches that trigger, returns to the vault, and walks through the altered wall:

    saaaasssaasssaaaasssdsssd
    awwwwddddwwddddd
    sssa

These are 25 + 16 + 4 moves on one connection. The local service and our official team instance both reached the win state. The service printed **hiCTF{maze-warden-vault-seed-2026_1ab476d6f6}**, and the official team snapshot records the challenge solved.

The token is instance-specific; another instance returns a different token. The route can also be disrupted by the moving warden, so a solver should check the changed wall and win state. The official archive SHA-256 is **e8e5e20c1c1e321e916bdd60d6d319fa1fd05ff36e14e97956d686d4f42a88da**.

AI agents assisted with disassembly and a static enumerator of the renderer's writes. The incorrect index, observed wall change, local and official win, and solve record support the explanation.
