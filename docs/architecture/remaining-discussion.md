# Remaining decisions and discussion route

## Current inventory (2026-11-04)

Use [the current remaining-decision inventory](../../Plan/decision-inventory.md) and R-01 sections 81-86.
Access/PHY/data/energy configuration choices are settled for the first research baseline.
Q-INFLUENCE-45 A accepts the numerical 1-uJ Tag profile. Q-INFLUENCE-46 A accepts ideal passive depletion recovery.
Numerical acceptance is not hardware calibration, simulator implementation or integrated validation.
Four study groups remain: SI-01 scenario/integration, BL-01 Baseline, FA-01 fairness and EX-01 experiments.
Q-INFLUENCE-47 B selects 600-ms Windows every 1000 ms with 400-ms gaps.
Q-INFLUENCE-48 B permits existing Guard cleanup after evaluation end within the outer Window.
Q-INFLUENCE-49 selects ample finite initial application data so the chosen TBS can carry its maximum valid payload.
Q-INFLUENCE-50 proposes the explicit two-service integration table in service-config-example.md; no numerical service table is accepted. Preserve all earlier service/visibility rules.
Continue one substantive decision at a time. Do not repeat settled decisions or count routine preparation as new preference questions.
Implementation, tests, human acceptance and existing remote delivery remain separate work. No new publication authorization.

## Earlier inventory (2026-10-22 through 2026-10-23)

> **2026-10-23 最新範圍**：本輪全部服務從全域 0 啟動，輪長取最晚 Deadline；舊多期清單／手填共同週期長度及全部 Deadline 嚴格早於輪末的前提已被 R-01 第 31 節取代。先做 [IAB 拓撲盤點](iab-topology-scope.md)，其直接決策不被下方全套 Config 討論阻擋；下方 D01／D02 舊週期問題只保留必要的單批服務契約。

更新：2026-10-22。依兩份產品規劃、[Config／DTO 草案](config-dto.md)及[系統模型決策](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md)整理。這是討論清單，不是新增已核准需求、OpenSpec tasks 或未實作行為的完成證據。

結論：已可繼續 Config／DTO 設計；本階段先封閉資料表示及跨模組契約，具體 PHY／EH／通道數值可留到依賴模組前確認。研究演算法與科學校準不阻擋純契約草案。每項不是一道固定訪談題；工程欄位／命名由代理先交完整草案，僅對影響模型、資訊權限、計帳或驗收的未決事項逐題詢問。

## 已確認，無須重問

- 單一共用 `.py` 放 Config／DTO／必要 Enum，採 dataclass；State 定義留各模組。
- Config 實例於 Notebook 情境設定 cell 建立，每次 run 保存完整配置快照。
- **2026-10-23 修訂**：本輪全部服務從全域 0 同時開始，輪長為最晚 Deadline；電量在一輪中連續演進，不獨立手填輪長或依序加入下一批服務。
- Notebook 明列服務需求，不自行隨機生成；2026-10-22 的逐期清單設計已由單批起點規則取代，不把服務批次設計延伸成首版多輪功能。
- 每模組 Notebook 原型 → 對應情境測試 → 人類逐段閱讀、理解與接受 → 抽離該模組 `.py` → 等價複驗；跨模組五類 ACPT 仍需完成。
- Policy 只提議 Tag/TBS；最多 8 Tag、固定 BD/SFS/CFA、CW 由 Donor 外生指定。
- 同時間事件批次結算、整數 ns、Deadline 排他；超額整數 bit 採最大餘數法，餘額同分按 Tag ID 升序。
- NO_OP 與 INVALID_ACTION 分開記錄，皆停止本 Window 後續新排程、下窗恢復；時間與既有事件照常。

## 一、Config／DTO 定稿時處理

| 編號 | 主題 | 還需要確定什麼 | 預期產出 |
|---|---|---|---|
| D01 | SimulationConfig／服務批次 | 單批服務集合、輪長推導的欄位表示；空服務集合的有效性；不重問已定共同起點與最晚 Deadline 輪長 | 單輪配置欄位表及非法設定例子 |
| D02 | ServiceConfig／Deadline 輸入 | 指定 Tag、最低 payload、服務識別；最後 Slot 或其他輸入如何換成從全域 0 起算的絕對排他 ns；最晚 Deadline 可等於輪末 | 15／20 s 同時啟動範例、期限邊界案例；不重問已定 `< deadline` |
| D03 | Tag／Access／EnvironmentConfig 形狀 | 依模組所需整理欄位、單位、型別與必填項；明確標出尚缺來源的實體值，不塞任意預設 | 共用 Config 清單與參數來源欄；數值可在相應模組前補齊 |
| D04 | Observation／Action／Result DTO | 具體欄位與誰可見／誰建立；唯讀巢狀集合、ID 型別及排序；區分 accepted／NO_OP／invalid 結果，內部計畫不暴露未來真值 | 生產者→消費者對照、範例資料及預期錯誤結果 |
| D05 | 資料驗證及 Trace 契約 | Config 錯誤在哪裡拒絕、Action 如何保留原始內容交 Validator；payload／事件身分欄位、序列化及關鍵 Trace 比對項 | 最小斷言情境、錯誤碼與快照格式草案 |

D01–D05 是討論包，不是要求先核准每個欄位才繼續。`contracts.py` 與具體路徑尚屬建議，可在第一份完整欄位草案中一併提出。`frozen=True`／tuple 等是達成既定唯讀要求的實作建議；需以情境驗證，不能當成深層不可變的已驗證保證。

## 二、依賴模組實作前處理

| 編號 | 模組／主題 | 未決配置或語意 | 時機 |
|---|---|---|---|
| M01 | 首版參數來源策略 | Q-TRADEOFFS-01 尚未回答：synthetic 測試 fixture 優先，或先補有來源的正式參數；各 fixture 的驗收範圍必須明示 | 第一個需要具體時長／功率／PHY 數值的模組前 |
| M02 | Tag／Energy | 容量、各模式功耗、啟動成本、EH／反射分流、功率到 EH 的關係；非傳輸期間電量耗盡後的模式／喚醒規則 | 能量模組前；不可默默把負能量裁零後繼續運作 |
| M03 | 固定接入／PHY 時序 | 合法 TBS、header／payload 映射、BD/SFS、CFA 實際資源表與確定性分配、同批起點／持續時間、Paging／Msg2／Guard 時長及 ns 取整 | Access／Validator 依賴前；來源先查規範索引再核原文 |
| M04 | ResourceTimeline／Channel | UE／DU 情境參數、跨窗通道更新／相關性、PHY 成功抽樣；功率預告精確時點、首窗初始化、RNG stream 分離 | 環境模組前；本窗 SNR 固定與資訊隔離已定，不重問 |
| M05 | Payload／ServiceManager | 新 payload 的產生與唯一 ID、內容符合哪些服務、重傳身分及跨期去重範圍；TBS 與有效新 bit 的實際關係 | 計帳模組前；共享與需求上限／比例認列已定 |
| M06 | Engine 邊界整合 | 服務週期交界若落在 DU Window 或已開始批次內如何處理；最後 run 終點的既有事件結算與禁止新決策的確切規則 | 引擎整合前；完整服務週期數停止並未自動回答物理批次跨期問題 |
| M07 | 執行環境與導讀交付 | 選定專案 Python/kernel、補足 Notebook 套件、案例與 Trace 儲存位置；每模組列具體情境和預期值 | 首個 Notebook 執行前及各模組開始時；逐模組測試／人工接受流程已定，不重問 |

2026-10-20 的 Python 套件 metadata 觀察只作環境線索，真正執行前需重新確認選用 kernel，不能把舊探測當作當前可執行證據。未安裝任何套件。

## 三、正式研究／演算法比較前處理

| 編號 | 主題 | 尚需完成的決策或證據 |
|---|---|---|
| R01 | Baseline 完整規則 | 排序、tie-break、TBS 調整、共享 Tag 是否額外加分；不能讓最小測試 Policy 冒充正式 Baseline |
| R02 | 公平性彙整 | 跨服務正規化分母、最差服務的評估集合與未達標服務呈現；主目標與服務內 Max–Min 方向已定 |
| R03 | 正式負載及科學驗證 | 有來源的 PHY／EH 校準、通道／理想觀測敏感度、負載分布、多 Seed、信賴區間與消融；研究假設不能當作 3GPP 既定事實 |
| R04 | AI 方法 | 僅在研究需求明確引入時討論；目前不為 AI 提前建立訓練架構 |

## 建議後續閱讀順序

先提供 D01＋D02 的欄位與「兩週期」完整範例，集中呈現要確認的週期長度／Deadline 表示。接著給 D03–D05 的資料契約表。具體參數在 M01–M07 所列時點逐項補齊；研究項目留到研究階段。

下一步仍是設計討論；本輪沒有建立／執行 Notebook 或模擬器，也沒有登記開發 workflow、建立 change、Issue/PR 或發布。OpenSpec CLI 於 2026-10-22 實際回傳空 changes。

2026-10-22 更新：D01／D02 已有 [兩週期欄位與輸入範例](service-config-example.md)，待人類閱讀；這是草案產出，不表示 D01／D02 已決策完成或情境測試通過。

2026-10-23 更新：DU Window 固定 600 ms，M04 不再預設生成可變 Window 長度；起點／間隔仍未決。Q-DESCRIPTION-02 已答 A：單項服務「至少 10～15 s 起」代表完成 Deadline，非共同 Service Cycle 或已定 Deadline 分布。回到 D01/D02 的 Q-DECISION-03；各期共同週期長度仍未決。100 ms 舊例已改為秒級說明例，數值非正式配置。

Current resource revision: R-01 section 58 sets seven Tags and seven fixed SFS values at tau. The numerical mapping gap is closed; older eight-resource statements are historical.

## 2026-11-03 | First-version reception simplification accepted

R-01 section 64 supersedes the earlier first-version RANDOM/FBL mapping.
Retain CW/zone classes: RELIABLE succeeds, UNREACHABLE fails, RANDOM uses constant packet-success probability p_rx.
The user selected revised Q-INFLUENCE-33 A. No numerical p_rx is accepted yet.
CRC/FEC overhead remains in duration and energy; within-class TBS/SINR decoder reliability is excluded.
Q-INFLUENCE-34 is open: proposed p_rx=0.5 research baseline versus a user-specified constant.
The proposal is not empirical calibration. Existing source still uses FBL; implementation is pending.

## 2026-11-03 | Reception aligned with prior CW table

R-01 section 65 records the custom Q-INFLUENCE-34 answer. Preserve LOW near/middle/far=RELIABLE/RANDOM/UNREACHABLE,
MEDIUM=RELIABLE/RELIABLE/RANDOM, HIGH=RELIABLE/RELIABLE/RELIABLE. No independent 50-percent setting is accepted.
The prior table specifies RANDOM qualitatively; numerical entries remain open before sampler implementation.
One shared constant versus separate entries is not decided. Section 64's shared-constant requirement is superseded.
FBL stays disabled; preserve CRC/FEC overhead and stored-energy admission. No source/runtime change. Influence stays 34.

## 2026-11-03 | Original hybrid reception restored

R-01 section 66 supersedes the earlier no-FBL and fixed-RANDOM-value discussion.
Q-INFLUENCE-35 A: retain RELIABLE success 1, UNREACHABLE success 0 and RANDOM success 1-epsilon_FBL(rho,k,n).
CW/zone classes stay unchanged. No extra constant probability, second FBL factor or arbitrary coding gain.
Existing channel source already implements this classification. Selected-TBS k/n/rho mapping still needs preparation and verification.
CRC/FEC time/energy overhead and all admission/accounting rules remain. Influence stays 35; no new question or code change.

## 2026-11-03 | Remaining decisions audited

Current discussion scope: five model/profile groups (AP-05 FBL mapping, AP-06 ns conversion, EN-01 source profile,
EN-02 Tag hardware profile, EN-03 depletion/wakeup) plus four later study groups (SI-01, BL-01, FA-01, EX-01).
These are nine discussion groups, not a fixed question count. Eleven work packages include two agent-owned reviews: AP-02 and AP-04.
Q-INFLUENCE-36 remains open; the Notebook note request did not accept either CRC/FBL interpretation.
The power-table/FBL hybrid is settled; no independent RANDOM probability is needed.
Plan/decision-inventory.md contains the current ordered snapshot. Influence stays 36; no new question or implementation.

## 2026-11-03 | FBL and conversion selected; energy-source discussion begins

R-01 sections 67-68: Q-INFLUENCE-36 A selects k=8*N,n=3*(8*N+16). UE-style ceil-to-ms conversion is accepted.
Complete D2R occupancy is 35/63/118/228 ms. Preserve nominal tables, cumulative Paging prefixes, seven-message 12 ms and exact 200-us Guard.
Three current energy discussion groups remain, plus four later study groups. AP-05/AP-06 source calibration and implementation checks remain preparation.
Q-INFLUENCE-37 asks whether harvesting counts serving-cell communication sources only or all configured compatible active sources.
No source scope, carrier, transmit powers, UE geometry or hardware curve is selected by the question.

## 2026-11-03 | Serving-cell harvesting scope accepted

R-01 section 69: Q-INFLUENCE-37 A counts only the serving DU and its configured communicating UE sources.
Use DU-to-Tag for DL and UE-to-Tag for UL; exclude neighbor harvesting contributions without changing reception interference.
Carrier-profile Q-INFLUENCE-38 is open: equivalent 915-MHz research carrier vs explicit NR-band communication sources.
No carrier, UE count/position, transmit power or compatible nonlinear hardware curve is accepted yet. Influence 38.

## 2026-11-03 | Equivalent carrier accepted; dual-frequency coexistence explored

R-01 section 70: Q-INFLUENCE-38 A selects the equivalent 915-MHz research communication carrier.
The user also requests literature on concurrent 3.5-GHz and 915-MHz operation and frequency isolation.
This is exploration only: no simultaneous UE-phase CW, D2R harvesting or zero-interference assumption is accepted.
Evidence: AgentDoc/openspec/discuss/2026-11-03-dual-frequency-coexistence.md.
Source powers, UE geometry and compatible harvesting hardware remain open. Influence stays 38; no new question or implementation.

## 2026-11-03 | RF hardware evidence and transition clarification

R-01 section 71 records the user-confirmed UE-end -> RF transition -> Tag-band procedure.
The transition is inside the 600-ms window, before Tag-band operations, and separate from the 200-us final Guard.
No duration is selected; no source-free harvesting credit or extra payload is assumed during transition.
ReferDoc/Plan/RF_Hardware_and_Frequency_Switching_Evidence.md records TMTT/NSDI hardware evidence and X310/SBX/AD9361 official links.
The future Notebook must show the transition interval, remaining Tag budget and evidence limits.
No simultaneous dual-band requirement or change to the equivalent 915-MHz profile is introduced. Influence stays 38.

## 2026-11-03 | Source-power time dependence under discussion

Q-INFLUENCE-39: A separately configured fixed-per-run DU/UE communication powers vs B external per-Window powers; no answer or numerical value.
Preserve R-01 section 32's one logical UE per DU without coordinates. New UL harvesting needs independent traceable link-gain input, not an invented UE position.
Communication powers do not automatically equal D2R CW tiers. Policy actions stay Tag/TBS. Influence 39; no source changes.

## 2026-11-03 | DU per-Window power; UE fixed power

R-01 section 72: DU communication transmit power is configured per Window; each UE uses fixed configured transmit power.
DL harvesting uses DU power; UL uses UE power. No source-power Policy action or within-Window power-control algorithm is added.
Q-INFLUENCE-40 asks whether communication and CW share a common Window power state; exact dBm remain unselected.
Influence 40. Existing resource/source, RF transition and reception rules remain unchanged. No code change.

## 2026-11-03 | Shared Window state and proposed RedCap/SUL source

R-01 section 73: DU communication and CW share LOW/MEDIUM/HIGH state, with distinct configured numerical mappings allowed. UE power stays fixed.
The user proposes RedCap UE characteristics and possible SUL transmission. Its source role is open under Q-INFLUENCE-41.
SUL is a supplementary communication uplink, not inherently a high-power or energy-only carrier. Capability and supported band combinations must be declared.
Keep the accepted equivalent 915-MHz abstraction and continuous-prefix research assumption unless explicitly revised. Influence 41; no code change.

## 2026-11-03 | Ordinary SUL source accepted; remaining inventory reconciled

R-01 section 74 accepts Q-INFLUENCE-41 A: ordinary scheduled SUL UL traffic from a suitably capable RedCap UE profile supplies RF for Tag harvesting.
No dedicated UE energy waveform or actual NR carrier is selected. Equivalent 915 MHz and fixed configured UE power remain research assumptions.
Remaining current groups: source/RF numerical operating profile (including RF transition duration), Tag hardware/energy profile and depletion/wakeup.
Four later groups remain scenario/integration, baseline, fairness and experiments. Seven discussion groups are not seven fixed questions.
AP-02/04/05/06 source/contract/schedule/validation work is agent-owned preparation. Influence stays 41; no new question or implementation.

## 2026-11-03 | EN-01 source/RF candidate for consolidated review

Q-INFLUENCE-42 is open: adopt or adjust ReferDoc/Plan/EN01_Source_RF_Profile_Candidate.md.
The synthetic candidate proposes DU DL 18/24/30 dBm, UE 20 dBm, common -50-dB UL gain and 1-ms RF transition; retained CW values are -2/10/22 dBm.
No new numerical value is accepted or implemented. One-way DL gains retain the accepted prototype reference; incident RF examples are not battery increments.
The UL equal-gain assumption and switching budget are research settings, not literature measurements. EN-02 hardware/energy choices remain open.
Influence 42; no code/runtime tests or calibration.

## 2026-11-03 | Source/RF baseline accepted; Tag energy profile starts

R-01 section 75 records Q-INFLUENCE-42 A. EN01_Source_RF_Profile_Candidate.md now records accepted source-rf-synthetic-v0.1 values.
Two current groups remain: Tag hardware/energy profile and low-energy recovery, plus four later study groups.
Q-INFLUENCE-43 is open: use a hardware-data table with piecewise interpolation or fit a normalized logistic RF-to-DC curve.
Both are nonlinear; no curve data, capacity or mode-cost numbers are accepted yet. Influence 43; no runtime/default changes.

## 2026-11-03 | Named charging-model paper required

R-01 section 76 supersedes Q-INFLUENCE-43's generic A/B choice with the user's named reference:
Throughput Optimization for Ambient IoT Systems in Indoor Factory Environments, WCSP 2025, DOI 10.1109/WCSP68525.2025.1010215.
Publisher metadata/abstract is verified; exact charging equations and coefficients are unavailable. Request a PDF or the relevant equation pages.
Preserve UE-prefix-only harvesting, persistent finite storage and stored-energy admission; do not silently import the paper's factory scenario or all parameters.
Report any conflict with the previous nonlinear assumption after inspecting the original. Influence stays 43; no implementation.

## 2026-11-03 | WCSP original inspected; zero-input correction proposed

R-01 section 77 and WCSP2025_Charging_Model_Mapping.md verify the user-provided paper's unnormalized Sigmoid (equation 3) and finite-capacity energy update (equation 5).
The raw formula has nonzero DC output at zero RF input. Table I coefficients have incomplete individual unit labels and are not transferred to our low-power profile.
Q-INFLUENCE-44 proposes zero-input correction plus newly supported passive parameters; no answer or Tag numerical values yet. Influence 44.
Preserve UE-prefix-only harvesting, event-based mode/startup costs, stored-energy admission and accepted source/timing profile. No code changes.
