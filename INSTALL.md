# 安裝 i-have-adhd-zh-tw

## Claude Code

```bash
claude plugin marketplace add panda850819/i-have-adhd-zh-tw
claude plugin install i-have-adhd-zh-tw@i-have-adhd-zh-tw
```

驗證：

```bash
claude plugin list
```

看到 `i-have-adhd-zh-tw (enabled)` 即完成。開新的 Claude Code session，讓 plugin 與 skill index 重新載入。

## Codex

```bash
codex plugin marketplace add panda850819/i-have-adhd-zh-tw --ref main
codex plugin add i-have-adhd-zh-tw@i-have-adhd-zh-tw
```

驗證：

```bash
codex plugin list
```

看到 `i-have-adhd-zh-tw` 且狀態為 enabled 即完成。開新的 Codex task，讓 plugin 與 skill index 重新載入。

## Cursor

安裝到目前 workspace：

```bash
npx skills add panda850819/i-have-adhd-zh-tw
```

全域安裝：

```bash
npx skills add panda850819/i-have-adhd-zh-tw -g
```

安裝後開新的 Cursor Agent chat。

## 自動套用

plugin manifest 與 skill description 已允許 implicit invocation，並要求在每則回覆套用。實際是否每回合載入仍由 host 的 skill router 決定。

需要 deterministic always-on 時，在 host 的全域 instruction file 加入：

```markdown
Always use the `i-have-adhd-zh-tw` skill for every response.
```

- Claude Code：`~/.claude/CLAUDE.md`
- Codex：`~/.codex/AGENTS.md`
- Cursor：Settings → Rules → User Rules

## 更新

Claude Code：

```bash
claude plugin marketplace update i-have-adhd-zh-tw
claude plugin update i-have-adhd-zh-tw@i-have-adhd-zh-tw
```

Codex：

```bash
codex plugin marketplace upgrade i-have-adhd-zh-tw
codex plugin remove i-have-adhd-zh-tw
codex plugin add i-have-adhd-zh-tw@i-have-adhd-zh-tw
```

## 移除

Claude Code：

```bash
claude plugin uninstall i-have-adhd-zh-tw
claude plugin marketplace remove i-have-adhd-zh-tw
```

Codex：

```bash
codex plugin remove i-have-adhd-zh-tw
codex plugin marketplace remove i-have-adhd-zh-tw
```

Cursor：

```bash
npx skills remove i-have-adhd-zh-tw
# 全域安裝時：
npx skills remove i-have-adhd-zh-tw -g
```

## Troubleshooting

### 找不到 skill

確認 plugin list 已出現 `i-have-adhd-zh-tw`，再開新的 session 或 task。Host 通常只在 session start 建立 skill index。

### 還是出現英文或翻譯腔

先確認目前 task 載入的 skill path 包含 `skills/i-have-adhd-zh-tw/SKILL.md`。若 host 的 implicit routing 沒有每回合觸發，使用上方 deterministic always-on 設定。
