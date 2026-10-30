[English](README.md) | [繁體中文](README.zh-TW.md)

# PY_NetworkSimulator

PY_NetworkSimulator 是使用 Python 開發的研究專案，探討整合存取與回傳（Integrated Access and Backhaul，IAB）網路中的 Ambient IoT。
本專案適合想了解網路部署，以及 Node 與 Tag 之間無線鏈路的讀者。

目前的模組可建立靜態網路拓撲，並根據該拓撲計算鏈路品質與封包接收結果。
通道模型已存在於本機工作目錄，遠端交付仍待完成。
能量、接入、排程與完整模擬時間軸尚未整合。

## 選擇閱讀路徑

- [快速開始](#快速開始)：執行範例，再透過 Notebook 查看部署圖與通道計算。
- [架構與資料流](#架構與資料流)：了解輸入、模組、輸出與研究限制。

## 快速開始

### 前置條件

拓撲範例需要 Python 3.10 以上版本與 Matplotlib。
通道計算另需 NumPy 與 SciPy。
執行 Notebook 的環境需要 Jupyter 和可用的 Python kernel；執行測試則需要 pytest。
若既有專案環境已有這些套件，請使用該環境。

請從專案根目錄執行以下命令。
`PYTHONPATH` 設定讓 Python 可以使用來源碼中的模組，不必將本專案安裝成套件。
上述第三方套件仍須事先準備。

### 1. 建立範例拓撲

```bash
PYTHONPATH=src python -c 'from iab.topology import build_topology, example_config; snapshot = build_topology(example_config()); print(len(snapshot.ues), len(snapshot.tags))'
```

預期輸出：

```text
5 30
```

這兩個數字代表範例中的 5 個使用者設備（UE）與 30 個 Tag，顯示範例拓撲已建立。
此命令不會執行通道模型或顯示部署圖。

### 2. 查看結果

在上述環境開啟 Notebook，從第一個 cell 依序執行：

- [拓撲 Notebook](notebooks/01_iab_topology.ipynb)：查看設定、Node 與 Tag 表格，以及部署圖。您可以修改範例設定，再重新執行各 cell。
- [通道 Notebook](notebooks/02_channel_model.ipynb)：查看指定拓撲的鏈路計算與封包接收結果。

設定、操作與問題排解請參考 [IAB 拓撲指南](ReferDoc/Implementation/IABTopology/README.md)與[通道指南](ReferDoc/Implementation/ChannelModel/README.md)。[使用說明索引](ReferDoc/Implementation/README.md)列出各模組文件。

拓撲匯出會覆寫同名檔案。
匯出失敗或中斷時，可能留下不完整檔案。
若要保留舊結果，請先複製再匯出。

## 架構與資料流

範例中的 Donor 是五個 IAB Node 的上游站台。
每個 Node 在邏輯上關聯一個 UE，並讀取分配給它的 Tag。
Tag 部署在所屬 Node 周圍；模擬期間拓撲保持固定。

1. **拓撲：** Node 位置、Tag 數量與亂數種子產生拓撲快照、表格與部署圖。快照記錄 Node、Tag 與其關係。
2. **通道：** 拓撲快照、通道設定與窗功率作為輸入，用於計算接收功率、SNR、SINR 與封包接收結果。SNR 比較訊號與噪聲功率；SINR 也考慮干擾。
3. **結果：** Notebook 顯示設定與計算過程。拓撲模組也能將圖與資料匯出為 PNG、SVG、JSON 和 CSV。

拓撲的近、中、遠區表示距離，不能證明 RF 覆蓋範圍、沒有干擾或實測訊號品質。

通道模型採用研究假設，並假設封包已具備傳送條件；其結果不能保證戶外場域性能。
[通道指南](ReferDoc/Implementation/ChannelModel/README.md)說明模型假設與參數來源。
IAB split 架構中的 Tag 讀取屬於研究擴充，並非完整符合標準的宣稱。

### 拓撲設定

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

### 程式與延伸閱讀

核心程式分為處理拓撲的 [src/iab](src/iab/) 與計算通道的 [src/channel](src/channel/)。對應測試位於 [tests/iab](tests/iab/) 與 [tests/channel](tests/channel/)。

- [整體架構](docs/architecture/system.html)
- [IAB 拓撲架構](docs/architecture/iab-topology.html)與[設計說明](docs/architecture/iab-topology-design.md)
- [通道架構](docs/architecture/channel-model.html)

## 驗證

從專案根目錄使用既有測試環境：

```bash
MPLBACKEND=Agg python -m pytest tests/iab/test_topology_notebook.py tests/iab/test_topology_extraction.py -q
python -m pytest tests/iab -q
python -m pytest tests/channel -q
```

如需在乾淨 kernel 執行，請使用[拓撲 Notebook 執行器](tests/iab/execute_topology_notebook.py)。
通道指南說明其對應執行器與環境。

本次 README 更新重新執行快速開始命令，輸出為 `5 30`。
本次文件修改未重新執行上述測試命令或 Notebook。
