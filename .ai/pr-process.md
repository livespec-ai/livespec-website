# PR process

Every tracked change lands through a pull request against `main` from a
dedicated worktree branch (see `AGENTS.md` §"Repository mutations").

## Merge automatically when CI passes

Maintainer directive (2026-11-14): merge a PR **automatically, without asking
the maintainer**, once its CI checks pass. Do not stop at "PR opened" and wait
for approval.

1. Push the branch and open the PR with `gh pr create --base main`.
2. Wait for the PR's checks to finish: `gh pr checks <number> --watch`.
3. When every check is green, merge with a rebase and delete the branch:
   `gh pr merge <number> --rebase --delete-branch`.
4. If any check fails, do NOT merge. Fix the cause on the branch, push, and
   repeat from step 2. Never bypass, skip, or weaken a check to get a merge.

GitHub's repository-level auto-merge setting is off and `main` has no branch
protection, so `gh pr merge --auto` is not available; the agent performs the
wait-then-merge itself.

## Until CI exists

The repository has no CI workflow yet. Until one exists, a PR with no checks
counts as passing once the local gates have passed (the lefthook `pre-commit`
and `pre-push` hooks, and `mise exec -- just check` once that recipe exists).
Merge it per step 3. When a CI workflow is added, its checks become the gate
and this section no longer applies.

## After merge

- Refresh the primary checkout: `git -C <primary-checkout> pull --ff-only`.
- Remove the merged worktree and its local branch.
- For changes under `site/`, carry the change through verified live
  publication per `SPECIFICATION/spec.md` §"Definition of Done" (after-merge
  part) once the site exists.

## Exceptions — ask before merging

- A PR that would merge with a merge conflict or that needs a force-push to
  `main`.
- A PR the maintainer has said to hold, or one marked draft.
