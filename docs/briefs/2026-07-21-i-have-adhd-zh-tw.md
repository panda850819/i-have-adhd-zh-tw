# i-have-adhd-zh-tw

## Problem

Claude Code、Codex 與 Cursor 常用空泛開場、翻譯腔、中國用語、重複摘要與客套結尾。原始 `i-have-adhd` 能減少部分廢話，但英文中心的規則會要求使用者執行 agent 能完成的工作，並可能用固定估時或重述狀態增加雜訊。

## Premise

- Original: translate `i-have-adhd` into Traditional Chinese.
- Revised: maintain a public, always-on Taiwan Traditional Chinese response-quality skill with observable evaluation cases.
- Still load-bearing: answer-first structure, low start friction, bounded steps, visible progress.

## Alternatives

### Add: direct localization

保留上游 plugin structure，改寫全部 identity、規則與公開文件。

### Add: native zh-TW rules plus regression cases

用台灣繁中情境重新撰寫規則，加入 deterministic validation 與 model-judged cases。

### Reject: English skill plus zh-TW overlay

兩層規則增加 cold-start context，衝突時也難以判斷生效來源。

## Chosen approach

合併前兩項：保留可辨識的上游結構，但以原生台灣繁中重寫核心規則；用小型 eval corpus 驗證實際目標。

Executable plan: `docs/plans/i-have-adhd-zh-tw.md`.

## Scope

In:

- `i-have-adhd-zh-tw` plugin and skill identity;
- always-on implicit invocation metadata;
- natural Taiwan Traditional Chinese rules;
- Claude Code, Codex, and Cursor install documentation;
- evaluation cases, rubric, validator, tests, and read-only CI.

Out:

- Panda-specific instructions;
- automatic upstream merges;
- alias under `i-have-adhd`;
- paid or provider-coupled live evaluation runner.

## Seams

- Plugin manifests and skill directory naming.
- Skill frontmatter and implicit invocation policy.
- Repository validator and CI.
- Representative Claude Code and Codex smoke responses.

## Next skill

Recommended: `sprint` because requirements and acceptance checks are concrete and the work must ship through a PR.

## Gotchas

- Implicit invocation eligibility does not guarantee deterministic activation in every host.
- Term checks must not rewrite code, quotes, logs, paths, or formal product names.
- Concision must not remove safety, correctness, rollback information, or requested detail.

## OPEN_QUESTIONS

- None.
