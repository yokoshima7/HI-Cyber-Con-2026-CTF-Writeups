# GhostBus — UARTのnonceでSPIの封印領域を復号する

[English](README.en.md)

分類: Hardware · チーム: ReFlection（Agentic AI）· [問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=b7d2e1fc-da43-4e73-975c-86cccad4d53e)

公式 `ghost_bus.zip` のSHA-256は `8ffeac83846c1261595323f18fa701d940c702cc724c185e312cebdd72ef2676`。ロジックアナライザの記録、ファームウェア、フラッシュダンプを突き合わせる問題だった。

## 解法

1. `capture.csv` の各チャネルを `AA 55 LEN CMD PAYLOAD CRC16_LE` のフレームとして読む。初期値 `0xffff`、反射多項式 `0xa001` のCRC16-Modbusで各フレームを検証する。チャネル0の最後は長さゼロのコマンド `0x10`、チャネル1の `0x10` 応答には16バイトのnonceが入っている。
2. `firmware.elf` を逆アセンブルする。受信処理はファームウェア内の24バイト定数に応答nonceを続けてSHA-256を計算し、その先頭16バイトをAES-128鍵としている。連結順序が重要。
3. ファームウェアはSPI NORの `0x6a000` から48バイトを読む。4バイトの各ワード内でバイト順を逆にしてからAES-CBCで復号する。IVはUART応答のnonce。
4. 自動的なパディング除去を行わず復号し、末尾の7個の `0x07` をPKCS#7として確認する。残りがフラグ。

計算の骨子は次のとおり。

```python
key = sha256(firmware_constant_24 + uart_nonce).digest()[:16]
sealed = flash_dump[0x6a000:0x6a030]
ciphertext = b''.join(sealed[i:i+4][::-1] for i in range(0, 48, 4))
plaintext = AES_CBC_decrypt(key, uart_nonce, ciphertext)
assert plaintext.endswith(b'\x07' * 7)
```

Flag: `hiCTF{gh0st_bu5_uart_n0nc3_r3v3al_9c3f12}`

ローカルのsolverはフレームCRC、パディング、フラグ形式を検査する。初期の解析メモでは提出未確認だったが、大会終了時の公式公開スナップショットにはGhostBusがReFlectionの解答済み問題として含まれる。AIを使った逆解析で三つの素材を結び、決定的な復号結果をローカルでも確認した。
