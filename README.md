<p align="center">
  <img src="./logo.png" alt="i-have-adhd-zh-tw" width="140" />
</p>
<p align="center">
  <strong>自然台灣繁中。答案先行。少一點廢話，多一點完成。</strong>
</p>

# i-have-adhd-zh-tw

給 Claude Code、Codex 與 Cursor 使用的公開 skill。它預設以自然的台灣繁體中文回覆，減少空泛開場、晶晶體、中國用語、重複摘要與不必要的客套結尾，同時保留正確性、安全性、必要細節與 agent autonomy。

這個 skill 適合希望資訊容易開始、快速掃讀、可以直接行動的人；使用它不代表，也不能證明任何人有 ADHD。

## 專案定位與上游

本專案是英文版 [I have ADHD](https://github.com/ayghri/i-have-adhd) 的非官方繁體中文衍生版本。原始英文版由 Ayoub Ghriss 建立；本專案只維護繁體中文版本所需的翻譯、台灣用語在地化、相容性調整與驗證。原始專案的設計與成果歸功於上游作者及其貢獻者。

本專案與上游作者沒有官方合作、授權代理或背書關係，也不以取代英文版或原作者成就為目的。上游變更只在人工審查後挑選，不會自動合併。

本專案由維護者免費提供，目前不收費，也不以此專案營利。這是維護者的專案立場，不是額外的授權限制；本專案仍依 MIT License 發布，使用者保有 MIT License 授予的權利，包括商業使用。

## 安裝

### Claude Code

```bash
claude plugin marketplace add panda850819/i-have-adhd-zh-tw
claude plugin install i-have-adhd-zh-tw@panda850819
```

### Codex

```bash
codex plugin marketplace add panda850819/i-have-adhd-zh-tw --ref main
codex plugin add i-have-adhd-zh-tw@panda850819
```

詳細安裝、更新與移除方式見 [INSTALL.md](./INSTALL.md)。

## 它會改變什麼

### 修改前

> 這是一個很好的問題。基於你目前所提供的資訊，我們可以針對登入流程的部分進行進一步的分析。首先，你可能需要檢查相關的配置，然後再考慮是否需要對代碼進行調整。希望這對你有幫助。

### 修改後

> 登入失敗是因為 request 沒有 `Authorization` header。已在 `src/auth.ts:42` 補上 header；`auth.spec.ts` 通過。

## 核心原則

1. 第一段直接給答案、完成結果或必要下一步。
2. 敘述使用台灣繁中；code、command、path、API 與錯誤訊息保持原樣。
3. 使用主動、自然的句子，刪除翻譯腔與空殼詞。
4. Agent 能安全完成的工作直接完成，不丟回給使用者。
5. 簡短不犧牲必要細節、安全、rollback 或明確 output contract。

完整規則見 [SKILL.md](./plugins/i-have-adhd-zh-tw/skills/i-have-adhd-zh-tw/SKILL.md)。

## 驗證

```bash
python3 scripts/check_repo.py
python3 -m unittest discover -s tests -v
```

案例涵蓋直接回答、agent autonomy、台灣用詞、晶晶體、technical literals、錯誤回報、安全確認、詳解、指定格式與日常對話。詳見 [evals/cases.jsonl](./evals/cases.jsonl) 與 [evals/rubric.md](./evals/rubric.md)。

## 授權與致謝

本專案 fork 自 [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)，沿用 [MIT License](./LICENSE)。`LICENSE` 完整保留原始著作權聲明 `Copyright (c) 2026 Ayoub Ghriss`；繁體中文版本的新增與修改由本專案維護者負責。

上游 README 另註明，其概念參考 J. Russell Ramsay 與 Anthony L. Rostain 的 *The Adult ADHD Tool Kit*，並將內容調整為適合 LLM 回覆的形式。本專案保留這項致謝；該書及其內容不包含在本 repo 的 MIT 授權範圍內。
