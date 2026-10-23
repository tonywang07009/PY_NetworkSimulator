# IAB 3GPP 規範索引

Agent 查詢入口：[`../spec_index.json`](../spec_index.json)；查詢方式見[主目錄 README](../README.md)。

依 `ReferDoc/DesignSimluator/Standards and Research Guide for an IAB-Based MAC_Protocol Simulator with Ambient-IoT Extensions.pdf` 選取文件。收錄範圍是 3GPP TS/TR；Release 19 作為模擬器的 RAN 基準。指南用來界定模擬範圍，規範性描述以本地 TS/TR PDF 為準。索引中的 L1/L2/L3 是模擬器責任分層，方便對應程式模組，並非宣稱 3GPP 將每份規範嚴格歸屬單一 OSI 層。

## L1：無線資源與 PHY 邊界

| 本地文件 | 規範與特性 | 模擬器對應 |
|---|---|---|
| [TS 38.300 V19.4.0](TS_138_300_v19.4.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138300/19.04.00_60/ts_138300v190400p.pdf) | IAB 架構與資源設定；DU 時域資源含 Hard、Soft、Unavailable 狀態，並有 MT/DU 切換的 guard symbol 條件。 | 抽象 PHY 的可排程 symbol mask、Soft 資源可用條件與 guard 時間。此文件也涵蓋 L3 架構，屬跨層骨幹。 |
| [TS 38.174 V19.2.0](TS_138_174_v19.2.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138100_138199/138174/19.02.00_60/ts_138174v190200p.pdf) | IAB 無線傳輸與接收要求。 | RF/PHY 規範參考；目前設計採 abstract PHY，未實作波形、RF 或無線設備符合性。 |
| [TS 38.175 V19.0.0](TS_138_175_v19.0.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138100_138199/138175/19.00.00_60/ts_138175v190000p.pdf) | IAB 電磁相容性（EMC）。 | 設備符合性參考，不是目前 MAC/網路模擬器的執行模型。 |

## L2：MAC、RLC、BAP 與資料轉送

| 本地文件 | 規範與特性 | 模擬器對應 |
|---|---|---|
| [TS 38.321 V19.4.0](TS_138_321_v19.4.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138321/19.04.00_60/ts_138321v190400p.pdf) | NR MAC 程序與 IAB 相關控制，包括 timing offset、guard symbol，以及 beam/power 控制效果。 | 排程資源、IAB MT/DU 時序、guard 消耗；若不模擬 RF，可將 beam/power 控制保留為事件或 metadata。 |
| [TS 38.322 V19.3.0](TS_138_322_v19.3.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138322/19.03.00_60/ts_138322v190300p.pdf) | NR RLC；包括 AM/UM、分段/重組與重傳。 | 當模擬器追蹤 BH-RLC queue、傳輸量或重傳時採用。 |
| [TS 38.340 V19.0.0](TS_138_340_v19.0.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138340/19.00.00_60/ts_138340v190000p.pdf) | Backhaul Adaptation Protocol（BAP）：路由識別、下一跳與 BH-RLC 對映、封包轉送/本地終止、header 處理及 flow control。 | 多跳 IAB 的核心資料面；若只用 donor-to-node 單一理想化連線，會省略 BAP 路由與逐跳壅塞行為。 |
| [TS 38.323 V19.1.0](TS_138_323_v19.1.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138323/19.01.00_60/ts_138323v190100p.pdf) | NR PDCP。 | 補充規範；只有在模擬 UE bearer 的 PDCP 行為時才需要，並非多跳 IAB BAP/BH-RLC 最小資料面必要項。 |

## L3：架構、組態與控制介面

| 本地文件 | 規範與特性 | 模擬器對應 |
|---|---|---|
| [TS 38.401 V19.3.0](TS_138_401_v19.3.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138400_138499/138401/19.03.00_60/ts_138401v190300p.pdf) | NG-RAN/IAB 實體與介面關係、IAB node integration、BH-RLC 建立與回收流程。 | CU、DU、MT、donor 與 parent/child link 的責任歸屬及狀態轉換。 |
| [TS 38.331 V19.4.0](TS_138_331_v19.4.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138331/19.04.00_60/ts_138331v190400p.pdf) | RRC 組態；包括 BAP entity/address、預設 UL route、預設 BH-RLC 與 BH-RLC add/modify/release。 | 將 RRCReconfiguration 的狀態效果映射到 BAP、BH-RLC 與 IP 組態。 |
| [TS 38.470 V19.2.0](TS_138_470_v19.2.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138400_138499/138470/19.02.00_60/ts_138470v190200p.pdf) | F1 一般架構與原則。 | CU↔DU 控制/使用者面與 IAB transport configuration 的介面框架。 |
| [TS 38.473 V19.3.0](TS_138_473_v19.3.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138400_138499/138473/19.03.00_60/ts_138473v190300p.pdf) | F1AP 訊息與 IE；承載 IAB resource、BAP routing/mapping、BH-RLC 等組態。 | 可用 typed event/struct 表示控制效果；只有要求互通時才需要 ASN.1/PER 與 SCTP。 |
| [TS 38.474 V19.0.0](TS_138_474_v19.0.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138400_138499/138474/19.00.00_60/ts_138474v190000p.pdf) | F1 使用者面資料傳輸。 | 若要表示 F1-U 封包、QoS、佇列或延遲才納入；抽象 IAB 傳輸可先用邏輯流表示。 |
| [TS 38.423 V19.4.0](TS_138_423_v19.4.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138400_138499/138423/19.04.00_60/ts_138423v190400p.pdf) | XnAP；涵蓋 inter-donor/inter-CU 的 IAB transport migration 等流程。 | 單一 donor、固定拓樸可先不納入；模擬跨 donor migration 或拓樸調整時才需要。 |

## 跨層研究報告

| 本地文件 | 文件性質與用途 |
|---|---|
| [TR 38.874 V16.0.0](TR_138_874_v16.0.0.pdf) · [ATIS/3GPP partner PDF](https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.874.V1600.pdf) | IAB 原始研究報告；提供部署、排程、QoS 與拓樸議題背景。TR 是研究報告，不能當成規範性程序或排程目標。 |

## 版本與範圍註記

- 本地 RAN 規範選用 Release 19，以符合設計指南的模擬基準。TS 38.174 另有 Release 20 V20.0.0；此資料夾保留 R19 V19.2.0，避免把 R20 RF 變更混入 R19 模型。
- 設計指南列出的 TS 38.473 V19.4.0 在 ETSI 發布目錄找不到；截至 2026-10-15，R19 最新可下載版本是 V19.3.0，因此本地收錄 V19.3.0。
- 設計指南提到 TS 38.176；官方 IAB 規範清單列出 TS 38.174（radio transmission/reception）及 TS 38.175（EMC）。本索引收錄這兩份實際對應 IAB 的 TS，未把 38.176 當作 IAB 規範。
- 未隨目前 profile 下載的選配 TR： [TR 38.809](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=3746) 是官方 3GPP 頁面標示為 internal 的 RF 背景報告；TR 33.824 是 security study；[TR 28.875](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=4265) 是 IAB management study。抽象 PHY、未模擬安全與 OAM 的 profile 不依賴這些報告。

## 最小閱讀順序

1. TS 38.300：整體架構、IAB 資源與跨層邊界。
2. TS 38.401：node/介面角色與 BH-RLC 建立程序。
3. TS 38.331、38.340、38.322：組態、BAP 與逐跳回程資料面。
4. TS 38.321、38.470、38.473：資源排程與 CU/DU 控制介面。
5. 依研究範圍再讀 TS 38.474、38.423、38.323 或 RF/EMC 規範。
