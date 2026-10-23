# IAB 拓撲交付導讀

## 目前狀態

- Change：add-iab-topology-notebook；本機交付分支feat/iab-topology，尚未commit／push。
- 原位置與目前位置：`/home/tonywang/Net_simluation/PY_NetworkSimulator/AgentDoc/openspec/changes/add-iab-topology-notebook`。
- 正式archive_path尚未成立；預備位置與條件見[archive-preparation.md](archive-preparation.md)。
- 原始Git基準0a5ff65f151febb53416d67855afa9850e2b1b13；本輪HEAD a87a2d8effcbd6986c1aaad545d529df2ae26c75。未提交內容以[source-manifest.json](source-manifest.json)辨識，不能視為HEAD既有程式。
- 使用者已理解主要邏輯並授權抽離，接受產品說明風格與Notebook列點說明。分章文件沿用已接受內容，沒有新增模型決策。
- 尚無Issue／PR／CI／merge；[PR草稿](pr-draft.md)為本機待發布內容，不是遠端交付證據。

## 實際tree（省略無關分支）

```text
/home/tonywang/Net_simluation/PY_NetworkSimulator/
├── AGENTS.md -> agent.md
├── README.md
├── src/iab/
│   ├── __init__.py
│   ├── contracts.py
│   ├── topology.py
│   └── plotting.py
├── tests/iab/
│   ├── test_topology_notebook.py
│   ├── test_topology_extraction.py
│   ├── execute_topology_notebook.py
│   └── fixtures/topology-before-extraction.json
├── notebooks/
│   ├── 01_iab_topology.ipynb
│   └── artifacts/iab-topology/ # snapshot.json、四份CSV、PNG／SVG
├── ReferDoc/Implementation/
│   ├── README.md
│   └── IABTopology/
│       ├── README.md / README.en.md
│       ├── 01-settings.zh-TW.md / 01-settings.en.md
│       ├── 02-usage.zh-TW.md / 02-usage.en.md
│       ├── 03-results.zh-TW.md / 03-results.en.md
│       ├── 04-troubleshooting.zh-TW.md / 04-troubleshooting.en.md
│       └── draft.zh-TW.md / draft.en.md # 保留的合併草稿
├── docs/architecture/
│   ├── system.html
│   └── code-trace.md
└── AgentDoc/openspec/
    ├── specs/iab-topology/spec.md
    └── changes/add-iab-topology-notebook/ # 目前change與本導讀
```

## 實作檔絕對與相對路徑

| 相對路徑 | 絕對路徑／狀態與用途 |
|---|---|
| `src/iab/__init__.py` | [__init__.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/iab/__init__.py)：新增：IAB套件入口 |
| `src/iab/contracts.py` | [contracts.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/iab/contracts.py)：搬移：全部共用dataclass／Enum；原src/network_simulator/contracts.py |
| `src/iab/plotting.py` | [plotting.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/iab/plotting.py)：搬移：等比例部署圖；原src/network_simulator/plotting.py |
| `src/iab/topology.py` | [topology.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/iab/topology.py)：搬移：設定驗證、生成、表格與匯出；原src/network_simulator/topology.py |
| `tests/iab/execute_topology_notebook.py` | [execute_topology_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/iab/execute_topology_notebook.py)：搬移：乾淨kernel執行器；原tests/execute_topology_notebook.py |
| `tests/iab/test_topology_extraction.py` | [test_topology_extraction.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/iab/test_topology_extraction.py)：搬移：4個保存基準比對；原tests/test_topology_extraction.py |
| `tests/iab/test_topology_notebook.py` | [test_topology_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/iab/test_topology_notebook.py)：搬移：69情境×2入口；原tests/test_topology_notebook.py |
| `tests/iab/fixtures/topology-before-extraction.json` | [topology-before-extraction.json](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/iab/fixtures/topology-before-extraction.json)：搬移：獨立保存的原型輸出；原tests/fixtures/同名檔 |
| `notebooks/01_iab_topology.ipynb` | [01_iab_topology.ipynb](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/01_iab_topology.ipynb)：修改：設定、列點說明、展示與情境；import iab |

所有正式.py與fixture搬移前後的SHA一致，見module-layout-baseline.json。舊位置只作歷史文字，不當成現行連結。

## 閱讀與資料流

1. [中文使用說明](../../../../ReferDoc/Implementation/IABTopology/README.md)／[英文使用說明](../../../../ReferDoc/Implementation/IABTopology/README.en.md)：用途、設定、操作、結果及常見問題。
2. Notebook `contracts` cell匯入iab資料格式；`run-example`呼叫example_config→build_topology。
3. contracts.py提供唯一資料格式；validate_config檢查tuple、ID、配額、座標與圓域分離。
4. build_topology局部RNG分配zone／owner，按環帶面積抽樣，由_position_in_ring檢查座標，回傳TopologySnapshot。
5. topology_tables與plot_topology使用同一結果；export_topology寫入JSON、CSV與PNG／SVG。匯出會覆寫同名檔案，中途錯誤可能留下部分輸出。

## 需求／實作／檢查對照

正式要求見[主規格](../../specs/iab-topology/spec.md)，與本change delta的7要求／14情境本文完全一致。

| 要求 | 實作 | 實際證據 |
|---|---|---|
| 靜態星狀、精確配額、唯一歸屬 | contracts、build_topology | test_builds_exact_global_quotas_and_one_ue_per_node等原有69案例 |
| 幾何、非法輸入、不可變、RNG隔離 | validate_config、classify_distance、build_topology | tests/iab/test_topology_notebook.py雙入口檢查 |
| 同一結果的表／圖／匯出 | topology_tables、plot_topology、export_topology | 表、圖、匯出情境及Notebook執行輸出 |
| 人工接受後抽離等價 | Notebook imports、正式模組 | 4個保存基準與extraction-green.log |
| 目錄搬移後可執行 | src/iab、tests/iab | module-layout-pytest.log、notebook-execution.json |

詳細命令、範圍與限制：[extraction-validation.md](extraction-validation.md)。本輪僅Markdown／說明拆分及主規格同步，沒有重新宣稱既有程式檢查為新測試結果。

## 架構、審查與後續

- [系統圖](../../../../docs/architecture/system.html)及[模組詳圖](architecture.html)保留；詳圖目前來源為src/iab，自動收據iab-layout-review/architecture.finalize-summary.json。本輪模組關係與程式碼未變，未重新生成圖形。
- 本輪Standards／Spec唯讀文件審查無阻擋問題；代理檢查與使用者理解、實際人工操作、遠端CI分開記錄。
- [歸檔準備](archive-preparation.md)記錄尚缺的Issue對應、task及移動後驗證條件；尚未歸檔、發布或合併。
