# 任務進度

更新：2026-10-18。當前任務：完整移植新版工作流，供使用者後續實證。

| 項目 | 狀態／證據 |
|---|---|
| 原有前置設定 | 保留 OpenSpec、AGENTS 入口、EvoSkill 與 Archify；2026-10-15 證據仍為當時紀錄 |
| 新版工作流 | 已更新 18 個技能及完整支援檔；兩個 EvoSkill 技能保留原位與探索連結 |
| 共用規範與範本 | 已更新 .agents/workflow-kit/docs、management 與初次提示詞；決策問題與人讀文件均遵循 output.md |
| 完整教材 | AgentDoc/WorkflowKit，含離線課程、首頁、安裝器、測試、來源與原始校驗碼 |
| 專案接入 | agent.md、路由／toolbox、使用指南與本次交接已同步 |
| 備份與比對 | EvenStore/workflow-migration-2026-10-18.json；原有來源 hash 紀錄不覆寫 |
| 目前 change | OpenSpec list 回傳空清單；本輪未建立模擬器 change |
| MCP | 本輪實際執行 filesystem allowed-root 與 SymDex list_repos；無模擬器索引，不推論語意查詢能力 |
| 實證 | 尚未開始；使用者先使用一段時間，再提供流程與可讀性回饋 |

安裝不代表實證通過，也不計為完成一個 workflow。CLM、tag、跨專案偏好共享
維持原先延後決策。沒有新增 Wiki、候選、個人 workflow 狀態、commit/push 或遠端 Issue/PR。
驗證與限制見 EvenStore/workflow-migration-verification.md；失敗時不把本表當作通過證據。

## 2026-10-20｜模擬器產品規劃閱讀與需求討論

- 已完整閱讀 ReferDoc/Plan 的兩份 Markdown；本輪僅閱讀、需求對齊與紀錄，未實作或執行模擬器測試。
- OpenSpec CLI 實際回傳 `{"changes":[]}`；個人 workflow index 無登記項目，未新增登記、Issue 或 PR。
- H-03b 文件差異已由使用者回答 A 關閉：採最大餘數法，餘額同分按 Tag ID 升序；已補 R-01 第 25 節並標示舊狀態被取代。僅文件確認，測試尚未執行。
- 合法空 Action 已由使用者選 A：NO_OP 停止本 Window 後續排程，下個 Window 恢復；自然時間與能量照常。已同步 R-01 第 26 節及 Handoff 第 5 節，未執行測試。
- 配置缺口包含 TBS/payload、固定 CFA 資源與時序、能量/PHY 及情境參數；等待首版驗收參數來源策略。文中三份原始 PDF 未在 ReferDoc 檔名查詢中找到，未核驗原圖、公式或標準符合性。
- 討論紀錄：`../../interview/2026-10-20-ambient-iot-des.md`；先沿用已決定的研究模型，不重啟既有決策訪談。

## 2026-10-20｜架構與工具規劃

- 使用者確認每模組 Notebook 原型 → 對應情境測試 → 人類逐段閱讀與接受 → 抽離該模組 .py；已更新 R-01 第 27 節與交接規格。單模組通過不取代五類整合驗收。
- 已建立 `docs/architecture/implementation-plan.md`，列模組責任、順序、情境、抽離規則與工具建議；屬設計草案，沒有模擬器／Notebook 實作或測試證據。
- 無阻擋架構規劃的未決問題；參數來源題暫緩到依賴模組前，使用者未選 synthetic／正式參數優先順序。
- 本機 Python 3.12.12 metadata 可查 pytest 9.1.1、NumPy 2.3.5、Matplotlib 3.10.8；未找到 ipykernel、nbformat、nbclient、nbconvert、jupyterlab、simpy。僅此解譯器觀察，未安裝／更改依賴。
- 互動模組圖 `docs/architecture/system.html` 已產生；Archify finalize 的 validate／deliver／check／browser-check 全部通過，receipt 為 `docs/architecture/system.finalize-summary.json`。這是規劃圖的自動化檢查，未做人工視覺檢閱，不是模擬器測試通過。沙箱子程序限制經核准執行解決，未更改工具版本。
- Config／DTO 討論：dataclass 集中 Config／DTO／必要 Enum，State 留各模組；Notebook 設定 cell 建立實例並保存快照；run 停止條件已選 A：完整指定服務週期數，總時間推得，電量跨期保留。下一題 Q-INFLUENCE-02 為各期服務需求來源。已同步 R-01 第 28 節及設計／訪談／交接紀錄；未建立程式檔。

## 2026-10-22｜逐期服務配置與剩餘議題整理

- 使用者回答 Q-INFLUENCE-02 的 B：Notebook 逐期明列服務設定，各期可相同或不同；已同步 R-01 第 28 節、交接規格、Config／DTO 草案及訪談紀錄。未決週期長度與實體參數不因此被自動選定。
- 已建立 `docs/architecture/remaining-discussion.md`：D01–D05 資料契約、M01–M07 模組實作前事項、R01–R04 研究階段議題。清單不是新增已核准需求或固定題數，不逐欄新增確認關卡。
- OpenSpec CLI 本輪實際回傳 `{"changes":[]}`；僅整理文件，未實作／執行模擬器、安裝套件、登記 workflow 或建立 Issue/PR。
- 後續依使用者要求整理 `docs/architecture/service-config-example.md`：Simulation／ServiceCycle／ServiceConfig 欄位、兩期設定、Deadline 換算及邊界情境草案。數值只作文件示例；本次僅核對例子算術與連結，沒有模擬器測試。資料表示建議仍待閱讀接受。
- 目前待答 Q-DECISION-03：週期長度為 A 每期各填（建議），或 B 全 run 共用固定長度；本題只確定配置位置，不擴及其他未決項目。依使用者要求繼續逐題討論，未開始實作。

## 2026-10-23｜場景時間尺度修正

- 使用者指定 DU Window 固定 600 ms，已記入 R-01 第 29 節及交接規格；不推定其起點每 600 ms 連續發生。未來長度未知的舊觀測描述需按固定長度設定對齊，未來起點／SNR／完整 Trace 仍不直接揭露。
- Q-DESCRIPTION-02 已答 A：10～15 s 起指各項服務完成 Deadline，非共同需求週期或實際傳輸時間。回到 Q-DECISION-03，每期／全 run 共用週期長度仍待答，不推定實際共同週期秒數。
- 已將 Config 範例改為 10／15／12 s Deadline；共同週期 20 s 僅算術示例，明標未選定，不作為本場景正式配置。僅核對範例算術與連結，沒有實作或模擬器測試。
- 今日目標依使用者最新指示改為開始 IAB 網路拓撲作為首個 Notebook 模組；先完成 Q-DECISION-03，再盤點拓撲直接依賴的決策，不以全部 Config／DTO 定稿阻擋。拓撲範圍尚未完成對齊，尚未實作。
- 使用者最新修正所有服務共同從 0 計時（S1=15 s、S2=20 s 為例），已記 R-01 第 30 節並標示舊多期例子暫停採用。Q-DESCRIPTION-03 待釐清首版全 run 單批服務或保留多期各自相對 0；Q-DECISION-03 暫緩，不把共同週期選擇當作單批拓撲的必答前置。未實作。

## 2026-10-23｜單輪時間定案，轉入 IAB 拓撲盤點

- 使用者答 A 並明確指定本輪長度為最晚服務 Deadline：所有服務全域 t=0 啟動，15／20 s → 輪長 20 s。R-01 第 31 節已同步；取代首版多期依序啟動／獨立指定週期長度，以及所有 Deadline 嚴格小於週期末的舊條件。服務認列仍為 `t<deadline`。
- Q-DESCRIPTION-03 已答；Q-DECISION-03 被新需求取代，無須再選 A/B。`service-config-example.md` 已改成單輪資料範例；其他設計文件加最新範圍說明。
- 已建立 `docs/architecture/iab-topology-scope.md`，盤點六項直接依賴決策與候選情境測試。當前唯一新題 Q-NICHE-01 為首版 Donor／Node 規模與回傳層級；Niche 題數 1/10，等待使用者回答。
- OpenSpec list 本輪仍空；僅文件範圍對齊，尚未實作拓撲／Notebook 或執行模擬器測試，不登記已完成進度。下一步依拓撲答案縮小最小資料契約與情境，不先實作能量／PHY／AI。

## 2026-10-23｜5 Node 拓撲與來源核對

- 使用者具體回答 Q-NICHE-01 的 B：1 Donor 直連 5 Nodes，各 1 UE／多個 Tags，隨機關聯與非均勻部署；指定共址與 IAB split 研究擴充、回傳無干擾／Node–Tag 有干擾。30 Tags 好10／中13／差7 是全場配置例，非每 Node 配額。已同步 R-01 第 32 節及拓撲盤點。
- main.pdf 已存在：11 頁，全文抽取，第 3／4 頁渲染檢視；原圖 2 Nodes 示意由新配置覆蓋，Distance/SNR zones 沒有公尺半徑或干擾數值。成功使用 /usr/bin Poppler；PATH MiKTeX 非零失敗不當證據。
- 依 spec_index 核對本地 TS 38.300 V19.4.0 §16.23.2（split 不支援）、TR 38.769 §3.1／Table 4.2.1-1（D1T1／共址）、TR 38.848 §4.2.2.1（D1 室內）。外部官方 TS 同版已核對，TR 本地原文為依據；不宣稱研究擴充符合標準。
- Q-DESCRIPTION-04 待答：農場／室外研究情境沿用 T1／共址意圖，或採完整 D1 室內條件。Description 題數 4/10；部署分區、尺度、抽樣約束留後續。沒有拓撲程式或模擬器測試。

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
