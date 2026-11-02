# LetMeOut — Unicode正規化とJinja sandboxの判定が食い違う

分類: Pwn。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=09cdea9f-9bb9-4e2d-9581-a229a5084dd9) · [English](README.en.md)

配布された `jail.py` はJinja2 3.1.6の `SandboxedEnvironment` を使い、通常のglobalとfilterを消していた。`rich` と `plain` だけが接続ごとにランダムな名前で公開される。入力はASCII、170文字以内、32行以内、異なる英字は最大3種類。実環境の `/flags` には本物1件とデコイ3件が8桁の16進ファイル名で置かれていた。

核心は `rich` が返す `str` 派生の `Tag` にある。`Tag.__str__` はNFKC正規化する。Jinjaのsandboxのitem lookupは実際の属性取得では `str(argument)` を使う一方、安全性判定には元のkeyオブジェクトを渡す。先頭を全角アンダースコア `＿` にしたkeyは、取得時には通常の `_` へ変わるのに、判定時には `_` 始まりと見なされない。

空文字列の `format` メソッドから、正規化したkey経由でPython関数の `__builtins__` に到達した。そこから `__import__('os').listdir('.')` で名前を列挙し、各ファイルを `open(name).read()` で読んだ。英字3種類の制約には、使えない英字をJinja文字列内の3桁八進エスケープに変換して対応した。`rich` のランダムなfilter名も候補から検出した。

仕組みを模式的に書くと次のとおり。

```text
''['format']['\uff3f_builtins__' | rich_filter] -> builtins
builtins['__import__']('os').listdir('.') -> 8桁16進のファイル名
builtins['open'](filename).read() -> 内容
```

取得した本物のflagは `hiCTF{__^_^__n0rm4l1z3_b3f0r3_y0u_tru5t__>_<___f15c49bdc5}`。残り3件はデコイだった。提出後、最終公開解答一覧にLetMeOutが載っている。上の模式図はそのまま投入する170文字以内のペイロードではなく、実際には八進エスケープとfilter名の検出が必要である。

公式ZIPのSHA-256は `f5a4368739359474fc7f075860ebf6ae70ebd87aec14a6a045e6ebf408de2e44`。ローカルZIPの `fake_flag_for_local_testing` は配布物のテスト値であり、受理されたflagではない。
