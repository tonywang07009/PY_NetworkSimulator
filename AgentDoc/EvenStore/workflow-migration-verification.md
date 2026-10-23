# 新版工作流移植驗證

日期：2026-10-18。範圍：把 Agent_workflow 目前配送版本完整移入 PY_NetworkSimulator，
保留專案 OpenSpec、EvoSkill、Archify、既有 Git 修改及工具設定。

| 檢查 | 本輪結果 |
|---|---|
| 原始套件 | 移植前 verify.py 通過，52 項測試通過 |
| 完整教材副本 | 依 SHA256SUMS 複製 140 個檔案，另保留原始 SHA256SUMS；移植後 verify.py 通過 |
| 副本測試 | 在 AgentDoc/WorkflowKit 執行 52 項測試，全部通過；安裝與狀態測試使用暫存根目錄 |
| 已部署檔案 | 225 個計畫內檔案 hash 一致，其中 202 個新增／更新；備份已核對 |
| 技能探索布局 | 18 個新版技能加保留的 Archify，共 19 個帶 SKILL.md 的入口；不代表本會話已重新載入每個技能 |
| 路徑適配 | 兩個 EvoSkill 技能保持原位／符號連結，跨技能 Markdown 連結依實體路徑適配 |
| Markdown | 99 個 active kit 本機連結可解析；檢查採實體路徑，未把程式範例當成實際檔案 |
| 保留內容 | README、LICENSE、既有 Archify、OpenSpec config、工具盤點與歷史證據共 164 個檔案 hash 不變；4 個既有入口／探索符號連結保留 |
| OpenSpec | 專案根目錄執行 OPENSPEC_TELEMETRY=0 openspec list --json，回傳 changes 空清單 |
| Git | rtk git diff --check 通過；既有 README／LICENSE 修改仍在，沒有 commit/push |
| 根目錄 AGENTS | 保留 AGENTS.md → agent.md，只增加 /AGENTS.md ignore；規則寫入 agent.md |
| 專案 MCP | filesystem 實際 allowed-root 呼叫指向本專案，SymDex 實際 list_repos 回傳空清單且 registry 位於本專案 |
| 離線課程 | 目標路徑執行瀏覽器 smoke：8 對話框、16 節點、導航／參考連結、focus/search/theme/export、桌面／手機寬度與無 runtime exception 通過 |
| 畫面檢視 | 移植後手機訪談對話框已實際檢視；長內容需垂直捲動，未宣稱量測認知負荷 |

備份：`/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/EvenStore/workflow-backups/20261018T140035Z`。
逐檔 before/after、布局對應與原始呼叫結果見 [移植紀錄](workflow-migration-2026-10-18.json)。
新舊版來源可由完整套件 PROVENANCE.json／SHA256SUMS 比對，歷史搬移 hash 保留原樣。
瀏覽器截圖位於 /tmp/py-networksimulator-workflow-course-preview，屬本機暫存證據。

## 使用與後續升級

日常使用見 [WORKFLOW_GUIDE.md](../WORKFLOW_GUIDE.md)。下一輪可探索新版技能；
若長會話已載入舊內容，開新會話並讓 Agent 讀專案入口。
本專案使用 EvoSkill 路徑對應布局；project-installation.json 記錄部署 hash，
不是標準 installation.json。標準升級器預期拒絕現有 skill 符號連結，不能強行
刪除連結。後續升級須先在暫存根目錄展開新版，比對這份紀錄與本地修改後移植。

AgentDoc、ReferDoc 與 .agents 繼續被原有 Git ignore 排除，需要移機時另外備份；
本輪未決定把這些內容納入公開 repository，也未改變全域 MCP／外部工具／模型設定。
沒有建立 interview、Wiki、改善候選、個人 workflow 註冊或模擬器 change。
首次功能範圍等待使用者實際需求，不需回答之前暫停的候選功能問題。

這些結果證明檔案交付、路徑、套件測試與課程操作；尚未驗證新流程對實際模擬器
開發、規格語意核對、人工 trace、Issue／PR 交付、Luna 寫作與訪談學習的成效。
沒有對本專案執行 macOS／Windows 安裝、遠端 CI、實際符號／呼叫查詢或模擬行為測試。
