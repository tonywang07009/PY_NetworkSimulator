## Why

使用者已完成首個IAB拓撲模組的模型決策，需要可執行、可重現且可逐段理解的Notebook，驗證幾何、Tag分配與歸屬，作為後續Channel／時序模組的輸入。

## What Changes

- 建立平面靜態拓撲Notebook：1 Donor直連5 Nodes，各1個只有ID／歸屬的UE。
- 精確三區配額、每Node至少2個Tag、依seed隨機關聯，區內按面積均勻生成；邊界10／30／50 m且Node區域不重疊。
- 提供設定／Node／Tag／連線表與部署圖、可重現情境測試，以及架構／code-trace供人工導讀。
- 本輪先完成Notebook。使用者明確接受後才抽離共用dataclass與實作至.py，並核對等價性。

## Capabilities

### New Capabilities
- `iab-topology`: 靜態平面IAB拓撲生成、輸入拒絕、輸出、重現性及Notebook人工驗收。

### Modified Capabilities
無。

## Impact

新增notebooks/01_iab_topology.ipynb、tests/test_topology_notebook.py與導讀證據；測試基礎設施.py不是提前抽離正式模組。保留既有README／LICENSE與無關修改。採標準庫dataclass、random及既有Matplotlib／Notebook環境，不實作SNR／BER／採能／UE物理座標／移動／排程。沒有commit／push或遠端發布授權，Issue先備本機草稿。
