---
title: "Keep Markdown in Git: md-with-git and Its Branded Host Sample"
date: 2026-10-31T18:00:00+09:00
author: "Giko"
image: "/images/posts/md-with-git-cover.png"
categories: ["Engineering", "Open Source", "Documentation"]
tags: ["Markdown", "Git", "React", "Documentation", "Open Source"]
draft: false
---

Markdown is easy to write. The harder part is keeping it easy to find, read, and trace as a project grows. Many teams already keep guides, handbooks, and decision records in Git, yet maintain a separate documentation back end on top of them.

**md-with-git** is my attempt to close that gap: the Git repository remains the source of content and history, while a viewer discovers, organizes, and renders the Markdown. The documents stay as ordinary files, while the reading experience feels closer to a lightweight knowledge base.

![An illustration of Markdown documents following Git history into a searchable viewer embedded in a branded product interface](/images/posts/md-with-git-cover.png)

## What does it solve?

md-with-git is a React documentation viewer and an npm package for embedding that viewer in an existing product. It does not treat the whole repository as a documentation site. Instead, `scope` selects a documentation directory. Navigation, the default landing page, full-text search, and relative links stay within that boundary, so application code and separate documentation spaces can live in one repository.

Data sources include GitHub, Bitbucket Cloud, local folders, and local Git repositories. Readers can browse Markdown, branches or tags, file history, and version comparisons. The viewer supports GFM, task lists, tables, frontmatter, relative assets, Mermaid, and KaTeX.

There are two ways to explore it now:

- [Standalone Viewer demo](https://yougikou.github.io/md-with-git/): try the full documentation-space experience.
- [GitHub repository](https://github.com/yougikou/md-with-git): read the source, architecture notes, and release information.

## The branded sample shows how to embed it

[md-with-git-branded](https://github.com/yougikou/md-with-git-branded) is a companion React host example, with a live [md-with-git-branded demo](https://yougikou.github.io/md-with-git-branded/). It uses Northstar Docs to show the split: the host owns the product shell, navigation, brand identity, and light or dark theme, while `DocsViewer` presents documents from Git.

The host passes branding and theme configuration through `DocsRendererProvider` and mounts the documentation route with React Router. If a product needs a custom presentation for a structured Markdown block, it can explicitly register a renderer in the host registry. The host supplies that extension; document content is data and cannot choose and load arbitrary React components.

The roles are straightforward: md-with-git provides the viewer, and the branded repository demonstrates how to make it part of your own product experience.

## Content, history, and security boundaries

The viewer reads repository content but does not modify the Git repository. Users provide private-repository tokens in the browser; tokens are isolated by platform and repository and kept in the current session's `sessionStorage`. They are not put in URLs, project settings, or the Service Worker cache. Use only the read permissions needed for the target repository, and enter tokens only on trusted devices.

When installed as a PWA, the Service Worker caches the application shell. It does not cache responses from remote repositories. That can improve the experience when reopening the app, but it does not synchronize an entire remote documentation set for offline use.

## Start with one documentation directory

If your documents are already in Git, begin by choosing a clear directory for `scope`. Then decide whether to use the standalone viewer or embed the npm package in an existing React app. The branded host sample provides working examples of routes, themes, and registered renderers; you can replace the Northstar presentation with your own product design.

- [Try the standalone Viewer](https://yougikou.github.io/md-with-git/)
- [Explore the branded host sample](https://yougikou.github.io/md-with-git-branded/)
- [md-with-git source and docs](https://github.com/yougikou/md-with-git)
- [Branded sample source](https://github.com/yougikou/md-with-git-branded)