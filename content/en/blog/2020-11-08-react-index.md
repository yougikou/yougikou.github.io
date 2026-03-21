---
title: "ReactIndex - Making Folder Index Pages More Practical"
language: "en"
date: 2020-11-08T12:00:00Z
author: "Giko"
image: "/images/posts/2020-11-08-ReactIndex.jpg"
categories: ["Technology", "Frontend Development"]
tags: ["react", "directory index", "review", "education", "tool"]
draft: false
---

## React learning and family needs

&emsp;Work requires exposure to React, and before formally contacting related products, to understand some basics. Besides examples in standard tutorials, it always felt a bit insufficient.
Coincidentally, my wife recently gave me a task:

- Our son's learning materials need organizing, while also being convenient for him to review.
- When reviewing, it's best to be able to quickly view, with answers preferably right beside, facilitating repeated memorization.

## Requirement analysis and refinement

In response to the leader's requirements, I immediately thought of

### Rough plan

- Web-based learning material browsing maximizes usability. As long as a self-built server exists, the child can browse during spare time anytime, anywhere.
- Answer toggling - simple, just use Javascript to make a simple image toggle.
- Most image links use python to automatically generate html pages.

### Started immediately, but preliminary plan attempt revealed several problems

- Image toggle JavaScript is simple, but generating static pages even with python automation still requires manual execution. File maintenance isn't just about image files themselves.
- Opening pages still requires entering from Directory index; for many folders, some classification functionality is needed.

### Implementation direction change

- Since Directory index form is fixed. Using ajax fetch can further process. Generate dynamic pages, requiring only maintenance of content files in folders.
- Use react to build, add content classification functionality.

## React index prototype

### Using Ant design to replace crude Directory index

![picture](/images/posts/2020-11-08-ReactIndex_better-ui.gif)

### Adding secondary classification functionality based on folder names

![picture](/images/posts/2020-11-08-ReactIndex_category-ui.gif)

### Adding folder content type setting to add Markdown text pages (preliminary attempt)

![picture](/images/posts/2020-11-08-ReactIndex_markdown-page.gif)

### Adding learning material review page - Using Ant design components appears stylish

![picture](/images/posts/2020-11-08-ReactIndex_simage-page.gif)

### Not very necessary - but still added category icon customization functionality based on online iconfont

![picture](/images/posts/2020-11-08-ReactIndex_icon-custmization.gif)

## Future plans

React Index design itself is for family internal website for simple viewing by family members.
As long as they understand folder and file organization management, mother and child can easily add content.
So based on some needs in current family usage, there are some future intentions:

1. Add PDF preview (without downloading PDF) (this still requires technical investigation; seems there are js libraries that can achieve).
2. Multi-domain support and switching, enabling configuration of multiple (maybe not very necessary).
3. See if functional pages can be made dynamically loadable, facilitating expansion.
4. Depending on leader's needs...