# File Viewer — a ZIP symlink became a file read

Category: Web. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=890c1d0d-40bf-477e-98bd-2a1f7a04dfab) · [日本語](README.ja.md)

The application accepted a ZIP at `POST /analyze`, then offered a link for each member at `/<upload-id>/<member-name>`. The important question was whether it served the extracted file or followed a link planted in the archive.

An ordinary `hello.txt` established the upload and immediate-read flow. The links expired quickly. I then made a ZIP entry whose Unix mode marked it as a symbolic link and whose body was its target path:

```python
import stat, zipfile

with zipfile.ZipFile("probe.zip", "w") as archive:
    link = zipfile.ZipInfo("link.txt")
    link.create_system = 3  # Unix mode bits
    link.external_attr = (stat.S_IFLNK | 0o777) << 16
    archive.writestr(link, "/etc/passwd")
```

Uploading this archive and immediately opening the returned `link.txt` URL returned the instance's `/etc/passwd`. That control showed the viewer followed the symlink. Repeating the same entry with `/app/flag.txt` returned the flag. Reading `/app/app.py` also confirmed the application directory; the tested `/flag`, `/flag.txt`, and `/app/flag` paths returned 404.

The team submitted `hiCTF{E45Y_5yml1Nk_15cba4b28e}`. The challenge page showed `Flag correct!` and `Challenge solved!`; File Viewer is also in ReFlection's final public solved set. The instance was stopped afterward.

The archived `../escape.txt` and template-looking filename tests did not produce the flag. The decisive bug was following an archive member's symbolic link outside its extraction directory.
