---
layout: post
title: "抛砖引玉 - 利用Cmder对本地Java运行时环境的切换应用"
subtitle: "个人使用的心得"
date: 2020-06-12 12:00:00
author: "Giko"
header-img: "img/post/2020-06-12-UseCmderSwitchEnv.jpg"
header-mask: 0.3
catalog: true
tags:
  - cmder
  - windows
  - JDK
---

### 多版本环境
做开发的朋友大多数都会有多个环境的切换困扰。通常一个好的运行时环境能有一个好的版本管理器比较重要。  
就譬如NodeJs的nvm - 虽然这也是因为Node的版本升级实在太快，不得不出这么一个（不然就是噩梦）。  
但是相对来说向前兼容性比较强的Java环境来说，这种需求不是很突出。所以这类版本管理在Java环境中就不是很常用。  

不过相对于比较滞后的企业应用，Oracle对JDK的不断升级迭代，很多旧系统不得不跟随步伐，  
很多商业软件也不得不跟随步伐的情况下。JDK的多版本环境的需求很多时候也是刚性的。

### Cmder
[Cmder](https://cmder.net/)是Windows命令行终端的一个很好代替，不光默认支持Git，甚至集成了一些Linux的工具命令。  
除了UI，对于Windows系统上下文菜单的集成配置自由度也是相当的高。

### 思路
在安装多个JDK需要切换的时候，通常就是在指定程序的启动bat里面临时替换JAVA_HOME和PATH。  
非常简单但是每次都要写一段，有时候需要改变运行时还需要改动。简单但是繁琐。  
由于Cmder本身带有一个初始化script。理论上把JAVA_HOME和PATH的替换命令加进去就可以了。  

### 做法
原理很简单，但是如何在一个工具中实现理论上的配置通常就是比较花时间的地方。  
而且工具也可能有多个地方可以更改，如何找到最优的方法也是比较花时间。  
下面是我个人认为最优的方法。无需编辑添加任何文件-直接在设置中添加。  

1. 打开Cmder设置，点击进入【启动-任务】设置
2. 复制一个现有任务（以管理员打开cmder比较好），加上适当后缀，譬如jdk7
3. 修改命令组内容，如下  
  ![picture](https://yougikou.github.io/img/post/2020-06-12-UseCmderSwitchEnv_1.jpg)  

    以下文本用于复制粘贴
    ```
    *cmd /k %ConEmuDir%\..\init.bat&SET JAVA_HOME="C:\Java\jdk1.7.0_25"&SET PATH=C:\Java\jdk1.7.0_25\bin;%PATH%
    ```
4. 点击进入【集成】设置
5. 选取一个菜单项（譬如Cmder Here）后，更改菜单项名称(譬如 Cmder Here w/jdk7)，命令（使用新建的jdk7任务），然后点击【注册】  
  ![picture](https://yougikou.github.io/img/post/2020-06-12-UseCmderSwitchEnv_2.jpg)

### 确认
这样你会发现在Windows系统的上下文菜单（右键菜单）中多了一个【Cmder Here w/jdk7】。  
在任意文件夹中右键点击该项，就会启动一个cmder的命令行窗口。  
![picture](https://yougikou.github.io/img/post/2020-06-12-UseCmderSwitchEnv_3.jpg)  
输入java -version 就可以确认到你预先设置好的Java环境了  
![picture](https://yougikou.github.io/img/post/2020-06-12-UseCmderSwitchEnv_4.jpg)

### 应用和TODO
上述是利用Cmder最基本的【在文件夹中打终端】功能，实现在特定PATH下指定运行时打开命令终端。  
- 同理可以应用到任何一种基于PATH的运行时环境的切换。  
- Cmder还可以把选中文件作为参数传入。这个我还没尝试成功如何设置。  
理论上应该可以指定Java JDK版本运行选中bat。加上这个功能的话用着就更加舒服了。  
有朋友知道的话，希望分享一下设置方法，命令组内容。
