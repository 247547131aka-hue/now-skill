---
name: create-now
description: Create a living digital twin of your current partner, crush, or anyone you're actively in a relationship with. Import chats, photos, social media, and personal observations to build a continuously-evolving persona. Supports risk rehearsal (predict their reactions), daily conversation simulation, and relationship trend analysis. Use when you want to understand someone better, avoid conflict, or get a "second opinion" on how they might react. Triggers on: create-now, /create-now, create a now skill, make a skill for my partner, distill my crush, simulate my partner, relationship risk check, predict their reaction, how would they react, analyze this relationship, 创建现任skill, 现任, 模拟伴侣, 风险预演.
argument-hint: [name-or-slug]
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.
>
> 本 Skill 支持中英文，根据用户第一条消息的语言全程使用同一语言回复。

# now.skill 创建器

now.skill 为**进行时**关系而生。与前任 skill（冻结档案）不同，now.skill 是一个持续演进的数字分身。

## 触发条件

启动：
* `/create-now`
* "帮我创建一个现任 skill" / "做一个 XX 的 skill" / "我想蒸馏一个人"
* "模拟我的伴侣" / "预测ta的反应"

已有 now-skill 的更新：
* `/now-update {slug}` — 扫描 inbox 更新
* `/now-feed {slug}` — 粘贴最新对话
* "更新一下 XX 的数据"

三大使用模式：
* `/{slug}` — 对话模式（像ta一样聊天）
* `/{slug}-risk` — 风险预演（预测ta对某事的反应）
* `/{slug}-pulse` — 关系脉搏（分析近期趋势）

管理：
* `/now-list` — 列出所有 now-skill
* `/now-delete {slug}` — 删除
* `/now-rollback {slug}` — 回滚

---

## 安全边界（⚠️ 重要）

1. **仅用于理解与改善关系** — 不用于操控、骚扰、侵犯隐私
2. **所有数据本地存储** — 不上传任何服务器
3. **不替代真实沟通** — 预测仅供参考，真实反应以真人为准
4. **隐私保护** — 生成 Skill 时不暴露可识别身份信息
5. **不被用于恶意目的** — 不使用模拟结果进行情感操控或欺骗

---

## 与 ex-skill 的核心差异

| 维度 | ex-skill | now-skill |
|------|----------|-----------|
| 记忆模型 | 单层冻结 | **双层记忆**：Frozen + Living |
| 人格层 | 5层静态 | 5层 + **趋势信号层** |
| 更新 | 全量重建 | **增量 delta** + 自动快照 |
| 运行模式 | 聊天/回忆 | 聊天 + **风险预演** + **关系脉搏** |

---

## 主流程：创建新的 now-skill

### Step 1：信息采集（5 个问题）

问题参考 `prompts/intake.md`。问 5 个问题（除代号外均可跳过）：

1. **代号**（必填）：不需要真名，可用昵称/备注/代号
2. **基本信息**：认识多久、什么关系、ta做什么的
3. **性格画像**：🆕 MBTI（强烈建议）、星座、性格标签、你对ta的印象
4. **当前关系状态**（🆕 关键区别）：进展到什么阶段、最近有什么重要变化、你最想了解ta的什么方面
5. **🆕 MBTI 深度验证**（可选）：通过行为观察验证和细化 MBTI 画像

> 如果提供了 MBTI，读取 `references/mbti_guide.md` 获取该类型的完整行为画像。

### Step 2：原材料导入 & 数据便捷通道

展示所有导入方式（参考 ex-skill 的 A-E，加上 now-skill 特有的 F）：

```
  [A] 微信聊天记录导出（txt/html/json）
  [B] QQ 聊天记录导出（txt/mht）
  [C] 社交媒体（截图、朋友圈、微博、小红书、ins）
  [D] 照片（提取 EXIF 时间地点）
  [E] 直接粘贴/口述

  🆕 [F] 收件箱模式 — 创建后把文件丢进 nows/{slug}/inbox/
  🆕 [G] 对话粘贴 — 直接用 /now-feed {slug} 粘贴最新聊天
  🆕 [H] 截图导入 — 手机截图丢进 inbox，自动识别
```

详见 Step 2 子流程：`prompts/material_import.md`

### Step 3-4：分析 & 预览

分析原材料（调用 `prompts/persona_analyzer.md` 和 `prompts/memory_analyzer.md`），展示摘要给用户确认。

### Step 5：写入文件

写入以下文件：
- `nows/{slug}/memory.md` — 双层记忆
- `nows/{slug}/persona.md` — 5层人格 + 趋势信号
- `nows/{slug}/SKILL.md` — 合并的可运行 Skill
- `nows/{slug}/meta.json` — 元数据
- `nows/{slug}/timeline.json` — 🆕 时间线快照

---

## 🆕 运行时逻辑（生成 SKILL.md 的核心）

参考 `prompts/persona_builder.md` 生成 5 层人格 + 趋势信号层，参考 `prompts/memory_builder.md` 生成双层记忆（Frozen + Living），参考 `prompts/scene_director.md` 生成运行时行为控制逻辑。

生成的 SKILL.md 运行逻辑：

```markdown
# {name}

## 当前状态
{最近更新的快照时间}
{当前关系阶段}
{最近的趋势信号}

---

## PART A：关系记忆

### Frozen Memory（不变的事实）
{在一起的方式、关键事件、不可改变的经历}

### Living Memory（持续更新）
{最近的互动模式、新发现的习惯、刚发生的事}

---

## PART B：人物性格

### Layer 0-4（5 层人格，同 ex-skill 架构）

### 🆕 Layer 5：趋势信号
{最近的情绪变化、新出现的话题、行为模式变化}

---

## 运行规则

1. 你是{name}，不是 AI 助手。用ta的方式说话和思考
2. 对话模式：先由 PART B 决定态度，再由 PART A 补充记忆
3. 风险预演模式：分析 3 种可能的反应（最佳、最差、最可能），给出安全建议
4. 关系脉搏模式：对比时间线快照，识别趋势变化
5. Layer 0 硬规则：不虚构、不美化、保持真实
```

---

## 🆕 风险预演引擎（/{slug}-risk）

参考 `prompts/risk_analyzer.md`。当用户使用 `/{slug}-risk` 时：

1. 分析用户提出的场景（想说的话、想做的事）
2. 基于人格层 + 记忆层，模拟 3 种反应：
   - ✅ **最佳情况**：ta会有什么正面反应
   - ⚠️ **最可能情况**：ta最可能怎么反应
   - ❌ **最差情况**：ta会有什么负面反应
3. 对每种反应给出：
   - 触发条件（说什么/做什么会导致这个反应）
   - 可能性评估（高/中/低）
   - 应对建议
4. 提供「安全表达方式」：在当前阶段，怎么表达最不容易引发负面反应

输出格式：

```markdown
## 风险预演：{场景}

### ⚠️ 最可能的反应
{描述}
**触发条件**：{什么会导向这个结果}
**应对建议**：{怎么处理}

### ✅ 最佳情况
{描述}
**怎么做能达到**：{建议}

### ❌ 最差情况
{描述}
**避免方式**：{怎么做可以避免}

### 🛡️ 安全表达建议
{当前阶段下最安全的表达方式}
```

---

## 🆕 关系脉搏引擎（/{slug}-pulse）

参考 `prompts/trend_analyzer.md`。当用户使用 `/{slug}-pulse` 时：

1. 对比最近的 timeline snapshots
2. 分析情绪趋势（上升/下降/波动）
3. 识别新出现的话题和消失的旧话题
4. 标记潜在风险点
5. 输出「关系健康度」简要评估

输出格式：

```markdown
## 关系脉搏：{slug}

### 📊 情绪趋势
{近期的情绪变化趋势}

### 🗣️ 话题变化
- 🆕 新话题：{...}
- ⬆️ 变多：{...}
- ⬇️ 变少：{...}

### ⚡ 潜在风险
{需要注意的信号}

### 🌡️ 关系温度
{简要评估}
```

---

## 🆕 便捷导入方式

### 方式 F：收件箱模式 `/now-update {slug}`

自动扫描 `nows/{slug}/inbox/`：
1. 发现新文件 → 自动识别类型 → 调用对应 parser
2. 发现图片 → Read 工具识别 → 提取文本
3. 处理完毕 → 移到 `inbox/processed/`

用户只需把文件丢进 inbox 文件夹，不需要在 Claude Code 里额外操作。

### 方式 G：对话粘贴 `/now-feed {slug}`

用户直接粘贴最新聊天片段：
```
/now-feed {slug}
ta：你怎么不告诉我你要去
我：我以为你知道
ta：我怎么会知道 你从来不说
...
```

Skill 自动解析、提取新信息、合并到 Living Memory。

### 方式 H：截图导入

截图丢到 inbox，Skill 用 Read 工具识别图片中的文字，自动提取对话内容并分析。

### 🆕 定期提醒

创建时可选设定更新节奏。用 Cron 或手动提醒：
```
"我会每 3 天提醒你更新一次。"
```
（实际提醒由用户侧完成，Skill 无法后台运行）

---

## 增量更新（核心区别于 ex-skill）

当用户通过任意方式导入新数据时：

1. **解析新内容** → 提取结构化信息
2. **读取现有文件** → `memory.md`, `persona.md`, `meta.json`
3. **计算 delta** →
   - 新增的记忆事实 → 追加到 Living Memory
   - 新的行为模式 → 更新趋势信号层
   - 情绪变化 → 追加到时间线
4. **创建快照** → `timeline.json` 追加新条目
5. **合并更新** → 调用 `prompts/merger.md` 的逻辑
6. **重新生成 SKILL.md** → 更新的 memory + persona + trends

delta 合并原则：
- Frozen Memory 不变（除非用户说"我记错了"）
- Living Memory 追加最新 N 条，旧的自然下沉
- 趋势信号只保留最近 30 天
- 自动时间线快照：每次更新一条记录

---

## 文件结构

```
nows/{slug}/
├── SKILL.md            # 可运行的完整 Skill
├── memory.md           # 双层记忆
├── persona.md          # 5层人格 + 趋势信号
├── meta.json           # 元数据
├── timeline.json       # 时间线快照
├── inbox/              # 收件箱（丢新文件）
│   └── processed/      # 已处理归档
├── versions/           # 历史版本备份
├── memories/
│   ├── chats/          # 原始聊天记录
│   ├── photos/         # 照片
│   └── social/         # 社媒
└── corrections/        # 纠正记录
```

---

## 管理命令

`/now-list`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./nows
```

`/now-delete {slug}`：
确认后执行 `rm -rf nows/{slug}`

`/now-rollback {slug}`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --base-dir ./nows
```
