[English](README.md) | [繁體中文](README.zh-TW.md)

# PY_NetworkSimulator

本專案使用 Python，支援 IAB 網路中的 Ambient IoT 研究。
目前本地模組可建立靜態網路拓撲，並計算無線鏈路品質。
您可以透過 Notebook 查看設定、計算過程與結果。

## 系統概覽

| 模組 | 輸入 | 輸出 |
|---|---|---|
| IAB 拓撲 | Node 位置、Tag 數量與亂數種子 | 拓撲快照、距離表與部署圖 |
| 通道模型 | 拓撲快照、通道設定與窗功率 | 接收功率、SNR、SINR 與封包接收結果 |

拓撲快照連接這兩個模組。
通道模型已存在於本機工作目錄，遠端交付仍待完成。

## 選擇閱讀路徑

| 目的 | 閱讀入口 |
|---|---|
| 執行小型範例 | [快速開始](#快速開始) |
| 理解系統 | [架構與資料流](#架構與資料流) |

## 快速開始

### 前置條件

拓撲模組使用 Python 3.10 以上版本與 Matplotlib。
通道計算另需 NumPy、SciPy；Notebook 範例需要可用的 Jupyter kernel。
測試需要 pytest。請沿用既有專案環境。

### 執行拓撲範例

從專案根目錄執行：

```bash
PYTHONPATH=src python -c 'from iab.topology import build_topology, example_config; snapshot = build_topology(example_config()); print(len(snapshot.ues), len(snapshot.tags))'
```

預期輸出：

```text
5 30
```

兩個值分別是範例的 UE 數量與 Tag 數量。
這種 `PYTHONPATH` 呼叫方式不需要安裝本套件。

### 接續閱讀 Notebook

- [拓撲 Notebook](notebooks/01_iab_topology.ipynb)：修改設定、查看表格與部署圖。
- [通道 Notebook](notebooks/02_channel_model.ipynb)：查看通道計算與封包接收。

選定環境後，從第一個 cell 依序執行。
兩份 Notebook 都匯入核心模組，並保留設定、示範與情境。

拓撲設定與操作見 [IAB 使用說明](ReferDoc/Implementation/IABTopology/README.md)。
通道操作見[繁體中文通道指南](ReferDoc/Implementation/ChannelModel/README.md)。
[使用說明索引](ReferDoc/Implementation/README.md)列出目前的模組文件。

## 拓撲設定

靜態二維範例有 1 個 Donor、5 個 Nodes，每個 Node 關聯 1 個 UE。
UE 只有邏輯歸屬。Tag 數量可設定，範例共有 30 個 Tags。
模組提供精確三區配額、表格，以及 PNG／SVG／JSON／CSV 匯出。

`TopologyConfig` 的三個集合欄位使用 tuple：

| 欄位 | 格式或範例 |
|---|---|
| `iab_nodes` | `(node_1, node_2, node_3, node_4, node_5)` |
| `zone_outer_radii_m` | `(10.0, 30.0, 50.0)`；近／中／遠區外邊界，單位為公尺 |
| `zone_tag_counts` | `(10, 13, 7)`；全場近／中／遠區 Tag 數量 |

不接受 list，也不自動轉換格式。
`frozen=True` 防止欄位重新賦值；tuple 防止容器元素被增刪或替換。
兩者共同維持設定固定，但不取代獨立的 ID 唯一性驗證。

型別註記不會自動執行輸入驗證。
`build_topology(config)` 會拒絕 list 與其他非法設定，並拋出含原因的 `ValueError`。
因此不需要額外的 `__post_init__` 格式轉換。

```python
zone_tag_counts = (10, 13, 7)  # Accepted: tuple
# zone_tag_counts = [10, 13, 7]  # Rejected: list
```

## 架構與資料流

來源碼與測試依模組分類：

```text
src/
├── iab/
│   ├── __init__.py
│   ├── contracts.py       # Shared dataclasses and TagZone
│   ├── topology.py        # Validation, generation, tables, and export
│   └── plotting.py        # Deployment plot with equal axis scaling
└── channel/
    ├── __init__.py
    ├── contracts.py       # Channel configuration, data types, and enums
    └── channel_model.py   # Channel calculations, windows, and packet reception
```

- [整體架構](docs/architecture/system.html)
- [IAB 拓撲架構](docs/architecture/iab-topology.html)
- [IAB 設計說明](docs/architecture/iab-topology-design.md)
- [通道架構](docs/architecture/channel-model.html)
- [拓撲測試](tests/iab/)與[通道測試](tests/channel/)

## 驗證命令

從專案根目錄使用既有測試環境：

```bash
MPLBACKEND=Agg python -m pytest tests/iab/test_topology_notebook.py tests/iab/test_topology_extraction.py -q
python -m pytest tests/iab -q
python -m pytest tests/channel -q
```

既有拓撲乾淨 kernel 執行器為 [execute_topology_notebook.py](tests/iab/execute_topology_notebook.py)。
通道指南列出對應的 kernel 執行器與環境。
本次 README 更新以 Python 3.12.12 執行快速開始命令，實際輸出為 5 30。
這次文件修改未重新執行上述測試命令。

## 限制

本指南說明目前的拓撲與通道模組；能量與排程仍是後續工作。
幾何分區不能證明 RF 覆蓋範圍、沒有干擾或 SNR 品質。
通道指南記錄模型假設與參數來源。

匯出會覆寫同名檔案；中斷或失敗可能留下部分檔案。
若要保留舊結果，請先複製後再匯出。
