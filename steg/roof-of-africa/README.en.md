# Roof of Africa

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=a17a88b6-f626-4738-ad9f-27bc6c23644d)

The ZIP contains a mountain photograph, `roof_of_africa.jpg`. The challenge says its secret is protected by the mountain's “most famous number”. The roof of Africa is Kilimanjaro; its commonly cited elevation, **5,895 metres**, supplies the passphrase `5895`.

The photograph is a steghide carrier. Given the official ZIP and `steghide`, the extraction is:

```sh
unzip roof-of-africa.zip
steghide info roof_of_africa.jpg -p 5895
steghide extract -sf roof_of_africa.jpg -p 5895 -xf roof_flag_v2.txt
cat roof_flag_v2.txt
```

`steghide info` reports an embedded 38-byte file named `roof_flag_v2.txt`; extraction returns:

```text
hiCTF{h4kun4_m4t4t4_m34ns_n0_w0rr13s}
```

We reran the extraction on the original JPEG. The extracted bytes have SHA-256 **69fac68656afba9aa98333b19e8921bb34e6914148c1d921bd5023d64de92cb1**. The official team snapshot also records this challenge as solved. Official ZIP SHA-256: **137a5a7ec2a314e1027a7a279d33e45cd0a95256f63b35cca2d3fb233c3209ed**.
