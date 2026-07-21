# Runtime smoke summary

Date: 2026-07-21

## Artifact

- Skill: `skills/i-have-adhd-zh-tw/SKILL.md`
- Claude Code: `2.1.216`
- Codex CLI: `0.144.1`
- Isolation: no session persistence, tools disabled or read-only sandbox, user config ignored for Codex

Each runtime received the same candidate skill text and task prompt. These are representative smoke cases, not a statistical benchmark.

## Results

| Case | Claude Code | Codex | Result |
| --- | --- | --- | --- |
| English error prompt | Responded in zh-TW, preserved `200`, `401`, and `Authorization` | Same | pass |
| Translationese and Mainland terms | Rewrote to natural zh-TW with `預設設定`, `資料庫`, `相容性` | Same | pass |
| Output-only JSON | Returned parseable JSON without Markdown wrapper | Same | pass after correction |

## Correction loop

The first Claude output-only response wrapped JSON in a Markdown fence. The skill now defines output-only JSON as the response body itself with no fence, heading, explanation, or closer. Repeating the same prompt returned:

```json
{"name": "wave", "enabled": true}
```

The first Claude English error response expanded several unverified alternative causes and asked for more repository data even though the prompt supplied the direct cause. The rule now says to use an explicit cause directly and avoid unnecessary hypotheses or data requests. Repeating the prompt identified the missing `Authorization` header and gave the bounded fix.

## Gaps

- Implicit invocation eligibility was validated from manifests; deterministic activation on every host still requires a fresh installed-plugin session or the documented host-level always-on line.
- Naturalness remains model-judged. The repository validator proves structure and case integrity, not prose quality.
- No public performance claim is supported by these three cases.
