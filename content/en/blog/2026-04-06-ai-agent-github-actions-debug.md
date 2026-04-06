---
title: "I Asked an AI Agent to Fix GitHub Actions—and Stepped Into a Chain of Traps"
date: 2026-04-06T21:35:00+09:00
author: "Giko"
image: "https://img.freepik.com/premium-vector/ai-coding-robot-assistant-programming-code-debugging-vector-illustration-concept_694862-52.jpg?w=1800"
categories: ["Tech", "GitHub", "Workflow"]
tags: ["GitHub Actions", "AI Agent", "CI/CD", "Debug"]
draft: false
---

Over the past two days, I asked an AI agent to help me modify a GitHub Actions workflow. The goal sounded simple:

- do not deploy during the PR stage
- only run build and deploy after the PR is merged into `main`

It sounded like a five-minute task. Instead, it turned into a neat collection of very typical mistakes. Which makes it a pretty good blog post.

![Comic-style illustration of an AI agent debugging GitHub Actions](https://img.freepik.com/premium-vector/ai-coding-robot-assistant-programming-code-debugging-vector-illustration-concept_694862-52.jpg?w=1800)

## The first misunderstanding: treating “merge into main” as a separate event

The easiest mistake was to think of “PR merged into `main`” as a standalone GitHub Actions event parallel to `push`.

But in GitHub’s actual event model:

> **A PR merge into `main` is, in essence, a `push` to `main`.**

So if your requirement is:

- nothing should run on the PR
- build and deploy should happen only after merge into `main`

then the simplest and most stable workflow trigger is actually:

```yaml
on:
  push:
    branches: ["main"]
```

That is not “going back to an old-school setup.” It is simply how GitHub models the event.

## The second trap: trying to deploy GitHub Pages directly from a PR event

The clearest error message I hit was this:

> `refs/pull/47/merge is not allowed to deploy to github-pages due to environment protection rules`

The core issue is:

- the ref running in a PR is usually not `main`
- it is something like `refs/pull/47/merge`
- the `github-pages` deployment environment has protection rules against that ref

In other words:

**You can do build validation on a PR, but you should not run GitHub Pages deploy directly on a PR ref.**

That is a platform rule, not something you can fully outsmart with two extra `if` lines in YAML.

## The third trap: overcomplicating the trigger chain

To get around the restriction, I tried a few “clever” patterns:

- `pull_request` + `types: [closed]`
- `workflow_run`
- mixing PR validation and deploy branching logic in a single workflow

These approaches are not always invalid, but they introduce a few problems:

1. **they are harder to read**
2. **they make it easier to misunderstand the real trigger path**
3. **they make it easier for both the human and the AI to lose track of what is actually supposed to happen**

This gets worse when an AI agent is making multiple iterative edits. You can easily end up in a state where each local fix seems reasonable, but the overall workflow becomes more and more confusing.

## The stable solution

In the end, the most reliable answer was also the plainest one:

```yaml
on:
  push:
    branches: ["main"]
```

Then let the workflow do all of the following in one main-branch push:

1. build
2. upload artifact
3. deploy pages

If your repo governance requires every change to go through a PR merge before reaching `main`, then combine that with branch protection:

- block direct pushes to `main`
- require pull requests
- require review / status checks

With that setup, the semantics become:

> **Build and deploy only when a PR is merged into main.**

## One thing this made even clearer to me

Using an AI agent to edit CI/CD config can absolutely speed things up.
But it works best when the task is:

- repetitive
- narrow in scope
- governed by clear rules

Once the task involves:

- platform event models
- permission boundaries
- changing requirements over multiple rounds
- process constraints like “don’t open a new PR”, “rebase main first”, or “reuse the current branch”

then it becomes very easy to fall into this pattern:

> Every single AI step sounds reasonable, but the overall result drifts away from your real intent.

That is not uniquely an AI problem. Humans do the same thing in complex workflows. The difference is just that AI can repeat the wrong move much faster.

## My takeaway

After all this, I’m keeping three rules in mind:

1. **Understand the event model before editing the workflow.**
2. **Do not deploy GitHub Pages from a PR ref.**
3. **When using AI to modify process configuration, define the constraints clearly and sync the latest `main` before every round.**

A lot of the time, the real time-saver is not “letting AI start immediately.”
It is making the boundary and the goal explicit first.

Otherwise the result looks like this:

- lots of code changes
- multiple PRs
- many CI runs
- but the original problem is still sitting there

So this post is basically a field note from today’s mistakes.
