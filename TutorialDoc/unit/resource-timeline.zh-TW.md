[English](resource-timeline.en.md) | [繁體中文](resource-timeline.zh-TW.md)

# 資源時間表單元

透過[資源 Notebook](../../notebooks/03_resource_timeline.ipynb)產生並查看 UE 與 Tag 的資源區間。
請先完成[快速開始](../../README.zh-TW.md#快速開始)，再從專案根目錄或 notebooks 目錄開啟 Notebook。

從第一個 cell 依序執行。設定 cell 使用 seed 42，並明列 synthetic 窗口起點 0 與 800 ms。
每個外層窗口長 600 ms，各 Node 先有 UE 占用，再提供 Tag 的 Paging、D2R 與 Guard 預算。
表格與圖使用同一份生成快照；窗間空白表示不可用資源。

Notebook 示範取整、可重現性、Node 查詢順序不影響結果，以及當前資源投影。
投影使用呼叫端提供的權威時間，不是防止惡意呼叫者查詢未來的安全沙箱。
通道交接沿用既有 ChannelModel，尚未實作完整引擎或封包排程器。

匯出預設關閉。在明確匯出 cell 將 EXPORT_RESULTS 改成 True，才會寫入 notebooks/artifacts/resource-timeline。
輸出包含 snapshot.json、resources.csv、timeline.png 與 timeline.svg；匯出會覆寫同名檔案，失敗時可能留下部分檔案。
若需保留舊結果，請先複製再匯出。

人工審核通過的核心已搬入 [src/timeline](../../src/timeline/)，Notebook 改為匯入這份核心。200 ms 間隔是 synthetic 輸入，不是已校準負載分布。
模型依據見[資源設計](../../docs/architecture/resource-timeline-design.md)與[決策紀錄](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md)第 34 節。

請依下列順序閱讀原始碼：

| 模組 | 責任 |
|---|---|
| [contracts.py](../../src/timeline/contracts.py) | 不可變設定、方向及快照資料結構 |
| [resource_timeline.py](../../src/timeline/resource_timeline.py) | 驗證、抽樣、生成、當前資源查詢與匯出 |
| [plotting.py](../../src/timeline/plotting.py) | 繪製生成的 UE 與 Tag 區間 |

Notebook 保留設定、說明、HTML 表格呈現與斷言。
人工審核時加入的註解隨對應函式搬入原始碼。
