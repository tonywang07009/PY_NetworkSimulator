# 模擬器基底實作盤點

日期：2026-11-06。範圍：核對現有 Plan、OpenSpec、src、Notebook 與測試；不新增模擬器功能。

**結論：已有四類可重用核心，但完整策略執行閉環尚未完成。**
M1 的 W01–W10 中，七個工作包仍有工程缺口；這不表示七包都尚未開始。
明天可以開始確認 baseline／比較對象的策略輸入輸出與演算法邏輯。
要在同一模擬器上執行可信的比較，仍需補齊共同的驗證、傳輸、資料／服務結算與再決策流程。
本盤點不構成新功能實作授權，也不承諾一天完成剩餘工作。

## 1. 逐工作包狀態

狀態以本地工作目錄為準，包含尚未提交的 energy 抽離及 Notebook 修改。
「核心已有」不等於遠端交付、整合驗收或硬體模型驗證完成。

| 工作包 | 已有證據 | 尚缺內容／判定 |
|---|---|---|
| 已交付拓樸 | [src/iab](../src/iab/)；Notebook 01、對應測試 | 作為現有基礎重用，不重做 |
| W01 通道品質 | [ChannelModel](../src/channel/channel_model.py)；分窗鏈路、功率表、FBL、逐次接收抽樣 | 核心已有；正式 TBS／符號率的呼叫串接歸 W04；遠端交付仍待處理 |
| W02 共用設定與資料契約 | iab/channel/timeline/energy 各有 contracts.py | 部分已有；缺整合 run 配置、Action、策略觀測、服務／資料、執行計畫與結果的共同契約。舊 Plan 的單一檔案草案不可當成現行結構，也不為形式搬移既有型別 |
| W03 UE／DU 資源時間表 | [src/timeline](../src/timeline/)；600-ms Window、UE 抽樣、當前資源投影 | 核心已有；參考情境的 1000-ms 起點間隔已定，組裝歸整合工作；遠端交付仍待處理 |
| W04 固定接入、TBS 與 PHY | 已接受 Paging/D2R/Guard 規則；energy 有 D2R 35/63/118/228 ms 與 200-us Guard；channel 已有接收能力 | 部分已有；缺由 Action 產生個別 Paging、response offset、七個 SFS 分配、共同 CW_OFF／Guard 的完整批次計畫；缺選定 TBS 到實際 Channel 接收的串接 |
| W05 Tag 能量帳本 | [src/energy](../src/energy/)；非線性採能、狀態、完整操作能量檢查、恢復、容量、完成 Tag 的 CW 尾段；Notebook 04/05 呼叫 | 核心已抽離；新 CW 行為人工接受待完成。Notebook 05 的 batch 輸入驗證有四項現行失敗，見下節 |
| W06 服務與資料認列 | 規則與參考服務已決定；目前 Engine 僅輸出完成／成功／期限 eligibility | 缺有限資料帳、傳輸與內容身分、失敗保留、唯一物理 goodput、服務共享／去重、同時按比例整數認列、需求封頂與完成凍結 |
| W07 動作驗證 | energy 有完整操作 admission；05 有部分批次原子拒絕 | 部分已有；缺完整 ActionValidator：0 項 NO_OP、1–7 Tag、重複／資格／TBS／SFS／時間／資料／能量檢查；非法動作同窗停排、下窗恢復；不可縮批或降 TBS |
| W08 離散事件引擎 | [Notebook 05](../notebooks/05_event_engine.ipynb) 有 EventQueue、同時事件與能量推進、跨窗 GAP、明示 BatchCW | 部分已有；仍是外部給定 requests/RF/接收結果的原型。缺 W04/W06/W07/W09 閉環及評估結束／Guard 收尾；模組化、紀錄生命週期與 src 抽離待完成 |
| W09 Node 觀測與最小測試策略 | timeline 有當前資源投影；Engine 回傳能量快照副本 | 缺完整 Node SchedulingObservation 與 Policy 呼叫：當前 CSI、能量、服務缺口、合法 TBS；Guard 後更新；隔離未來資料。固定 requests 不是策略閉環 |
| W10 端到端整合與首版操作 | 各模組測試、Notebook 與局部連接 | 缺完整一輪入口、配置快照、共同結果與重跑證據，以及 ACPT-01–05 的完整整合驗收 |

七個仍有工程缺口的工作包：**W02、W04、W06、W07、W08、W09、W10**。
W05 的人工接受及現行 Engine adapter 缺陷另列，不能因不在七包計數內而略過。
不以檔案數、測試數或 OpenSpec 勾選比例推算產品完成百分比。

## 2. 本輪測試與已確認缺陷

本輪實際執行現有完整測試，不重新產生 Notebook 輸出：

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 MPLBACKEND=Agg MPLCONFIGDIR=/tmp/pynet-inventory-mpl \
/home/tonywang/miniforge3/envs/RL/bin/python -c "import sys; sys.path.append('/home/tonywang/miniforge3/lib/python3.12/site-packages'); import pytest; raise SystemExit(pytest.main(['tests','-q','--tb=short']))"
```

結果：**448 passed、4 failed**。先前 452 passed 屬較早來源快照，不是目前工作目錄的通過證明。

四個失敗均屬 [test_batch_geometry_rejects_mutable_or_malformed_collections](../tests/event_engine/test_event_engine_notebook.py) 的參數案例：

| 輸入 | 現行結果 | 預期 |
|---|---|---|
| list 成員集合 | 未拒絕 | 在處理事件前以 ValueError 拒絕 |
| tuple 內含 list 成員 | 未拒絕 | 同上，避免 frozen record 仍持有可變幾何 |
| 長度錯誤的成員 pair | dict 轉換錯誤，錯誤訊息不符合契約 | 明確的 tuple/pair 驗證與 ValueError |
| None | TypeError | 明確的 ValueError |

現行建構函式直接執行 `dict(batch.tag_distances_m)`，缺少契約要求的前置形狀／不可變性檢查。
這是已重現缺陷；未證實造成既有合法輸入的能量數值錯誤，也未判定修改來源。
本輪只記錄，未修改使用者正在導讀的 Notebook 或放寬測試。

## 3. Engine 模組化目前停在哪裡

依 [現有討論紀錄](../AgentDoc/openspec/discuss/2026-11-06-event-engine-modularization.md)：

| 項目 | 已確認／待完成 |
|---|---|
| 相容邊界 | 可以改 constructor 與狀態讀取；實作時一起更新 callers/tests |
| 狀態所有權 | Scenario／State／Records 三個 dataclass；保留既有 EventQueue |
| 寫入責任 | helper 回傳結果，Engine 明確提交狀態 |
| 能量觀測 | 固定快照副本；每 Window 起迄摘要；輪末畫圖後釋放已使用緩衝；只留最新輪圖，保留 live state 與 GAP 能量 |
| 公開能量驗證 | 已選單一 validate_energy_inputs；現行 source 尚未提供，須重用既有檢查 |
| 完成結果交付 | Q-ENGINE-08 待答：輪末交付或逐次推進交付；不能丟棄未消費結果 |

上述已選方向仍未實作。Engine 重構不是 W04／W06／W07／W09 的替代品。
Q-ENGINE-08 是這次重構的開放決策，不代表整個物理模型要重新訪談。

## 4. 明天開始 baseline／比較對象的條件

| 目標 | 就緒程度 |
|---|---|
| 提供並確認演算法；整理排序、同分、Tag/TBS 選擇與無可行動作行為 | 可以開始；不需重做已接受的物理／能量模型 |
| 以明示 Observation fixture 寫純策略邏輯與決策案例 | 可作為局部工作；需先對齊共用觀測與 Action 契約，不能當完整模擬比較 |
| 兩個策略透過同一模擬器跑完參考情境 | 尚未就緒；需要補齊七包中的最小串接，以及現行缺陷／相關接受 |
| 發表公平性、跨 seed 或真實場景效能結論 | 尚未就緒；另需公平性定義、實驗配置與模型適用範圍證據 |

建議先完成的共同流程是：

1. 收斂現有 Engine 決策，修復 batch 驗證，完成受影響測試及 CW 人工接受。
2. 對齊最小共用配置／觀測／Action／結果；重用既有四類核心。
3. 接上 Access/PHY 批次計畫、資料／服務帳與完整原子動作驗證。
4. 接成事件推進 → 同時完成／服務結算 → Guard 後觀測 → Policy → 驗證 → 執行的閉環。
5. 用最小腳本策略跑完整參考輪及 ACPT-01–05，再讓 baseline／比較對象共用同一入口。

這是依賴順序建議，不是本輪新增實作範圍或核准排程。
baseline 的正式算法仍由使用者提供；比較對象本輪未重新指定，不推定為 CLM，也不修改外部模型。

## 5. 驗收、交付與舊 Plan 的差異

| 項目 | 現況 |
|---|---|
| Channel change | CLI 11/12；未完成項屬遠端交付，不是通道核心缺一功能 |
| Timeline change | CLI 8/9；同樣為遠端交付待處理 |
| Energy change | CLI 15/17；新 CW 人工接受與遠端交付待完成 |
| Engine change | CLI 4/6；人工接受／抽離與遠端交付待完成，模組化另有未實作方向 |
| 研究後段 | W11 baseline／fairness、W12 校準、W13 實驗框架、W14/W15 歷史 CLM 路線不可當已完成；CLM 仍為未來工作 |

CLI 數字來自本輪 `OPENSPEC_TELEMETRY=0 openspec list --json`；任務勾選不能取代現行測試結果。
舊 Plan 的八 Tag 上限已被 **七 Tag** 取代；TBS 為 {8,16,32,64} bytes。
600-ms Windows 的參考間隔已選 1000 ms；TBS、採能與能耗數值也已有接受設定，不再列成全部待選。
正式 TBS 的 FBL 呼叫需遵守 R-01 §67：k=8N、n=3(8N+16)、資料群符號率 7500/s；不能沿用所有傳輸 k=64/n=128 的示例。
完整批次要保留連續 Paging 累積邊界、ms 向上取整與固定 200-us Guard 的各自規則。
服務在 t=0 開始，T_end 取最晚 Deadline；停止認列／新排程與既有 Guard 收尾必須分開。

原 `schedule.json`、AOA／CPM、CSV 與 SVG 是規劃估算，沒有本次逐活動實際耗時。
本輪不重算工期，也不以「舊總工時減已存在模組」宣稱明天能完成。

權威與驗證入口：

- [R-01 最新決策](../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md)，尤其 §§58、67–68、83–87、93。
- [現有工作包範圍](01-scope-and-modules.md)；較後正式決策優先於歷史草案。
- [Energy 驗證紀錄](../AgentDoc/openspec/changes/add-tag-charging-trace-notebook/validation.md)與[Engine 範圍](../AgentDoc/openspec/changes/add-event-engine-notebook/proposal.md)。

本輪未重跑 clean kernels、進行硬體校準、完成人工接受或遠端交付。
測試通過部分只支持既有局部行為；完整模擬器驗收與研究適用性仍為 [Needs Verification]。
