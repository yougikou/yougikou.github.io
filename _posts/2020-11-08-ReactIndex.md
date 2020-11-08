---
layout: post
title: "ReactIndex - 让文件夹index页面变得更有实用性"
subtitle: "替换传统Web服务器的文件夹index页面"
date: 2020-11-08 12:00:00
author: "Giko"
header-img: "img/post/2020-11-08-ReactIndex.jpg"
header-mask: 0.3
catalog: true
tags:
  - react
  - directory index
  - 复习
  - 教育
  - 工具
---

## React的学习和家庭需求

&emsp;工作上有需要接触React，而在正式接触相关产品之前为了了解一些基础。除了标准教程里面的例子意外，总觉得有点不够。  
正好孩子他妈最近交给我一个任务：

- 儿子的学习资料需要整理，同时要方便他复习。
- 复习的时候最好可以迅速查看，答案最好就在旁边，方便反复记忆。

## 需求分析和精炼

针对领导的要求，本人第一时间想出

### 大致方案

- Web方式的学习资料浏览最大限度的提高了可用性。只要自建服务器，随时随地可以让孩子利用空余时间浏览。
- 答案切换 - 简单，用Javascript做个简单的图片切换即可。
- 大部分图像链接使用python自动生成html页面。

### 说动手就动手，结果初步方案尝试下来发现几个问题

- 图片切换的JavaScript很简单，但是生成静态页面即便使用python自动化，也还是需要手动执行。文件的维护不仅仅只是图像文件本身。
- 打开页面还是需要从Directory index进入，对于大量文件夹，多少需要分类的功能。

### 实现方案方向变更

- 由于Directory index的形式就是固定的。使用ajax获取后可以进一步处理。生成动态页面，实现仅仅需要维护文件夹中的内容文件即可。
- 使用react构筑，添加内容分类功能。

## React index的雏形

### 使用Ant design替换了简陋的Directory index

![picture](https://yougikou.github.io/img/post/2020-11-08-ReactIndex_better-ui.gif)

### 加入基于文件夹名的二级分类功能

![picture](https://yougikou.github.io/img/post/2020-11-08-ReactIndex_category-ui.gif)

### 加入文件夹内容类型设定添加Markdown文本页面（初步尝试）

![picture](https://yougikou.github.io/img/post/2020-11-08-ReactIndex_markdown-page.gif)

### 添加学习资料复习页面-使用Ant design组件显得有逼格

![picture](https://yougikou.github.io/img/post/2020-11-08-ReactIndex_simage-page.gif)

### 不是很需要-但是还是加入基于在线iconfont的分类图标自定义功能

![picture](https://yougikou.github.io/img/post/2020-11-08-ReactIndex_icon-custmization.gif)

## 后续计划

React Index的设计本身就是用于家庭成员简单查看的家庭内部网站。
只要懂得文件夹、文件的组织管理，妈妈孩子都可以很容易的添加内容。
所以针对现在家庭使用中的一些需求，有一些后续打算

1. 添加（不用下载PDF的）PDF预览（这个还需要技术调查，好像有js库可以实现）。
2. 多域名支持和切换，这样可以配置多个（可能不是很有必要）。
3. 功能页面看看能不能做成动态加载，方便扩展。
4. 看领导需求。。。
