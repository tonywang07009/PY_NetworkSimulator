# IAB 拓撲交付與歸檔準備

## 目前狀態

- 本機分支：`feat/iab-topology`，尚未 commit／push。
- 主規格已同步，中文／英文產品說明與 Notebook 列點說明沿用使用者接受內容。
- 本 change 仍位於 `AgentDoc/openspec/changes/add-iab-topology-notebook/`，尚未實際歸檔。
- 預計目的地：`AgentDoc/openspec/changes/archive/2026-10-23-add-iab-topology-notebook/`。這是計畫位置，不是已存在的歸檔證據；若實際執行日期不同，依當日日期重新計算。

## 已備妥

| 項目 | 來源 |
|---|---|
| 已接受的功能及拒絕規則 | 主規格 `AgentDoc/openspec/specs/iab-topology/spec.md` |
| 來源碼與測試 | `src/iab/`、`tests/iab/` |
| Notebook 與輸出 | `notebooks/01_iab_topology.ipynb`、`notebooks/artifacts/iab-topology/` |
| 使用說明 | `ReferDoc/Implementation/IABTopology/README.md` 與 `README.en.md` |
| 驗證／審查／導讀 | 本目錄的 `extraction-validation.md`、`review.md`、`code-trace.md` |
| 發布文字 | 本目錄的 `issue-draft.md`、`pr-draft.md` |

## 移動前仍需完成

- 建立本 change 的實際 Issue 並記錄對應 URL；不得以草稿或假 URL 取代。
- 核對 tasks 中未完成的交付／合併項目，遵循 archive skill 的任務檢查；沒有將未完成事項勾成完成。
- 核對實際日期與目的地，確認沒有同名歸檔。
- 移動時同步修正根 README、Notebook、導讀、架構候選與收據、workflow 索引的可用路徑；保留歷史原始命令，不將舊紀錄改寫成新執行結果。
- 移動後重新檢查連結、來源指紋與所有目前可執行命令。

## 發布範圍與 Git 忽略規則

- 現有 `.gitignore` 忽略整個 `ReferDoc/` 與 `AgentDoc/`；本輪保留該設定。
- 發布時只納入此模組說明、主規格及經檢閱的 change／歸檔證據。若需要加入被忽略的檔案，使用明確檔案清單，不整批加入 ReferDoc 或 AgentDoc。
- `.gitignore`、既有訪談、無關工作流資料及其他未提交修改不屬本輪發布授權範圍。
- 正式發布前，將 PR 草稿中的路徑補成實際提交版本的可用連結，並檢查遠端 base branch 與 required checks。

## 權限與完成條件

- `$workflow` 授權本機開發與交付準備，沒有授權 commit、push 或遠端發訊息。
- 本機草稿與主規格同步不等於 PR 已發布；歸檔成功也不等於合併。
- 由使用者執行 merge；核對真實結果後才更新 change／workflow 完成狀態。
