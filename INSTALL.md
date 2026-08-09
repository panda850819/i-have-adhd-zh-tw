# 安裝 i-have-adhd-zh-tw

本專案使用標準 Agent Skill 格式，以 [`skills`](https://skills.sh/) CLI 安裝，不需要 Claude、Codex 或其他 host 的 plugin marketplace。

## 安裝

安裝到目前專案：

```bash
npx skills add panda850819/i-have-adhd-zh-tw
```

全域安裝：

```bash
npx skills add panda850819/i-have-adhd-zh-tw -g
```

要略過互動選單並安裝到 CLI 偵測到的所有 agents：

```bash
npx skills add panda850819/i-have-adhd-zh-tw --all
```

安裝後開新的 agent session，讓 host 重新載入 skill index。

## 驗證

先確認 repository 能被辨識：

```bash
npx skills add panda850819/i-have-adhd-zh-tw --list
```

輸出應包含：

```text
i-have-adhd-zh-tw
```

再查看目前專案已安裝的 Skills：

```bash
npx skills list
```

全域安裝則使用：

```bash
npx skills list -g
```

## 持續套用

Skill description 會要求 agent 在每則回覆套用規則，但實際載入時機仍由 host 的 skill router 決定。需要 deterministic always-on 時，在 host 的 instruction file 加入：

```markdown
Always use the `i-have-adhd-zh-tw` skill for every response.
```

常見位置：

- Claude Code：`~/.claude/CLAUDE.md`
- Codex：`~/.codex/AGENTS.md`
- Cursor：Settings → Rules → User Rules
- 其他 agents：使用該 host 的全域 instruction file

## 用 Skill 簡化 AGENTS.md

不要把語言、格式、答案先行與 agent autonomy 規則整段複製到每個 repo 的 `AGENTS.md`。完整規則由這個 Skill 集中維護；專案只需保留上面的一行啟用指令。

多個 repo 可以共用同一套規則。更新回覆風格時只需更新 Skill，不必逐一修改每份 `AGENTS.md`。若 host 的 SessionStart 或 persistent mode 能保證每個 session 載入 Skill，這一行也可以省略。

## 更新

更新目前專案安裝的 Skill：

```bash
npx skills update i-have-adhd-zh-tw
```

更新全域安裝：

```bash
npx skills update i-have-adhd-zh-tw -g
```

## 移除

移除目前專案安裝：

```bash
npx skills remove i-have-adhd-zh-tw
```

移除全域安裝：

```bash
npx skills remove i-have-adhd-zh-tw -g
```

## Troubleshooting

### 找不到 Skill

執行：

```bash
npx skills add panda850819/i-have-adhd-zh-tw --list
```

若清單包含 `i-have-adhd-zh-tw`，重新安裝並開啟新的 agent session。Host 通常只在 session start 建立 skill index。

### 沒有持續套用

確認目前 task 載入的 skill path 指向 `skills/i-have-adhd-zh-tw/SKILL.md`。若 host 的 implicit routing 沒有每回合觸發，加入「持續套用」段落中的一行 instruction。
