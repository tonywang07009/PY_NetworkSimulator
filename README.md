# PY_NetworkSimulator
For mine master thesis used.


## 拓撲設定的輸入規則

`TopologyConfig`的三個集合欄位統一使用 **tuple**：

| 欄位 | 格式／範例 |
|---|---|
| `iab_nodes` | `(node_1, node_2, node_3, node_4, node_5)` |
| `zone_outer_radii_m` | `(10.0, 30.0, 50.0)`，近／中／遠區外邊界，單位m |
| `zone_tag_counts` | `(10, 13, 7)`，全場近／中／遠Tag數量 |

不接受list，也不自動轉換格式。`frozen=True`防止欄位重新賦值，tuple防止容器元素被增刪或替換；兩者共同維持設定固定。這是統一輸入格式，不是檢查資料是否重複；ID唯一性另行驗證。

型別註記不會自動驗證輸入；`build_topology(config)`會拒絕上述欄位的list及其他非法設定，拋出含原因的`ValueError`。因此不需要額外的`__post_init__`型別轉換。

```python
zone_tag_counts=(10, 13, 7)  # 正確：tuple
# zone_tag_counts=[10, 13, 7]  # 不接受：list
```

主要邏輯經人工導讀理解並授權後，業務程式已抽離至 `src/iab/`；[拓撲Notebook](notebooks/01_iab_topology.ipynb) 改為 import 正式模組，保留設定、展示與情境測試。

## 靜態拓撲模組

目前提供 1 Donor／5 Nodes／每 Node 1 UE 的靜態二維部署、Tag 精確三區配額、表格與 PNG／SVG／JSON／CSV 匯出。UE 只有邏輯歸屬；Channel／PHY、能量與排程尚未實作。

```text
src/iab/
├── __init__.py       # 套件入口
├── contracts.py      # 全部共用 dataclass 與 TagZone
├── topology.py       # 驗證、生成、表格與匯出
└── plotting.py       # 等比例部署圖
```

在專案根目錄執行，使用已有 Python 3.10 以上與 Matplotlib 環境；本輪實測 Python 3.12／3.11。不需要安裝本套件即可透過 `PYTHONPATH=src` 使用：

```bash
PYTHONPATH=src python -c 'from iab.topology import build_topology, example_config; snapshot = build_topology(example_config()); print(len(snapshot.ues), len(snapshot.tags))'
```

預期印出 `5 30`。完整設定、操作與結果說明見 [Implementation 索引](ReferDoc/Implementation/README.md)，提供中英文分章使用說明。

```bash
MPLBACKEND=Agg python -m pytest tests/iab/test_topology_notebook.py tests/iab/test_topology_extraction.py -q
```

測試需要 pytest；Notebook 另需可用 Jupyter kernel。既有乾淨 kernel 執行器為 `tests/iab/execute_topology_notebook.py`。匯出目錄內同名檔案會覆寫，匯出中途失敗可能留下部分檔案。幾何分區不代表已驗證 RF 無干擾或 SNR 品質。

來源碼與測試依模組分類：目前IAB拓撲程式位於 `src/iab/`，對應測試與比對資料位於 `tests/iab/`。從專案根目錄執行 `python -m pytest tests/iab -q` 可檢查此模組。
