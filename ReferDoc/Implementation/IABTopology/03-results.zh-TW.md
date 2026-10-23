# 閱讀結果

[回到使用說明](README.md)

## 如何閱讀結果？

### 表格

| 表格 | 可以查到什麼？ |
|---|---|
| 設定表 `settings` | 本次使用的位置、半徑、Tag 數量與隨機種子 |
| Node 表 `nodes` | 每個 Node 的位置、UE，以及近／中／遠區 Tag 數量 |
| Tag 表 `tags` | 每個 Tag 的編號、位置、所屬 Node、距離與區域 |
| 連線表 `links` | Donor 連到哪些 Node，以及各 Node 連到哪些 UE、Tag |

預設範例應有 5 個 Node、5 個 UE、30 個 Tag；近／中／遠區分別為 10／13／7 個。每個 Node 至少有 2 個 Tag，但各 Node 的總數不必相同。

### 部署圖

| 圖上標記 | 意義 |
|---|---|
| 星形 | Donor 的位置 |
| 方形 | Node 的位置 |
| 藍綠、橘褐、紫色圓框與 Tag 圓點 | 分別表示近區、中區、遠區 |
| 圓點旁的數字 | Tag 編號，例如 `001` 代表 `Tag-001` |
| Donor 與 Node 之間的線 | 兩者的連接關係 |

圖上的 x、y 軸都以公尺表示，兩軸比例相同。UE 目前只記錄所屬 Node，沒有設定實際位置，因此不畫在圖上。

### 儲存的檔案

| 檔案 | 用途 |
|---|---|
| `deployment.png`、`deployment.svg` | 查看或放入報告的部署圖 |
| `settings.csv`、`nodes.csv`、`tags.csv`、`links.csv` | 可用試算表工具開啟的四份表格 |
| `snapshot.json` | 保存本次完整設定與部署結果的資料檔 |
