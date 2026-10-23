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
| 最小實作檢查 | 已安裝 Ponytail plugin skill | 是 skill/plugin；本次未新增 Ponytail MCP |
| 架構視覺化 | `.agents/skills/archify/SKILL.md` | 圖不能取代來源證據；依該 skill 執行驗證 |
| 知識與技能改善 | `.agents/skills/llm-wiki`、`skill-evolution` | 維護證據與候選分離，遵循原技能門檻 |

原本名稱 `symdex` 的 MCP 使用 OAI 索引目錄，`filesystem` 也允許 OAI 路徑；本專案請選帶 `-py-networksimulator` 的名稱。兩個新服務註冊於使用者 `~/.codex/config.toml`，非僅限本專案可見；資料／允許路徑則限於本專案。現有服務未改名或移除。
