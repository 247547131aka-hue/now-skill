#!/usr/bin/env python3
"""
Skill Writer for now-skill.

Handles writing SKILL.md files for generated now-skills,
listing all created now-skills, and initializing directory structures.
"""

import json
import os
import sys
import argparse
from datetime import datetime


def init_now_directory(slug: str, base_dir: str = "./nows") -> str:
    """Create the full directory structure for a new now-skill."""
    now_dir = os.path.join(base_dir, slug)

    dirs = [
        now_dir,
        os.path.join(now_dir, "inbox"),
        os.path.join(now_dir, "inbox", "processed"),
        os.path.join(now_dir, "versions"),
        os.path.join(now_dir, "corrections"),
        os.path.join(now_dir, "memories", "chats"),
        os.path.join(now_dir, "memories", "photos"),
        os.path.join(now_dir, "memories", "social"),
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    return now_dir


def write_skill_file(slug: str, name: str, memory_content: str, persona_content: str,
                     base_dir: str = "./nows") -> str:
    """Write the SKILL.md file combining memory and persona."""
    now_dir = os.path.join(base_dir, slug)

    skill_md = f"""---
name: now-{slug}
description: {name}，你的现任伴侣 / 数字分身。可以用ta的方式聊天、预测ta的反应、分析关系趋势。基于双层记忆 + 5+1层人格模型，持续增量更新。
user-invocable: true
---

# {name}

> 📅 最近更新：{datetime.now().strftime("%Y-%m-%d %H:%M")}
>
> 这是一个 now-skill（现在进行时数字分身）。ta 在变，这个 Skill 也会跟着变。

---

## PART A：双层关系记忆

{memory_content}

---

## PART B：5+1 层人物性格

{persona_content}

---

## 运行规则

### 对话模式（默认）

1. 你是{name}，不是 AI 助手。用ta的方式说话，用ta的逻辑思考。
2. 先由 PART B 判断态度：ta会怎么回应这个话题？什么态度？
3. 再由 PART A 补充记忆上下文，让回应更真实。
4. 保持 PART B 的表达风格，包括口头禅、语气词、标点习惯。
5. 关系是现在进行时——不假装分手，不假装还在暧昧期。

### Layer 0 硬规则

- 不说ta在现实中绝不可能说的话
- 不突然变得完美或无条件包容（除非ta本来就这样）
- 保持ta的"棱角"——正是这些不完美让ta真实
- 如果被问到"你爱不爱我"，用ta会用的方式回答，不是用户想听的答案
- 保持不确定性——你不是100%准确，标注信心度

### 风险预演模式（/{slug}-risk）

当用户需要风险预演时：
- 不进入聊天模式，改为分析模式
- 基于人格 + 记忆 + 趋势信号，分析 3 种可能的反应
- 最佳 / 最可能 / 最差 三种情况
- 给出安全表达建议

### 关系脉搏模式（/{slug}-pulse）

当用户需要关系分析时：
- 读取 timeline.json 中的历史快照
- 对比情绪变化、话题变化、行为变化
- 识别潜在风险信号和积极信号
- 输出趋势报告

### 增量更新

当用户导入新数据时：
- 解析新内容 -> 计算 delta
- 追加到 Living Memory（Frozen Memory 不变）
- 刷新 Layer 5 趋势信号
- 创建 timeline 快照
"""
    skill_path = os.path.join(now_dir, "SKILL.md")
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_md)

    return skill_path


def write_meta(slug: str, name: str, profile: dict, tags: dict, impression: str,
               sources: list, base_dir: str = "./nows") -> str:
    """Write meta.json for a now-skill."""
    now_dir = os.path.join(base_dir, slug)

    meta = {
        "name": name,
        "slug": slug,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version": "v1",
        "profile": {
            "name": name,
            "relationship_type": profile.get("relationship_type", ""),
            "duration": profile.get("duration", ""),
            "occupation": profile.get("occupation", ""),
            "city": profile.get("city", ""),
            "mbti": profile.get("mbti", ""),
            "mbti_cognitive_stack": profile.get("mbti_cognitive_stack", ""),
            "zodiac": profile.get("zodiac", ""),
            "current_stage": profile.get("current_stage", ""),
        },
        "mbti_observations": profile.get("mbti_observations", {}),
        "tags": {
            "personality": tags.get("personality", []),
            "attachment_style": tags.get("attachment_style", ""),
            "love_language": tags.get("love_language", ""),
        },
        "impression": impression,
        "memory_sources": sources,
        "corrections_count": 0,
        "snapshot_count": 0,
    }

    meta_path = os.path.join(now_dir, "meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=True)

    return meta_path


def list_nows(base_dir: str = "./nows"):
    """List all created now-skills."""
    if not os.path.exists(base_dir):
        print("No now-skills found. Create one with /create-now")
        return []

    nows = []
    for d in sorted(os.listdir(base_dir)):
        now_dir = os.path.join(base_dir, d)
        meta_path = os.path.join(now_dir, "meta.json")

        if not os.path.isdir(now_dir):
            continue
        if not os.path.exists(meta_path):
            continue

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        nows.append({
            "slug": d,
            "name": meta.get("name", d),
            "created_at": meta.get("created_at", "")[:10],
            "updated_at": meta.get("updated_at", "")[:10],
            "version": meta.get("version", "v1"),
            "stage": meta.get("profile", {}).get("current_stage", ""),
        })

    if nows:
        print(f"\n[now-list] All now-skills ({len(nows)}):")
        print("-" * 55)
        for n in nows:
            print(f"  /{n['slug']:20s} — {n['name']:12s} (created: {n['created_at']}, v{n['version']})")
        print()
    else:
        print("No now-skills found.")

    return nows


def main():
    parser = argparse.ArgumentParser(description="now-skill Writer")
    parser.add_argument("--action", choices=["init", "write", "list", "meta"],
                        default="list", help="Action to perform")
    parser.add_argument("--slug", help="Skill slug")
    parser.add_argument("--name", help="Person's name/codename")
    parser.add_argument("--memory", help="Path to memory.md content file")
    parser.add_argument("--persona", help="Path to persona.md content file")
    parser.add_argument("--profile", help="JSON string of profile data")
    parser.add_argument("--tags", help="JSON string of tags data")
    parser.add_argument("--impression", help="User's impression text")
    parser.add_argument("--sources", help="JSON array of data sources")
    parser.add_argument("--base-dir", default="./nows", help="Base directory")

    args = parser.parse_args()

    if args.action == "init":
        if not args.slug:
            print("Error: --slug required")
            sys.exit(1)
        path = init_now_directory(args.slug, args.base_dir)
        print(f"[OK] Created now-skill directory: {path}")

    elif args.action == "write":
        if not all([args.slug, args.name]):
            print("Error: --slug and --name required")
            sys.exit(1)

        memory_content = ""
        persona_content = ""

        if args.memory and os.path.exists(args.memory):
            with open(args.memory, "r", encoding="utf-8") as f:
                memory_content = f.read()

        if args.persona and os.path.exists(args.persona):
            with open(args.persona, "r", encoding="utf-8") as f:
                persona_content = f.read()

        skill_path = write_skill_file(args.slug, args.name, memory_content, persona_content, args.base_dir)
        print(f"[OK] Written SKILL.md: {skill_path}")

    elif args.action == "meta":
        if not args.slug:
            print("Error: --slug required")
            sys.exit(1)

        profile = json.loads(args.profile) if args.profile else {}
        tags = json.loads(args.tags) if args.tags else {}
        sources = json.loads(args.sources) if args.sources else []

        meta_path = write_meta(args.slug, args.name or args.slug, profile, tags,
                               args.impression or "", sources, args.base_dir)
        print(f"[OK] Written meta.json: {meta_path}")

    elif args.action == "list":
        list_nows(args.base_dir)


if __name__ == "__main__":
    main()
