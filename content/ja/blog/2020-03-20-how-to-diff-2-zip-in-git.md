---
title: "Git - Windows git環境で2つのコミット間のファイル差分を抽出しzipにパッケージ化する方法"
date: 2020-03-20T12:00:00Z
author: "Giko"
image: "/images/posts/post-bg-git.png"
categories: ["技術"]
tags: ["git", "windows", "bash", "sourcetree", "custom actions"]
draft: false
---

### 背景

仕事でGitを使い始めてしばらく経ちました。同僚はコマンドラインを直接使うことを勧めますが、私はやはりUIが好きです。SVN時代には、2回のコミット間の変更ファイルを抽出するのは非常に一般的な操作でした。Gitに切り替えてから、このコマンドをどう実現するか気になっていました。さまざまな方法があるのは知っていましたが、いつも自分の使い慣れた方法にはなりませんでした。
最近新しいアプローチを発見したので、整理して皆さんの参考に供します。

### Googleでよく見つかる方法

1. TortoiseGitにはログ画面で選択したファイルをエクスポートする機能が組み込まれています
   ![TortoiseGit Export Selection To...](/images/posts/2020-03-20-HowToDiff2ZipInGit-1.jpg)
   この機能は単一のコミットからファイルを抽出するのに便利ですが、複数コミットにわたる累積変更には使えません。ログ画面で2つのコミットを選択するのはSVNとは全く異なり、ファイルが見えなくなります。この小技を紹介する記事はありますが、この理由で…完璧ではありません。

2. Windowsバッチ
   一時的に使っていた、日本人の開発者が書いたものです。原理はgit diffの結果をループに入れ、1つずつコピーするものです。
   SourceTreeのCustom Actionsに設定して直接使用できます。
   その人のブログは今では見つけられないので、リンクは貼りません。しかも、この方法には欠点があります！
   Windows環境では、ファイルパスに長さ制限があります。多くのプロジェクトでフォルダの階層が深すぎると、「ファイルが見つかりません」問題が発生します。
   もちろんWindows 10以降はグループポリシーでこの制限を解除できますが、環境によっては誰でもうまく設定できるわけではないことを証明しているので…完璧ではありません。

3. シェルスクリプト
   `Git diff $sha1 $sha2 --name-only | xargs tar -zcvf update.tar.gz` これはコマンドラインの方法で、Linuxでは最も一般的です。
   確かにうまくいきます。WindowsにGit付属のLinuxツールをインストールした後、使用するのにまったく問題ありません。
   しかし、毎回SHA値をコピーするのは面倒ですし、tarの圧縮方式はWindowsでは違和感があり、解凍には2段階必要…完璧ではありません。

4. SourceTreeのネイティブ機能は言うまでもなく、プロジェクト全体の状態をArchiveするだけなので、あまりに手間がかかります。

### いくつかのキーポイントと解決方法

1. GUI操作から選択したSHA値をどう渡すか
   SourceTreeのCustom Actionsはこの機能を提供しており、$SHAをScriptに渡すことができます。

2. SourceTreeのCustom Actionsでbashのshell scriptを実行させる方法
   この点が最も重要な鍵ですが、この解決策を探しているとき、どの記事にもこの点は言及されていませんでした。まったく無関係な記事の中で偶然答えを見つけました。設定は以下の通り、Gitは皆がインストールするもので、bashは自動的に付属します。
   ![SourceTree Custom Action Run Bash Script](/images/posts/2020-03-20-HowToDiff2ZipInGit-2.jpg)

3. これでWindowsでも便利なshell commandを使って、2つのコミット間の変更ファイルを抽出し、同時にパッケージ化できます。
   しかし、zipにどうパッケージ化するかという問題が残っています。Windows自体にはこのためのコマンドがありません。GitのLinuxツールパッケージにはunzipとtarが含まれていますが、zipは含まれていません。（これには小さなエピソードがあります：私には2台のPCがあり、1台にはzipコマンドがあり、もう1台にはありませんでした。最初は何をインストールした違いでこの差が生じたのかわかりませんでした。長い時間をかけて、Oracleデータベースのインストールディレクトリのbinにzip.exeが含まれていることに気づきました…まあ）

   ポイントは、オンラインでこのプロジェクト（Info-ZIP）のソースコードは見つかっても、コンパイル済みのzip.exeを見つけてコピーして使うことができなかったことです。必要な方はここから直接ダウンロードできます（[zip.exe.zip](/attached/zip.exe.zip)）。
   GitのLinuxツールパッケージのパス（Git\usr\bin）に置けば、他のコマンドのように直接使用できます。

   以下はshell script自体です。わかってしまえば大したことはありません。必要に応じて参考にしてください。

   _$Repoは必須ではありません。SourceTreeで実行するとき、現在のフォルダは自動的にプロジェクトのルートディレクトリになります。_

   ```shell
      # use parameter -> $REPO $SHA
      repo=""
      sha1=""
      sha2=""
      if [ -n "$1" ] && [ -n "$2" ] && [ -n "$3" ] && [ -z "$4" ]; then
      repo=$1
      sha1=$3
      sha2=$2
      echo "Repository is ${1}."
      echo "Current path is ${PWD}."
      echo $2
      echo $3
      # git diff --diff-filter=ACM $sha1 $sha2 --name-only | xargs tar -czvf update.tar.gz
      git diff --diff-filter=ACM $sha1 $sha2 --name-only | xargs zip -r ./update.zip
      else
      echo "please select two commit"
      fi
      exit
   ```

補足：--diff-filter=ACMを追加することで、変更を追加・変更されたファイルに限定します。削除されたファイルはパッケージング時に当然見つかりません。ログを確認するか、このオプションを追加して事前に除外できます。

私のようにまだWindowsを主要開発環境として使い、上記の要件を持つ友人がどれだけいるかわかりません。長い間探しても完璧な解決策が見つかりませんでした。この方法は私が比較的完成していると思うもので、必要な方の参考に供します。
十数年も字を書いていないので、これだけ書くだけで少し疲れました:-O