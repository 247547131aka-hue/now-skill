# now.skill — 把现任蒸馏成 AI Skill

> ⚡ **ex-skill 的前任是过去式，now-skill 的现任是现在进行时。**

把你的现任伴侣（或任何人）变成可运行的 AI Skill。导入聊天记录、照片、社交媒体、主观描述，生成双层记忆 + 5+1 层人格模型，支持**风险预演**、**日常对话模拟**、**关系趋势分析**，持续增量更新。

---

## 🔥 与 ex-skill 的核心区别

| 维度 | [ex-skill](https://github.com/therealXiaomanChu/ex-skill) | **now-skill** |
|------|----------|-----------|
| **时间态** | 过去式，档案冻结 | **现在进行时，持续演进** |
| **记忆模型** | 单层冻结记忆 | **双层记忆**：Frozen + Living |
| **人格模型** | 5 层静态人格 | 5 层静态 + **趋势信号层** |
| **更新方式** | 手动备份→全量重建 | **增量 delta** + 自动时间线快照 |
| **核心场景** | 怀旧聊天 | 聊天 + **风险预演** + **关系脉搏** |
| **数据导入** | 手动指定文件 | **收件箱拖放** + **对话粘贴** + 截图即导 |

---

## 🎯 三大模式

### 💬 对话模式 `/{slug}`
像 ta 一样跟你聊天。用 ta 的说话方式、口头禅、情感模式。

### ⚠️ 风险预演 `/{slug}-risk`
预测 ta 对你的话/行动会有什么反应——最佳、最可能、最差三种情况 + 安全表达建议。

```
User: /baby-risk 我想跟ta说我最近工作压力大，需要减少见面频率
```

### 📊 关系脉搏 `/{slug}-pulse`
分析最近的互动趋势：情绪走向、话题变化、潜在风险信号。

---

## 🚀 快速开始

### 安装

**一键安装（推荐）：**

在 Claude Code 中直接粘贴：
```
/plugin install 247547131aka-hue/now-skill
```

**手动安装：**

```bash
# 全局安装（所有项目可用）
git clone https://github.com/247547131aka-hue/now-skill ~/.claude/skills/now-skill

# 或项目级安装
mkdir -p .claude/skills
git clone https://github.com/247547131aka-hue/now-skill .claude/skills/now-skill
```

### 创建第一个 now-skill

在 Claude Code 中输入：

```
/create-now
```

然后回答 4 个问题即可。创建完成后：

```
/baby-risk 我想送ta一个手工礼物，但不知道ta会不会觉得廉价
```

---

## 📥 数据导入（零摩擦）

| 方式 | 怎么用 | 适合 |
|------|--------|------|
| **收件箱** 📥 | 文件丢进 `nows/{slug}/inbox/`，运行 `/now-update {slug}` | 批量导入 |
| **对话粘贴** 💬 | `/now-feed {slug}` 然后贴聊天 | 刚聊完立刻记录 |
| **截图导入** 📸 | 手机截图丢进 inbox | 不方便导出时 |
| **传统导入** 📂 | 同 ex-skill，支持微信/QQ/社媒/照片 | 首次大规模导入 |

---

## 📁 文件结构

```
nows/{slug}/
├── SKILL.md            # 可运行的 Skill
├── memory.md           # 双层记忆（Frozen + Living）
├── persona.md          # 5+1 层人格
├── meta.json           # 元数据
├── timeline.json       # 时间线快照（核心！）
├── inbox/              # 📥 丢新文件在这里
│   └── processed/      # 已处理归档
├── versions/           # 历史版本
└── memories/
    ├── chats/          # 聊天记录存档
    ├── photos/         # 照片存档
    └── social/         # 社媒存档
```

---

## 🛠️ 命令速查

| 命令 | 功能 |
|------|------|
| `/create-now` | 创建新的 now-skill |
| `/{slug}` | 对话模式 |
| `/{slug}-risk` | 风险预演 |
| `/{slug}-pulse` | 关系脉搏 |
| `/now-update {slug}` | 扫描 inbox 更新 |
| `/now-feed {slug}` | 对话粘贴更新 |
| `/now-list` | 列出所有 now-skill |
| `/now-delete {slug}` | 删除 |
| `/now-rollback {slug}` | 回滚到上一版本 |

---

## ⚠️ 安全边界

1. **仅用于理解与改善关系** — 不用于操控、骚扰、侵犯隐私
2. **所有数据本地存储** — 不上传任何服务器
3. **不替代真实沟通** — 预测仅供参考
4. **隐私保护** — 不暴露可识别身份信息
5. **不被用于恶意目的** — 不使用模拟结果进行情感操控

---

## 📄 许可

MIT License

## 🙏 致谢

本项目灵感来自 [ex-skill](https://github.com/therealXiaomanChu/ex-skill)、[colleague-skill](https://github.com/titanwings/colleague-skill) 和 [yourself-skill](https://github.com/notdog1998/yourself-skill)。
