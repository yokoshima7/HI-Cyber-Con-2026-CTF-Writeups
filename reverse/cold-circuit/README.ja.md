# Cold Circuit（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=928427a9-59bb-4675-a771-f736940ac853) · 配布ZIPのSHA-256: `cd9e56173d294497a6e07d560db89c46abe359a702b40be1165332cb9adb4c1c`

strip済みx86-64チェッカーは、`hiCTF{`、32桁の16進数、`}` という形式を要求する。16進数を16バイトに戻した後、20ラウンドにわたって、ラウンド鍵の加算（256を法とする）、256値の置換表、16位置の並べ替えを行い、最後に固定の16バイトと比較する。

置換表は全256値の全単射であり、位置表も0～15の順列なので、各ラウンドは逆算できる。埋め込みの目標値からラウンド19→0の順で、位置の並べ替えを戻し、逆置換を適用し、ラウンド鍵を256を法として引いた。別途、求めた入力を順方向に流して目標値へ戻ることを確認した。

16バイトは `6e305f6a7461675f6e65656465642121`（ASCIIでは `n0_jtag_needed!!`）。フラグは `hiCTF{6e305f6a7461675f6e65656465642121}`。元のチェッカーが `Access granted.` を出して正常終了し、公式画面でも `Flag correct!` と `Challenge solved!` を確認した。
