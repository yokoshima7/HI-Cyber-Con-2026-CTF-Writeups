# Stillwell Estates — absolute path read and a significant leading space

Category: Web. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=fe0fbf3a-5036-476e-af77-d50a20aeeb4d) · [日本語](README.ja.md)

The agency portal previewed Brotli-compressed partner exports. Its sample used a `stillwell.agency-export/1` JSON object containing `properties`, with each property's `document` field selecting a previewed file. A normal `welcome.txt` read worked. A parent traversal such as `../welcome.txt` was rejected, but an absolute path such as `/etc/hostname` was read. This distinguished an absolute-path escape from simple `..` traversal.

A compact test export had this shape before Brotli compression:

```json
{"format":"stillwell.agency-export/1","properties":[{"title":"Check","neighborhood":"Greenpoint","price":1,"document":"/etc/hostname"}]}
```

It was sent to `POST /api/agency/import/preview` with `Content-Type: application/json` and `Content-Encoding: br`. Reading the application's source through the same preview showed why this worked: its resolver rejected names containing `..`, then called `path.resolve(PARTNER_DOCS, name)` without rejecting absolute paths. For an absolute `name`, the base directory is discarded.

The source placed a closing authorization token in `/tmp/stillwell-private/escrow-ledger.txt`. Previewing that exact file returned the ledger. The flag value began with one ASCII space (`0x20`):

```text
" hiCTF{s1l3nt_l4n73rn_3573735_d31ee7dd8c}"
```

Submitting the text without that space failed. Submitting it with the space in the normal challenge form also failed: the platform's client code called `.trim()` before submission, and the field then displayed the stripped text. An exact, authenticated request to the official challenge submission API preserved the leading byte and returned `kind: goodFlag`, `The flag is correct.` The reloaded page showed `Challenge solved!`, and the final public solved set includes Stillwell Estates.

The extra space in the ledger's label separator is distinct from the space inside the token: the source constructed `Closing authorization: ` plus a flag value that itself starts with a space. Reproduction depends on preserving the token byte-for-byte. No private session material or support correspondence is included here.
