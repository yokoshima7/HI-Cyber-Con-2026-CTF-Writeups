# File Viewer — ZIP内のシンボリックリンクからファイルを読む

分類: Web。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=890c1d0d-40bf-477e-98bd-2a1f7a04dfab) · [English](README.en.md)

このアプリはZIPを `POST /analyze` で受け取り、各ファイルに `/<upload-id>/<member-name>` 形式の閲覧リンクを作る。着目したのは、ZIPに入れたシンボリックリンクを閲覧時に辿るかどうかだった。

まず通常の `hello.txt` で、アップロード直後ならリンクから内容を読めることを確認した。リンクは短時間で失効する。次に、Unixのファイル種別をシンボリックリンクにしたZIPエントリを作った。エントリ本文はリンク先パスになる。

```python
import stat, zipfile

with zipfile.ZipFile("probe.zip", "w") as archive:
    link = zipfile.ZipInfo("link.txt")
    link.create_system = 3  # Unixのモードビット
    link.external_attr = (stat.S_IFLNK | 0o777) << 16
    archive.writestr(link, "/etc/passwd")
```

これをアップロードし、返された `link.txt` のURLをすぐ開くと、インスタンス内の `/etc/passwd` が返った。リンク先を `/app/flag.txt` に替えるとflagが返った。`/app/app.py` も読めたのでアプリの配置場所を裏付けられる。一方、試した `/flag`、`/flag.txt`、`/app/flag` は404だった。

取得した `hiCTF{E45Y_5yml1Nk_15cba4b28e}` を提出すると、公式画面に `Flag correct!` と `Challenge solved!` が表示された。最終公開解答一覧にも自チームのsolveとして載っている。検証後に自チームのインスタンスは停止した。

`../escape.txt` やテンプレート風のファイル名は解法にならなかった。原因は、ZIPの展開領域の外を指すシンボリックリンクを閲覧処理が辿ったことにある。
