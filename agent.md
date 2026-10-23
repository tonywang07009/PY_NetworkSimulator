# 專案 Agent 入口

每次開始任務前，必須先前往 `AgentDoc/openspec/`，閱讀 `PROGRESS.md` 與 `HANDOFF.md`，確認任務進度、交接內容及尚未完成項目，再開始工作。

- 若已有進行中的 change，接著閱讀其 proposal、design、specs 與 tasks；執行 `OPENSPEC_TELEMETRY=0 openspec list --json` 確認現況。
- 本專案 OpenSpec 唯一實體位置是 `AgentDoc/openspec/`；根目錄 `openspec` 僅為 CLI 探索用符號連結。從專案根目錄執行 OpenSpec CLI。
- 專案路由與工具：`AgentDoc/openspec/projects/py-networksimulator/spec.md`、`toolbox.md`。
- 知識與技能位置：`AgentDoc/EvoSkill/README.md`。不得將候選技能放入 `.agents/skills` 自動啟用。
- 規範查詢入口：`ReferDoc/Spec/spec_index.json`；先查索引，再讀指定 TS/TR 原文。研究假設不可寫成 3GPP 既定規範。
- 結束任務時更新進度與交接；區分已完成、已驗證、待驗證與阻塞。缺少證據的技術主張標記 `[Needs Verification]`。
- 保留無關工作與既有 Git 修改；未經明確指示不 commit、push 或發佈。

`AGENTS.md` 連結至本檔，供 Codex 自動載入；本檔不取代上層適用規則。


## 新版工作流（2026-10-18 移植）

- 開始或接續開發使用 `$workflow`；新需求以 `$grill-with-docs` 訪談，沿用已確認答案。
- 共用輸出規範是 `.agents/workflow-kit/docs/output.md`：決策問題、選項與人讀文件均適用。預設繁體中文，保留程式、命令及原始證據。
- 新流程每個 change 對應一個 Issue 與一份 PR；先對齊需求及 OpenSpec，再追蹤進度。遠端發布、commit/push 仍依明確授權；使用者手動合併，核對實際 merge 才算完成並開始下一個 change。
- 實作使用 TDD、Ponytail 與既有設計規範；每項可驗證行為完成後核對 OpenSpec、實作／呼叫端與測試。範圍內缺陷直接修正並複驗。
- 程式閱讀格式：相鄰且獨立的 `if` 驗證區塊之間保留一個空行，適用於 Notebook、`.py` 與導讀範例；保留原縮排及 `if/elif/else` 分支關係。
- change 審查執行 code-review 與 ponytail-debt。合理延後事項在 `AgentDoc/openspec/tech_improve.md` 保留穩定 TI 編號、原因、影響、證據與何時需要重新評估；有實際事項才建立，驗收缺陷不能以登記代替修正。
- 訪談開始時才建立／沿用 `interview/`；六面向、每面向最多 10 題、每次一題，提供實例、選項與選填備註。未決事項在依賴的實作前詢問。
- 討論後依 Archify 產生整體／change 架構；人工 trace 前更新完整圖與 tree 式 `code-trace.md`，列每個實作檔絕對／相對路徑、需求與測試對照。人工接受並修正後，程式、規格、README 與歸檔放在同一 PR。
- 專案結案原位整理索引、摘要、連結及訪談學習，交 llm-wiki／skill-evolution；候選保持隔離，啟用仍需指定版本授權。CLM 留作未來待辦，Jev/TypeSafe 不採用。
- 安裝與恢復先讀 `.agents/workflow-kit/docs/install.md` 及 `PROJECT-INSTALL.md`；專案設定優先，新增使用者／系統層級變更先列具體差異確認。維持選定模型與 effort。
- `AgentDoc/WorkflowKit/` 是完整教材與來源副本，其 management 範本與歷史 course/sources 不是本專案活動規則；本專案進度、需求及路由仍以本檔指定的 OpenSpec 為準。
