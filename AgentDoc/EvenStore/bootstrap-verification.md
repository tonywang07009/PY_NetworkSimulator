# 前置設定驗證（2026-10-15）

- OpenSpec 1.4.1：根目錄 list --json 回傳 {"changes":[]}；list --specs 回報 No specs found。這是新初始化專案，尚無 simulator change/spec。
- llm-wiki 4 檔、skill-evolution 6 檔逐檔 SHA-256 一致；技能入口、OpenSpec、AGENTS 連結與兩技能 SKILL.md 的本地文件連結皆存在。
- Archify v3.1.0 固定提交安裝成功；CLI guide JSON 回應正常。--version 不支援，未將該探測當成成功的版本查詢。尚未生成或瀏覽器驗證圖表。
- 新增兩個 MCP 於使用者 config；獨立 STDIO client initialize/list_tools 通過（SymDex 21 tools、filesystem 14 tools），filesystem list_allowed_directories 僅列此專案。見 mcp-smoke.json。
- 預設沙箱下初次 STDIO 測試未完成回應；經核准的外部沙箱執行通過。verify_mcp.py 為重跑版本，單次請求有 20 秒上限。這是環境差異，不是完整執行行為證據。
- 既有 OpenSpec、RTK、SymDex、Ponytail 版本盤點，沒有重裝或升級；沒有修改原有 OAI MCP 路徑。
- 初始 LICENSE/README.md/.gitignore 狀態保留；未 commit/push。
