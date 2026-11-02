# Whispers in the Margin

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=82fcce1d-1297-45d3-856e-9ead7887c4e5)

The ZIP contains `chall/chall.jpg` and a DOCX titled `Those numbers are process counts.docx`. The document starts with an ordinary discussion of browser process counts. Its apparently blank later paragraphs carry the first clue as spaces and tabs in `word/document.xml`.

Starting at paragraph 9 (zero-based), take every other paragraph through 57. Ignore all but its final seven space/tab characters. Interpret a space as 0 and a tab as 1, then decode each seven-bit ASCII value. This script reproduces the first layer from the original DOCX:

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

The output is the passphrase `haha! u got me, now what?`. Use it with steghide on the JPEG:

```sh
unzip whispers-in-the-margin.zip
steghide info chall/chall.jpg -p 'haha! u got me, now what?'
steghide extract -sf chall/chall.jpg -p 'haha! u got me, now what?' -xf flag.txt
cat flag.txt
```

`steghide info` reports a 27-byte embedded file named `flag.txt`. Extraction gives:

```text
hiCTF{573g4n0gr4phy_!5_fun}
```

We reran both layers on the original files. The extracted bytes have SHA-256 **eac72b2bacf941ee28643258c37065417a600a8ae3e3533bc7483814d59becc7**. The official team snapshot also records this challenge as solved. Official ZIP SHA-256: **e7633b86df93f2ab68eb769c978130b07aadbeff9e51e685f090867a8739f55e**.
