# Orphaned Context — a trusted descriptor for a recycled slot

Category: Web. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=b8d28d25-e9fa-4e94-a4ed-364826f04cdd) · [日本語](README.ja.md)

The relay console exposed status, audit events, and incidents. Its audit trail showed an interrupted capture whose recovery descriptor survived, followed by an untrusted maintenance note in a work slot. The active incident `IR-7731` advertised a retained `seal` artifact. This suggested a lifetime mismatch: a descriptor could still authorize a slot after its original capture had been removed.

The challenge description referred to an investigator handout, but the public challenge metadata initially had no attached file. The route names below were established from the console and bounded own-instance checks. They should be read as the observed API sequence, not as a claim that the absent handout was available.

1. `POST /api/capture/open` with `{}` created a capture and returned a `recovery_descriptor`. Record its request ID and descriptor.
2. `POST /api/capture/interrupt` with that request ID retained the descriptor while freeing slot 0.
3. `POST /api/note/store` with `{"text":"#!relay-maint/1\nhelp\nls /\n"}` placed an **untrusted** note in the recycled slot.
4. `POST /api/recover/preview` with the old descriptor returned `trusted: true` and executed the note's virtual diagnostic commands. This was the trust-boundary failure.
5. Discard that note using its returned ID and epoch, then store a new note in the same slot:

   ```text
   #!relay-maint/1
   ls /incidents
   ls /incidents/IR-7731
   cat /incidents/IR-7731/seal
   ```

6. Preview again with the original descriptor. It read the incident's `seal` from the relay's **in-memory diagnostic map**. This was not operating-system shell execution.

The seal text was `hiCTF{local_dev_fixture_not_a_real_flag_9ec7b16d04}`. Its name made it look like a fixture, so the team submitted it once for validation. The official page showed `Challenge solved!`, and Orphaned Context appears in ReFlection's final public solved set. The exact per-instance descriptor and note IDs are intentionally omitted: they are generated during the run and should be taken from each response.
