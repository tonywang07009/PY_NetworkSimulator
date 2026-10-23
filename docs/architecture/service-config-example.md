# 同起點服務批次：Config 與輪長範例

更新：2026-10-23。依使用者最新明確決策重整，取代此文件先前依序啟動兩個服務週期的草案。依據：[R-01 第 31 節](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md)、[系統模型決策](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md)。尚未實作或執行模擬器。

## 已確定的時間規則

一輪全部服務在全域 `t=0` 同時出現，需求於起點固定。輪長由本輪最晚 Deadline 決定，不再另外指定獨立共同週期長度或依序加入其他服務批次。

```text
service_start_ns[i] = 0
deadline_exclusive_ns[i] > 0
round_end_ns = max(deadline_exclusive_ns[i])
credit_allowed[i] = D2R_END_ns < deadline_exclusive_ns[i]
```

| 服務 | 起點 | 排他 Deadline | 說明 |
|---|---:|---:|---|
| S1 | 0 s | 15 s | 只能在 15 s 以前完成合格新 payload 的認列 |
| S2 | 0 s | 20 s | 只能在 20 s 以前完成合格新 payload 的認列 |
| 本輪 | 0 s | 終點 20 s | 取兩項服務的最晚 Deadline |

15 s／20 s 是使用者的說明例，不自動成為所有服務的預設值。服務可提前達標，但不因此改寫由配置 Deadline 推得的本輪長度。DU Window 持續時間固定 600 ms，起點／間隔未定；不能以 20 s 除以 600 ms 就宣稱已知可用 Window 數。

**邊界修正**：這輪允許最晚服務 Deadline 等於輪末；先前要求全部 Deadline 嚴格早於期末的草案不再適用。S2 在 `19_999_999_999 ns` 完成，在其他條件合格時可認列；在 `20_000_000_000 ns` 完成不認列。輪末能量與既有物理事件的收尾細節，仍在 Engine 設計時封閉。

## Config 形狀建議（尚未實作）

在 Notebook 明列本輪服務，集中共用 dataclass 定義，內部 State 留各模組；後續仍按原型、情境測試、人類接受後才抽離 `.py`。

| 結構／欄位草案 | 用途／狀態 |
|---|---|
| SimulationConfig.scenario_id | 情境識別；完整配置快照仍必須保存 |
| SimulationConfig.seed | 隨機環境來源之一，不自行改寫明列服務需求 |
| SimulationConfig.services | 本輪全部 ServiceConfig；建議直接聚合單批服務，不先增加多期結構 |
| ServiceConfig.service_id | 服務識別；具體 ID 型別及排序待整體契約設計 |
| ServiceConfig.required_tag_ids | 服務指定的完整 Tag 集合 |
| ServiceConfig.min_payload_bits | 正的最低有效新 payload 需求，不是完整 TBS |
| ServiceConfig.last_allowed_slot | 候選輸入方式：從全域 0 起算的最後允許 Slot；尚未核准具體輸入欄位 |
| 衍生 round_end_ns | 取各服務絕對排他 Deadline 的最大值，不另填任意數值 |

不再為首版要求使用者填 `ServiceCycleConfig.duration_ns`、`num_cycles` 或完整 `cycles` 清單。若保留 ServiceCycleConfig 名稱，也只能表示這一輪批次，輪長仍推得；具體類別命名不是需要另開研究決策的問題。多輪需求更新／獨立實驗重跑留待後續明確需求。

Tag、Access、Environment 仍需在相應模組配置；只靠上表不能執行完整模擬器。當前優先工作為 [IAB 拓撲模組](iab-topology-scope.md)，未完成的服務契約不阻擋純拓撲盤點。

## Slot／ns 換算說明

若後續採用已提議的最後 Slot 欄位，沿用 `T_slot=1_000_000 ns`：

```text
deadline_exclusive_ns = (last_allowed_slot + 1) * 1_000_000
15 s -> last_allowed_slot = 14_999
20 s -> last_allowed_slot = 19_999
round_end_ns = max(15_000_000_000, 20_000_000_000)
             = 20_000_000_000
```

這是欄位表示建議及算術換算，沒有將服務 Deadline 自動向後延長；原始輸入如何轉 Slot 仍需明示規則。

## 待依賴模組時封閉的邊界

- 空服務集合時，最大 Deadline 沒有定義；配置入口拒絕還是支援無服務情境，留契約定稿時決定。
- 服務 ID 重複、空／重複／不存在的 Tag、非正 payload 或 Deadline 的輸入處理。
- 輪末若落在 DU Window、Guard 或進行中傳輸內，Engine 如何阻止超出本輪的新排程並結算既有事件。
- 最小測試：共同起點、輪長最大值、Deadline 前 1 ns／當下、服務提前達標不改配置輪長、電量不隨服務結束重置。

以上是待實作情境，不能標記為測試通過。已確認的輪長規則不需再詢問；現在轉入拓撲範圍對齊。
