# Roof of Africa

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=a17a88b6-f626-4738-ad9f-27bc6c23644d)

ZIPには山の写真 `roof_of_africa.jpg` が入っている。問題文によると、秘密はその山の「最も有名な数字」で守られている。アフリカ最高峰のキリマンジャロから、よく知られる標高 **5,895 m** をパスフレーズ `5895` と推測する。

写真にはsteghideでファイルが埋め込まれている。公式ZIPと `steghide` を用いて次のように抽出できる。

```sh
unzip roof-of-africa.zip
steghide info roof_of_africa.jpg -p 5895
steghide extract -sf roof_of_africa.jpg -p 5895 -xf roof_flag_v2.txt
cat roof_flag_v2.txt
```

`steghide info` は埋め込みファイル名 `roof_flag_v2.txt` とサイズ38バイトを示す。抽出結果は次の通り。

```text
hiCTF{h4kun4_m4t4t4_m34ns_n0_w0rr13s}
```

元のJPEGから抽出を再実行した。抽出データのSHA-256は **69fac68656afba9aa98333b19e8921bb34e6914148c1d921bd5023d64de92cb1**。公式のチーム解答一覧でもこの問題は解答済みとなっている。公式ZIPのSHA-256は **137a5a7ec2a314e1027a7a279d33e45cd0a95256f63b35cca2d3fb233c3209ed**。
