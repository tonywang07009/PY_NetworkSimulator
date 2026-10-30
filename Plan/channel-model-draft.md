# 通道模型整合草案

日期：2026-10-29。核心判定與entry pack測試值已確認。Notebook原型已建立，正式校準仍待後續。

## 1. 已確認的模型條件

| 項目 | 已確認內容 |
|---|---|
| 拓樸 | 沿用固定平面IAB拓樸 |
| 距離 | 使用Tag到所屬Node的實際距離 |
| 反射能力 | 所有Tag共用固定beta；原型為0.1，正式校準另定 |
| 調變 | 固定BPSK，採相干接收 |
| 自身CW殘餘干擾 | 0 W |
| 外部干擾 | 每Node配置固定等效功率；一輪內不變 |
| 窗級變動 | 同Node共用dB偏移 |
| 偏移分布 | Uniform(-3 dB,+3 dB)，屬測試設定 |
| 同窗行為 | SNR固定，不因Paging／Guard重抽 |
| 跨窗行為 | 獨立更新共同因子，品質要有變化 |
| CW控制 | 系統按Window提供功率設定 |
| Policy | 只選Tag與TBS，不選CW功率 |
| 品質排序 | 同Node／同Window近區優於遠區 |

來源與限制見[公式依據](channel-formula-evidence.md)。
接受的決策見[R-01第33節](../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md)。

## 2. 已確認的接收目標

| 系統CW檔位 | 近區 | 中區 | 遠區 |
|---|---|---|---|
| 低 | 成功 | 隨機成功／失敗 | 失敗 |
| 中 | 成功 | 成功 | 隨機成功／失敗 |
| 高 | 成功 | 成功 | 成功 |

- 成功的目標掉包率為0。
- 失敗的目標掉包率為1。
- 隨機類的目標掉包率介於0與1。
- 中區要進入可靠接收，CW須升到中檔。
- 單靠±3dB不可觸發這項轉換。
- 此表只描述具備傳送條件的PHY接收。
- 能量、時間及接入限制仍獨立檢查。
- 系統不一定採低→中→高的固定順序。

## 3. 功率與品質計算骨架

候選單程增益：

\[
\bar g(d)=g_0(d/d_0)^{-\eta}.
\]

候選窗級因子：

\[
\delta_{j,w}\sim U(-3,3)\ \mathrm{dB},\qquad
a_{j,w}=10^{\delta_{j,w}/10}.
\]

若因子作用於整條反射功率鏈路：

\[
P_{\mathrm{rx},k,w}
=P_{\mathrm{CW},j,w}\beta\bar g(d_k)^2 a_{j,w}.
\]

\[
\mathrm{SNR}=P_{\mathrm{rx}}/N,\qquad
\mathrm{SINR}=P_{\mathrm{rx}}/(N+I_j).
\]

- g0是參考功率增益。
- d0是參考距離。
- eta控制單程損失隨距離增加的速度。
- 整條鏈路只能乘一次a。
- 單程EH若共用此傳播假設，需核對sqrt(a)。
- 雙程偏移不可完整重複加到單程EH。
- 功率先使用線性單位，再轉dB。
- 有效最小距離及正式參數尚未定案。

## 4. 有限碼長骨架

\[
\epsilon_{\mathrm{FBL}}
\approx Q\!\left(\frac{nC(\rho)-k}{\sqrt{nV(\rho)}}\right).
\]

- k是資訊bit數。
- n是資料碼字的通道使用次數。
- rho須符合所選BPSK接收器的定義。
- C與V須匹配二元輸入。
- 此近似不是特定規範碼的實測BLER。
- CRC、重複、SFS及ambles不能混成新payload。
- TBS到k／n及時間的映射仍待封閉。

## 5. 已確認：功率表優先

1. 系統按CW檔位及TagZone選接收類別。
2. 成功類使用掉包率0。
3. 失敗類使用掉包率1。
4. 隨機類使用FBL近似。
5. PHY在封包完成時產生一次結果。

- 距離仍影響SNR與隨機類錯誤率。
- 0／1類別由研究規則決定。
- 系統不修改SNR來迎合分類。
- 先前的純SINR分段骨架已被取代。
- 原始FBL估計與最終掉包率分開保留。
- 具體綁定方式見[鏈路對照](channel-link-binding.md)。

## 6. 待設計的最小資料流

- Topology提供距離、所屬Node及TagZone。
- 系統配置提供當窗CW檔位及實際功率。
- Channel提供當窗接收功率、SNR及SINR。
- Access提供k、n、傳送時間與格式識別。
- PHY依接受的規則計算掉包率。
- Engine在唯一完成事件提交結果。
- Service只認列成功的新payload。

這些是責任界線，不是已存在的函式名稱。

## 7. 後續須封閉的內容

開發前的必要確認已集中整理於[開發起始清單](channel-development-entry.md)。正式校準及完整Access映射可延後，不以它們阻擋明標測試輸入的原型。

候選數值與距離方案已寫入[開發起始表](channel-entry-pack.md)。測試配置已接受，Notebook原型已建立。

- 原型已接受：CW=-2／10／22dBm、915MHz、beta0.1、路損指數2。
- 原型已接受：有效距離1～50m、超界拒絕及接收器參數。
- 原型已接受：跨Node獨立偏移、分離seed及明列k/n。
- 後續須整合：合法TBS、CRC、編碼及SFS配置。
- 後續須整合：TBS到k／n及時間的單位對應。
- 正式實驗前需評估：場域校準與理論近似的適用範圍。

Channel Notebook已人工接受，核心已抽離至src/channel/。
本草案不是實作完成或研究驗證證明。
