# 知識與技能改善

| 用途 | 專案相對路徑 |
|---|---|
| LLM Wiki 完整原始技能定義 | `AgentDoc/EvoSkill/skills/llm-wiki/` |
| Skill Evolution 完整原始技能定義 | `AgentDoc/EvoSkill/skills/skill-evolution/` |
| wiki_root（明確設定） | `AgentDoc/EvoSkill/wiki/` |
| 改善提案、baseline、候選、評估與回復證據 | `AgentDoc/EvoSkill/wiki/evolution/<candidate-id>/` |
| 搬移完整性證據 | `AgentDoc/EvenStore/skill-relocation-sha256.json` |

`.agents/skills/llm-wiki` 與 `skill-evolution` 是指向上述原始定義的符號連結；搬移時未修改技能語意或支援檔案。其他技能維持原位。

目前只建立路徑映射，尚未匯入 Wiki 知識、產生候選或執行改善評估。首次授權寫入時依 llm-wiki 建立必要 index/log/source/page；不要預先建立空候選。Wiki 更新後必須執行 skill-evolution assess，無足夠證據可回報 insufficient-evidence；技能啟用仍須依該 skill 的門檻與使用者授權。

此處的 llm-wiki 是 Agent 流程，與外部 LLM Wiki 桌面應用分開；本次未安裝該桌面應用。
