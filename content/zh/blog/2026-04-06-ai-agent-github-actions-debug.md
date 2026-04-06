---
title: "我让 AI 代理改 GitHub Actions，结果踩了一串坑"
date: 2026-04-06T21:35:00+09:00
author: "Giko"
image: "https://img.freepik.com/premium-vector/ai-coding-robot-assistant-programming-code-debugging-vector-illustration-concept_694862-52.jpg?w=1800"
categories: ["技术", "GitHub", "工作流"]
tags: ["GitHub Actions", "AI Agent", "CI/CD", "Debug"]
draft: false
---

这两天我让 AI 代理帮我修改 GitHub Actions，目标其实很简单：

- PR 阶段不要触发部署
- 只有 PR merge 到 `main` 之后，才执行 build 和 deploy

听起来像是一个几分钟就能改完的小任务，结果一路改下来，踩了不少很典型的坑。刚好适合记一篇博客。

![AI 代理在调 GitHub Actions 的漫画风插图](https://img.freepik.com/premium-vector/ai-coding-robot-assistant-programming-code-debugging-vector-illustration-concept_694862-52.jpg?w=1800)

## 一开始的误解：把“merge 到 main”理解成了单独事件

最开始很容易犯的错误是，把“PR merge 到 `main`”理解成一个和 `push` 平行的、单独的 GitHub Actions 事件。

但在 GitHub 的实际模型里：

> **PR merge 到 `main`，本质上就是一次 `push` 到 `main`。**

所以如果需求是：

- PR 不跑任何东西
- merge 到 `main` 以后才 build + deploy

那 workflow 里最直接、也最稳定的写法其实就是：

```yaml
on:
  push:
    branches: ["main"]
```

这不是“退回 old school 写法”，而是 GitHub 本身的事件模型决定的。

## 第二个坑：试图在 PR 事件里直接做 GitHub Pages deploy

后面踩到的一个更明显的问题，是这个报错：

> `refs/pull/47/merge is not allowed to deploy to github-pages due to environment protection rules`

这个问题的核心是：

- PR 上运行的 ref 通常不是 `main`
- 而是类似 `refs/pull/47/merge`
- GitHub Pages 的部署环境 `github-pages` 对这种 ref 有保护限制

换句话说：

**你可以在 PR 上做构建校验，但不要在 PR 上直接跑 Pages deploy。**

这是平台规则，不是 YAML 写两行 if 就能完全绕过去的。

## 第三个坑：为了绕开限制，走了过度复杂的触发链

后来又尝试过几种“看上去更聪明”的方式，比如：

- `pull_request` + `types: [closed]`
- `workflow_run`
- 在一个 workflow 里混合 PR 校验和 deploy 条件分支

这些方案的问题不是完全不能用，而是：

1. **可读性变差**
2. **更容易误判触发条件**
3. **更容易让自己和 AI 都搞混真实执行路径**

尤其是在让 AI 代理多轮连续修改时，这种复杂度很容易把任务拖进“局部修好了、整体却越来越绕”的状态。

## 真正稳定的解决方案

最后回到最朴素也最稳定的方案：

```yaml
on:
  push:
    branches: ["main"]
```

然后让 workflow 在一次 main push 中完成：

1. build
2. upload artifact
3. deploy pages

如果仓库治理上要求“必须通过 PR merge 才能进 main”，那再配合 GitHub 的 branch protection：

- 禁止直接 push `main`
- 要求必须走 PR
- 要求 review / status checks

这样组合起来，语义上就等于：

> **只有 PR merge 到 main 时，才触发 build 和 deploy。**

## 这次让我更确定的一件事

让 AI 代理改 CI/CD 配置，确实能提速。
但它最适合的是：

- 重复性高
- 变更面小
- 规则清晰

一旦任务涉及：

- 平台事件模型
- 权限保护
- 多轮需求变更
- 还夹杂“不要新开 PR / 要先 rebase main / 要沿用旧分支”这种流程约束

那就非常容易出现一种情况：

> AI 每一步看起来都“有道理”，但整体结果却偏离你的真实意图。

这不是 AI 特有的问题，人类在复杂流程里一样会犯。区别只是 AI 会更快地把错误执行很多次。

## 我的结论

这次折腾完之后，我给自己总结了三条：

1. **事件模型先搞清楚，再写 workflow。**
2. **GitHub Pages deploy 不要放在 PR ref 上做。**
3. **让 AI 改流程配置时，约束要一次说清，并且每轮都先同步最新 main。**

很多时候，真正省时间的不是“让 AI 立刻开始改”，而是先把边界和目标讲明白。

否则最后就会变成：

- 代码改了很多轮
- PR 开了好几个
- CI 也跑了很多次
- 但真正的问题还在原地

这篇文章，算是给今天踩过的坑做个存档。
