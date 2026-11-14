# Agent working style

Maintainer directive (2026-11-14): keep driving the work until everything is
done or you are genuinely blocked on the maintainer. Do not end a turn with a
"next steps — want me to…?" summary when the next step is something you can do
yourself.

- After finishing a step, start the next one immediately.
- Stop only for decisions that are genuinely the maintainer's: product choices,
  credentials and secrets, account ownership, and human-only UI actions
  (registrar, Cloudflare, GitHub App creation, analytics/search-console
  accounts).
- When blocked, batch every open blocker into one clear ask, with a recommended
  option for each, and keep doing any unblocked work in the meantime.
- PRs merge automatically on green per [pr-process.md](pr-process.md); merging
  is not a reason to stop and ask.
- Durable guidance goes in `AGENTS.md` / `.ai/`, never in per-session agent
  memory (a hook enforces this).
