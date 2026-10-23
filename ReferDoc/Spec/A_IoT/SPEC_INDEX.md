# Ambient IoT（A-IoT）3GPP 規範索引

Agent 查詢入口：[`../spec_index.json`](../spec_index.json)；查詢方式見[主目錄 README](../README.md)。

依 `ReferDoc/DesignSimluator/Standards and Research Guide for an IAB-Based MAC_Protocol Simulator with Ambient-IoT Extensions.pdf` 及此目錄現有 PDF 整理。收錄範圍限 3GPP TS/TR。L1/L2/L3 是模擬器功能對照方式，不是嚴格 OSI 分層；TS/TR 也會跨越多層。

本機 A-IoT 規範以 Release 19 RAN/MAC 為主。既有 TS 23.369、TS 24.369 是 Release 20，列作核心網補充資料；在確認與 R19 模型的互通邊界前，不應把它們當作同一個 R19 profile。

## L1：PHY、Tag/Reader/CW 無線要求

| 本地文件 | 版本與特性 | 模擬器對應 |
|---|---|---|
| [TS 38.291](TS38291_PHY.pdf) | V19.3.0；A-IoT PHY 程序與物理傳輸格式。 | abstract PHY 可依 MAC grant 計算傳輸時間、可解碼結果或接收 bits；不代表實作波形、coding 或 RF。 |
| [TS 38.191](TS_138_191_v19.0.0.pdf) | V19.0.0；Ambient IoT device radio transmission/reception。 | Tag/device RF 需求參考，非 MAC 模擬器執行項目。 |
| [TS 38.194](TS_138_194_v19.0.0.pdf) | V19.0.0；A-IoT BS 與 Carrier-Wave node radio transmission/reception。 | Reader/CW RF 需求參考；不由抽象 PHY 驗證。 |
| [TR 38.769](TR38769.pdf) | V19.0.0；NR 支援 Ambient IoT 的 RAN solutions study。 | PHY/MAC/RAN 設計背景，屬 informative TR。 |
| [TR 38.848](TR38848.pdf) | V18.0.0；較早期的 RAN Ambient IoT study。 | 歷史研究背景；Release 19 規範應優先於此報告。 |

## L2：A-IoT MAC、存取流程與 D2R grant

| 本地文件 | 版本與特性 | 模擬器對應 |
|---|---|---|
| [TS 38.391 V19.4.0](TS_138_391_v19.4.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138391/19.04.00_60/ts_138391v190400p.pdf) | 目前採用的 R19 MAC 版本；包括 Paging、CFA/CBRA、Msg1/Msg2、D2R Scheduling Info、D2R MAC PDU 與 segmentation。 | Tag 存取流程、grant 欄位與 MAC 狀態機的主要規範依據。Msg2 的 D2R Scheduling Info 為 24 bits，且由該 Msg2 的 1–8 個 ID entries 共用；若每 Tag 需要不同 grant，應安排不同 grant-bearing message。CBRA Paging 的 D2R Scheduling Info 是另一個 18-bit 欄位，請勿混淆。 |
| [TS 38.391 V19.3.0（歷史版本）](TS_138_391_v19.3.0_historical.pdf) | 既有較舊版本；保留作為版本差異追溯。 | 新整理與規範判讀請優先使用 V19.4.0。 |
| [TR 38.769](TR38769.pdf)、[TR 38.848](TR38848.pdf) | RAN study reports。 | 可作 PHY/MAC 方案背景，不取代 TS 38.291/38.391 的規範語義。 |

## L3：服務需求、核心網架構與控制程序

| 本地文件 | 版本與特性 | 模擬器對應 |
|---|---|---|
| [TS 22.369](TS_22_369_v19.3.0.pdf) | V19.3.0；Ambient power-enabled IoT service requirements，Stage 1。 | 服務需求與用途邊界。原檔名 `TR22369.pdf` 與文件類型不符，已按 PDF 首頁更正為 TS 22.369。 |
| [TR 22.840](TR22840.pdf) | V19.0.0；Ambient power-enabled IoT study。 | Stage 1 服務與需求背景，informative。 |
| [TR 23.700-13](TR23700.pdf) | V19.0.0；A-IoT architecture support study。 | 核心網架構方案來源，informative；與後續 TS 23.369 分開判讀。 |
| [TS 23.369](TS23369.pdf) | V20.0.0；A-IoT architecture support，Stage 2，Release 20。 | 核心網架構補充資料；與 R19 RAN/MAC 版本不同代，互通映射 [Needs Verification]。 |
| [TS 24.369](TS24369.pdf) | V20.0.0；5GS Ambient IoT NAS protocol，Stage 3，Release 20。 | 若模型含 NAS signaling 才需實作；目前只作核心網協定參考，且與 R19 RAN profile 跨版本。 |
| [TS 29.369](TS29369.pdf) | V19.3.0；5GS Ambient IoT Data Management Services，Stage 3。 | AIoT service/core data-management API 的規範參考。 |
| [TS 33.369](TS33369.pdf) | V19.3.0；isolated private networks 的 AIoT security。 | 只有模擬安全程序時才納入。 |
| [TS 38.413 V19.4.0](TS_138_413_v19.4.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138400_138499/138413/19.04.00_60/ts_138413v190400p.pdf) | NGAP；包含 Ambient IoT procedures，例如 Inventory Request/Report。 | 若要模擬標準 gNB↔core 服務請求，可依 NGAP 建模；最佳化實驗可先用明確標註的 service API 抽象。 |
| [TS 38.300 V19.4.0（共用 IAB 文件）](../IAB/TS_138_300_v19.4.0.pdf) · [ETSI 原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138300/19.04.00_60/ts_138300v190400p.pdf) | RAN Stage 2 的 A-IoT 架構與 IAB 共用。 | 規範 A-IoT RAN stack 與 IAB/A-IoT 組合邊界；指南指出 R19 A-IoT 不支援 split-gNB，Reader 與 IAB-DU 共置屬研究延伸。 |

## 規範邊界

- R19 A-IoT MAC/PHY/RAN 以 TS 38.391、TS 38.291、TS 38.300 與 TS 38.413 為主要依據；TR 只用來理解研究背景，不能當成 normative requirement。
- Tag energy harvesting、fairness/deadline scheduler、CW/Reader 共置，以及把 Tag Reader 放進 IAB-DU 都是模擬器/研究模型選擇，不應標成 TS 要求。
- TS 23.369 與 TS 24.369 本地檔為 R20，而核心 RAN 參考為 R19；R20 核心網程序如何映射到此 R19 profile 尚未核實。
- 現有 `README.md` 保留實驗環境與證據說明；本索引只整理規範版本、層級與標準特性。
