# 建立靜態 IAB 拓撲首模組

本機 Issue 草稿，尚未發布。對應 OpenSpec change：`add-iab-topology-notebook`。

## 目的

讓研究者透過 Notebook 建立 1 Donor／5 Nodes 的靜態平面部署，設定 Tag 三區數量，並查看位置、歸屬、表格與部署圖。

## 交付內容

- `src/iab/`：集中資料格式、驗證、生成、表格、繪圖及匯出。
- `tests/iab/`：同一模組的正常、邊界、拒絕及抽離比對情境。
- `notebooks/01_iab_topology.ipynb`：以列點說明引導操作，使用相同正式模組。
- `ReferDoc/Implementation/IABTopology/`：中英文分章產品使用說明。
- 主規格：`AgentDoc/openspec/specs/iab-topology/spec.md`。

## 核對條件

- 每個 Node 1 UE，每個 Tag 只有一個所屬 Node。
- 三區配額精確、每 Node 至少 2 個 Tag，支援調高最低數量。
- 依距離分區、區內按面積隨機放置，Node 部署圓域不重疊或相切。
- 相同設定與種子於相同實作／環境可重現；生成不改全域亂數。
- 設定非法時說明原因；表格、圖與匯出都使用同一份結果。
- Notebook 先導讀接受再抽離.py，抽離前後結果一致。

## 目前進度

- 本機實作、情境檢查、程式審查與主要邏輯人工導讀已完成。
- 產品說明風格、Notebook 列點說明已接受，目錄已分類至 iab。
- 主規格同步、分章文件與本機 PR 草稿已整理。
- 遠端發布、實際歸檔、PR、CI、使用者 merge 尚未完成。

訊號品質、電量、排程與跨模組整合不在本 change 範圍內。

## 已發布位置

- Issue：https://github.com/tonywang07009/PY_NetworkSimulator/issues/1
- 草稿PR：https://github.com/tonywang07009/PY_NetworkSimulator/pull/2
- 目前內容已push至feat/iab-topology；未合併、未實際歸檔。
