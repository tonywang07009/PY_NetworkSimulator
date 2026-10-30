[English](iab-topology.en.md) | [繁體中文](iab-topology.zh-TW.md)

# IAB 拓撲單元

本單元說明拓撲設定與輸入限制。請先完成[快速開始](../../README.zh-TW.md#快速開始)。

## 拓撲設定

範例有一個 Donor、五個 Node，每個 Node 對應一個 UE，全場共有 30 個 Tag。Tag 數量可設定。`TopologyConfig` 的三個集合欄位必須使用 tuple：

| 欄位 | 範例與意義 |
|---|---|
| `iab_nodes` | `(node_1, node_2, node_3, node_4, node_5)` |
| `zone_outer_radii_m` | `(10.0, 30.0, 50.0)`；近、中、遠區的外邊界，單位為公尺 |
| `zone_tag_counts` | `(10, 13, 7)`；全場近、中、遠三區的 Tag 數量 |

模組不接受 list，也不自動轉換。
`frozen=True` 防止欄位重新賦值；tuple 防止集合元素被增刪或替換。
模組會另行檢查 ID 唯一性。

型別註記不會自動執行輸入驗證。
`build_topology(config)` 遇到無效設定時，會拋出包含原因的 `ValueError`。

```python
zone_tag_counts = (10, 13, 7)  # Accepted: tuple
# zone_tag_counts = [10, 13, 7]  # Rejected: list
```

詳見[拓撲指南](../../ReferDoc/Implementation/IABTopology/README.md)與[架構與資料流](../architecture.zh-TW.md)。
