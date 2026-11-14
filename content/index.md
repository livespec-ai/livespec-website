---
title: "livespec: spec <-> impl, in a living feedback loop"
description: "livespec is an experimental \"dark\" software factory by Chad Woolley: a living specification in a feedback loop with its implementation, quality dials turned toward 11, and minimal human attention."
---

# What is livespec?

<div class="prose">

livespec is a **"dark" software factory**: AI agents turn a living, natural-language specification into a working implementation, with as little human involvement as possible. The lights are off because nobody needs to be on the factory floor. It's an **experimental work in progress**.

For the genesis of some of the ideas behind it, see my February 2026 article [The Software Factory: A Practitioner's Guide](https://thewoolleyweb.com/software-factory-practitioners-guide.html), which explores the earliest iterations of the "dark factory" approach.

</div>

# Blog

## [Read the blog](blog/index.html)

<p class="caption">The journey toward the goals below.</p>

# Goals

<div class="prose">

livespec explores three goals:

## 1. A circular feedback loop between specification and implementation {#feedback-loop}

A living, natural-language specification ("intent") drives the implementation (through identified "gaps" where the implementation does not match the specification). What building and running the implementation reveals (doesn't work, doesn't perform, isn't what we wanted) flows back into the specification through a governed revision process (identifying "drift" and "proposing changes" to the specification), so the two stay in sync in live, real-time.

The goal is a "living specification". Hence the name: "livespec".

## 2. Every quality dial turned as close to 11 as possible {#quality-dials}

Fast, cheap, right: the old triangle says pick two. livespec asks how far "right" can be pushed: Test-First development, code quality metrics, strict and detailed architecture standards, evals, definition-and-proof-of-done, code coverage, linting, fuzzing, mutation testing, etc, etc... All of these enforced as much as possible by mechanical, non-LLM mechanisms.  While balancing these goals against cost and speed constraints (token and infrastructure costs).

## 3. By relying on the previous goals, find the *minimal human attention* the factory needs {#minimal-attention}

How little human attention can the factory get while still producing usable, high-quality implementations? The goal is to:

- Interface primarily with AI surfaces.
- Rarely, if ever, directly review code
- Leverage AI as much as possible for authoring and review of the specification.
- Primarily rely on review of the delivered, working implementation.
- Rely on observability signals from every part of the factory and the implementation for guidance.

</div>

# Where things stand, and what I've learned

<div class="prose">

DISCLAIMER: As a result of following the goals above, the repos linked below consist of millions of lines of code and documentation. As of November 2026, about 3.2 million lines, and 5.5 total lines modified. 99.9% (repeating) of these lines I have *NEVER LOOKED AT ONCE*.

My primary activity has been dogfooding the building of the factory itself, and all of the distributed (kubernetes/gitops) infrastructure to run it, plus a few small "real" projects.

In the pursuit of Goal 3 above (minimal attention), I've gone through several different iterations of "AI management layers", as I've tried to zero in on approaches which:

- A) Keep working constantly, don't stall, and raise ONLY the right things for my attention
- B) Actually produce working implementations, without spinning and thrashing and yak-shaving and burning tokens forever with nothing to show for it

Hence the plethora of "supervisors", "overseers", "coordinators", "consoles", "cockpits", etc., scattered across the repos below.

I've also explored how to automate the enforcement of Goal 1. For example, requiring Gherkin Use-Case "GIVEN-WHEN-THEN" style scenarios in the specification for all new features (example from the livespec's own [SPECIFICATION/scenarios.md](https://github.com/thewoolleyman/livespec/blob/master/SPECIFICATION/scenarios.md)). Then I mechanically require that each scenario have at least one associated E2E top-of-the-testing-pyramid test, and require that all work items have Definition-of-Done requirements, which are in turn required to be anchored to a scenario in the specification.

However, as the system has grown and I've invested most heavily in Goals 2 and 3, and automation of Goal 1, the "cheap" and "fast" sides of the triangle suffered greatly as they tried to maintain the hard-enforced "right" quality standard, with minimal attention. I have also leaned into 

This, in turn has forced me to divert attention the from Goal 1 in an attempt to stop the spend from spiraling out of control into the 4-figures-plus-monthly $USD range on tokens and infra (now at well over a dozen machines running kubernetes worker nodes across the cloud and my homelab).

Which is, in itself, a very useful learning outcome from the experiment: This endeavour is *EXPENSIVE* and *RESOURCE INTENSIVE*.

If I had to summarize what I've learned in a sentence: The LLMs are getting better, very fast, but for the foreseeable future, they are polymath geniuses who have the memories of a fruit fly and are incapable of seeing the forest for the trees.

</div>

# Links and stuff

## [The specification](https://github.com/thewoolleyman/livespec/blob/master/SPECIFICATION/spec.md)

<p class="caption">livespec's own living spec, governed by livespec. There's several diagrams here, if you want visuals of how the system works (again, mostly unreviewed after initial generation, and probably badly rotted)</p>

## [Activity](https://github.com/thewoolleyman/livespec/blob/master/docs/activity/livespec-governed-repo-activity.md)

<p class="caption">Pull requests and lines changed across every livespec-governed repository.</p>

## [livespec core](https://github.com/thewoolleyman/livespec)

<p class="caption">The README: what livespec is, the spec/implementation lifecycle, and the operations.</p>

## [Installation](https://github.com/thewoolleyman/livespec/blob/master/docs/installation.md)

<p class="caption">One paste-able agent prompt that sets livespec up on a project. It kind of works, but several bugs in the backlog for it. ;)</p>

## [Drivers](https://github.com/thewoolleyman/livespec-driver-claude)

<p class="caption">Per-agent bindings for LLM harnesses: <a href="https://github.com/thewoolleyman/livespec-driver-claude">Claude Code</a>, <a href="https://github.com/thewoolleyman/livespec-driver-codex">Codex</a>, and <a href="https://github.com/thewoolleyman/livespec-driver-pi">pi</a>.</p>

## [Orchestrators](https://github.com/thewoolleyman/livespec-orchestrator-beads-fabro)

<p class="caption">Implementation-side work tracking: <a href="https://github.com/thewoolleyman/livespec-orchestrator-beads-fabro">Beads/Dolt + Fabro</a>, or zero-infrastructure <a href="https://github.com/thewoolleyman/livespec-orchestrator-git-jsonl">git + JSONL</a> (the git/JSONL is an incomplete reference implementation, not practical for actual factory work at scale. The main learning here is that you DO NOT WANT TO STORE YOUR TASK ACTIVITY LEDGER IN GIT).</p>

## [Supporting tools](https://github.com/thewoolleyman/livespec-dev-tooling)

<p class="caption"><a href="https://github.com/thewoolleyman/livespec-dev-tooling">dev-tooling</a>, <a href="https://github.com/thewoolleyman/livespec-runtime">runtime</a>, <a href="https://github.com/thewoolleyman/livespec-console-beads-fabro">console</a>, and <a href="https://github.com/thewoolleyman/livespec-overseer">overseer</a>.</p>

## [This website's spec](https://github.com/livespec-ai/livespec-website/tree/main/SPECIFICATION)

<p class="caption">This site is governed by livespec too.</p>

# Who is responsible for this?

<div class="prose">

I'm Chad Woolley. Bio blurb from my LinkedIn: Ex-GitLab, Ex-Pivotal, Ex-IBM, Open Source. Coder/hacker/sysadmin/ops for 40+ years. Apple II → mainframes → web developer since the web came out → agentic AI → ??? 🤔😳

After getting laid off at GitLab in June 2026 (the fourth "involuntary departure" of my career), I decided to take a hiatus to retool my knowledge and skills at the dawn of the Age of AI, and explore the limits of what is possible. livespec is the vehicle I chose.

I spent 4 decades learning to use my hands to efficiently craft beautiful and high-quality code and documentation, and I probably wrote around a half-million lines of it with those hands (and often, with a pair-programmer).

But now, that skill is as marketable as a wagon-wheelwright in the age of automobiles. However, I still have decades of valuable knowledge from my myriad failures, and I've learned from countless brilliant humans how to see the forest for the trees.

This makes me confident that I can find a way in this brave new world. I, for one, welcome my idiot savant robot overlords...

There's more about me at [thewoolleyweb.com](https://thewoolleyweb.com/).

</div>
