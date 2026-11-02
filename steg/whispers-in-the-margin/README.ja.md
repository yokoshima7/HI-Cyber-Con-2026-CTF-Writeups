# Whispers in the Margin

[English](README.en.md) · [公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=82fcce1d-1297-45d3-856e-9ead7887c4e5)

公式ZIPには `chall/chall.jpg` と `Those numbers are process counts.docx` が入っている。文書の前半はブラウザのプロセス数についての普通の説明だが、後半の空白に見える段落には、`word/document.xml` 上でスペースとタブが並んでいる。

0から数えた9段落目から57段落目まで一つおきに取り、それぞれの末尾7個のスペース・タブを読む。スペースを0、タブを1とし、7ビットASCIIとして復号する。以下のスクリプトで元のDOCXから第一層を再現できる。

```python
from zipfile import ZipFile
from xml.etree import ElementTree as ET

docx = "chall/Those numbers are process counts.docx"
w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
root = ET.fromstring(ZipFile(docx).read("word/document.xml"))
paragraphs = root.findall(".//w:body/w:p", {"w": w})

message = []
for paragraph in paragraphs[9:59:2]:
    row = "".join(
        (node.text or "") if node.tag == f"{{{w}}}t" else "\t"
        for node in paragraph.iter()
        if node.tag in (f"{{{w}}}t", f"{{{w}}}tab")
    )
    bits = row[-7:].replace(" ", "0").replace("\t", "1")
    message.append(chr(int(bits, 2)))
print("".join(message))
```

出力 `haha! u got me, now what?` がJPEGに使うパスフレーズとなる。

```sh
unzip whispers-in-the-margin.zip
steghide info chall/chall.jpg -p 'haha! u got me, now what?'
steghide extract -sf chall/chall.jpg -p 'haha! u got me, now what?' -xf flag.txt
cat flag.txt
```

`steghide info` は埋め込みファイル名 `flag.txt` とサイズ27バイトを示す。抽出結果は次の通り。

```text
hiCTF{573g4n0gr4phy_!5_fun}
```

元のファイルで両層を再実行した。抽出データのSHA-256は **eac72b2bacf941ee28643258c37065417a600a8ae3e3533bc7483814d59becc7**。公式のチーム解答一覧でもこの問題は解答済みとなっている。公式ZIPのSHA-256は **e7633b86df93f2ab68eb769c978130b07aadbeff9e51e685f090867a8739f55e**。
