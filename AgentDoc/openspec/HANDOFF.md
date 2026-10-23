# 任務交接

更新：2026-10-18。

1. 使用者選定此專案試用新版工作流，這一輪只要求完整移植，尚未指定實證功能；不必再追問先前的候選功能問題。後續使用者提出工作時，再依需求訪談。
2. 開始先讀 PROGRESS、本檔與 projects/py-networksimulator/spec.md、toolbox.md，從根目錄執行 OpenSpec CLI。實體根目錄仍是 AgentDoc/openspec，openspec 連結保留。
3. 已移植 18 個技能與共用資源，Archify 額外保留，共 19 個可探索入口。llm-wiki、skill-evolution 實體仍在 EvoSkill/skills；相對連結做路徑適配，沒有變更候選資格／啟用門檻。
4. 新規則入口為 agent.md；完整使用與恢復方法見 ../WORKFLOW_GUIDE.md 及 ../../.agents/workflow-kit/PROJECT-INSTALL.md。完整教材在 ../WorkflowKit/，management 與 course/sources 不是本專案活動政策。
5. 版本、來源檔／部署檔 hash、路徑對應、實際驗證與備份位置見 ../EvenStore/workflow-migration-2026-10-18.json。保留舊搬移證據，不能拿舊 hash 驗證這次已更新的技能。
6. 標準 install.py 會拒絕本專案既有 skill 符號連結，這是保護行為；不要刪除 EvoSkill 連結以強行升級。後續先在暫存根目錄展開新版，依移植紀錄比對／備份／適配，保留本地修改。
7. .gitignore 仍忽略 AgentDoc、ReferDoc、.agents；這些本機工作流與教材不會隨一般 git clone 攜帶。需要帶入遠端時另對齊版本控管策略；本輪沒有擅自解除 ignore。只新增根目錄 /AGENTS.md ignore，不影響 agent.md。
8. 保留原有 LICENSE、README.md 與其他 Git 修改。沒有新功能、Wiki、改善候選、個人狀態或遠端發布。使用者手動 merge；首個 change 需先確認真正的功能與驗收。

## 2026-10-20｜產品規劃討論交接

- 使用者要求先完整閱讀 ReferDoc/Plan，再討論如何實作；尚未授權 Notebook/Simulator 實作。兩份 Markdown 已讀完；本次依使用者答案補齊 R-01 決策來源。
- H-03b 已由使用者回答 A 確認：最大餘數法、餘額同分按 Tag ID 升序。R-01 已補第 25 節並註明取代第 21–24 節歷史未決狀態；與 Handoff 第 6 節對齊，實作／測試未開始。
- Q-DECISION-01 已回答 A：空 Action 為合法 NO_OP，停止本 Window 後續排程，下個 Window 再決策，時間／既有事件／自然能量照常；R-01 第 26 節與 Handoff 第 5 節已同步。不要重問 H-03b 或空 Action。
- Q-TRADEOFFS-01 未回答，使用者改為先規劃架構與工具；暫緩至相關模組實作前。不得推定選 A。synthetic fixtures 只能證明 Engine 行為，不證明 PHY/EH 科學有效性。原始三份 PDF 未於 ReferDoc 檔名查詢中找到。
- CLI changes 為空、workflow index 為空；尚未建立 change、Issue/PR 或登記工作流。原有 Git 修改保留。

## 最新交付流程與架構草案（2026-10-20）

- 使用者主動確認逐模組 Notebook 原型、對應情境測試、人類理解程式並接受後才轉 .py。以 R-01 第 27 節及 Handoff 置頂修訂取代整體 Notebook 全通過才開始任何轉檔的舊順序；五類整合測試義務仍保留。
- `docs/architecture/implementation-plan.md` 已列模組與工具建議；尚未實作或安裝依賴，沒有任何模組已獲人工接受。
- 首個可討論的模組是 Config／DTO：欄位、單位、型別、讀寫權限與對應情境。先對齊 Interface，再於啟動實作前解決相關配置及 kernel 環境；目前無須為架構再追加參數問卷。
- `docs/architecture/system.html` 為未實作的模組規劃圖，Archify 自動化四項 gates 通過，未人工視覺檢閱；receipt 見同目錄 system.finalize-summary.json。工具仍為 3.1.0，本輪僅提示可用 3.2.0，未升級。
- 使用者已指定共用 dataclass 集中於單一 `.py`，並回答 Q-INFLUENCE-01 的 A：Config／DTO／必要 Enum 同檔，內部 State 定義留各模組。R-01 第 28 節、交接規格及設計草案已同步，不重問此題。檔名 `contracts.py` 是建議，未建立程式檔。
- Q-TRADEOFFS-02 已答 A：Notebook 情境設定 cell 建立 dataclass Config 實例，每次 run 保存配置快照，不需先做外部 JSON 載入器。原 synthetic／正式參數題仍暫緩，不混為同題。
- Q-DECISION-02 已答 A：一次 run 完整跑完指定服務週期數；總時間由週期長度推得，不重設跨期電量。不是重啟 N 個滿電 run；不要重問停止方式。
- Q-INFLUENCE-02 於 2026-10-22 已答 B：Notebook 逐期明列服務設定，可相同或不同；不自行隨機生成服務需求。不重問此題；週期長度和實際數值未被選定。

## 2026-10-22｜剩餘議題清單

- 使用者本輪要求整理剩餘項目，不另提新決策題；題數未增加。
- 閱讀 `docs/architecture/remaining-discussion.md`：Config／DTO 定稿的 D01–D05、相關模組實作前的 M01–M07、研究階段的 R01–R04。這些是分組議題，非逐項審批清單；命名／欄位由代理先提出完整草案，只問影響模型或驗收的決策。
- 建議下一步提供 Simulation／ServiceCycle／ServiceConfig 的兩期完整欄位範例，再處理 Observation／Action／Result 交換資料。參數策略 Q-TRADEOFFS-01 仍暫緩，不能推定 synthetic 已獲選。
- 本輪僅文件整理；OpenSpec list 實際為空，沒有模擬器實作或測試證據。
- 已進一步產出 `docs/architecture/service-config-example.md`，供閱讀三層 Config 欄位與兩期範例。建議每期填 duration_ns、週期數由清單長度推得、Deadline 輸入相對本期 last_allowed_slot、整數 ID／跨期複合身分；這些未被使用者接受，不當成已決策。空服務週期是否允許仍未決；不另發起多題或啟動原型。
- 使用者要求整理下一個決策問題繼續；目前唯一新題 Q-DECISION-03 為服務週期長度：A 每期各填 duration_ns（建議）或 B 全 run 共用 cycle_duration_ns。等待答案；已更新 Decision/feedback 題數為 3/10，不捆綁詢問其他資料表示，也不開始原型。

## 2026-10-23｜固定 DU Window 與服務時間澄清

- 使用者明確指定 DU Window 長度固定 600 ms，R-01 第 29 節及 Handoff 規格已同步；Window 起點／間隔仍未定，不把固定持續時間當成固定重複間隔。
- Q-DESCRIPTION-02 已答 A：單項服務 10～15 s 起指完成 Deadline；Description 題數維持 2/10，不重問。Q-DECISION-03 仍未答，回到 A 每期共同服務需求週期各填長度／B 全 run 共用固定長度，沿用原題數，不推定選 A/B。
- Config 範例已換成秒級 Deadline；示例共同週期 20 s 明標未選定，不當正式配置或已接受參數。只核對文件算術／連結，沒有開始實作／模擬器測試。先前「未來 Window 長度不可知」須與固定長度配置對齊，不能藉此揭露未來起點／SNR／完整時序。

## 2026-10-23｜今日目標改為首個 IAB 拓撲模組

- 使用者最新指定今日要開始 IAB 網路拓撲模組：完成眼前 Q-DECISION-03 後，先盤點拓撲所需決策，再準備 Notebook 原型；此為優先順序調整，不能繼續無限擴充全部 Config 問卷。
- 當前只重述原 Q-DECISION-03 的 A 每期需求週期各填長度／B 全 run 固定長度，等待答案；不增加題數、不把服務 Deadline 的 A 誤認為本題已答。
- 下一階段沿用已決定的 IAB／Reader／Tag 模型，針對拓撲直接依賴項對齊範圍；不要為單純拓撲預先實作能量／PHY／AI。先前模組順序是建議，依新目標調整。尚未建立拓撲程式、Notebook 或 OpenSpec change。

## 最新：服務共同從 0 起算（2026-10-23）

- 使用者明確表示所有服務均從 0 開始，S1 Deadline 15 s、S2 20 s 為例；不得依清單排列將服務 2 延後開始。R-01 第 30 節、Handoff 置頂與舊兩期範例警示已同步。
- 現在唯一新待答 Q-DESCRIPTION-03：A 首版一個 run 只有一批全域 t=0 同時開始服務（依本次措辭建議），或 B 保留多期、每期全部服務相對當期起點為 0，全球時鐘不歸零。Description 題數為 3/10。未改寫 run 停止條件，未視為原 Q-DECISION-03 已答。
- 週期長度選擇先暫緩，釐清後就盤點 IAB 拓撲；若單批即可，不要求使用者先完成多週期設定。未開始任何模擬器程式。

## 目前生效：單輪 t=0＋最晚 Deadline，下一步拓撲（2026-10-23）

- 使用者答 Q-DESCRIPTION-03 的 A，並指定本輪長度取最大 Deadline，例 15／20 s → 20 s。R-01 第 31 節是目前首版時間權威，取代先前獨立週期數／多期依序啟動／手填共同週期長度。Q-DECISION-03 已被新需求取代，不再詢問 A/B。
- 最晚 Deadline 允許等於輪末；原嚴格 `d_i<T_cycle` 不適用首版，改為 `d_i<=T_round=max d_i`。但成功認列仍嚴格 `D2R_END<d_i`，不因輪末相等而寬放。原 100 ms／20 s 兩期文件已改成使用者的單輪 15／20 s 範例。
- 已轉入使用者今日優先 IAB 拓撲原型盤點。閱讀 `docs/architecture/iab-topology-scope.md` 六項主題、責任草案與測試候選；只問必要決策，不回頭擴充全部服務 Config 問卷。
- 目前待答 Q-NICHE-01：A 1 Donor／1 整合 Reader 的 IAB Node／若干 Tags（建議）；B 1 Donor／多個直接回傳 Donor 的 Nodes；C Node 經 Node 回傳的多跳。Niche 題數 1/10。UE 是否獨立表示、位置、Tag 數及關聯規則稍後處理，不捆綁本題。
- 本輪只做規格／討論文件；OpenSpec list 仍空，沒有拓撲程式、Notebook、模擬器測試或人類程式接受。已具體產出可審閱盤點，下一步依答案開始最小契約與驗收對齊。

## 目前生效：5 Nodes／5 UE／非均勻 Tag（2026-10-23）

- Q-NICHE-01 已具體回答 B：1 Donor 直連 5 IAB Nodes，各 1 UE／多個 Tags。Node 整合 Reader，Tag 隨機關聯／部署，Node 分處不同區域。使用者例子是全場 30 Tags，好10／中13／差7；不自行固定為每 Node 各30或強制均分，不默認抽樣機率或近鄰關聯。
- 使用者明確接受 IAB 支援 A-IoT split／DU Reader 的研究假設，CW／Reader 共址；回傳無干擾、Node–Tag 段有干擾。干擾來源／強度仍未決，不推論回傳零路損／零延遲或遠區干擾一定大。
- `ReferDoc/Plan/main.pdf` 11 頁已全文抽取、渲染閱讀第3／4頁。圖4是同心 Distance/SNR 示意，圖3是農場；無幾何尺度／干擾值，圖中2Nodes僅示例，不覆蓋本次5Nodes。工具用 /usr/bin Poppler，PATH MiKTeX 因只讀使用者設定失敗已避開，未安裝或改設定。
- 已核 TS 38.300 V19.4.0 §16.23.2：A-IoT split不支援；研究擴充須保留標示。TR38.769 §3.1 D1T1=Deployment1＋Topology1，Table4.2.1-1 的A2為CW與Reader同節點；TR38.848 §4.2.2.1 D1是室內。首版是否採農場室外但借T1/共址，或完整D1室內條件，為當前唯一待答 Q-DESCRIPTION-04，Description 4/10。
- 已用 domain-modeling 建立 CONTEXT.md 詞彙表、更新R-01第32節及拓撲盤點。不要重問已定規模；環境對齊後問分區幾何／品質、座標尺度、關聯與配額生成，避免提前實作PHY。無Notebook／程式／測試。

## 2026-10-23｜室外場景確認與文獻調查

- Q-DESCRIPTION-04 已回答 A：農場室外研究情境，借用 T1 直連／CW-Reader 共址意圖，不套完整 D1 室內參數；IAB-DU Reader 仍標研究擴充。取代上文待答狀態，Description 題數仍4/10。
- 已完成 `docs/architecture/outdoor-literature-evidence.md`，核對本地TR38.848／38.769、官方TR38.901、LoRea／LoRa Backscatter原文與IEEE TCCN2026。區分設計目標／實測／模擬、共址／分置、RSSI／噪聲／自干擾；不能直接定三區干擾dBm或保證半徑。
- 三份原文PDF及來源URL／SHA-256 manifest保存於 `ReferDoc/Literature/A_IoT/`。已同步訪談、R-01第32節與拓撲盤點；後續仍需對齊分區含義及幾何／抽樣，沒有替使用者選半徑、頻段、功率或門檻。本次沒有另提出決策題。
- OpenSpec list仍為空；只完成文件與來源調查，未建立拓撲Notebook／程式，未執行模擬器測試。保留既有無關Git修改，沒有commit／push／發布。

## 2026-10-23｜完美消除自干擾；距離語意待釐清

- 使用者指定Node完美消除自身CW殘餘自干擾，作為理想化研究假設：0 W，不是0 dBm；不建模該自干擾造成的前端去敏／飽和。其他來源干擾仍待定，CW傳播／採能保留。
- 下一題Q-DESCRIPTION-05：A距離影響實際接收SNR、固定PHY與目標錯誤率的成功門檻不額外隨距離提高（建議），或B另設遠區更高門檻。尚未回答，不能推定使用者已選幾何分區或門檻模型。Description目前5/10。
- 仍為原拓撲訪談，未建立Notebook／程式／測試；CLI changes及個人workflow索引均空，未進行登記或遠端操作。

## 2026-10-23｜距離語意已確認；分區定義待答

- Q-DESCRIPTION-05已回答A：距離影響實際接收SNR；同一PHY設定與目標錯誤率使用相同成功門檻，不另提高遠區門檻。取代上文待釐清狀態；完美消除自身CW殘餘自干擾仍生效。
- 下一題Q-DESCRIPTION-06：A依所屬Node距離定近／中／遠幾何區（建議，實際品質另算），或B依鏈路品質定好／中／差。10／13／7為全場配額例子；尚未選定其分區含義、半徑或品質門檻。Description目前6/10。
- 同步訪談、拓撲盤點與R-01；OpenSpec list仍空，沒有Notebook／程式／模擬器測試或遠端操作。

## 2026-10-23｜距離分區與品質排序約束

- Q-DESCRIPTION-06回答A附條件：按所屬Node距離分近／中／遠區，但近區品質須優於遠區，屬system model假設，不可僅當平均趨勢或允許任意反轉。先以同Node／同Window SNR比較，不推定跨Node排序；中區嚴格排序與差距仍未定。成功門檻不隨區域提高。
- Q-TRADEOFFS-03待答：首版三區外邊界10／30／50 m（建議工程起始配置）、20／60／100 m或自訂；不作已驗證覆蓋承諾。Description6/10，Tradeoffs3/10。
- 已同步訪談、拓撲盤點與R-01。仍為文件／訪談階段，沒有Notebook、程式或模擬器測試。

## 2026-10-23｜三區半徑已選定

- Q-TRADEOFFS-03已回答A：五個Node共用可配置三區外邊界10／30／50 m，依所屬Node距離分區，內側含上界／外側排除下界；d=0不納入，Channel有效最小距離仍待定。這是部署幾何，非已驗證覆蓋半徑。
- 下一題Q-TRADEOFFS-04：A Donor／Node座標明列Config、Tags依seed隨機生成（建議），或B Donor固定、Node也依seed生成。位置、高度、邊界與重疊尚未選定。Tradeoffs4/10，Description6/10。
- 訪談、拓撲盤點及R-01已同步；仍無Notebook／程式／模擬器測試。

## 2026-10-23｜固定Node位置；區域重疊待答

- Q-TRADEOFFS-04已回答A：Donor與五個Node的座標在Config明列、run內固定，Tags仍隨機關聯／部署；具體座標及高度尚未定。
- 下一題Q-TRADEOFFS-05：A五個50 m部署區域不重疊（首版建議），或B允許重疊、Tag仍單一歸屬。幾何不重疊不等於RF無干擾。Tradeoffs5/10，Description6/10。
- 已同步訪談、拓撲盤點及R-01；尚未建立Notebook／程式或執行模擬器測試。

## 2026-10-23｜部署區域不重疊；Tag配額分配待答

- Q-TRADEOFFS-05已回答A：五個Node的50 m部署區域不重疊；平面圓形座標草案採間距大於100 m避免相切，尚未選具體座標。不代表RF干擾為零。
- 下一題Q-TRADEOFFS-06：A依seed隨機分配全場三區配額至Nodes（建議），或B明列每Node三區配額、ID與位置隨機。建議每Node至少2個以落實多個Tag，不要求每Node每區都有Tag；數值仍為本題提案。Tradeoffs6/10，Description6/10。
- 同步訪談、拓撲盤點與R-01，沒有Notebook／程式／模擬器測試或遠端操作。

## 2026-10-23｜隨機分配配額與每Node至少2個Tag已定

- Q-TRADEOFFS-06回答A：依seed隨機分配各Node三區數量，精確維持全場配額且每Node至少2個，不強制均分、不要求每Node每區有Tag。先歸屬／分區後生成位置；總數不足2倍Node數時拒絕。30與10／13／7維持可配置例子。
- 下一題Q-TRADEOFFS-07：A區內按面積均勻隨機（建議），或B區內局部群聚。已定的跨區非均勻數量不自動決定區內空間密度。Tradeoffs7/10，Description6/10。
- 同步訪談、拓撲盤點與R-01；沒有Notebook／程式／模擬器測試。

## 2026-10-23｜區內面積均勻已定；剩餘決策盤點

- Q-TRADEOFFS-07已回答A：每分區內按面積均勻隨機、角度無偏好，跨區維持精確非均勻配額；每Node至少2個、隨機歸屬等決策沿用。
- 已新增 `docs/architecture/iab-topology-remaining-decisions.md`，盤點三項模型邊界：空間維度及分區距離定義、Tag／UE在run內是否移動、UE實體座標需求。具體示例座標、dataclass／資料流、有限步驟生成與驗收由代理提出草案，不逐項加訪談題。
- 頻段／功率／傳播／外部干擾／中區品質排序／採能校準留相關Channel／EH契約前，避免阻擋純拓撲。缺少品質數值時不輸出虛構SNR。
- 本輪僅盤點，未新增問題；Tradeoffs7/10、Description6/10。OpenSpec list仍空，無Notebook／程式／模擬器測試或遠端操作。

## 2026-10-23｜平面／靜態已定；UE座標實例說明

- 使用者明確指定暫不考慮高度、系統靜態：首版平面x／y公尺座標、三區採水平距離、run內位置不變。不據此取消Window級通道更新／外生資源時序。
- 使用者要求UE表示實例；Q-INFLUENCE-03待答：A僅UE ID／Node歸屬、資源占用由既有時序模組描述（若只表示負載則建議），或B加入固定UE座標以供後續幾何干擾使用。A不自動將UE干擾設0，B也不單靠座標宣稱干擾值。
- 已同步盤點／訪談／R-01。剩餘三項模型邊界中兩項已定，僅UE表示待答；Influence3/10、Description6/10、Tradeoffs7/10。無Notebook／程式／模擬器測試。

## 2026-10-23｜UE表示已定；拓撲設計草案完成

- Q-INFLUENCE-03已回答A：UE僅ID與Node歸屬，無物理座標，資源占用留時序模組；不自動將UE干擾設0。三項拓撲模型邊界均已定，不再重問。
- 已完成 `docs/architecture/iab-topology-design.md`：固定座標示例、最小dataclass／快照、局部seed及有限步驟配額生成、面積取樣、Notebook導讀與情境驗收。名稱／座標是工程草案，非已接受程式；尚未建立最終.py。
- CLI changes仍空，尚無Notebook／模擬器測試／Issue／PR或workflow登記。後續依本草案整理OpenSpec與原型；未變更遠端授權。Influence3/10、Description6/10、Tradeoffs7/10不變。

## 2026-10-23｜拓撲實作規劃架構圖

- 依使用者要求用Archify完成 `.archify/architecture-iab-topology-20261023-131337/iab-topology.html`，候選JSON與檢查收據保存在同目錄，設計文件已加入連結。
- 圖示設定→驗證→生成→不可變快照→情境測試→表／部署圖→人工導讀→接受後抽離.py；Config／DTO集中與後續Channel邊界另有說明。這是未實作設計，不是HEAD程式碼追溯，沒有偽造來源行號。
- Archify finalize的validate／deliver／check／browser-check均pass，無診斷；未做截圖視覺審閱，不等於Notebook或模擬器測試通過。初次沙箱spawnSync EPERM，經核准本機重跑成功。
- 發現Archify3.1.0→3.2.0更新，僅通知，未安裝更新。沒有Notebook實作、commit／push或遠端發布。

## 2026-10-23｜程式tree、輸出與人工接受說明

- 依使用者要求在 `docs/architecture/iab-topology-design.md` 補充路徑草案：notebooks/01_iab_topology.ipynb；人工接受後src/network_simulator/{contracts,topology,plotting}.py與tests/test_topology.py；保留既有目錄。上述程式均未建立，不作現況tree。
- 補充設定／Node摘要／Tag明細／連線表、等比例二維三區部署圖、精確10／13／7示意計數表，標明示意非執行結果。UE僅關聯表、圖色不冒稱實測SNR。
- 人工流程：自動測試與乾淨kernel執行→架構與絕對路徑code-trace→逐段導讀→使用者提問／修改設定→修正複驗→明確接受Notebook→抽離.py並跑相同情境核對等價。行為改動須重新接受；模組接受不等於遠端合併或整體模擬器驗證。
- 本輪只解釋與文件補充，未新增訪談題、程式、Notebook或模擬器測試，也未取得人工程式接受。

## 2026-10-23｜IAB拓撲Notebook已完成驗證，待人工接受

- 使用者已明確授權依workflow開始執行。建立change `add-iab-topology-notebook`，實體為AgentDoc/openspec/changes/add-iab-topology-notebook；workflow ID 24fa04df-cec9-487a-b821-11f46fcd9b4e，Git基準0a5ff65f151febb53416d67855afa9850e2b1b13。保留README／LICENSE等既有修改，無commit／push。
- Notebook：notebooks/01_iab_topology.ipynb，所有業務定義仍在definitions cells。測試：tests/test_topology_notebook.py；執行器：tests/execute_topology_notebook.py。正式src模組尚未建立，人工接受前不得抽離.py。
- 最終66 pytest通過；真實乾淨kernel完成11 code cells、0錯誤、kernel_shutdown=true；Notebook內8教學情境通過。既有RL Python3.11.15可用，base Python3.12跑pytest；mcp metadata存在但缺decorator導致kernel失敗，未當成功，未安裝或改環境。
- 結果在notebooks/artifacts/iab-topology/：完整snapshot.json、settings／nodes／tags／links.csv、deployment.png／svg。seed42 Node Tag總數8／3／8／5／6，全場近10／中13／遠7。圖／表同快照，UE僅歸屬，無SNR等假數值。
- Standards／Spec兩軸review完成；Spec圓周端點浮點誤拒絕、整數差值OverflowError，以及Standards外部kernel清理問題均修正並複驗。debt掃描0 marker，未建立空TI登記。細節見change review.md／validation.md／tdd-evidence.md。
- 整體docs/architecture/system.html與change architecture.html均通過Archify finalize／browser-check；明暗雙尺寸截圖已生成，代理檢視change亮色與整體暗色桌面及最終部署圖。Archify3.1→3.2更新僅通知，未更新技能。
- 完整實際tree及每個實作檔絕對／相對路徑：change code-trace.md；docs/architecture/code-trace.md為導讀入口。版本SHA-256在source-manifest.json，需行為變動時複驗／更新接受範圍。
- 任務8/12完成，未完成3.3人工接受、4.1正式.py抽離等價複驗、4.2交付／4.3merge結案。現在從Config／DTO段逐步導讀，等待使用者問題／明確接受，不重啟訪談。
- Issue／PR未獲發布授權，僅issue-draft.md；workflow維持github契約且未冒造URL。索引stage保留spec（helper的apply／review需真Issue），next_step及evidence明示本機實作／review已完成、待人工接受／遠端授權。未歸檔、未合併、workflow完成數仍0。

## 2026-10-23｜導讀前檢查.gitignore

- 依使用者要求唯讀檢查目前.gitignore，UTF-8正常、無NUL／BOM；Git可解析規則，Notebook／tests／未來src程式路徑沒有被目前規則匹配。
- 發現效果差異：第10行openspec/只匹配目錄，根目錄openspec實際為符號連結，git check-ignore --no-index未匹配，status仍列?? openspec。建議若要忽略該根連結改為/openspec；未修改使用者.gitignore或暫存區。
- 目前工作區已有使用者暫存變動，保持原樣。拓撲Notebook仍待人工接受，尚未抽離.py。

## 2026-10-23｜開始人工導讀

- 使用者要求開始導讀，已讀實際Notebook contracts／run-example cells。第一小段說明Position2D、FixedNodeConfig及frozen dataclass，以Node-1=(0,0)對照資料結構。
- 導讀仍進行中，尚未取得理解／接受回饋；下一段為TopologyConfig欄位、tuple與__post_init__，再接結果DTO。未改業務程式，未抽離.py；tasks3.3維持未完成。

- 人工導讀進度：使用者已確認Position2D／FixedNodeConfig及frozen初始化概念OK；現在接續TopologyConfig欄位與__post_init__。這是局部理解，整份Notebook與task3.3尚未接受／完成，未改業務程式。

## 人工導讀修訂｜tuple唯一輸入與README註記

- 使用者明確選第三種：iab_nodes／zone_outer_radii_m／zone_tag_counts直接輸入tuple，拒絕list、不自動轉換。已移除__post_init__，保留其餘使用者Notebook註解。
- 已追加根README的tuple規則／原因／範例／build_topology驗證時點，保留既有README內容；未commit／push或改暫存區。
- 已同步OpenSpec輸入契約、設計、測試與導讀。TDD新增3個拒絕案例先3 failed／66 passed，再69 passed；更新舊轉換案例以符合已確認新契約。完整kernel11 cells／0 errors／kernel_shutdown=true，snapshot.json與修改前SHA-256一致。
- 原型仍待人工導讀接受，未抽離正式.py，tasks3.3未完成。先前list轉tuple導讀為歷史，不再適用；下一段可讀UE／Tag／Snapshot結果DTO。

- 人工導讀依使用者要求轉入第2節，先說明_finite_number及四函式責任；接著讀_validate_radii／classify_distance／validate_config。仍為局部導讀，尚無整份Notebook接受，未改業務程式或抽離.py。

## 人工導讀｜if區塊留白與validate_config

- 使用者要求工作流程式排版：獨立if驗證區塊間保留一空行；已依writing-for-agents記入本專案agent.md（AGENTS.md連結），套用Notebook validation cell，保留使用者註解及分支／縮排。
- 只插入6個空行並清除留白行空白字元；AST一致，69 pytest通過，無業務行為／輸出改變，未重跑未受影響kernel／圖。整份人工接受仍未完成。
- 本輪導讀validate_config總覽、Config／站點型別、單元素tuple合併、逐站點ID／座標及重複ID檢查；後續配額、保留ID、Node間距檢查分段續讀。

## 2026-10-23｜主要邏輯理解接受、.py抽離與雙語文件草稿

- 使用者明確表示主要邏輯已理解並要求依workflow打包.py，完成3.3；建立src/network_simulator/{__init__,contracts,topology,plotting}.py，Notebook definitions改import、保留設定／展示／8教學情境，完成4.1；任務10/12。
- 抽離前保存原型與四場景baseline；TDD先4 failed（套件尚不存在），再142 passed＝69情境×Notebook／模組兩入口＋4獨立基準，並非142種獨立場景。乾淨kernel11 cells／0 errors／kernel_shutdown=true；seed42 snapshot.json SHA不變。
- code-review兩軸獨立審查：Spec無阻擋缺陷，Standards發現if空行已修正並複驗；debt 0 markers。移除表格內教學print、更正幾何／面積註解，保留其餘使用者註解及完整原型。
- 整體與詳圖Archify四gate通過，收據各在system-extraction-review-2及extraction-review-2；本輪無新人工截圖檢閱。code-trace與README已更新當前路徑。
- 使用者選ReferDoc/Implementation/README.md作索引，每模組多文件；再要求依write-reviewable-pr先交中文／英文草稿。現有IABTopology/draft.zh-TW.md、draft.en.md，確認內容後再拆正式章節；尚未完成文件人工檢閱。
- 下一步與使用者討論草稿；4.2規格sync／archive／交付準備、4.3實際merge／知識結案仍未完成。Issue／PR無發布授權，不commit／push，workflow完成數仍0。詳細證據見change/extraction-validation.md。

## 2026-10-23｜雙語草稿改為標準流程圖

- 依使用者要求，ReferDoc/Implementation/IABTopology/draft.zh-TW.md與draft.en.md的第3節改為兩張標準Mermaid流程圖：生成快照與使用快照。
- 使用起訖、輸入／輸出、處理、子程序及判斷符號；補齊設定拒絕、Tag迴圈、座標生成失敗及輸出操作選擇。匯出的finally範圍與部分輸出失敗限制依實際topology.py說明。
- 只修改文件，未變更.py／Notebook或測試結果；無需重跑業務測試。圖形語意與雙語節點／邊對照可核對；未另產生Archify HTML，既有系統架構圖保留。草稿仍待檢閱，任務維持10/12。

## 2026-10-23｜依讀者回饋改寫產品使用說明

使用者指出文件目的是產品說明書，代理執行的142項檢查不應作為說明主體，術語過多；要求依write-reviewable-pr易讀原則修訂。已重寫Implementation索引及中英文草稿，以功能、準備、設定、操作、結果、常見問題、使用範圍七節呈現。移除測試統計、測試函式、開發版本／交付資訊與非必要術語，既有開發驗證紀錄完整保留於本change；沒有更改產品行為或既有人工接受狀態。

保留標準流程圖，以使用者操作呈現，雙語節點與連線相同。範例改為seed=7且保持預設配額，實際載入Notebook imports並執行該範例及既有教學檢查，確認相容；補充修改Tag數量時預設教學檢查也需調整的現有限制。只更新文件，未重跑完整pytest／kernel，未聲稱新增測試或使用者已驗收。三份文件的本地連結及Markdown結構核對通過，Mermaid未另渲染。仍待使用者檢閱草稿、後續拆文件，任務10/12，未commit／push。

## 2026-10-23｜產品說明風格接受；Notebook列點說明更新

- 使用者明確接受重寫後的產品說明內容，要求後續沿用此風格：先說用途、設定、操作與結果，少用術語，不將代理測試統計當產品說明主體；Notebook說明盡量列點。此偏好供本專案後續文件沿用，不修改共用技能或全域記憶。
- 已改寫notebooks/01_iab_topology.ipynb原有9個Markdown cell，另在表格展示與匯出前各補1個Markdown cell。介紹設定格式、區域邊界、隨機分配、圖表閱讀、預設教學檢查及輸出覆寫／儲存失敗處理。
- 保留全部11個code cells的source、outputs、execution_count與metadata，Notebook層級metadata亦一致。nbformat驗證、cell ID唯一性及Markdown本地連結檢查通過；未重跑未變更的業務測試或kernel。
- 已接受產品說明內容，但本輪未拆分正式多文件、未sync／archive、未commit／push；整個change仍10/12，後續依使用者安排接續交付準備。

## 2026-10-23｜IAB模組目錄分類完成

- 使用者要求來源與測試依模組分類，已將src/network_simulator整體移至src/iab，對應三份測試／執行器及fixture移至tests/iab。全部dataclass與Enum仍集中contracts.py；沒有新增未實作的角色模組或相容包裝。
- Notebook imports改為from iab...；測試與執行器的專案根目錄計算改為parents[2]。README、產品說明相關入口、目前code-trace及架構圖來源路徑已同步。原型與歷史log／收據保留原路徑文字，作歷史證據。
- module-layout-baseline.json核對搬移前後四份正式.py與fixture的SHA完全一致，沒有變更產品行為。`MPLBACKEND=Agg MPLCONFIGDIR=/tmp/pynet-iab-layout python -m pytest tests/iab -q --tb=short`通過142項（既有雙入口69案例＋4基準），原始輸出見module-layout-pytest.log。
- `tests/iab/execute_topology_notebook.py`於既有RL環境完成11 code cells、0 errors、kernel_shutdown=true；新import命令實跑輸出5 UE／30 Tags，Notebook既有列點Markdown保留。
- code-review唯讀獨立審查分Standards／Spec兩軸：無阻擋缺陷，另獨立跑同組142項通過；本輪未新增行為所以沿用既有測試，不新增只測路徑的重複案例。debt掃描0 marker，無新增TI。
- 現行入口文件38個本地連結有效，範圍內diff --check通過。詳圖更新src/iab來源文字後通過Archify四項自動gate，收據iab-layout-review/architecture.finalize-summary.json；本輪未另做人工視覺檢閱。整體圖的模組關係未變，無需重新生成。
- 使用者已接受產品說明風格與Notebook列點說明；本輪依授權分類目錄。任務仍10/12，規格sync／archive／PR／實際merge尚未完成；無commit／push或遠端發布。

## 2026-10-23｜正式文件與主規格同步，本機交付準備

- 依使用者要求再次核對Notebook：所有imports使用iab，新增Markdown列出src/iab與tests/iab，連結改為正式使用說明；code cells、outputs與execution_count由本輪修改前後相等檢查確認未變，nbformat驗證通過。
- 使用者已接受的中英文合併說明拆成10份正式文件（各語言總覽／設定／操作／結果／常見問題），原草稿保留。分章未改實質規則，Notebook與Implementation總索引更新正式入口。
- 主規格AgentDoc/openspec/specs/iab-topology/spec.md已建立，7要求／14情境與delta本文完全相同，主spec及change嚴格驗證通過。
- 建立本機分支feat/iab-topology，無commit／push／stage；Issue／PR草稿、歸檔準備與候選檔案清單已備妥。規格與產品說明不改模型或程式，沿用搬移後情境及kernel證據，不重跑未變程式。
- code-review本輪文件Standards／Spec兩軸無阻擋缺陷；產品文案不混入代理測試統計，PR保留代理／人工／CI區分。
- 未實際archive：archive skill要求先檢查未完成tasks與GitHub Issue映射，當前4.2／4.3及Issue對應未成立，不假勾選或冒稱完成。發布前需取得僅本change之commit／push／Issue／PR授權，再核對最終staged檔案與ignore依賴。
- 現有ReferDoc／AgentDoc忽略規則維持；不整批加入其文件或無關修改。下一步僅缺遠端交付授權及歸檔gate處理；任務10/12，workflow仍active，完成數0。

## 2026-10-23｜使用者授權全部內容發布；Issue已建立

- 使用者明確准許commit／push／Issue／PR，並要求目前內容都push。授權範圍包含現有研究參考、AgentDoc與專案工作流資料；執行快取及本機帳號／Git內部資料不納入。原gitignore不改。
- 已唯讀核對GitHub repo tonywang07009/PY_NetworkSimulator為public，預設分支main，沒有既有IAB Issue或此分支PR；建立Issue #1：https://github.com/tonywang07009/PY_NetworkSimulator/issues/1。
- 歸檔skill與既有task4.3實際merge核對存在順序衝突，未修改規則或假勾選，先發布draft PR保留active change。發布不等於完成／合併；EvoSkill與明日模組討論不啟動下一個change實作。

## 2026-10-23｜目前內容已push；草稿PR #2已發布

- 使用者明確授權後，已提交並push目前專案內容至origin/feat/iab-topology，包含程式、Notebook、ReferDoc、AgentDoc、現有工作流工具與訪談。排除帳號設定、Git內部資料、執行快取及新生成的暫存HTML；該暫存檔留本機未刪除。
- Issue #1：https://github.com/tonywang07009/PY_NetworkSimulator/issues/1；草稿PR #2：https://github.com/tonywang07009/PY_NetworkSimulator/pull/2，base main，未merge。首次交付commit 131b23806f7f107e18884f8c72e1ef0e163bc257；本段發布紀錄另以後續commit補入。
- 發布前重新執行tests/iab：142 passed，1.42s；主規格與change strict驗證通過，沒有把代理檢查當使用者實際操作驗收或遠端CI。
- 實際archive仍受未完成lifecycle task與archive skill順序衝突限制；保留draft PR、active change，workflow stage維持review（不是awaiting_merge／complete），不偽造archive_path。
- 使用者要求push後討論明日模組與EvoSkill：可先討論距離→SNR的通道品質模組，或600ms DU Window出現時刻的資源時間表；未替使用者選參數、建立下一change或開始實作。
- EvoSkill流程為有來源的回饋紀錄→資格評估→隔離候選比較→使用者指定版本啟用；本輪產品文案修訂只構成一個回饋事件，不能拆成多個同根因事件充數。當前不建立空候選、不修改既有技能，正式知識結案依workflow待所有change合併後執行。
