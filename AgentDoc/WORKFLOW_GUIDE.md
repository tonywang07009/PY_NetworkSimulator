# 本專案新版工作流使用方式

新版已接入此專案。後續直接在專案根目錄開始工作；例如：

```text
$workflow
我想實作：<這次要改善的問題或行為>。
請先讀 AgentDoc/openspec 的進度與交接，沿用已確認內容，先與我對齊範圍。
```

| 想找的內容 | 本專案位置 |
|---|---|
| 自動入口／現況 | ../agent.md、openspec/PROGRESS.md、openspec/HANDOFF.md |
| 實際工具路由 | openspec/projects/py-networksimulator/toolbox.md |
| 寫作與選項式詢問 | ../.agents/workflow-kit/docs/output.md |
| 初次提示詞 | ../.agents/workflow-kit/初次下提示詞模板.txt |
| 訪談與文件管理 | ../.agents/workflow-kit/docs/說明.md |
| 完整離線課程 | WorkflowKit/index.html |
| 安裝／恢復 | ../.agents/workflow-kit/PROJECT-INSTALL.md |
| 來源、校驗與備份位置 | EvenStore/workflow-migration-2026-10-18.json |

先前的功能選擇問題暫停，無須現在回答。本輪不替您選模擬協定或新增功能。
新的 skill 定義在下一輪互動可供探索；若既有長會話仍使用已載入的舊版內容，
請開新會話並在本專案啟動，確認 Agent 讀取本機入口。

每次新需求先訪談，確認後才進 OpenSpec；每項行為完成核對需求、程式及測試。
change 結束執行 code-review／ponytail-debt，更新完整架構與絕對路徑 tree 導讀，
交人工 trace。接受並修正後，同一 PR 交付程式、規格、README 與歸檔，
您手動合併，Agent 核對實際 merge 才計完成。發布、commit/push 沿用明確授權。

請回報具體情境，例如「問了已回答的問題」「trace 找不到實際檔案」或
「PR 某段看不出修改原因」，附對應輸出／路徑即可；暫不新增評分服務。
實際訪談才建立 interview/，有真實延後事項才建立 tech_improve.md，
結案時才做授權的 Wiki capture／assessment，不預建空成果。

AgentDoc、ReferDoc 與 .agents 目前被既有 Git ignore 排除。移機時須另外備份；
本輪沒有修改此版本控管選擇，也沒有改動全域 MCP、外部工具或模型設定。
