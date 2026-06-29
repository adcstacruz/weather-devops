# Workflow & Traceability

The rule for this repo: **no change without a tracked work item.** Every commit traces back to an issue, the way an agile team keeps work auditable. This is the loop you follow for all 13 modules.

```
issue  →  branch  →  commits  →  PR  →  merge  →  issue auto-closes
 #12      feat/12     refs #12    Closes #12         board → Done
```

> Module 0 sets up the *conventions* below (manually). Module 2 adds the *automation* (auto-close, board moves). Until then, you close issues by hand.

---

## 1. Issues

Every unit of work starts as a GitHub Issue. Keep them small — one issue ≈ one PR. Use labels to categorize (`module-0`, `feat`, `chore`, `bug`).

A loose mapping for this project: each module is an **epic**, and the steps inside it become individual issues.

## 2. Branch naming

`<type>/<issue-number>-<short-slug>`

Examples:
- `feat/12-add-redis-cache`
- `fix/18-handle-upstream-timeout`
- `chore/4-add-pre-commit`

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`.

Branch off `main`, one branch per issue. (Trunk-based: short-lived branches, merge often.)

## 3. Commit messages — Conventional Commits

```
<type>(<optional scope>): <summary>

<optional body>

refs #<issue>
```

Examples:
- `feat(cache): add Redis cache-aside layer\n\nrefs #12`
- `fix(adapter): apply timeout to upstream call\n\nrefs #18`

Why: a consistent, machine-readable history that later enables auto-generated changelogs and makes `git log` actually useful. `refs #12` links the commit to its issue in GitHub.

## 4. Pull requests

- Open a PR from your branch into `main`.
- The PR description **must** include a closing keyword: `Closes #12` (or `Fixes #12`). This is what auto-closes the issue on merge.
- CI must be green before merge (enforced from Module 2 onward).
- Use the PR template (added in Module 0) so the issue link is never forgotten.

## 5. Project board

A GitHub Projects board with columns: **Todo → In progress → Done.**
- Module 0: create it, move cards by hand.
- Module 2: Actions move cards automatically as issues open / PRs open / PRs merge.

## 6. Closing keywords reference

In a PR body or a commit on the default branch, any of these auto-close the linked issue on merge:
`close / closes / closed / fix / fixes / fixed / resolve / resolves / resolved #<n>`

Use `refs #<n>` (no keyword) when you want to *link* without closing — e.g. a commit that's part of a larger issue.

---

## Quick reference card

| Step | Command / action |
|------|------------------|
| Start work | Create issue → note its number `#N` |
| Branch | `git switch -c feat/N-short-slug` |
| Commit | `git commit -m "feat(scope): summary" -m "refs #N"` |
| Push | `git push -u origin feat/N-short-slug` |
| PR | Open PR into `main`, body includes `Closes #N` |
| Merge | Squash-merge once CI is green → issue auto-closes |
