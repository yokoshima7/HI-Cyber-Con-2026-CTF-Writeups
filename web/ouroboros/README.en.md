# Ouroboros — code hoisted out of EJS `sourceURL`

Category: Web. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=c65b4463-2d45-440d-87ff-53a1e9011d90) · [日本語](README.ja.md)

After a normal username-only login, `POST /api/report/preview` rendered a fixed EJS template containing escaped `title`, `footer`, and `body` fields. A controlled render error showed that `data.filename` changed EJS's diagnostic filename. That put a user-supplied value on a path into EJS compilation.

In the EJS versions checked offline (3.1.9 and 3.1.10), `Template.compile` appends the JSON-stringified filename to generated JavaScript as a `//# sourceURL=` comment. `JSON.stringify` leaves U+2028, the JavaScript line separator, intact. A filename beginning with ordinary text, then U+2028, then a `function escapeFn(...)` declaration therefore creates a new JavaScript statement. The declaration is hoisted and replaces the escaping callback used by the fixed `<%= ... %>` tags.

The harmless offline control changed the rendered title to `CANARY_T`. A live control initially failed because double quotes inside the injected function were escaped by JSON stringification. Using single quotes produced the same canary on the team's instance. The final function returned the content of the observed `/flag.txt` when EJS escaped the title marker `T`:

```js
const filename = 'ordinary\u2028' +
  "function escapeFn(v){if(v==='T'){return process.mainModule.require('fs').readFileSync('/flag.txt','utf8')}return String(v)}//";
// Send {data:{title:'T',body:'B',filename}} to POST /api/report/preview
```

Before the file read, the same confirmed hook listed `/app` and the root directory, where `flag.txt` was present. The preview then returned `hiCTF{pr0to_pollution_to_cust0m_new_Function_gadget_rce_ac7288e92a}` in the title. The official challenge page showed `Challenge solved!`; Ouroboros is in ReFlection's final public solved set.

Separately, saving a nested `constructor.prototype.delimiter` changed EJS delimiter behavior, demonstrating prototype pollution. That observation was **not** the step that read the flag. The successful path was the direct `data.filename` → EJS `sourceURL` → hoisted function chain. Many other EJS option probes produced no effect and are not prerequisites for this solution.
