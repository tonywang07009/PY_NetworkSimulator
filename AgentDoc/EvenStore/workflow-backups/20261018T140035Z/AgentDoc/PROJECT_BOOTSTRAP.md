# 專案前置流程快速指南

驗證日期：2026-10-15。適用本機 Linux；實際版本見 tool-inventory.json。以下以 `<project>` 表示新專案絕對路徑，執行前替換，不可原樣貼入。

1. 先確認目標、範圍、交接與既有 Git 修改，盤點 `node --version`、`openspec --version`、`rtk --version`、`symdex --version`、`codex --version`。重用可用工具；安裝不是每次升級。
2. 本次已安裝 OpenSpec 1.4.1、RTK 0.42.1、SymDex 0.1.26；Ponytail plugin 5.2.0 已存在。本次未重裝上述套件。新機依各官方安裝文件處理並記錄實際版本；不要將此盤點當作跨版本相容保證。
3. 初始化文件位置，在專案根目錄執行：

```bash
mkdir -p AgentDoc/EvoSkill/skills AgentDoc/EvenStore
OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 openspec init --tools none AgentDoc
ln -s AgentDoc/openspec openspec
```

`--tools none` 避免覆寫既有自訂技能；在新的專案若尚無 OpenSpec skills，應另外選擇要安裝的技能。上述 ln 只用於目標不存在時；既有資料先檢查，不覆寫。根目錄連結使 CLI 能找到同一份 OpenSpec，不需從 AgentDoc 再產生巢狀根目錄。

4. 建立根目錄 `agent.md`，寫入每次先讀 OpenSpec 進度與交接的規則；再建立 `AGENTS.md -> agent.md`。Codex 自動識別的是 AGENTS.md；只寫小寫 agent.md 不足以建立預設入口。建立 `AgentDoc/openspec/config.yaml`、PROGRESS.md、HANDOFF.md，並填實際狀態，不將空目錄視為實作完成。
5. 搬移 llm-wiki 與 skill-evolution 的完整目錄到 `AgentDoc/EvoSkill/skills/`；先確認目的地不存在，保存逐檔 SHA-256，搬移後比對，再於 `.agents/skills/` 建立 `../../AgentDoc/EvoSkill/skills/<name>` 連結。Codex 支援符號連結技能。設定明確 wiki_root，不從安裝位置猜測。改善候選放 Wiki evolution 中，不能放進技能探索目錄。
6. Archify 為 skill，不是獨立 MCP。此次透過 skill-installer 安裝原始 `archify/` 子目錄，固定 v3.1.0 對應提交 `1c2b42d660e4a7571813fb43839c79e3e9ca7720`：

```bash
python3 /home/tonywang/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo tt-a1i/archify --path archify \
  --ref 1c2b42d660e4a7571813fb43839c79e3e9ca7720 \
  --dest <project>/.agents/skills
```

此安裝器路徑依本機 Codex 安裝而定。初次嘗試 `skills/archify` 路徑不存在，未安裝成功；確認上游樹後改用 `archify` 成功。外部 LLM Wiki 桌面應用與 WikiSkill 論文是參考，未當作 MCP 安裝。

7. 先 `codex mcp list` 檢查配置。既有服務可能綁定別的專案，應使用唯一服務名與本專案獨立索引。本次新增以下兩個使用者層級設定，未變動既有服務：

```bash
codex mcp add symdex-py-networksimulator -- \
  /home/tonywang/miniforge3/bin/symdex --state-dir <project>/AgentDoc/tool-state/symdex serve
codex mcp add filesystem-py-networksimulator -- \
  /usr/local/bin/mcp-server-filesystem <project>
```

新專案需更換服務名與路徑。全域註冊不等於所有會話已載入；重開 Codex 工作階段後確認新服務可見。若不希望全域註冊，可依官方文件使用可信任專案的 `.codex/config.toml`；本會話該目錄受保護，因此本次使用 Codex CLI 註冊。本機執行檔路徑不可直接套用其他主機。移除本次註冊可用 `codex mcp remove <service-name>`，不刪除其他服務與索引。
8. 驗證 `openspec list --json`、技能連結與逐檔 hash、MCP initialize/list_tools 及 filesystem list_allowed_directories；保存原始結果於 EvenStore。本次 MCP 煙霧驗證腳本為 `EvenStore/verify_mcp.py`。這只證明連線與工具列表，不證明模擬器程式索引或完整行為。程式碼就緒後再做有邊界的 SymDex 索引與符號／呼叫查詢。
9. 每個任務結束更新 PROGRESS/HANDOFF。本次未建立研究實作 change、未匯入 Wiki、未評估候選、未 commit/push。

| 資料 | 攜帶方式 |
|---|---|
| 技能與支援檔 | 保留完整目錄及符號連結；複製後驗證 hash |
| MCP 設定 | 重建服務名與絕對路徑，不複製含憑證的全域 config |
| 工具執行檔 | 新機依官方安裝，記錄版本與安裝路徑 |
| AgentDoc／ReferDoc | 目前被 .gitignore 忽略，需另外備份；不可假定 git clone 可取得 |

官方依據：[OpenSpec](https://github.com/Fission-AI/OpenSpec)、[SymDex](https://github.com/husnainpk/SymDex)、[RTK](https://github.com/rtk-ai/rtk)、[Ponytail](https://github.com/DietrichGebert/ponytail)、[Archify](https://github.com/tt-a1i/archify)、[Codex MCP](https://developers.openai.com/codex/mcp)、[技能探索與連結](https://developers.openai.com/codex/skills)、[AGENTS.md](https://developers.openai.com/codex/guides/agents-md)。
