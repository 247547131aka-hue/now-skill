#!/usr/bin/env python3
"""
Social media content parser for now-skill.

Extracts stylistic patterns, tone, and persona signals from
social media posts (screenshots, text dumps, etc.).
Built to work with Claude's image recognition output.
"""

import re
import sys
import json
import os
import argparse
from collections import Counter


def analyze_social_content(text: str) -> dict:
    """
    Analyze social media post text for persona signals.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
        r"\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
        r"☀-⛿✀-➿️]"
    )
    hashtag_pattern = re.compile(r"#\w+")
    url_pattern = re.compile(r"https?://\S+")

    all_emojis = []
    all_hashtags = []
    all_urls = []

    for line in lines:
        all_emojis.extend(emoji_pattern.findall(line))
        all_hashtags.extend(hashtag_pattern.findall(line))
        all_urls.extend(url_pattern.findall(line))

    emoji_counter = Counter(all_emojis)

    # Tone indicators
    exclamation_ratio = sum(1 for l in lines if "!" in l) / max(len(lines), 1)
    question_ratio = sum(1 for l in lines if "?" in l) / max(len(lines), 1)
    ellipsis_ratio = sum(1 for l in lines if "..." in l or "…" in l) / max(len(lines), 1)
    avg_line_length = sum(len(l) for l in lines) / max(len(lines), 1)

    # Content category detection
    categories = {
        "music": any(kw in text.lower() for kw in ["music", "song", "歌", "音乐", "播放", "听"]),
        "food": any(kw in text.lower() for kw in ["food", "eat", "吃", "美食", "好吃", "餐厅"]),
        "travel": any(kw in text.lower() for kw in ["travel", "trip", "旅行", "旅游", "出发", "风景"]),
        "work": any(kw in text.lower() for kw in ["work", "job", "工作", "上班", "加班", "会议"]),
        "fitness": any(kw in text.lower() for kw in ["gym", "workout", "健身", "运动", "跑步"]),
        "reading": any(kw in text.lower() for kw in ["book", "read", "书", "读", "阅读"]),
        "pets": any(kw in text.lower() for kw in ["cat", "dog", "猫", "狗", "宠物", "喵", "汪"]),
        "gaming": any(kw in text.lower() for kw in ["game", "游戏", "玩", "打"]),
    }

    active_categories = [cat for cat, present in categories.items() if present]

    return {
        "post_count": len(lines),
        "avg_chars_per_post": round(avg_line_length, 1),
        "top_emojis": emoji_counter.most_common(8),
        "emoji_per_post": round(len(all_emojis) / max(len(lines), 1), 2),
        "hashtags": all_hashtags[:20],
        "url_count": len(all_urls),
        "exclamation_frequency": f"{round(exclamation_ratio * 100)}%",
        "question_frequency": f"{round(question_ratio * 100)}%",
        "ellipsis_frequency": f"{round(ellipsis_ratio * 100)}%",
        "active_categories": active_categories,
        "tone": "casual" if avg_line_length < 50 else "detailed",
        "samples": lines[:10],
    }


def main():
    parser = argparse.ArgumentParser(description="Social media content parser for now-skill")
    parser.add_argument("--dir", help="Directory containing social media text/image files")
    parser.add_argument("--text", help="Pasted social media text")
    parser.add_argument("--output", default="/tmp/social_out.txt", help="Output file path")

    args = parser.parse_args()

    all_text = ""

    if args.text:
        all_text = args.text

    elif args.dir and os.path.isdir(args.dir):
        for fname in sorted(os.listdir(args.dir)):
            fpath = os.path.join(args.dir, fname)
            if fname.startswith("."):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext in (".txt", ".md", ".csv"):
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    all_text += f"\n--- {fname} ---\n" + f.read()

    else:
        print("Error: Provide --dir or --text")
        sys.exit(1)

    if not all_text.strip():
        print("Error: No text content found")
        sys.exit(1)

    analysis = analyze_social_content(all_text)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# Social Media Analysis\n\n")
        f.write(f"Posts analyzed: {analysis['post_count']}\n")
        f.write(f"Average chars/post: {analysis['avg_chars_per_post']}\n")
        f.write(f"Tone: {analysis['tone']}\n")
        f.write(f"Active categories: {', '.join(analysis['active_categories'])}\n\n")
        f.write(f"Top emojis: {json.dumps(analysis['top_emojis'], ensure_ascii=False)}\n")
        f.write(f"Hashtags: {json.dumps(analysis['hashtags'], ensure_ascii=False)}\n\n")
        f.write("## Sample Posts\n")
        for s in analysis["samples"]:
            f.write(f"- {s[:200]}\n")

    print(json.dumps(analysis, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
