---
slug: i-have-adhd-zh-tw
brief: docs/briefs/2026-07-21-i-have-adhd-zh-tw.md
---

# i-have-adhd-zh-tw plan

## Tasks

### T1: Establish independent plugin identity

- scope: manifests, skill directory, inherited workflows
- acceptance: `jq -e '.name == "i-have-adhd-zh-tw"' .agents/plugins/marketplace.json .claude-plugin/plugin.json .codex-plugin/plugin.json && test -f skills/i-have-adhd-zh-tw/SKILL.md && test ! -f skills/i-have-adhd/SKILL.md`
- depends-on: none
- status: todo

### T2: Author native Taiwan Traditional Chinese behavior

- scope: `skills/i-have-adhd-zh-tw/SKILL.md`
- acceptance: `rg -n '每一則回覆|台灣繁體中文|不把 agent 的工作丟回給使用者|發送前檢查' skills/i-have-adhd-zh-tw/SKILL.md`
- depends-on: T1
- status: todo

### T3: Publish localized documentation

- scope: `README.md`, `INSTALL.md`, attribution and upstream policy
- acceptance: `rg -n 'panda850819/i-have-adhd-zh-tw|ayghri/i-have-adhd|自動套用' README.md INSTALL.md`
- depends-on: T1, T2
- status: todo

### T4: Add evaluation corpus and validation

- scope: `evals/`, `scripts/`, `tests/`, validation workflow
- acceptance: `python3 -m unittest discover -s tests -v`
- depends-on: T1, T2
- status: todo

### T5: Verify representative runtime behavior

- scope: Claude Code and Codex read-only smoke cases
- acceptance: `test -f evals/results/smoke-summary.md`
- depends-on: T3, T4
- status: todo
