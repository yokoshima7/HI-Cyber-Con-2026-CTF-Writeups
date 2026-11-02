# The Inner Engine（Reverse Engineering）

[English](README.en.md)

[公式問題](https://ctf.hiddeninvestigations.net/challenges?challenge=f7603a79-8925-4e5e-8fb7-299a4205f836) · 配布ZIPのSHA-256: `8c20991917e05093d0c87268ae9563515cd33abc90dd36b916413b5667559f46`

strip済みNim製ELFは、1命令5バイトのスタックVMを実行する。`.rodata` から命令列を取り出し、算術、スタック、メモリ、条件分岐、終了の各opcodeを読み解いた。成功経路を記号実行し、24個の検査分岐について「失敗命令へ飛ばない」という条件を24バイトの印字可能な鍵へのZ3制約にした。

条件を満たす鍵の一つは `L1c#N0d3_7mQ9f3a2b8c6d1e`。ただしVMの条件だけでは別のモデルもある。成功処理は鍵をSHA-256にかけ、そのダイジェストとビッグエンディアンのカウンターを再度ハッシュして40バイトの鍵ストリームを作る。埋め込み暗号文とXORすると `hiCTF{vm_byt3c0d3_1nn3r_3ng1n3_unw0und!}` となり、そのSHA-256はELF内の期待値 `e4f870dad765bfab3d282870ec136b8f450dc8c606cd894b9ea78c91736a5272` と一致した。

ローカルではVMの処理と暗号検査を再現したが、macOS上でELF自体は実行していない。大会終了時の自チームの公式解答済み一覧にはThe Inner Engineが含まれる。
