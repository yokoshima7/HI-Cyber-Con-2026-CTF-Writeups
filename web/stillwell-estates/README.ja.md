# Stillwell Estates — 絶対パス読み取りとflag先頭の空白

分類: Web。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=fe0fbf3a-5036-476e-af77-d50a20aeeb4d) · [English](README.en.md)

不動産ポータルはBrotli圧縮された提携先のexportをpreviewする。公式サンプルは `stillwell.agency-export/1` 形式のJSONで、`properties` 内の `document` が閲覧する文書を指定する。通常の `welcome.txt` は読め、`../welcome.txt` は拒否された。一方、絶対パス `/etc/hostname` は読めた。単純な `..` トラバーサルではなく、絶対パスによる脱出だった。

Brotli圧縮前の小さな検証データは次の形になる。

```json
{"format":"stillwell.agency-export/1","properties":[{"title":"Check","neighborhood":"Greenpoint","price":1,"document":"/etc/hostname"}]}
```

`Content-Type: application/json` と `Content-Encoding: br` を付けて `POST /api/agency/import/preview` へ送る。同じpreviewでアプリのソースを読むと、`..` を含む名前は拒否する一方、絶対パスを拒否せずに `path.resolve(PARTNER_DOCS, name)` を呼んでいた。`name` が絶対パスなら基準ディレクトリは捨てられる。

ソースは決済用の認可トークンを `/tmp/stillwell-private/escrow-ledger.txt` に作成していた。そのファイルのpreviewから得たflag値には、先頭にASCII空白（`0x20`）が**一つ含まれる**。

```text
" hiCTF{s1l3nt_l4n73rn_3573735_d31ee7dd8c}"
```

空白を除いて提出すると不正解。空白付きで通常の問題フォームへ入力しても不正解だった。公開クライアントの提出処理が `.trim()` を呼び、空白を削っていたためである。公式の提出APIに認証済みの正確な値を送ると `kind: goodFlag` と `The flag is correct.` が返り、再読込後の画面にも `Challenge solved!` が表示された。最終公開解答一覧にも載っている。

台帳の `Closing authorization: ` というラベル区切りの空白とは別に、flag値そのものも空白から始まる。再現にはその1バイトを維持する必要がある。セッション情報や非公開のサポート連絡は掲載しない。
