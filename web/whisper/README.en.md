# Whisper — blind regex extraction followed by a signed export

Category: Web. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=def51bc6-83ae-48ea-a989-f9f8680c695e) · [日本語](README.ja.md)

The instance's `/clients` page named `report-signer` as the client with `report:export` scope. `/docs` documented `POST /api/token` and an HMAC-protected `POST /internal/export`. Supplying an object instead of a literal `client_secret` exposed a credential-query flaw: `{"client_id":"report-signer","client_secret":{"$ne":null}}` returned HTTP 200. That bearer token alone did not authorize export, so the actual client secret was needed for the HMAC.

The same input accepted an anchored `$regex` predicate. A match returned 200 and a mismatch 401. Bounded controls established that the secret contained exactly 32 lowercase hex characters. For each position, the solver split the remaining 16-character alphabet in half, asked whether the known prefix plus the next character matched, and retained the matching half. Four decisions per character recovered the secret in 128 oracle calls. One ordinary login with the recovered literal secret returned 200. The secret itself is omitted because the method, not that instance credential, is the reusable part.

For a raw `{}` request body and an empty query, the signature covered six LF-separated lines, including one empty query line:

```text
POST
/internal/export

<lowercase SHA-256 hex of the raw {} body>
<X-Timestamp in Unix seconds>
<unique X-Nonce>
```

The key was the recovered secret's ASCII bytes. A correctly signed five-line attempt gave a replay-protection hint requiring `X-Nonce` as the sixth line. The final request sent `X-Client-Id: report-signer`, `X-Timestamp`, `X-Nonce`, and lowercase `X-Signature: HMAC-SHA256(key, string-to-sign)`. `POST /internal/export` returned HTTP 200 and `hiCTF{bl1nd_regex_3xfil_then_f0rge_the_cust0m_s1gner_aa5337c956}`. A second request with a fresh nonce returned the same flag.

The official page then displayed `Flag correct!` and `Challenge solved!`; Whisper appears in ReFlection's final public solved set. The extraction was rate-limited to at least one second between requests and used a saved resume cursor. The demonstrated bug is the query operator in credential validation, followed by normal use of the recovered HMAC key.
