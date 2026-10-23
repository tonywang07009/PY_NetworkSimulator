# 戶外 A-IoT：部署距離與干擾數值的證據整理

查詢日期：2026-10-23。目標：為 1 Donor／5 IAB Nodes、每 Node 1 UE／多 Tag、CW-Reader 共址的室外農場研究場景尋找距離與干擾依據。使用者已選室外研究配置，不直接套完整 D1 室內模型；IAB-DU Reader 整合仍為研究擴充。

**結論**：有可用的 3GPP 設計目標、共址自干擾分析、農場實測與 IEEE 分析論文，但沒有在本次已閱讀資料中找到一組能直接保證本場景「某固定半徑＋好／中／差各固定干擾 dBm」的通用參數。首個拓撲原型可以參數化幾何半徑與精確分區數量；正式通訊可達性仍需頻段、天線、CW 功率、Tag 電路、接收帶寬及干擾來源共同決定。

## 查詢範圍與證據等級

- 先查 `ReferDoc/Spec/spec_index.json`，讀本地 TR 38.848 V18.0.0、TR 38.769 V19.0.0 的指定條款，不把 TR 視為具約束力的 TS 覆蓋保證。
- 搜尋 IEEE 原出版資訊、大學作者版／機構典藏、3GPP／ETSI 原文；具體數值只取已閱讀的原文，不靠摘要、專利或二手網站推導參數。
- 代表關鍵字：`ambient IoT outdoor coverage interference dBm`、`monostatic backscatter outdoor range`、`LoRa Backscatter farm`、`LoRea monostatic`、`3GPP TR 38.848 coverage`。
- 本文是一份有範圍的調查，不宣稱文獻搜羅完整，也不聲稱讀過的本地規範版次就是截至今日的最新版。

## 距離：目標、模擬與實測不能混用

| 來源／位置 | 核到的量化結果 | 證據性質與本場景適用限制 |
|---|---|---|
| [3GPP TR 38.848 V18.0.0](../../ReferDoc/Spec/A_IoT/TR38848.pdf) §5.3，印刷 p.17；§4.2.2.4，p.15 | 戶外最大通訊距離的設計目標範圍為 **50–500 m**，室內為 10–50 m；戶外裝置／基地台情境為 Deployment scenario 4 | 是按裝置能力與場景可再選定的目標範圍，非實測半徑或所有被動 Tag 都能達 500 m。明確註記需進一步研究 sensitivity、BLER、power 等 |
| [LoRea，ACM SenSys 2017 作者版](../../ReferDoc/Literature/A_IoT/LoRea_SenSys2017_author.pdf) §4.5，PDF p.12；[作者來源](https://uu.diva-portal.org/smash/get/diva2:1163386/FULLTEXT01.pdf) | 戶外比較實驗中，商用 Impinj Speedway R420＋WISP 5.0 約 **17 m** 最大距離；載波設定 **26 dBm**，天線與 Tag 約離地 1 m，WISP **外部供電**以免採能範圍限制 | 實際戶外通訊實驗，但不是 3GPP PHY，且未證明無電池 Tag 在該距離有足夠 RF 採能。功率設定不可自行當成 EIRP |
| 同份 LoRea §4.1／§4.5 | 報告 Tag 到載波源、Tag 到接收器皆約 **75 m** 的等距結果；還有載波源靠近 Tag 時的公里級結果 | **不是實際 CW／Reader 共址的 75 m 保證**。作者 §4.5 明述因自干擾無法用 monostatic setup，透過分離 Tx／Rx 且與 Tag 等距來模擬等效路損；不能消除本場景共址自干擾的難題 |
| [LoRa Backscatter，ACM IMWUT 2017](../../ReferDoc/Literature/A_IoT/LoRa_Backscatter_IMWUT2017_author.pdf) §6.1.2、Fig.15，PDF pp.19–20；[作者來源](https://longrange.cs.washington.edu/files/loRaBackscatter.pdf) | 一英畝蔬菜農場 **4,046 m²**；20 個測點，LoS／NLoS 混合；中位 RSSI **−137 dBm**、最低 **−143 dBm** | 真實農場部署；RF source 與 receiver 位於農場兩端，Tag 置於植物／灌木間地面，使用 1 MHz 頻移。**bistatic、LoRa/CSS，面積不是圓形半徑，RSSI 不是干擾功率**。不能把 2.8 km／475 m 或此面積套成本場景共址服務半徑 |
| [Al-Nahari et al., IEEE TCCN 12 (2026), pp.2369–2382](../../ReferDoc/Literature/A_IoT/Ambient_IoT_Topologies_TCCN2026.pdf) §IV-A，印刷 p.2376；[DOI](https://doi.org/10.1109/TCCN.2025.3586219) | 分析／Monte Carlo 範例採 **915 MHz、P=30 dBm、path-loss exponent=3、d1=10 m、d2=3d1**；Fig.4 比較反射鏈路距離並固定 d2=40 m | 高品質 IEEE 期刊，適合比較拓撲、距離與 outage，但**不是戶外農場實測**。不同論文的 T1/T2/T3 定義須逐一映射，不能只按名稱套 3GPP；文中的固定指數是模型選擇，不是農場校準結果 |

LoRa Backscatter 出版資料為 Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies，Vol.1 No.3，Article105，2017；不要誤標為另一篇 SIGCOMM 論文。LoRea 為 SenSys 2017。兩者皆為可用的系統研究原文，但波形與硬體條件不同於本研究首版。

## 干擾：有數值，但量測位置與含義必須一致

### 3GPP 共址 CW 自干擾分析

來源：[TR 38.769 V19.0.0](../../ReferDoc/Spec/A_IoT/TR38769.pdf) §6.7.5.2.1，印刷 pp.180–182，尤其 Table 6.7.5.2.1-1；§6.7.5.1 分為空間隔離、類比消除及數位消除。這是研究報告中的公司分析，不是全體設備必需支援的測試設定。

| 數值 | 真正含義 | 不應如何使用 |
|---|---|---|
| 33 dBm／23 dBm | 分析考慮的 monostatic CW 發射功率，參考天線端 | 不是所有部署的指定 CW 功率，也不是 Node 接收干擾功率 |
| −74 dBm 或更低 | 此分析描述的微弱所需接收訊號尺度 | 不是好／中／差區的三個干擾等級 |
| CW=33 dBm、return loss=15 dB → 洩漏 **18 dBm** | 類比前端看到的強 CW 洩漏例子 | 不是 Tag 位置受到的空間外部干擾，也不是經全部消除後的殘餘干擾 |
| 洩漏18 dBm、容許約3 dB去敏 → LNA IIP3 約 **28 dBm** | 前端線性度／去敏分析，說明共址接收的硬體困難 | IIP3 不是接收干擾功率；3 dB去敏不是可直接指定的終端 SINR |
| 約40 dB CW cancellation，幅度誤差約0.09 dB、相位誤差約0.5° | 此章引用實作精度挑戰的例子 | 不是本場景自動具備的固定消除量或已校準參數 |

本地報告 §6.6 與 §8 明確主要研究 NR macro 在室外、A-IoT 系統在室內的鄰頻共存；不能把其所有共存結果直接改稱「農場純戶外的實測干擾」。共址硬體機制可參考，戶外幾何及多 Node 外部干擾仍需重新建模。

### IEEE 論文的噪聲設定

上述 IEEE TCCN §IV-A 採熱噪聲密度 **−174 dBm/Hz**、A-IoT 帶寬 **10 kHz**、另一接收帶寬 **1.4 MHz**。若只按該文 `N0*B` 換算（不額外加入未給定 NF），10 kHz 的熱噪聲約 **−134 dBm**，1.4 MHz 約 **−112.54 dBm**。

這是**噪聲**，不是別的 Node 或 UE 造成的干擾。真實接收器通常還需考慮所選 NF／濾波帶寬與前端限制，不能把兩種帶寬的功率直接比較，更不能當成本場景已選的接收帶寬。

對本研究較清楚的後續契約是分開保存：所需 D2R 訊號、其他發射源造成的有效帶內干擾、經隔離與消除後的等效殘餘 CW 影響、接收噪聲。若使用總 SINR，分母各功率先轉成相同帶寬、接收位置與線性單位；前端飽和／非線性去敏不一定能只靠一個加性干擾數字充分表達。

## 戶外通道：TR 38.901 是模型，不是 Tag 覆蓋半徑

已讀 [TR 38.901 V18.0.0 官方原文](https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/18.00.00_60/tr_138901v180000p.pdf) §7.2 RMa、Table7.2-3、§7.4.1 Table7.4.1-1。RMa 是農村宏站模型，預設 BS 高35 m／UT高1.5 m；表中 RMa 適用 BS 高度10–150 m、UT高度1–10 m，另有頻率及距離限制。**不能只因場景是農場就自動採用宏站35 m與公里級站距**；若 IAB Reader 高度低於10 m，不能不作說明直接套原 RMa 高度適用範圍。

正向 CW/R2D 與返回 D2R 的幾何／傳播路徑都要處理，且反射調變損失、Tag 天線／採能能力及殘餘自干擾另外決定是否可達；單程 NR 路損模型不是整條反射鏈路的 link budget。

## 文獻搜尋的存取限制與候選線索

- IEEE VTC2019-Spring，*Validation of Backscatter Link Budget Simulations with Measurements at 915 MHz and 2.4 GHz*，DOI [10.1109/VTCSpring.2019.8746365](https://doi.org/10.1109/VTCSpring.2019.8746365)：IEEE 出版摘要可查，指向戶外915 MHz／室內2.4 GHz 的 bistatic 量測；Xplore 完整頁遭驗證限制，未取得全文，**不引述其精確距離／干擾值**。
- IEEE WCNC2020，*Monostatic Backscatter Communication in Urban Microcellular Environment Using Cellular Networks*，DOI [10.1109/WCNC45663.2020.9120830](https://doi.org/10.1109/WCNC45663.2020.9120830)：[作者機構頁](https://research.aalto.fi/en/publications/monostatic-backscatter-communication-in-urban-microcellular-envir/) 已確認為3D ray tracing模擬，不因摘要稱 empirical 就改稱 RF 實測；未讀到全文，不擷取精確參數。
- 搜尋出較新 TR38.769 outdoor／Release20 章節的二手線索；本次未取到相應官方全文，不把其中50–200 m／50–500 m的裝置類別結論加入已核證參數表，也不聲稱本地V19.0.0是最新。
- ETSI 的TR38.848／38.769部分網路路徑不可讀；相關主張以已檢查的本地原文及版次為據，外部TR38.901可讀。IEEE作者機構PDF經核准的公開下載成功取得，原始網頁403不等於論文不存在。

## 對第一個拓撲原型的建議（未選定配置）

1. **幾何與通訊可達性分開**：TopologyConfig 提供每 Node 的部署半徑／區域、節點位置與Tag數量；不要把半徑內每個Tag都標成必定成功回傳。
2. **30 Tag 配額可精確驗收**：10好／13中／7差可作使用者情境輸入，但先確認「好／中／差」是幾何帶還是鏈路品質；沒有文獻直接支持本場景任意三個圓圈就是三個固定干擾dBm。
3. **半徑用配置及敏感度呈現**：可以討論50／100／200 m等戶外幾何候選尺度，但這些是工程探索取值，不是文獻已證明本場景能覆蓋；尚未獲使用者選定。不以最遠論文紀錄定單一正式值。
4. **實際定通訊半徑前需補**：頻段、CW發射功率／EIRP、Node／Tag天線高度與增益、Tag類型／反射損失、接收頻寬與性能／NF／可容許錯誤率、採能靈敏度及干擾來源。這些先列可替換參數，不要求拓撲原型立刻完成PHY校準。
5. **干擾先分來源再定值**：明確外部Node／UE／其他Tag干擾是否存在，以及共址CW殘餘是否理想消除；不能把Node–Tag有干擾直接等同遠Tag有更高外部干擾。

下一個仍可處理的拓撲決策為分區的幾何／鏈路品質含義；本次按使用者要求完成文獻查詢，沒有額外提出決策題，也沒有替使用者選半徑、功率或三區門檻。

## 可重查的來源檔

三份已讀原文儲存於 `ReferDoc/Literature/A_IoT/`，[來源URL／SHA-256 manifest](../../ReferDoc/Literature/A_IoT/outdoor-source-manifest-2026-10-23.json)。保存原始PDF，不修改其內容；引用與摘述依上述章節，未將全文拷入本文件。此次只做文件調查與算術核對，未實作拓撲或執行模擬器測試。
