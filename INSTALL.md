# 安装指南

## 快速安装

### Claude Code（推荐）

**全局安装**（所有项目可用）：
```bash
git clone https://github.com/<your-username>/now-skill ~/.claude/skills/now-skill
```

**项目级安装**：
```bash
mkdir -p .claude/skills
git clone https://github.com/<your-username>/now-skill .claude/skills/now-skill
```

安装后重启 Claude Code，输入 `/create-now` 即可开始。

### Claude.ai / 其他平台

1. 下载本仓库
2. 将 `SKILL.md` 的内容复制到新对话中
3. 根据 SKILL.md 的指引操作

## 验证安装

在 Claude Code 中输入：
```
/create-now
```

如果看到「代号/基本信息/性格画像/当前关系状态/MBTI深度」5 个问题的采集流程，说明安装成功。

## 依赖

### 必需
- Claude Code（或支持 Skill 的 Claude 环境）
- Python 3.8+

### 可选（增强功能）
- [Pillow](https://python-pillow.org/)：完整 EXIF 提取（`pip install Pillow`）
  - 不安装也能运行，但照片地点/时间提取会受限

## 数据导出工具推荐

参考 [导出指南](docs/EXPORT_GUIDE.md)
