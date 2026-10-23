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
