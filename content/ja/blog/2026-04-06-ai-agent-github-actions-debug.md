---
title: "AIエージェントにGitHub Actionsを直させたら、見事にハマった話"
date: 2026-04-06T21:35:00+09:00
author: "Giko"
image: "https://img.freepik.com/premium-vector/ai-coding-robot-assistant-programming-code-debugging-vector-illustration-concept_694862-52.jpg?w=1800"
categories: ["技術", "GitHub", "ワークフロー"]
tags: ["GitHub Actions", "AI Agent", "CI/CD", "Debug"]
draft: false
---

ここ数日、AIエージェントに GitHub Actions の修正を頼んでいました。目的はかなりシンプルです。

- PR の段階では deploy しない
- PR が `main` に merge されたあとだけ build と deploy を実行する

数分で終わる小さな修正に見えたのですが、実際にはかなり典型的な落とし穴をいくつも踏みました。せっかくなので、ブログとして残しておきます。

![GitHub Actions をデバッグしている AI エージェントの漫画風イラスト](https://img.freepik.com/premium-vector/ai-coding-robot-assistant-programming-code-debugging-vector-illustration-concept_694862-52.jpg?w=1800)

## 最初の誤解：「main に merge される」は独立したイベントだと思っていた

最初にやりがちな勘違いは、「PR が `main` に merge される」という出来事を、`push` とは別の独立した GitHub Actions イベントだと思ってしまうことです。

でも GitHub の実際のイベントモデルでは、

> **PR が `main` に merge されることは、本質的には `main` への `push` です。**

なので、要件がこうであるなら：

- PR 上では何も動かしたくない
- `main` に merge されたあとだけ build + deploy したい

一番素直で安定した書き方は、実はこれです。

```yaml
on:
  push:
    branches: ["main"]
```

これは「古い書き方に戻った」のではなく、GitHub のイベントモデルにそのまま従っているだけです。

## 2つ目の落とし穴：PR イベント上で GitHub Pages を直接 deploy しようとしたこと

次にぶつかった、かなり分かりやすいエラーがこれでした。

> `refs/pull/47/merge is not allowed to deploy to github-pages due to environment protection rules`

ポイントはこうです。

- PR 上で動く ref は通常 `main` ではない
- `refs/pull/47/merge` のような ref になる
- `github-pages` 環境には、その ref に対する保護ルールがある

つまり、

**PR 上で build の検証はできても、GitHub Pages の deploy を PR ref 上でそのまま実行するべきではない**

ということです。

これは YAML の `if` を少し足せば回避できる種類の話ではなく、プラットフォーム側の制約です。

## 3つ目の落とし穴：制約を避けようとして、トリガーを複雑にしすぎたこと

この制約を回避しようとして、途中でいくつか“賢そうな”書き方も試しました。

- `pull_request` + `types: [closed]`
- `workflow_run`
- 1つの workflow の中で PR 検証と deploy 条件を分岐させる

これらは完全に間違いというわけではありません。ただ、次のような問題を生みやすいです。

1. **可読性が落ちる**
2. **実際にどのイベントで何が動くのかを誤解しやすい**
3. **人間も AI も、実際の実行経路を見失いやすい**

特に AI エージェントに何度も連続で修正させる場合、局所的には正しそうな変更が積み重なって、全体としてはどんどん分かりにくくなる、という状態に入りやすいです。

## 最終的に安定した解決策

結局、最後に残ったのは一番素朴な形でした。

```yaml
on:
  push:
    branches: ["main"]
```

そして 1 回の `main` への push の中で、順番にこう処理します。

1. build
2. artifact の upload
3. GitHub Pages への deploy

もしリポジトリ運用として「`main` には必ず PR merge 経由でしか入れない」ようにしたいなら、さらに branch protection を組み合わせます。

- `main` への直接 push を禁止する
- PR を必須にする
- review や status checks を必須にする

これで意味としては、

> **PR が main に merge されたときだけ build と deploy が走る**

という状態になります。

## 今回あらためてはっきりしたこと

AI エージェントに CI/CD の設定変更を任せると、確かにスピードは上がります。
でも本当に向いているのは、

- 繰り返しが多い
- 変更範囲が狭い
- ルールが明確

そういうタスクです。

逆に、

- プラットフォームのイベントモデル
- 権限や保護ルール
- 何度も変わる要件
- 「新しい PR は作るな」「毎回 main を rebase しろ」「既存ブランチを使え」みたいな運用制約

こういったものが絡んでくると、かなり簡単に次の状態になります。

> AI の各ステップはそれぞれもっともらしいのに、最終結果は本来の意図からズレていく。

これは AI 特有の問題ではなく、人間でも同じです。ただ AI は、間違った方向に進む速度も速いだけです。

## 今回の結論

今回の件で、自分の中では次の3つがかなりはっきりしました。

1. **workflow を触る前に、イベントモデルを先に理解する**
2. **GitHub Pages の deploy を PR ref 上でやらない**
3. **AI に運用系の設定を直させるなら、制約を最初に明文化し、毎回最新の `main` を同期してから始める**

多くの場合、本当に時間を節約するのは「AI にすぐ作業させること」ではなく、先に境界と目的をはっきりさせることです。

そうしないと最後は、

- 修正は何度も入った
- PR もいくつもできた
- CI も何度も回った
- でも本当の問題はそのまま残っている

ということになりがちです。

というわけで、これは今日ハマったことの備忘録です。
