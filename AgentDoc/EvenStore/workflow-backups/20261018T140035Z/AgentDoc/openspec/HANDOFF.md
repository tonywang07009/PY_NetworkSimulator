# 任務交接

更新：2026-10-15。

1. 先讀 PROGRESS.md、專案 spec.md/toolbox.md，再執行根目錄 `openspec list --json`。此次初始化前不存在已登錄的進行中 change，未偽造舊進度。
2. 已確認需求：OpenSpec 置 AgentDoc；llm-wiki 與 skill-evolution 的原始定義及後續產物置 EvoSkill；根目錄 agent.md 提醒每次讀取進度與交接；安裝／盤點工具並留下可重用指南。
3. `.agents/skills` 中兩個技能是連結，修改原始定義時實際檔案位於 EvoSkill/skills。搬移內容未變更；baseline hashes 見 EvenStore。未啟動任何改善候選。
4. MCP 使用新名稱 symdex-py-networksimulator 與 filesystem-py-networksimulator；新會話確認載入。舊 symdex、filesystem 綁定 OAI，不能據此宣稱本專案可用。MCP 連線證據不能當作模擬器查詢或程式執行驗證。
5. 規範資料入口為 ReferDoc/Spec/spec_index.json，詳細分類見各目錄索引；後續重新檢查所需 PDF 與版本，不從設計指南推定實作已完成。
6. 下一步由使用者指定模擬器工作範圍，或明確授權有邊界的 Wiki 匯入。本次未執行完整 Wiki 知識建置或 simulator change。
7. 初始 Git 已有 LICENSE、README.md 修改與未追蹤 .gitignore，保持原樣。AgentDoc/ReferDoc 受既有 ignore 規則影響；需另外備份。無 commit/push。
