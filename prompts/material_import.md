# 原材料导入流程

## 所有数据导入方式

根据用户选择，支持以下导入路径：

---

### 方式 A：微信聊天记录

```
python3 ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py \
  --file {path} \
  --target "{name}" \
  --output /tmp/wechat_out.txt \
  --format auto
```

支持：txt/csv/html/json

---

### 方式 B：QQ 聊天记录

```
python3 ${CLAUDE_SKILL_DIR}/tools/qq_parser.py \
  --file {path} \
  --target "{name}" \
  --output /tmp/qq_out.txt
```

支持：txt/mht

---

### 方式 C：社交媒体

```
python3 ${CLAUDE_SKILL_DIR}/tools/social_parser.py \
  --dir {screenshot_dir} \
  --output /tmp/social_out.txt
```

截图直接使用 Read 工具读取。

---

### 方式 D：照片

```
python3 ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py \
  --dir {photo_dir} \
  --output /tmp/photo_out.txt
```

---

### 方式 E：直接粘贴/口述

用户粘贴或口述的内容直接作为文本原材料。

---

### 🆕 方式 F：收件箱模式

创建 now-skill 后，用户只需把新文件丢进 `nows/{slug}/inbox/`。

执行 `/now-update {slug}` 时：

1. 扫描 `nows/{slug}/inbox/` 下所有文件
2. 根据扩展名判断类型：
   - `.txt` `.csv` `.json` `.html` → 微信/QQL解析（尝试多个 parser）
   - `.jpg` `.jpeg` `.png` `.bmp` → 图片，Read 工具识别文字内容
   - `.md` `.pdf` → Read 工具读取
3. 提取新信息并合并到 Living Memory
4. 处理完的文件移到 `inbox/processed/`

inbox 模式的优势：无需每次都在对话中指定文件路径，文件即数据。

---

### 🆕 方式 G：对话粘贴 `/now-feed {slug}`

用户直接粘贴聊天：

```
/now-feed {slug}
ta：今天吃饭了吗
我：吃了 你呢
ta：我也吃了 今天好累
```

处理流程：
1. 识别对话格式（`名字：内容` 或 `名字: 内容`）
2. 提取 ta 的消息内容
3. 分析新信息：新话题、情绪变化、新的口头禅
4. 合并到 Living Memory + 趋势信号

对话粘贴的优势：零摩擦，刚聊完就可以立刻记录。

---

### 🆕 方式 H：截图导入

用户截图丢进 inbox。

处理流程：
1. 使用 Read 工具读取图片
2. 提取图片中的对话文本
3. 按对话格式解析
4. 按方式 G 的逻辑提取新信息

截图导入的优势：手机聊天不方便导出时，截图即可。

---

## 导入后流程（无论哪种方式）

1. 解析新内容 → 提取结构化信息
2. 读取现有 `memory.md`、`persona.md`、`meta.json`、`timeline.json`
3. 计算 delta（新增事实、行为模式变化、情绪变化）
4. 创建 timeline snapshot
5. 合并到 Living Memory + 趋势信号层
6. 重新生成 SKILL.md
7. 告知用户发现了哪些新信息
