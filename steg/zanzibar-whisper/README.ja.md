# Zanzibar Whisper

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=864156fe-12ef-45c3-9add-3fbc89ac8782)

公式ZIPに入るJPEGは1024 × 683ピクセルで、EXIF領域やJPEG終端後の追記データはない。搬送路はsteghideで、パスフレーズは空文字列だった。

公式JPEGを取り出した後、次を実行する。

    steghide extract -sf zanzibar_whisper.jpg -p ''

抽出される28バイトのASCIIテキストには、フラグと改行が入っている。

Flag: **hiCTF{sp1c3_1sl4nd_s3cr3ts}**

ZIPのSHA-256は **48aedaaf1a363d859ceaece068354394edd6a8ff1ea7245af3fde395aa749a67**。ローカル抽出と公式のチーム解答一覧で結果を確認した。AIはファイルの調査に使用し、抽出操作自体は決定的である。
