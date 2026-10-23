# 本專案安裝配置與恢復

移植日期：2026-10-18。來源套件內容版本：`db81e767d30dd8e4f2b7f27f31e197c5609a2f93c1dfdb8faca212d69d6031c7`。

本專案採專案路徑對應布局：18 個技能由 .agents/skills 探索，llm-wiki 與
skill-evolution 實體保留在 AgentDoc/EvoSkill/skills，Archify 保留原版本。
EvoSkill 的 Markdown 連結按實體路徑適配；原始來源仍可在完整教材比對。
`project-installation.json` 記錄這個布局，並非標準 installation.json。

標準套件 install.py 拒絕既有目錄或 skill 符號連結，不可直接以 --upgrade
覆蓋此專案。後續請先讀本專案移植紀錄，在暫存專案展開新版，對照
logical／physical 路徑及當前 hash，只更新已檢視的變更，保留額外檔案。
不要刪除連結、偽造標準 manifest 或把本專案資料複製成新預設。

完整套件在 AgentDoc/WorkflowKit，含 install.py、verify.py、tests、課程、
PROVENANCE.json 與原始 SHA256SUMS。套件在其他全新專案可使用標準安裝器；
原始套件 verify.py 檢查套件本身，不是本專案模擬器測試。

移植前每個覆寫檔案均備份，位置見 AgentDoc/EvenStore/workflow-migration-2026-10-18.json。
恢復時先保存移植後的新修改，依紀錄確認對應檔案；恢復備份中的原有檔案，
只刪除紀錄中原本不存在且仍與本次部署 hash 一致的新檔，勿刪除後續工作。
保留兩個 EvoSkill 連結與 OpenSpec／AGENTS 連結。不要把全域設定當作可回復檔案。

本輪未更動外部執行檔、使用者層級 MCP、模型選擇，也未建立個人 workflow 狀態。
實際專案入口為 agent.md，與教材管理範本、歷史快照分開。
