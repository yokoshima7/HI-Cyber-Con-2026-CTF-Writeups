# LetMeOut — Unicode normalization defeated a Jinja sandbox check

Category: Pwn. [Challenge page](https://ctf.hiddeninvestigations.net/challenges?challenge=09cdea9f-9bb9-4e2d-9581-a229a5084dd9) · [日本語](README.ja.md)

The provided `jail.py` used Jinja2 3.1.6 `SandboxedEnvironment`, removed normal globals and filters, and exposed `rich` and `plain` under randomized names. Input was ASCII, at most 170 characters and 32 lines, with no more than three distinct alphabetic characters. In the running container, the real flag and three decoys had random eight-hex-character filenames under `/flags`.

The crucial mismatch involved `rich`, which returned a `Tag` subclass of `str`. Its `__str__` performed NFKC normalization. Jinja's sandbox item lookup converted the key with `str(argument)` for the actual attribute access, but passed the original key object to its safety check. A key whose first character was fullwidth underscore (`＿`) normalized to ordinary underscore when accessed, yet did not appear to start with `_` to the safety check.

The solver began with the empty string's `format` method and used the normalized key to reach that Python function's `__builtins__`. From there it called `__import__('os').listdir('.')`, then opened each listed filename and read it. To satisfy the three-letter restriction, it encoded disallowed letters as three-digit octal escapes inside Jinja string literals. It also probed the possible randomized `rich` filter names rather than assuming one fixed name.

The key idea can be expressed schematically as:

```text
''['format']['\uff3f_builtins__' | rich_filter] -> builtins
builtins['__import__']('os').listdir('.') -> eight-hex filenames
builtins['open'](filename).read() -> file content
```

The observed true flag was `hiCTF{__^_^__n0rm4l1z3_b3f0r3_y0u_tru5t__>_<___f15c49bdc5}`; the other three files said they were not the flag. The team submitted it, and the final public solved set includes LetMeOut. The ASCII/octal encoding and filter-name probing are required for a live payload; the schematic lines above are explanatory, not literal 170-character submissions.

Official ZIP SHA-256: `f5a4368739359474fc7f075860ebf6ae70ebd87aec14a6a045e6ebf408de2e44`. The local ZIP's `fake_flag_for_local_testing` is a fixture, not the accepted flag.
