---
title: "Hermes 又报 Too Many Open Files，但问题可能不只一个"
date: 2026-04-18T23:51:32+09:00
author: "Giko"
image: "/images/posts/hermes-too-many-open-files/cover.svg"
categories: ["调试", "自动化"]
tags: ["Hermes", "Too many open files", "Errno 24", "launchctl", "plist", "macOS"]
draft: false
---

今天花了不少时间处理 Hermes / OpenClaw 一侧一串看起来很像、但其实不完全一样的故障。

最先冒出来的关键词很明确：`Too many open files`、`Errno 24`。这类报错很容易把人带去一个直接结论：是不是系统 fd limit 太低，应该立刻去改 `ulimit`、改 `launchctl`、改 plist。

但今天这轮排查里，事情没有这么直线。

![Hermes open files debugging cover](/images/posts/hermes-too-many-open-files/cover.svg)

## 先坏掉的不是业务，而是工具层

一开始出问题的不是某个具体功能，而是工具链本身。

有些 cron 任务、搜索和 terminal 调用在执行前就直接失败，错误很统一：

```text
OSError: [Errno 24] Too many open files
```

麻烦在于，这类错误一旦同时出现在搜索、terminal、定时任务这些不相干的地方，排查方向就不能再停留在“某个命令坏了”，而要切换成“整个运行时的资源生命周期可能有问题”。

这时真正需要怀疑的是一整串东西：

- 长生命周期进程有没有累积句柄
- sandbox / worker 有没有清理不及时
- 后台 gateway 是否重复拉起
- skill 扫描、日志文件、subprocess pipe 有没有残留
- 系统 fd limit 本身是不是偏低

也就是说，单纯把 `ulimit -n` 调大，通常只能缓解，不一定能解释现象。

## 现场数字并没有直接支持“已经爆掉”

按最直觉的办法，先去看 limit 和进程 fd 数量。

现场查到的一个关键数字是：

```text
ulimit -n = 1024
```

1024 当然不算特别宽松，但也不是那种一眼就能断言“必炸”的配置。更关键的是，当时相关进程的 fd 数量并没有高到夸张：

- 一个 Hermes 相关进程大约 97 个
- 一个 gateway 相关 Python 进程大约 91 个

如果只看这一刻的现场数据，其实很难直接下结论说“系统现在已经把文件描述符耗尽了”。

这就出现了第一个反直觉点：日志里在大喊 `Too many open files`，但你现场量出来的数字，并没有同步支持这个结论。

比较合理的解释反而有三种：

1. 真有过 fd 压力，但高峰在你量之前已经过去
2. 是某个局部子流程、短时 burst 或旧状态把系统拖坏了
3. `Too many open files` 只是表面症状，当前真正卡死服务的已经是别的问题

今天越往后查，越像第三种。

## 最吓人的日志，不一定是当前主因

继续翻日志时，确实能看到很扎眼的警告：

```text
[Errno 24] Too many open files: '/Users/yougikou/.hermes/config.yaml'
```

这行日志很容易让人顺手得出结论：Hermes 连配置文件都打不开了，那肯定就是 fd 爆了。

但再往下看栈，真正让 gateway 当场起不来的，反而是另一个更具体、也更低级的错误：

```text
NameError: name 'ensure_open_file_limit' is not defined
```

这一下就把问题性质改掉了。

因为它说明：即使 `Too many open files` 曾经真实出现过，当前这一轮 gateway 无法正常启动的直接原因，已经不是 fd 不够，而是入口代码里调用了 `ensure_open_file_limit()`，却没有正确导入这个函数。

换句话说，系统前面可能确实经历过资源压力，但到了我真正抓现场的时候，阻塞启动的那张多米诺骨牌已经换成了 import 级别的 bug。

这类场景很值得记一笔：排查日志时，最频繁出现的错误，不一定等于最接近当前故障面的错误。

## plist、launchctl 和后台服务，也不是旁观者

问题到这里还没结束，因为 Hermes 的运行方式本身就把事情变复杂了。

我这边同时看到了两套 LaunchAgent：

- `ai.hermes.gateway`
- `ai.openclaw.gateway`

以及对应的后台进程。

这意味着就算它们不是同一份逻辑，也至少说明系统里存在两套相近的 gateway / agent 运行路径。在这种情况下，资源占用、重复连接、旧进程残留、日志混杂，都会让“到底谁在制造 fd 压力”这件事变得不那么干净。

后面日志里还出现了另外两个侧面的干扰信号：

- Discord bot token 已被其他进程占用
- Discord privileged intents 配置也有问题

这两类错误本身都不是 `Too many open files`，但它们会制造另一种错觉：你会看到服务不断拉起、重试、报错、重连，然后开始怀疑是不是这些反复失败让句柄没能及时释放。

这个推断目前还没有完整证据链，但它至少比“只是把上限调高一点就没事了”更接近真实系统里常见的问题形态。

## 今天真正学到的，不是怎么调大上限

如果只从操作层面总结，今天当然可以列出一串传统动作：

- 查 `ulimit -n`
- 看 `launchctl` 管理的服务
- 查 LaunchAgent 的 plist
- 看 gateway 的 stdout / stderr 日志
- 数进程的 fd 占用
- 排除是否有重复 gateway 在跑

但今天更重要的收获其实不是这些步骤本身，而是一个判断顺序：

先确认是不是资源问题，再确认是不是仍然是资源问题，最后才决定要不要改系统配置。

这听起来像废话，实际很容易做反。因为一旦先入为主认定“报 `Errno 24` 就一定是 limit 太小”，后面所有证据都会被你解释成这个结论的补充材料。可今天的现场恰恰说明，日志里的 `Too many open files`、运行时的 fd 数量、gateway 当前真正的崩溃点，这三件事并没有完全对齐。

它们有关，但不等价。

## 现在我对问题的判断

截至今天，我更倾向于把它看成一个复合故障，而不是单点故障：

- 一部分现象像是文件描述符压力或清理不及时
- 一部分现象来自后台服务重复存在或重启链条混乱
- 还有一部分则是明确的代码入口 bug，和 fd 本身没直接关系

也正因为如此，`Too many open files` 现在对我来说更像一个症状标签，还不能算最终结论。

如果后面只修掉 `NameError`，问题也许会缓解；如果只改高 `ulimit` 或 plist，问题也许也会暂时不那么容易触发。但这两种动作都还不足以证明根因已经被抓到。

## 还没有结论的部分：plist 到底该怎么改

接下来最值得验证的，反而是 macOS 这一层到底该不该、以及该怎么改 LaunchAgent 的 plist。

目前有一个很自然的猜测：如果 launchd 启动的服务默认 fd limit 偏低，或者它和交互 shell 里的 `ulimit` 并不一致，那么在 plist 里补充对应限制，可能会减少这类问题。

但这里我还没有结论。

原因很简单：现在手上的证据还不足以证明 plist 修改一定是正确方向，更不足以证明某一种改法是可靠的。

所以这件事暂时只能停在“值得继续验证”的阶段，而不是“已经找到标准答案”。

今天的排查先记到这里。`Too many open files` 看起来像主角，但它未必是唯一主因。至于 plist 应该怎么改、改完是否真的能稳定解决问题，我还在继续研究和验证，目前只有推测，还没有最终结论。
