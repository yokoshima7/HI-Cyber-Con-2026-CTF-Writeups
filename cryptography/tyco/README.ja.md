# Tyco（暗号）

[English](README.en.md)

[公式 Tyco](https://ctf.hiddeninvestigations.net/challenges?challenge=2914b4ef-91ea-4270-8965-2d224b7788e0) の配布 ZIP の SHA-256 は `f88f50cb0857595fce5457bc73d756215326093d6a1a478ae552d58460dc99f2` でした。自チームの最終公式記録では解答済みです。

## 関連平文 RSA

`chall.py` が公開するのは RSA の法 `N`、指数 `e`、既知の差 `d`、および `t1 = r^e mod N` と `t2 = (r+d)^e mod N` です。したがって `f(x)=x^e−t1` と `g(x)=(x+d)^e−t2` は `Z/NZ` 上で `x−r` という共通因子を持ちます。Franklin–Reiter の関連平文攻撃なら、`N` を素因数分解せず多項式の最大公約因子から `r` を求められます。

PARI/GP で `N` を法とする多項式演算を行うと一次の gcd が得られ、その根が `r` でした。`pow(r,e,N)==t1` と `pow(r+d,e,N)==t2` の両方を確認し、`r` をビッグエンディアンの UTF-8 として読むと `hiCTF{your_ai_slop_bores_me}` になります。両暗号文との整合性と公式の解答済み記録で確認した解法です。
