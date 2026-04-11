---
title: "How I Configured Hermes Agent as a Fixed-Rhythm Blog Assistant"
date: 2026-04-11T20:00:26+09:00
author: "Giko"
image: "https://img.freepik.com/premium-vector/ai-coding-robot-assistant-programming-code-debugging-vector-illustration-concept_694862-52.jpg?w=1800"
categories: ["Workflow", "Automation"]
tags: ["Hermes Agent", "cronjob", "workflow", "Hugo", "GitHub Pages"]
draft: false
---

I reconfigured Hermes Agent and my blog workflow in a pretty simple way: save the long-term rules first, lock the schedule next, handle thin-source weeks with topic generation, and keep publishing on a fixed Git flow.

![Concept illustration for Hermes Agent and a blog workflow](https://img.freepik.com/premium-vector/ai-coding-robot-assistant-programming-code-debugging-vector-illustration-concept_694862-52.jpg?w=1800)

## Save the long-term rules first

I started by teaching the agent a few durable preferences:

- respond quickly and keep things short
- write in a practical tone
- output Chinese, English, and Japanese versions
- adjust structure based on the topic instead of forcing a fixed template
- follow a consistent Git publishing flow

This matters because a single conversation is easy to forget. Once the preferences are stored, the workflow becomes much more stable.

## Then lock the schedule

Next, I attached a recurring schedule.

The current rhythm is every Tuesday, Thursday, and Saturday. Each run checks recent conversations, work updates, and interest notes. If there is enough material, it moves directly into drafting. If not, it first proposes topic candidates from current tech and geek areas.

That means the agent does not have to force a post when the source material is thin.

## When material is thin, generate topics instead of forcing a draft

This part matters most to me.

If the current material is not enough, I want the agent to look at topics like:

- AI
- GitHub
- Hugo
- automation
- geek tooling
- recent tech trends

But instead of writing the post for me, it should first present topic directions. That helps me decide:

- whether the topic is worth going deeper on
- what I actually think about it
- whether it deserves a full blog post

That is the real point of writing, at least for me.

## Keep publishing on a fixed Git flow

Once the draft is ready, I publish it through a fixed Git process:

1. sync main first
2. create a new branch
3. write the post on that branch
4. push the branch
5. open a PR

I want drafting and publishing to stay clearly separated. A draft should stay a draft, and publishing should follow the normal collaboration flow.

## What I verified

After the setup, I confirmed two things:

- Hermes Agent can work on a fixed cadence
- when the source material is thin, it helps me find a direction instead of forcing a finished post

That turns the blog workflow into something repeatable, not a one-off setup.
