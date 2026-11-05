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

## 2026-11-04 reference-calendar correction

Q-INFLUENCE-47 B selects 600-ms Windows every 1000 ms from t=0, with 400-ms gaps.
Earlier unselected-spacing text is historical. The illustrative 20-s round has Window starts at 0 through 19 s.
This calendar arithmetic does not select service defaults or establish a feasible transmission count.
Q-INFLUENCE-48 final Guard cleanup at evaluation end remains open.

## 2026-11-04 final Guard correction

Q-INFLUENCE-48 B resolves the final Guard boundary.
The evaluation end remains the latest configured service deadline; all batch D2R ends must precede it.
An existing full Guard may finish afterward within its outer Window. Reserve its full energy and time during admission.
At evaluation end, stop service credit and new Policy/Paging. Finish only Guard cleanup, with a separately recorded physical cleanup end.
The earlier open-Guard statement is historical. Numerical service workload values are still not selected.

## Q-INFLUENCE-50 | Reference service workload [ACCEPTED A]

Date: 2026-11-04. Facet: Influence, total 50; other counts unchanged. Answer: A; accepted on 2026-11-04.
Purpose: select a complete, inspectable service table for the first small integrated reference run.
The input method is already settled: explicitly list services in the Notebook. Do not ask about random generation again.
Keep all services at t=0, ample finite initial Tag data, the accepted calendar/energy/PHY rules and strict exclusive deadlines.

| Service | Required Tag IDs | Minimum valid application data | Exclusive deadline |
|---|---|---|---|
| S1 | Tag-001, Tag-002, Tag-003 | 128 bytes = 1024 bits | 15 s = 15000000000 ns |
| S2 | Tag-003, Tag-004, Tag-005 | 256 bytes = 2048 bits | 20 s = 20000000000 ns |

These are proposed synthetic integration inputs, not measured farm-service requirements or a formal experimental workload.
The current topology generator creates Tag-001 style IDs. Require all five IDs to exist in the actual topology before using this table.
Do not relocate Tags, change their Node/zone ownership or assume these IDs represent specific channel classes.
Retain the full configured topology. Only the listed Tags contribute to these two services under existing eligibility rules.
This small service subset does not establish coverage of every Node/zone or representative five-Node network load.
The different demands and deadlines exercise heterogeneous services; Tag-003 exercises shared credit.

Example: while both services are active and have enough remaining demand, one eligible new 30-byte payload from Tag-003 earns 30 bytes for each service.
Physical new payload is still 30 bytes. After that event, remaining demands are 98 and 226 bytes if no earlier credit exists.
Apply all existing content eligibility, duplicate suppression, service caps, failure and deadline rules.
Do not replace the service aggregate minimum with a separate minimum per Tag.
The derived evaluation horizon is 20 s. Under the accepted calendar, Window starts are 0 through 19 s.
This counts reference calendar starts, not successful transmissions or demonstrated service completion.
Any required final Guard may finish after evaluation end only under the accepted cleanup/Window constraints.

A, recommended: adopt this complete two-service table as the first small integration reference.
B: adjust the table to the user's intended workload before selecting a reference; the user may supply service counts, Tag sets, data amounts or deadlines.
A keeps the trace small and covers shared credit and heterogeneous requirements.
B can match a particular use case, but needs the corresponding numerical inputs.
Both preserve the declared input method and previously accepted semantics.
Optional notes may adjust individual cells. No answer or new numerical service acceptance is recorded.
No simulator implementation, performance result, commit, push or publication.

## 2026-11-04 | Q-INFLUENCE-50 A accepted; Tag energy preparation requested

Original instruction:
> A 這邊可以,這邊的目標是請先確定好目前的組態內容,則baseline的部份我等等會給您算法 因此先不用做,則這邊我確定下可以先實做tag 的電量改變跟我們剛剛討論內容的模組媽 這邊的模組輸出請遵照 $workflow

Accept the complete small reference table: S1 Tag-001/002/003, 128 valid bytes, exclusive deadline 15 s; S2 Tag-003/004/005, 256 valid bytes, deadline 20 s.
Both start at zero. Retain actual topology ownership, shared credit, ample finite initial data and the accepted max-deadline horizon.
The user will supply the Baseline algorithm later. Do not design or implement Baseline now.
Prepare Tag energy update, conversion, operation-energy checks and depletion recovery as an independent first module scope.
Module output must follow workflow: executable teaching Notebook, behavior checks, architecture and tree-form code trace, human acceptance before source extraction.
Accepted configuration is sufficient for isolated energy behavior checks using explicit event sequences; no Baseline algorithm is required.
Implementation scheduling remains subject to the existing merge rule. No local-first exception is inferred from this request.
ReferDoc/Plan/Tag_Energy_Implementation_Readiness.md records the complete configuration, scope, acceptance cases and the verified workflow gate.
Influence stays 50; no new model preference question. No new change/specification or implementation started.
