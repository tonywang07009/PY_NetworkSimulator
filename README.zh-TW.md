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

以下步驟適用於 Linux 與 Bash。請先準備 Python 3.10 以上版本，並取得本專案的本機副本。
安裝套件需要網路連線。
請從包含本 README 與 `src/` 的專案根目錄執行命令。

### 1. 準備 Python 環境

為本專案建立獨立環境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install matplotlib numpy scipy jupyterlab ipykernel pytest
python -m pip check
```

Matplotlib 用於繪圖；NumPy 與 SciPy 用於通道計算。
JupyterLab 與 ipykernel 提供 Notebook 操作介面與 Python kernel；pytest 用於執行測試。
套件會安裝在 `.venv/` 中。
若 `.venv/` 已是您的專案環境，請從啟用命令開始。
每次開啟新終端機後，請先啟用環境，再執行專案命令。

確認 Python 使用此環境：

```bash
python -c 'import sys; print(sys.executable)'
```

路徑應以 `/.venv/bin/python` 結尾；`pip check` 應顯示 `No broken requirements found.`。
若建立環境時顯示缺少 `venv` 或 `ensurepip`，請安裝發行版中對應 Python 版本的 venv 套件，再重新建立環境。
若套件安裝失敗，請先處理錯誤訊息，再繼續操作。
若匯入時出現 `ModuleNotFoundError`，請確認環境已啟用，再重新執行安裝命令。

範例透過 `PYTHONPATH=src` 尋找來源碼中的模組，不必將本專案安裝成套件。
操作結束後，可執行 `deactivate` 離開環境。

### 2. 建立範例拓撲

```bash
PYTHONPATH=src python -c 'from iab.topology import build_topology, example_config; snapshot = build_topology(example_config()); print(len(snapshot.ues), len(snapshot.tags))'
```

預期輸出：

```text
5 30
```

這兩個數字代表範例中的 5 個使用者設備（UE）與 30 個 Tag，顯示範例拓撲已建立。
此命令不會執行通道模型或顯示部署圖。

### 3. 查看結果

啟用環境後，啟動 JupyterLab：

```bash
python -m jupyterlab
```

若瀏覽器未自動開啟，請開啟終端機顯示的本機網址。
從檔案列表開啟 Notebook，選擇上述環境的 Python kernel，再從第一個 cell 依序執行：

- [拓撲 Notebook](notebooks/01_iab_topology.ipynb)：查看設定、Node 與 Tag 表格，以及部署圖。您可以修改範例設定，再重新執行各 cell。
- [通道 Notebook](notebooks/02_channel_model.ipynb)：查看指定拓撲的鏈路計算與封包接收結果。
- [Tag 充電 Notebook](notebooks/04_tag_energy.ipynb)：執行已確認的 RF／DC、電量與狀態切換 trace，核對操作可行性、容量及被動恢復。已接受的核心已移至 `src/energy`；新增的 TBS 完成後 batch CW trace 仍待人工核對。
- [事件引擎 Notebook](notebooks/05_event_engine.ipynb)：使用既有時序／能量核心，追蹤情境準備、明確狀態寫入、逐窗電量摘要與輪末結果清理。此本地原型尚待人工接受。

設定、操作與問題排解請參考 [IAB 拓撲指南](ReferDoc/Implementation/IABTopology/README.md)與[通道指南](ReferDoc/Implementation/ChannelModel/README.md)。[使用說明索引](ReferDoc/Implementation/README.md)列出各模組文件。

拓撲匯出會覆寫同名檔案。
匯出失敗或中斷時，可能留下不完整檔案。
若要保留舊結果，請先複製再匯出。

## 架構與資料流

拓撲設定產生網路快照；通道模型使用該快照計算鏈路品質與封包接收結果。
[架構與資料流](TutorialDoc/architecture.zh-TW.md)說明模組關係與研究限制。

## 模組單元

[教學單元索引](TutorialDoc/README.zh-TW.md)提供建議閱讀順序。

- [IAB 拓撲](TutorialDoc/unit/iab-topology.zh-TW.md)：設定、分區與輸入限制。
- [通道模型](TutorialDoc/unit/channel-model.zh-TW.md)：公式、研究規則與接收流程。

## 驗證

從專案根目錄使用既有測試環境：

```bash
MPLBACKEND=Agg python -m pytest tests/iab/test_topology_notebook.py tests/iab/test_topology_extraction.py -q
python -m pytest tests/iab -q
python -m pytest tests/channel -q
```

如需在乾淨 kernel 執行，請使用[拓撲 Notebook 執行器](tests/iab/execute_topology_notebook.py)。
通道指南說明其對應執行器與環境。

2026-10-31 以 Linux、Python 3.12.12 的全新暫存環境完成設定檢查。
拓撲命令輸出 `5 30`，通道查詢成功；拓撲與通道的 227 項測試通過。
在隔離專案副本中，拓撲與通道 Notebook 分別完成 11 與 13 個程式區塊，皆無錯誤且 kernel 正常關閉。
Chrome 中的 JupyterLab 已開啟通道 Notebook。
十份文件在 1280 與 390 像素寬的視窗完成渲染，頁面沒有水平溢出，Mermaid 流程圖也正常渲染。
已檢視中文 README、通道單元與 JupyterLab 截圖；通道單元另提供 SVG 流程圖供放大閱讀。
上述文件檢查使用本機 Markdown 預覽，不代表已驗證 GitHub 的渲染結果。
其他 Python 版本與完整 STE 符合性仍待驗證；套件版本未固定。
