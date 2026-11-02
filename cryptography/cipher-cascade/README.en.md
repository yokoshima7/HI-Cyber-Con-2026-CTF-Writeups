# Cipher Cascade (Cryptography)

[日本語](README.ja.md)

The team's solution to the [official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=5ef939e5-6535-482e-9f67-b59e96a22ceb) was accepted by the platform.

## Decoding

The attached text gives an “Encoded message.” The layers unwind in reverse order: reverse the entire encoded string, Base64-decode it, parse the resulting hexadecimal string into bytes, decode those bytes as text, then apply ROT13. The local solver's core is:

```python
message = encoded_message.strip()
rot13_input = bytes.fromhex(base64.b64decode(message[::-1]).decode()).decode()
flag = codecs.decode(rot13_input, "rot_13")
```

The result was `hiCTF{l4y3r_by_l4y3r_unw1nd}`. The earlier layers are encodings rather than cryptographic encryption: once the order and whole-string reversal are identified, each step is deterministic. The official solved record confirms the recovered text was accepted.
