---
slug: i-have-adhd-zh-tw
brief: docs/briefs/2026-07-21-i-have-adhd-zh-tw.md
---

# i-have-adhd-zh-tw plan

## Tasks

### T1: Establish independent Skill identity

- scope: standard Skill directory and inherited workflows
- acceptance: `test -f skills/i-have-adhd-zh-tw/SKILL.md && test ! -e .claude-plugin && test ! -e plugins/i-have-adhd-zh-tw`
- depends-on: none
- status: done

### T2: Author native Taiwan Traditional Chinese behavior

- scope: `skills/i-have-adhd-zh-tw/SKILL.md`
- acceptance: `rg -n '每一則回覆|台灣繁體中文|不把 agent 的工作丟回給使用者|發送前檢查' skills/i-have-adhd-zh-tw/SKILL.md`
- depends-on: T1
- status: done

### T3: Publish localized documentation

- scope: `README.md`, `INSTALL.md`, attribution and upstream policy
- acceptance: `rg -n 'npx skills add|ayghri/i-have-adhd|持續套用' README.md INSTALL.md`
- depends-on: T1, T2
- status: done

### T4: Add evaluation corpus and validation

- scope: `evals/`, `scripts/`, `tests/`, validation workflow
- acceptance: `python3 -m unittest discover -s tests -v`
- depends-on: T1, T2
- status: done

### T5: Verify standard Skill discovery

- scope: `npx skills` read-only discovery and representative cross-agent smoke cases
- acceptance: `npx --yes skills add . --list | grep -q i-have-adhd-zh-tw && test -f evals/results/smoke-summary.md`
- depends-on: T3, T4
- status: done
