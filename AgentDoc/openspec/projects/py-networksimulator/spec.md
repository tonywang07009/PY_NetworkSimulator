# PY_NetworkSimulator 專案路由

| 欄位 | 值 |
|---|---|
| project_key | py-networksimulator |
| project_root | repository root |
| openspec_root | AgentDoc/openspec |
| spec_path | AgentDoc/openspec/projects/py-networksimulator/spec.md |
| toolbox_path | AgentDoc/openspec/projects/py-networksimulator/toolbox.md |
| wiki_root | AgentDoc/EvoSkill/wiki |

本表為專案明確路徑映射，不宣稱是 OpenSpec CLI 原生設定格式或已註冊全域 workflow。

任務以 OpenSpec change 的需求與驗收為準。開始先讀 PROGRESS/HANDOFF；無已核准的模擬器實作需求時，先對齊範圍，不自行選擇協定模型。

規範使用 `ReferDoc/Spec/spec_index.json` 查 domain/layer/keyword，TS/TR 原文作為技術依據。設計指南與 Wiki 為導覽及推論，不能取代規範。程式符號、呼叫關係由本專案 SymDex 索引查詢；一般文件以 rg 與直接閱讀查詢，無程式碼不建置空索引。索引缺漏或過期回到來源碼，不能從搜尋結果宣稱執行成功。


## 新版工作流與責任邊界（2026-10-18）

共用資源位於 `.agents/workflow-kit/`，完整教材副本在 `AgentDoc/WorkflowKit/`。
需求、設計、任務與驗收只有本 OpenSpec 一份權威；Issue 鏡像排程與進度，
架構／trace 是有來源的衍生視圖，Wiki 保留有證據的知識。

新 workflow 採一個 change／Issue／PR、人工 trace 後準備同 PR 歸檔與 README，
使用者手動 merge，核對實際合併後才算完成。每項行為完成先核對規格／程式／測試；
change 結束執行 code-review 與 ponytail-debt，具體架構摩擦才啟動架構整理。
合理延後事項依 workflow technical-debt 指引保存在本根目錄 tech_improve.md，
有實際事項才建立，不能取代正式驗收。詢問決策及人讀文件均遵循共用 output.md。

本輪只移植已核准的工作流，沒有建立模擬器需求、change、Wiki、改善候選或個人
workflow 計數；也沒有授權遠端發布或替使用者合併。後續首次實證再確認功能範圍。
