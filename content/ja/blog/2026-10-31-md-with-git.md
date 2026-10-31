---
title: "MarkdownをGitの中で活かす：md-with-gitとブランドホストのサンプル"
date: 2026-10-31T18:00:00+09:00
author: "Giko"
image: "/images/posts/md-with-git-cover.png"
categories: ["エンジニアリング", "オープンソース", "ドキュメント"]
tags: ["Markdown", "Git", "React", "ドキュメント", "オープンソース"]
draft: false
---

Markdownを書くのは簡単です。難しいのは、プロジェクトが大きくなっても必要な情報を見つけやすく、読みやすく保ち、変更の経緯も追えるようにすることです。説明書や設計メモをすでにGitリポジトリに置いていても、別のドキュメント管理画面を運用しているチームは少なくありません。

**md-with-git**は、その距離を縮めるために作りました。内容と変更履歴はGitリポジトリに置いたまま、ViewerがMarkdownを見つけて整理し、読みやすく表示します。文書は普通のファイルのまま、閲覧体験は軽量なナレッジベースに近づけられます。

![Markdown文書がGitの履歴をたどって検索できるViewerへ集まり、ブランド化された製品画面に組み込まれるイラスト](/images/posts/md-with-git-cover.png)

## 何を解決するのか

md-with-gitはReact向けのドキュメントViewerで、既存プロダクトに組み込むためのnpmパッケージも提供します。リポジトリ全体をドキュメントサイトにするのではなく、`scope`で対象ディレクトリを指定します。ツリー、既定のトップページ、全文検索、相対リンクはその範囲に限定されるため、アプリのソースコードと複数の独立した文書セットを同じリポジトリで管理できます。

データソースはGitHub、Bitbucket Cloud、ローカルフォルダー、ローカルGitに対応します。Markdownの閲覧に加え、ブランチやタグ、ファイル履歴、バージョン差分を確認できます。GFM、タスクリスト、表、frontmatter、相対リソース、Mermaid、KaTeXも扱えます。

すぐに試せる入口は2つあります。

- [単体Viewer Demo](https://yougikou.github.io/md-with-git/)：ドキュメント空間全体の操作を確認できます。
- [GitHubリポジトリ](https://github.com/yougikou/md-with-git)：ソース、設計、リリース情報を確認できます。

## ブランド版が見せる「組み込み方」

[md-with-git-branded](https://github.com/yougikou/md-with-git-branded)は、連携方法を示すReactホストのサンプルです。[オンラインDemo](https://yougikou.github.io/md-with-git-branded/)ではNorthstar Docsを例に、製品の外枠、ナビゲーション、ブランド、ライト／ダークテーマをホスト側が管理し、`DocsViewer`がGit上の文書を表示します。

ホストは`DocsRendererProvider`でブランドとテーマを渡し、React Routerから文書ルートを開きます。特定のMarkdownデータを独自コンポーネントで表示したい場合は、ホスト側の登録表にレンダラーを明示的に登録できます。拡張コードはホストが提供し、文書自体はデータとして扱うため、Markdownから任意のReactコンポーネントを選んで読み込む仕組みにはなっていません。

役割はシンプルです。md-with-gitがViewer機能を提供し、brandedリポジトリがそれを自分の製品に組み込む方法を示します。

## 内容・履歴・セキュリティの境界

Viewerはリポジトリを読み取りますが、Gitの内容を変更しません。プライベートリポジトリのトークンはブラウザー上でユーザーが入力し、プラットフォームとリポジトリごとに分離して、現在のセッションの`sessionStorage`に保存されます。URL、プロジェクト設定、Service Workerのキャッシュには入りません。利用時は対象リポジトリに必要な読み取り専用権限だけを付け、信頼できる端末で入力してください。

PWAとしてインストールした場合、Service Workerがキャッシュするのはアプリのシェルです。リモートリポジトリの応答はキャッシュしません。そのため再訪時の体験は改善できますが、リモート文書一式を端末へ同期してオフライン利用できる、という意味ではありません。

## まずは1つの文書ディレクトリから

文書がすでにGitにあるなら、最初に`scope`として明確なディレクトリを1つ選びます。そのうえでViewerを単体で使うか、npmパッケージ経由で既存のReactアプリに組み込むかを決められます。ブランド版サンプルにはルーティング、テーマ、拡張レンダラーの実装例があり、Northstarの見た目を自分の製品デザインに置き換える参考になります。

- [単体Viewerを試す](https://yougikou.github.io/md-with-git/)
- [ブランドホストのサンプルを見る](https://yougikou.github.io/md-with-git-branded/)
- [md-with-gitのソースと文書](https://github.com/yougikou/md-with-git)
- [ブランドサンプルのソース](https://github.com/yougikou/md-with-git-branded)