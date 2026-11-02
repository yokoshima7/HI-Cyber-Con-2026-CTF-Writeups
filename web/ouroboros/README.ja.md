# Ouroboros — EJSの `sourceURL` から関数宣言を差し込む

分類: Web。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=c65b4463-2d45-440d-87ff-53a1e9011d90) · [English](README.en.md)

通常のユーザー名だけでログインし、`POST /api/report/preview` にデータを送ると、`title`、`footer`、`body` をエスケープして固定のEJSテンプレートへ埋め込む。制御したレンダーエラーで `data.filename` がEJSの診断用ファイル名に反映された。つまり、ユーザー入力がコンパイル処理へ届く。

保存したEJS 3.1.9/3.1.10で確認すると、`Template.compile` はJSON文字列化したファイル名を、生成JavaScriptの末尾に `//# sourceURL=` コメントとして追加する。一方 `JSON.stringify` はJavaScriptの改行区切りU+2028を残す。通常の文字列にU+2028と `function escapeFn(...)` 宣言を続けると、コメントの次の行にJavaScript文ができる。この宣言が巻き上げられ、固定テンプレートの `<%= ... %>` が呼ぶエスケープ関数と入れ替わる。

無害なローカル検証ではタイトルが `CANARY_T` になった。実インスタンスで最初に使った二重引用符入りの宣言はJSON文字列化時のエスケープで構文エラーになったが、単一引用符へ替えるとcanaryが通った。最終ペイロードではタイトルの目印 `T` が渡されたとき、確認済みの `/flag.txt` を返した。

```js
const filename = 'ordinary\u2028' +
  "function escapeFn(v){if(v==='T'){return process.mainModule.require('fs').readFileSync('/flag.txt','utf8')}return String(v)}//";
// {data:{title:'T',body:'B',filename}} を POST /api/report/preview へ
```

ファイルを読む前に、同じhookで `/app` とルートを一覧し、`flag.txt` の存在を確認した。previewのタイトルに `hiCTF{pr0to_pollution_to_cust0m_new_Function_gadget_rce_ac7288e92a}` が返り、公式画面の `Challenge solved!` と自チームの最終公開解答一覧で受理を確認した。

別の検証では `constructor.prototype.delimiter` の保存によりEJSの区切り文字が変化した。これはprototype pollutionの存在を示すが、**実際のflag取得には使っていない**。成功した経路は `data.filename` → EJSの `sourceURL` → 巻き上げられた関数宣言である。
