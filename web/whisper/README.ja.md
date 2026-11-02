# Whisper — 正規表現オラクルで秘密を回収し、正規の署名でexportする

分類: Web。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=def51bc6-83ae-48ea-a989-f9f8680c695e) · [English](README.en.md)

`/clients` は `report-signer` に `report:export` 権限があると示し、`/docs` は `POST /api/token` とHMACで保護された `POST /internal/export` を説明していた。文字列の代わりに `client_secret` へオブジェクトを渡すと、資格情報検索の不備が露出する。`{"client_id":"report-signer","client_secret":{"$ne":null}}` はHTTP 200を返した。ただし、得たBearer tokenだけではexportできず、HMAC用の実際のsecretが必要だった。

同じ入力は、先頭と末尾を固定した `$regex` 条件も受け付けた。一致なら200、不一致なら401。限定的な検証でsecretは小文字16進数32文字と分かった。各位置について候補16文字を半分ずつに分け、既知の先頭部分と次の1文字が一致するか質問する。1文字につき4回、計128回の真偽判定でsecretを回収した。回収した文字列による通常の認証も1回だけ試し、200を確認した。インスタンスのsecret値自体は掲載しない。

本文が生バイトの `{}`、クエリが空の場合、署名対象は空のクエリ行を含む次の6行をLFで連結したものだった。

```text
POST
/internal/export

<{} の生バイトのSHA-256小文字hex>
<Unix秒のX-Timestamp>
<一意のX-Nonce>
```

鍵は回収したsecretのASCIIバイト。正しい5行形式の署名を送ると、リプレイ防止のエラーが6行目の `X-Nonce` を要求した。最終リクエストでは `X-Client-Id: report-signer`、`X-Timestamp`、`X-Nonce` と、小文字hexの `X-Signature: HMAC-SHA256(key, string-to-sign)` を付けた。`POST /internal/export` がHTTP 200と `hiCTF{bl1nd_regex_3xfil_then_f0rge_the_cust0m_s1gner_aa5337c956}` を返し、新しいnonceで再実行しても同じ結果だった。

公式画面に `Flag correct!` と `Challenge solved!` が表示され、最終公開解答一覧にもWhisperが載った。抽出はリクエスト間隔を最低1秒とし、再開用カーソルを保存した。核心は資格情報検証に検索演算子を通せたことで、その後は回収したHMAC鍵を正規の仕様どおりに使っている。
