# Blind Index — score references in a later instance

[日本語](README.ja.md)

Category: AI / LLM · Division: Agentic AI · [Challenge](https://ctf.hiddeninvestigations.net/challenges?challenge=9a82a5dd-903a-4000-bb12-5856c046e9ba)

The challenge presents ten 24-character hexadecimal reference records and a similarity-score oracle. A reference string cannot be looked up directly in its own instance: the service returns `reference_record`. The documented API offers `/records`, `/status`, and `/lookup`, with 400 scored texts per instance. The decisive observation was that the scorer stayed constant across instances while each new instance generated a different blocked reference set.

## Solving path

1. Save the ten strings and their zero-based indices from the first team's own instance. A local estimate from 399 neighbor queries left three close pairs unresolved, so it was not enough to justify a full ranking.
2. Start a later own-team instance. Its `/records` list differs. Two previously scored non-reference controls returned the same six-decimal scores, showing that the scoring function was stable for those controls across the two instances.
3. Submit the first instance's ten now-unblocked strings as one `/lookup` batch. The service returned their exact scores:

   | Old index | Score | Old index | Score |
   | ---: | ---: | ---: | ---: |
   | 0 | +0.224797 | 5 | +0.067722 |
   | 1 | +0.080045 | 6 | +0.118937 |
   | 2 | +0.519453 | 7 | +0.370114 |
   | 3 | −0.129120 | 8 | −0.077011 |
   | 4 | +0.170042 | 9 | −0.270360 |

4. Sort by descending score, giving indices `2,7,0,4,6,1,5,8,3,9`. Serializing the indices without separators gave `2704615839`. The official challenge pane accepted `hiCTF{2704615839}` with both `Flag correct!` and `Challenge solved!`; the team counter became 59/69. The close-time public snapshot also includes Blind Index.

Flag: `hiCTF{2704615839}`

The exact ordering is verified for that saved reference set. A separate generated set had a different ranking, so this does not establish a universal fixed permutation. The platform did not expose why a stopped instance's old rank remained accepted after new instances generated different records. The public endpoint also did not document the answer serialization. We therefore report the observed successful submission without claiming to have fully reconstructed the checker. AI-assisted testing explored local score models, but the decisive evidence came from the cross-instance control and exact-score batch.
