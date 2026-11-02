# Orphaned Context — 再利用されたスロットに古い権限が残る

分類: Web。[問題ページ](https://ctf.hiddeninvestigations.net/challenges?challenge=b8d28d25-e9fa-4e94-a4ed-364826f04cdd) · [English](README.en.md)

リレーのコンソールから状態、監査イベント、インシデントを読めた。監査履歴には、復旧用descriptorが残った中断済みcaptureと、作業スロットに保存された非信頼の保守noteが現れる。稼働中の `IR-7731` には `seal` がある。元のcaptureが消えても古いdescriptorが同じスロットを認可する、という寿命の食い違いを検証した。

問題文は調査員向けhandoutに言及していたが、当初の公開問題データには添付がなかった。以下のAPI名はコンソールと自チームのインスタンスでの限定的な確認から得たもので、handoutを入手したという意味ではない。

1. `POST /api/capture/open` に `{}` を送り、返されたrequest IDと `recovery_descriptor` を控える。
2. そのIDで `POST /api/capture/interrupt` を呼ぶ。descriptorを残したままslot 0が空く。
3. `POST /api/note/store` へ `{"text":"#!relay-maint/1\nhelp\nls /\n"}` を送り、**非信頼**のnoteを再利用されたslot 0へ置く。
4. 古いdescriptorで `POST /api/recover/preview` を呼ぶと `trusted: true` が返り、noteの仮想診断コマンドが動いた。これが権限境界の破れである。
5. 返されたnote IDとepochでnoteを破棄し、同じslotに次のnoteを保存する。

   ```text
   #!relay-maint/1
   ls /incidents
   ls /incidents/IR-7731
   cat /incidents/IR-7731/seal
   ```

6. 元のdescriptorで再度previewすると、リレーの**メモリ内診断マップ**から `seal` を読めた。OSコマンドを実行したわけではない。

出力は `hiCTF{local_dev_fixture_not_a_real_flag_9ec7b16d04}` だった。fixtureに見える名称なので一度だけ公式チェッカーへ提出し、画面の `Challenge solved!` と最終公開解答一覧で受理を確認した。descriptorやnote IDはインスタンスごとに変わるため、各レスポンスの値を使う。
