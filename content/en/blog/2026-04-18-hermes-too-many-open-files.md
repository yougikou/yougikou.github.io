---
title: "Hermes Reported Too Many Open Files, but That May Not Be the Whole Problem"
date: 2026-04-18T23:51:32+09:00
author: "Giko"
image: "/images/posts/hermes-too-many-open-files/cover.svg"
categories: ["Debugging", "Automation"]
tags: ["Hermes", "Too many open files", "Errno 24", "launchctl", "plist", "macOS"]
draft: false
---

I spent a good part of today chasing a Hermes / OpenClaw failure that looked simple at first, but turned out not to be a single straight-line bug.

The obvious keywords were `Too many open files` and `Errno 24`. Errors like that push you toward a very direct conclusion: maybe the system fd limit is too low, so the next move should be changing `ulimit`, `launchctl`, or a plist.

But today’s investigation did not stay that clean.

![Hermes open files debugging cover](/images/posts/hermes-too-many-open-files/cover.svg)

## The first thing that broke was not the product logic, but the tooling layer

The earliest visible failures were not in a specific feature. They showed up in the tooling itself.

Some cron runs, searches, and terminal calls failed before they really started, all with the same message:

```text
OSError: [Errno 24] Too many open files
```

Once this kind of error starts appearing across unrelated subsystems like search, terminal, and scheduled tasks, the investigation can no longer stay at the level of “that command is broken.” It becomes a runtime resource-lifecycle problem.

At that point the real suspects are a chain of things:

- whether long-lived processes are accumulating descriptors
- whether sandboxes or workers are cleaning up too slowly
- whether the gateway is being launched more than once
- whether skill scans, log files, or subprocess pipes are lingering
- whether the system fd limit is simply too low

So increasing `ulimit -n` may reduce pressure, but it does not automatically explain what happened.

## The live numbers did not directly support “the system is exhausted now”

The obvious next step was to check the limit and count file descriptors on the relevant processes.

One key number was:

```text
ulimit -n = 1024
```

1024 is not especially generous, but it is also not a number that instantly proves the machine must be collapsing.

More importantly, the live fd counts at that moment were not extreme:

- one Hermes-related process was around 97
- one gateway-related Python process was around 91

If I looked only at that snapshot, it was hard to say the machine was actively exhausting file descriptors right then.

That created the first counterintuitive point: the logs were screaming `Too many open files`, but the live measurements were not fully lining up with that conclusion.

A few explanations fit better:

1. there really was fd pressure earlier, but the peak had already passed
2. a local burst, a short-lived subprocess, or a stale state caused damage indirectly
3. `Too many open files` was only the surface symptom, and the thing currently preventing startup had already changed

The deeper I went, the more it looked like the third case.

## The scariest log line is not always the current root blocker

While reading logs, I did find a very alarming warning:

```text
[Errno 24] Too many open files: '/Users/yougikou/.hermes/config.yaml'
```

That kind of message makes it very tempting to conclude that Hermes cannot even open its config file, so the fd story must be the whole answer.

But further down the stack, the thing that was actually stopping the gateway from starting was a different and much more concrete error:

```text
NameError: name 'ensure_open_file_limit' is not defined
```

That changed the picture immediately.

It means that even if `Too many open files` had happened for real earlier, the direct reason the gateway was failing at that moment was no longer descriptor exhaustion. The direct failure was that the entrypoint called `ensure_open_file_limit()` without importing it correctly.

In other words, the system may have gone through resource pressure first, but by the time I captured the live failure, the blocking domino had already shifted into a plain import-time bug.

That is worth remembering: the most repetitive error in a log is not always the error closest to the current failure surface.

## plist, launchctl, and background services are not neutral bystanders

The situation became messier because of how Hermes is actually run.

On this machine I found two LaunchAgents:

- `ai.hermes.gateway`
- `ai.openclaw.gateway`

and their corresponding background processes.

Even if they are not exactly the same runtime path, they still mean the system contains two closely related gateway / agent service tracks. Once that happens, resource usage, duplicate connections, stale processes, and mixed logs all make it harder to tell who is really creating descriptor pressure.

Two other signals showed up in the logs as well:

- the Discord bot token was already in use by another process
- Discord privileged intents were also misconfigured

Neither one is itself a `Too many open files` error. But both create another kind of confusion: the service keeps starting, retrying, failing, and reconnecting, which makes it reasonable to wonder whether repeated failed startup cycles are part of what keeps descriptors or sockets alive longer than they should be.

I do not have a complete proof chain for that yet. But it is already a more realistic system-level hypothesis than “just raise the limit and the problem goes away.”

## The real lesson today was not how to raise a limit

If I summarize today only at the command level, the list looks familiar:

- check `ulimit -n`
- inspect services under `launchctl`
- read the LaunchAgent plist
- inspect gateway stdout and stderr logs
- count process file descriptors
- rule out duplicate gateway processes

But the more important thing I learned was not the checklist itself. It was the order of judgment.

First confirm whether this is a resource problem. Then confirm whether it is still a resource problem. Only after that decide whether changing system configuration is justified.

That sounds obvious, but it is easy to get backward. Once you decide too early that `Errno 24` must mean the limit is too small, every later clue gets interpreted as supporting evidence.

Today’s evidence did not line up that cleanly. The log messages, the live fd counts, and the gateway’s current crash point were related, but they were not identical.

## My current read of the situation

As of today, I see this more as a composite failure than a single bug:

- part of it looks like descriptor pressure or slow cleanup
- part of it looks like duplicated background services or a messy restart chain
- part of it is a clear entrypoint bug that is not directly about fd pressure at all

Because of that, `Too many open files` feels more like a symptom label than a finished diagnosis.

If the `NameError` is fixed, the system may improve. If the fd limit or plist is adjusted, the issue may become harder to trigger. But neither action, by itself, would prove that the real root cause has been fully captured.

## The part that is still unresolved: how the plist should actually change

The next thing worth validating is whether the macOS LaunchAgent plist should change at all, and if so, how.

There is an obvious hypothesis: if the service launched by `launchd` inherits a lower fd limit than the interactive shell, or if its effective limit differs in practice, then adding the right limit-related change to the plist might reduce the chance of these failures.

But I do not have a final answer yet.

The evidence I have right now is not enough to prove that plist changes are definitely the correct direction, and it is not enough to prove that any specific plist change is reliable.

So this is where I have to stop for now. `Too many open files` still looks like the lead actor, but probably not the only one. As for what the plist should look like, and whether changing it would actually stabilize the system, I am still investigating and validating. Right now I only have hypotheses, not a conclusion.
