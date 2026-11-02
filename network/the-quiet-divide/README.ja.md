# The Quiet Divide（Network）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=46aa0afb-e480-4614-8634-528586911f7d) · Agentic AI部門

配布ZIPのSHA-256は `15c7f337f5eae52865fbece148237ca5f01b2f4fa703d64a54c4f35a7bb40225` で、152,240,093バイトのPCAPが入っています。複数のもっともらしいアーカイブから、正式なproduction転送を特定する問題です。アーカイブ3件はいずれも認証付き復号に成功するため、復号タグが正しいだけでは選べません。

## 証拠をつなぐ

1. PCAPをストリーム処理し、TCPの各方向を再構成してHTTPの要求と応答を対応付けます。約99秒間に110,248パケット、185件のHTTP取引があります。要求ストリーム190、204、222にはそれぞれ `AVLT10` 形式の暗号化アーカイブ書き込みと成功レシートがあります。バッチのfinalizeは保存完了を示しますが、正式なrelease対象までは決めません。
2. ストリーム29の `ARCH-14` 登録記録は、`IDX-S9` shardのproduction機器を示します。ストリーム21、23、25、27の4つのHTTP byte rangeからファームウェアv7.7.0を再構成し、SHA-256 `0835dfce789d002d55f3d20fe7f953a30da0adbef336a861839ce8f579958836` を確認します。キャプチャ内の `/v10/sdk` 応答には、以下で使うバイナリ配置と鍵導出規則があります。
3. HTTPの2つのescrow share（ストリーム50、52）をXORするとproduction QUICのkeylogになります。各shareとレシートのハッシュ、XOR結果と宣言されたkeylogハッシュを照合します。`10.77.40.14` から `10.77.40.37` への1-RTT観測を復号すると、`ARCH-14`、sequence 848971、queue depth 31、load 8%、v7.7.0ファームウェアハッシュが得られます。canonical signed objectのSHA-256 `60369e7f8427e6bc708a33afab217c9b42b64be3b43a7ef5ecc7396ba5a211eb` はACKとstatus serviceに一致します。別のrecovery sessionは `dr-ops` の `REC-14` が署名しており、`fleet-prod` のrelease範囲外です。
4. TCPストリーム34とUDPにある `PLS2` のlive frameを、SDKのCRCと状態規則で検証します。frame counterは **10450910**、scheduler queueは23、loadは71、epochは `1793517529318` msです。このepochは `ARCH-14` のattestationと一致します。
5. `/v8/audit` の5つのcustody event、epoch 732 ROOT、733 PREP/COMMIT、734 PREP/COMMITを検証します。`MIRRORBREAK/CUSTODY/B1\0` domainのevent hash、親リンク、Ed25519委員署名15件を確認します。各eventにchairを含む3鍵のquorumがあります。末端event hashは `b34dc728c1fa1525020b1969a8af2698b2bcd91a95d58b3e3b940de35deda6e1`。独立したW0 checkpoint（ストリーム172/188）は `fleet-prod` のepoch 734 COMMITを固定し、そのcanonical hashは `5e4f78ad0e23d862a60ef8fca9891b47997dc1936043dd13efe419beaf7b3c53` です。その後のepoch 735の複製記録は、この立会済みrelease点に置き換わりません。v7.7.1の適格性報告はインストール済みの証拠ではありません。

## アーカイブを選んで開く

SDKの配置規則と上記のproduction証拠を使い、final sealのsaltから `AVLT10` のアーカイブ鍵を導きます。3件とも認証付き復号に成功し、別々のSQLiteデータベースになります。`transfers`、`receipts`、`fragments` テーブルを照合します。要求ストリーム **222** のtransaction `6dd9ec588c9914ca95df44b2` だけが、末端custody hash、機器nonce `12060f75d51d36eb9db836f46f49f575`、frame counter **10450910**、origin `OPS-17`、version 10、W0 checkpoint hash、codec観測、保存レシート、4断片のdigestとmaterial commitmentを同時に満たします。ストリーム190はnonceが異なり、204はcounterが異なります。222内の他の行もcase、origin、checkpoint、stateのいずれかが合いません。

選ばれた4断片のmaskを外し、production証拠とW0 checkpointの署名を使うSDKの `final_key` 導出規則を適用します。指定のAADとAES-256-GCMでfinal sealを復号すると、認証済み平文は次の値です。

```text
hiCTF{c8c46fdbd6e5e4eacabfba53a156ff9ab10567f2}
```

公式問題画面はこの値に `Flag correct!` と `Challenge solved!` を表示し、自チームの大会終了時の公開解答済み一覧にも本問が含まれます。提出後にローカルソルバーを再実行しても該当転送は1件だけでした。ファームウェア、checkpoint、sealの内容は、キャプチャ中のハッシュ、検証済みcustody chain、認証付き復号で結び付けています。ただし、公開SDKが規定していない一部の個別署名domainは独立には検証していません。
