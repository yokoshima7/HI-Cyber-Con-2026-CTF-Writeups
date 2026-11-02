# Cipher Cascade（暗号）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=5ef939e5-6535-482e-9f67-b59e96a22ceb)に対する ReFlection の解答は、公式プラットフォームで受理されました。

## 復号順序

添付テキストの `Encoded message` を、文字列全体の反転 → Base64 → 16 進文字列をバイト列に変換 → テキスト化 → ROT13 の順に戻します。ローカル solver の中心部分は次のとおりです。

```python
message = encoded_message.strip()
rot13_input = bytes.fromhex(base64.b64decode(message[::-1]).decode()).decode()
flag = codecs.decode(rot13_input, "rot_13")
```

結果は `hiCTF{l4y3r_by_l4y3r_unw1nd}`。暗号鍵を探す問題ではなく、文字列全体を反転する箇所と層の順序を見抜けば各段階は決定的です。公式の解答済み記録にも含まれています。
