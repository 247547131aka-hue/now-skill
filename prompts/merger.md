# 增量更新合并器

## 核心原则

now-skill 的增量更新遵循以下原则，区别于 ex-skill 的全量重建：

### 🔑 关键差异

| | ex-skill | now-skill |
|--|----------|-----------|
| 合并策略 | 全量重建 | 增量合并 |
| 旧数据 | 覆盖 | 归档到 timeline |
| 新数据 | 替换所有 | 追加 + 趋势更新 |

## 合并流程

### 1. 解析新内容
- 调用对应 parser（wechat/qq/social/photo）
- 提取结构化信息：时间、话题、情绪、新行为

### 2. 读取现有数据
- `memory.md` → 最新的 Living Memory
- `persona.md` → Layer 5 趋势信号 + Layer 0-4 人格
- `timeline.json` → 历史快照
- `meta.json` → 元数据

### 3. 计算 Delta

**新增的事实**：
- 之前没有的约会地点/记忆片段
- 新出现的口头禅/口头语
- 新发现的偏好/习惯
→ 追加到 Living Memory

**变化的行为**：
- 回应速度的变化（快→慢 / 慢→快）
- 主动聊天频率的变化
- 互动模式的变化
→ 更新 Layer 5 趋势信号

**稳定的模式（无变化）**：
→ 不做修改，标注"确认仍符合模式"

**矛盾的信息**：
- 新的行为与 Layer 0-4 矛盾
→ 不修改核心人格层，在 Layer 5 标注"最近出现不一致"

### 4. 创建 timeline snapshot
```json
{
  "timestamp": "ISO时间",
  "source": "微信聊天记录 / 口述 / 社媒 / inbox",
  "delta": {
    "new_facts": [...],
    "behavior_changes": [...],
    "emotions": {...},
    "topics": {...}
  },
  "summary": "一句话总结这次更新发现了什么"
}
```

### 5. 写入更新

**不改动的文件**：
- `memory.md` → Frozen Memory（除非用户纠正）
- `persona.md` → Layer 0-4（除非用户纠正）

**更新的文件**：
- `memory.md` → Living Memory（追加新内容在前）
- `persona.md` → Layer 5（刷新趋势信号）
- `timeline.json` → 追加新快照
- `meta.json` → 更新 updated_at

**重新生成**：
- `SKILL.md` → 合并最新的 memory + persona

### 6. 报告给用户

```
✅ 更新完成！

发现了这些新信息：
- 🆕 新口头禅：{xxx}
- 📊 情绪变化：{xxx}
- 🗣️ 新话题：{xxx}

没有发现变化的部分：
- 核心人格特征保持稳定
- Frozen Memory 没有改动

时间线快照已保存。
```

## 特殊处理

### 纠正型更新
如果用户说"不对，ta应该是..."：
- 判断属于 Memory 纠正还是 Persona 纠正
- Memory 纠正 → 修改对应的 Frozen/Living Memory
- Persona 纠正 → 修改对应的 Layer
- 追加纠正记录到 `corrections/`

### 冲突型更新
如果新数据与 Frozen Memory 矛盾：
- 如果是事实矛盾 → 提醒用户确认，不自动覆盖
- 如果是行为矛盾 → 记录为"行为变化"，不覆盖核心人格层

### 不足数据的更新
如果新数据太少（少于 10 条消息或 100 字口述）：
- 仍处理但不做趋势推断
- 只在 Living Memory 追加新事实
- 不刷新 Layer 5（需要累计数据变化才更新趋势信号）
