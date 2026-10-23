# 工具路由

所有命令預設 cwd 為專案根目錄；版本、安裝與驗證見 `AgentDoc/tool-inventory.json` 和 `AgentDoc/PROJECT_BOOTSTRAP.md`。

| 情境 | 工具與命令 | 副作用與證據界線 |
|---|---|---|
| 任務／規範進度 | `OPENSPEC_TELEMETRY=0 openspec list --json`；`openspec status --change <name> --json` | list/status 唯讀；完成 artifact 不等於實作通過 |
| Git 輸出 | `rtk git status`、`rtk git diff` | 壓縮輸出；需要原始證據時用 git |
| 文件定位 | `rg -n <pattern> <bounded-path>` | 文字命中不是行為驗證 |
| 3GPP 規範 | `jq '.documents["TS 38.340"]' ReferDoc/Spec/spec_index.json` | 接著讀原始 TS/TR |
| 程式索引 | `symdex --state-dir "$PWD/AgentDoc/tool-state/symdex" index <source-folder>` | 寫入專案索引；只索引需要的原始碼，勿納入整份規範庫 |
| 程式查詢 | MCP `symdex-py-networksimulator` | 新會話載入；每次指定正確 repo；目前未建立模擬器程式索引 |
| 檔案存取 | MCP `filesystem-py-networksimulator` | 僅允許本專案根目錄；寫入需符合使用者授權 |
| PDF 轉文字 | 已配置 markitdown MCP 或本機 PDF 工具 | 個別轉換尚未於本次驗證 |
| 最小實作與技術債 | 專案內 `.agents/skills/ponytail`、`ponytail-debt` | 優先使用本輪 bundled 定義，保留選定模型／level；plugin hooks/dashboard/MCP 非必要 |
| 架構視覺化 | `.agents/skills/archify/SKILL.md` | 圖不能取代來源證據；依該 skill 執行驗證 |
| 知識與技能改善 | `.agents/skills/llm-wiki`、`skill-evolution` | 維護證據與候選分離，遵循原技能門檻 |

原本名稱 `symdex` 的 MCP 使用 OAI 索引目錄，`filesystem` 也允許 OAI 路徑；本專案請選帶 `-py-networksimulator` 的名稱。兩個新服務註冊於使用者 `~/.codex/config.toml`，非僅限本專案可見；資料／允許路徑則限於本專案。現有服務未改名或移除。


## 新版資源與實證路由（2026-10-18）

| 工作 | 入口與界線 |
|---|---|
| 工作流／訪談 | `.agents/skills/workflow`、`grill-with-docs`；實際訪談才建立 interview/ |
| 決策詢問與人讀文件 | `.agents/workflow-kit/docs/output.md`；英文指令，預設繁體中文輸出 |
| 每項行為語意核對 | TDD 的 local semantic check；需求 → 實作／呼叫端 → 測試／原始證據 |
| change 審查 | code-review + ponytail-debt；合理延後事項依 workflow/references/technical-debt.md |
| 技術債 owner | `AgentDoc/openspec/tech_improve.md`，有具體事項時由 management/tech_improve.md 起稿 |
| 圖與導讀 | 保留既有 Archify；根目錄 docs/architecture/ 作為新圖預設位置，change 圖與 code-trace.md 隨實際 CLI 路徑 |
| GitHub | origin 為 https://github.com/tonywang07009/PY_NetworkSimulator；目前分支 main。PR base、保護／required checks 與發布授權在實際交付前確認，不從本機設定推定遠端狀態 |
| 安裝／升級 | `.agents/workflow-kit/PROJECT-INSTALL.md`；本專案保留 EvoSkill 符號連結，不能直接套用標準無連結布局的升級器 |
| 課程與原始套件 | `AgentDoc/WorkflowKit/index.html`、`README.md`、`install.py`、`tests/`、`PROVENANCE.json`、`SHA256SUMS`；不覆蓋本專案政策 |

本輪實際 MCP 呼叫：filesystem 允許根目錄正確，SymDex list_repos 回傳空清單，
且 registry 位於本專案 AgentDoc/tool-state/symdex。這只證明相應唯讀呼叫可用，
不代表已建模擬器索引、查到符號／呼叫關係、轉換 PDF 或完成模擬行為驗證。
CLI 本機觀察為 OpenSpec 1.4.1、SymDex 0.1.26、Node v24.14.1；沒有升級外部工具。
