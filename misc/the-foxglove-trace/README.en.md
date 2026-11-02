# The Foxglove Trace

[日本語版](README.ja.md) · [Official challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=50ab1909-d636-4e0c-868f-49d7772834aa)

The abandoned tracker project leaves a note, trusted Wi-Fi access point weights, a 33-row scan export, and one verbose run. The note says to score signal strength only while the owner was moving, then weight it by trust. The run log labels step delta **40** stationary and **41** moving, so the effective rule for these integer records is **step_delta > 40**.

For each access point listed in aps.conf, sum **signal × weight** only over qualifying rows. Ignore unlisted access points. Recomputing the export gives:

| Access point | Kept rows | Score |
| --- | ---: | ---: |
| FoxgloveCoffee_Guest | 5 | 1,044 |
| CafeDelMundo | 3 | 364 |
| NETGEAR-8841 | 3 | 240 |
| HomePlex_5G | 1 | 174 |

FoxgloveCoffee_Guest wins even though the home router has individually stronger signals. The submission uses the access point spelling exactly as recorded:

Flag: **hiCTF{FoxgloveCoffee_Guest}**

The official team snapshot lists the challenge as solved. Original ZIP SHA-256: **e76d9c898c069fa96e85d929009f3bd16e94a747940e90f7a23df2424ef3e5e4**. The access point names come only from the provided challenge files.
