# 規範查詢入口

Agent 請優先查詢 [`spec_index.json`](spec_index.json)。此檔涵蓋本地 IAB/A-IoT PDF，以規範編號為 key，並提供功能、分層與領域的反向索引。

| JSON key | 用途 | 範例 |
|---|---|---|
| `documents` | 規範編號 → 文件資訊 | `documents["TS 38.340"]` |
| `by_keyword` | 功能關鍵字 → 規範編號陣列 | `by_keyword["bap"]`、`by_keyword["msg2"]`、`by_keyword["排程"]` |
| `by_layer` | L1/L2/L3 → 規範編號陣列 | `by_layer["L2"]` |
| `by_domain` | IAB/A_IoT → 規範編號陣列 | `by_domain["A_IoT"]` |

`documents` 含本地版本、Release、PDF 相對路徑、分層、關鍵字、使用條件與來源 Markdown。`historical_versions` 保留舊版路徑；預設使用文件主項目的 `path`。所有 PDF 路徑以本目錄為基準，同一份跨領域文件只保存一個主項目。

從專案根目錄查詢（需要 `jq`）：

```bash
# 直接查一份規範
jq '.documents["TS 38.340"]' ReferDoc/Spec/spec_index.json

# 功能關鍵字 → 文件資訊；找不到時回傳空陣列
jq --arg keyword msg2 '. as $catalog | [(.by_keyword[$keyword | ascii_downcase] // [])[] | $catalog.documents[.]]' ReferDoc/Spec/spec_index.json

# 查詢 A-IoT 的 L2 文件
jq '. as $catalog | [.by_domain.A_IoT[] | $catalog.documents[.] | select(.layers | index("L2"))]' ReferDoc/Spec/spec_index.json
```

Agent 查詢順序：先查規範編號或關鍵字，再用 `domains`、`layers`、`usage` 與 `scope` 篩選；需要條款或規範原句時讀取對應 PDF。英文關鍵字採小寫，中文別名可直接查詢。未命中時可列出 `by_keyword` 的 keys，或回查 [IAB 索引](IAB/README.md) 與 [A-IoT 索引](A_IoT/SPEC_INDEX.md)。

此 JSON 是文件導航索引，沒有規範全文，也不表示版本已做即時更新查核。L1/L2/L3 沿用現有模擬器責任分類；跨 Release 與研究模型邊界請讀取 `model_boundaries`。

新增、重新命名或更新 PDF 時，同步更新 `documents`、三個 `by_*` 索引及 `metadata_updated_on`。每份本地 PDF 應出現在主項目的 `path` 或 `historical_versions`。目前專案的 `.gitignore` 忽略 `ReferDoc/`，此索引也在忽略範圍內。
