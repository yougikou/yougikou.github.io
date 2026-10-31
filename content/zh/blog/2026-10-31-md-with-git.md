---
title: "让 Markdown 活在 Git 里：md-with-git 文档阅读器与品牌宿主示例"
date: 2026-10-31T18:00:00+09:00
author: "Giko"
image: "/images/posts/md-with-git-cover.png"
categories: ["工程", "开源", "文档工具"]
tags: ["Markdown", "Git", "React", "文档站", "开源"]
draft: false
---

Markdown 很容易写，难的是让它在项目变大之后仍然好找、好读，也能看清每次修改从哪里来。很多团队已经把说明、手册和决策记录放在 Git 仓库里，却还要额外维护一套文档后台。

我做的 **md-with-git** 想把这段距离缩短：Git 仓库继续保存内容和历史，阅读器负责发现、组织与呈现 Markdown。文档仍然是普通文件，阅读体验则可以接近一个轻量的知识库。

![Markdown 文档沿着 Git 历史汇入可搜索的阅读空间，并嵌入品牌化产品界面的插图](/images/posts/md-with-git-cover.png)

## 它解决什么问题？

md-with-git 是一个 React 文档阅读器，也提供可以嵌入既有产品的 npm 包。它不会把整个仓库都当作文档站，而是通过 `scope` 指定一个文档目录。目录树、默认首页、全文搜索和相对链接都限制在这个范围内，因此源码仓库里可以同时存在应用代码与多套彼此独立的文档。

数据来源包括 GitHub、Bitbucket Cloud、本地文件夹和本地 Git 仓库。阅读者可以浏览 Markdown，查看分支或标签、文件历史和版本差异；内容支持 GFM、任务列表、表格、frontmatter、相对资源、Mermaid 与 KaTeX。

项目里有两个可以直接体验的入口：

- [独立 Viewer Demo](https://yougikou.github.io/md-with-git/)：展示完整的文档空间体验。
- [GitHub 仓库](https://github.com/yougikou/md-with-git)：查看源码、架构说明与发布信息。

## 品牌示例展示的是“怎么嵌入”

[md-with-git-branded](https://github.com/yougikou/md-with-git-branded) 是配套的 React 宿主示例，线上地址是 [md-with-git-branded Demo](https://yougikou.github.io/md-with-git-branded/)。它以 Northstar Docs 为例：产品外壳、导航、品牌标识、深浅主题由宿主掌控，`DocsViewer` 则显示 Git 中的文档。

宿主通过 `DocsRendererProvider` 提供品牌与主题配置，通过 React Router 接入文档路由。如果产品需要把特定 Markdown 数据块呈现成组件，也可以在宿主注册表里显式登记渲染器。扩展由宿主代码提供；文档内容只是数据，不能自行选择并加载任意 React 组件。

这两部分的分工很直接：md-with-git 提供阅读器能力，branded 仓库说明如何把它放进自己的产品体验里。

## 内容、历史与安全边界

阅读器只读取仓库内容，不会替你修改 Git 仓库。私有仓库令牌由用户在浏览器中提供，按平台和仓库隔离，并保存在当前会话的 `sessionStorage`，不会放进 URL、项目设置或 Service Worker 缓存。使用时仍应只授予目标仓库所需的只读权限，并只在可信设备上输入令牌。

安装为 PWA 后，Service Worker 缓存的是应用外壳；远程仓库的响应不会被缓存。因此它可以改善应用再次打开时的体验，但不等于把远程文档完整同步到离线设备。

## 从一个文档目录开始

如果文档已经在 Git 里，可以先选一个明确的目录作为 `scope`，再决定要独立使用 Viewer，还是通过 npm 包把它嵌入现有 React 应用。品牌宿主示例提供了路由、主题和扩展渲染器的参考实现，之后可以把 Northstar 的外观换成自己的产品设计。

- [在线查看独立 Viewer](https://yougikou.github.io/md-with-git/)
- [在线查看品牌宿主示例](https://yougikou.github.io/md-with-git-branded/)
- [md-with-git 源码与文档](https://github.com/yougikou/md-with-git)
- [品牌示例源码](https://github.com/yougikou/md-with-git-branded)