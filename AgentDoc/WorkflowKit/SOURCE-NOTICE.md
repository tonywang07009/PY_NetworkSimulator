# 來源聲明

目前配送 18 個 skills。2026-10-18 後續新增 ponytail 與 ponytail-debt，
取自 DietrichGebert/ponytail 的 09c434ab73ca43761c5d8b0c5d341926c2fba710，
各保留 MIT LICENSE。教材整合段落銜接既有規格、技術債登記及輸出規範；
上游來源雜湊與本地改編雜湊分開記錄，未修改套件外的原始技能。
Hooks、dashboard 與外部 plugin/MCP 並非這兩個 bundled skills 的必要依賴。

本輪加入安裝基線、預覽、衝突處理、備份與失敗回復，以及三平台 CI 定義。
OpenSpec 1.14.3、SymDex 0.1.26 與既有固定 revision 的 Archify 已在 Linux
暫存專案做 CLI 操作檢查；CI 定義不等於已在 macOS／Windows 執行。
GitHub Actions 固定 commit，.gitattributes 統一文字換行，避免平台換行轉換
破壞原始來源與配送檔案的雜湊比對。

目前架構圖驗證紀錄在 course/review-implementation-debt/；舊的根目錄
finalize 記錄保留一次過期瀏覽器證據不匹配的失敗嘗試，不作為現行驗證。
PROVENANCE.json 的 workflow_quality_and_upgrade 指向此次有效紀錄。

11 個通用 skills 取自講師目前專案的工作流快照；逐檔來源及差異見 PROVENANCE.json。保留各檔案原有作者與授權 metadata，本教材不以單一授權覆蓋原來源條件。

另新增 `workflow`、`llm-wiki`、`skill-evolution`，原先合計 14 個 skills。
2026-10-18 將使用者提供的 write-reviewable-pr 移入 skills/，目前合計 15 個；
保留其認可的 PR 結構，共通寫作規則引用 docs/output.md。
通用版依使用者確認的設計撰寫管理範本、工具指南與品質演進流程；
原有技能的教材副本調整專案接入與責任銜接，原來源雜湊保留於 PROVENANCE.json。
本次未修改套件外的原始 skills。WikiSkill 論文是方法來源，並非已重現實驗。

2026-10-18 擴充共通寫作規範：技能指令參考 AI Hero 的 Writing for Agents
（https://www.aihero.dev/skills-writing-for-agents），人讀文件沿用 GMU 的銜接原則，
並將 Not Only Blogger 的九項文章技巧依工程用途調整。這是使用者需求下的本地
應用規則；該輪尚未配送上游 writing-for-agents skill，也沒有驗證特定模型的閱讀成效。

同日後續依使用者同意，新增第 16 個技能 writing-for-agents，取自
mattpocock/skills 的 49dd158d1076134a641b33efb035946536778336，
保留 SKILL-MECHANICS.md、原 UI metadata 與 MIT 授權（技能內 LICENSE）。
套件入口另加 host 相容及 evolution／人讀文件責任指引；逐檔原始雜湊與改編雜湊
記於 PROVENANCE.json。evolution 只在合格候選撰寫時讀取，沒有改動啟用門檻。
output.md 改為英文指令，預設繁體中文輸出；中文範例按需載入，未聲稱 tokenizer
無關的節省比例。

現行 course/workflow.html 已依使用者要求，使用本機 archify 專案的
3.1.0 CLI 重新生成；原始規格為 course/workflow.archify.json。
使用者授權來源 https://github.com/tt-a1i/archify，checkout 位於 .tools/archify，
revision 記錄在 PROVENANCE.json；該工具 checkout 不隨套件配送。
course/build.py --archify-root 可重跑 finalize（含 deliver、provenance 與 browser checks），保留來源與產物雜湊。
Archify 原授權及歷史驗證產物繼續保留；本次未修改其專案程式碼。

Archify 產生的檢視器來源為 tt-a1i/archify，隨附原 LICENSE 與 THIRD_PARTY_NOTICES。通用包沒有包含 Archify CLI、OpenSpec CLI、RedCap 原始碼、論文 PDF 或 MCP 憑證。

課程說明與案例為本次製作；來源快照用於離線對照，正式結論應回原專案與論文查核。

2026-10-18 原 # MCP 工具.txt 升級為 docs/install.md，依使用者確認的三平台
目標與專案設定優先原則撰寫 agent 安裝程序。外部工具指令來源連回各官方專案；
未配送其執行檔，也未將文件視為三平台安裝成功證據。來源索引中的研究與桌面
應用仍是參考／選用項目，不列為 workflow 必裝依賴。
