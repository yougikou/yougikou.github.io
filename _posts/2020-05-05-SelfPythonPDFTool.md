---
layout: post
title: "Python PDF自制工具"
subtitle: "扫描文档的快速编辑"
date: 2020-05-05 12:00:00
author: "Giko"
header-img: "img/post/2020-05-05-SelfPythonPDFTool-1.jpg"
header-mask: 0.3
catalog: true
tags:
  - Python
  - windows
  - PDF
  - Tool
  - PDF merge, split, rotate
---

### 方便的快速编程语言和丰富的扩展
&emsp;我对于Python的印象就是一个好写, 好除虫, 快速上手的强大的批处理工具语言.当然由于工作上不是经常用到,所以认识比较浅薄. 
这阶段由于为了帮孩子有效复习, 买了可以双面扫描的打印机后, 发现家用打印机毕竟不是商用, 一些功能还是比较不方便.
譬如, 扫描下来的页面只能是竖着的, 电脑上查看要横过来还得自己旋转. 有些是书本册子的, 中间的装订线去除后扫描, 页面需要分割, 顺序也需要重新排序. 虽然有PDF编辑软件, 但每次这种单纯操作的工作量还是很大.
而且很狗屁的是很多所谓的免费PDF编辑软件都一些基本功能, 还要安装. 一旦需要高级一点的马上需要升级订阅.
这时我首先想到了Python.

### 使用PDF库
&emsp;pdfrw - 至少对于我的需求这个库非常的好.
一开始使用PyPDF2, 但是在分割的时候发现会造成文件大小翻倍, 也不能压缩.
所以途中放弃转用pdfrw, 而且该作者还很热心, 在PyPDF2的文件大小翻倍的issue thread上给出pdfrw的写法.

### 自制工具
&emsp;所有工具追求易用, 都采用选择PDF, 拖拽带相应的py上后就开始执行.
所有输出统一到同文件夹内新建out的子文件夹中.
出现任何异常console画面会停顿10面可以查看出错的命令行数, 错误内容.

使用前先安装pdfrw(pip install pdfrw)
最好把Python升级到3.8以上, 我发现有新的python launcher可以自动关联py文件.
双击, 拖拽文件执行都很方便.

1. [mergePdf.py](https://yougikou.github.io/attached/mergePdf.py)
把拖拽的多个文件合并成一个文件. 拖拽时鼠标拖动的文件最好是第一个.
不然可能点中的文件可以跑到头上去.

2. [rotateL90.py](https://yougikou.github.io/attached/rotateL90.py)
把拖拽的多个文件都执行向左旋转90度

3. [split&sort.py](https://yougikou.github.io/attached/split&sort.py)
这个比较高级点. 是根据以下的扫描前提进行处理的.\
去装订线扫描时 - 从中间页(为第一页)开始扫描.\
这样譬如中间页是 11,12, 则 Page1(11,12), Page2(13,10), Page3(9,14)...\
所以这个py把拖拽的多个文件都执行下述操作后输出为一个新的pdf.\
原文件可供制册打印, 处理后的文件可用于电脑阅读.\
   - 分页: 把每页分成左右两页
   - 排序: 根据上述规则, 把分割的页面按真正的页序排序

分享py以供有同样需求的朋友, 或者当样例参考, 毕竟需求类似的话比自己从0开始考虑要省力很多.


