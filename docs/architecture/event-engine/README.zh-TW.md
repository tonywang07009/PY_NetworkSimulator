# 事件引擎 Notebook

[English](README.md)

原本的 Engine 建構函式同時處理驗證、索引、排程與執行狀態，閱讀時難以分辨資料在哪裡改變。
Notebook 05 現在分開情境、當下狀態與本輪紀錄，讓計算結果與引擎寫入可以逐步 trace。
Engine 仍留在 Notebook，等待人工接受；時序與能量核心則直接從 src 匯入。

## 快速執行

在既有 RL 環境，從專案根目錄或 notebooks 目錄開啟 [Notebook 05](../../../notebooks/05_event_engine.ipynb)。
依序執行各 cell；最後應顯示一張 Window 起訖電量圖，並檢查紀錄已清理、即時狀態仍保留。
乾淨暫存 kernel 的執行指令：

```bash
python tests/energy/execute_tag_energy_notebook.py /tmp/pynet-event-engine-execution.json notebooks/05_event_engine.ipynb
```

不需註冊使用者 kernel、安裝套件或自動匯出資料。

## 架構閱讀路徑

先看[目前流程圖](../../../.archify/dataflow-event-engine-modular-notebook-20261106-173444/event-engine-modular.html)，再依[完整程式 trace](code-trace.md)閱讀。
圖描述尚未提交工作樹的介面契約，不是固定 commit 的來源證據。

| Notebook 節次 | 閱讀內容 |
|---|---|
| 1-2 | 匯入既有核心、整數 ns 的 EventQueue |
| 3 | 操作輸入、三組 dataclass 與情境準備 |
| 4 | 讀舊快照、取得計算結果，再由引擎明確寫入 |
| 示範 | 觀察 D2R 中途、完成結果、GAP 與下一窗 |
| 5 | 輪末使用結果、更新同一張圖，成功後才清理 |
| 6 | 人工接受與尚待整合的範圍 |

計算函式回傳值；Engine 方法負責狀態、佇列與紀錄的寫入。
prepare_scenario 檢查資料關係；建構時呼叫 validate_energy_inputs，全部通過才建立佇列。
project_tag_operation 保留計畫內的當下投影與數值保護；背景區段沿用 advance_tag_interval。
run_until 先收集同時完成結果，再更新資源、處理新請求；完整儲能准入維持原規則。

## 資料與保存期限

EngineScenario 保存複製後的唯讀索引；EngineState 保存目前快照、階段與操作計畫。
EngineRecords 保存當前／最近一窗 trace、尚未結束的窗起點、本輪摘要與完成結果。
每個已結束 Window 為每個 Tag 增加一筆起訖摘要；重複觀察不增加逐事件電量樣本。
跨 GAP 仍計算耗能與恢復；清理紀錄不會補回電量。

外層明列輪末並呼叫 finish_round(consume_results)。
消費函式取得紀錄副本；成功後移除已消費前綴，失敗保留資料供重試。
尚未結束的窗起點、active、當下時間／電量與事件佇列都不因清理而重設。
render_round 更新外層提供的同一個顯示區，並在 finally 關閉 figure；多輪執行時沿用該顯示區。
該區只保留最新圖，不自動寫檔或刪檔。
端點圖不能還原窗內所有充電／耗盡轉折；單輪記憶體仍隨輸入規模增加。

## 證據與限制

18 個重構前快照／完成結果觀察點全數吻合；既有 RL 環境全測試 463 項通過。
Notebook 05 的乾淨 RL kernel 執行 13 個 code cells，零錯誤並正常關閉。
base 環境相關檢查為 134 項通過；缺顯示依賴時跳過兩項繪圖檢查。
完整命令、review 修正與 kernel 收據保留於對應 OpenSpec 驗證紀錄。
圖表自動檢查與程式測試不能代替人工可讀性接受。

RF、Access 時序、接收結果與明確 batch CW 仍由外部提供。
未提供完整 CFA/SFS 排程、ServiceManager、Policy／Baseline、FBL 抽樣或硬體標定。
本輪未抽離 Engine 核心、發布或合併；完整 STE 字典符合性仍為 [Needs Verification]。
