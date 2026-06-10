#!/usr/bin/env python3
"""
QQ and generic chat log parser for now-skill.

Handles QQ txt/mht exports and provides a generic "paste" parser
for the /now-feed frictionless import path.
"""

import re
import sys
import json
import os
import argparse
from collections import Counter


def parse_qq_txt(filepath: str, target_name: str = "") -> list:
    """
    Parse QQ chat txt export.
    Format: "YYYY-MM-DD HH:MM:SS Name\nMessage\n"
    or: "Name  MM/DD HH:MM:SS\nMessage\n"
    """
    messages = []
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Pattern 1: Timestamped lines
    pattern = re.compile(
        r"(?:(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+)?([^\n]+?)(?:\n|\s+)(.*?)(?=\n\d{4}-\d{2}-\d{2}|\n[^\n]+?\s+\d{1,2}/\d{1,2}|\Z)",
        re.DOTALL
    )

    for match in pattern.finditer(content):
        timestamp, name, msg = match.groups()
        msg = (msg or "").strip()
        name = (name or "").strip()
        if msg and name:
            messages.append({
                "timestamp": (timestamp or "").strip(),
                "name": name,
                "message": msg,
                "is_target": target_name and target_name in name,
            })

    return messages


def parse_pasted_chat(text: str, target_name: str = "") -> list:
    """
    Parse pasted chat text from /now-feed.

    Recognizes these formats:
    - Name: Message
    - Name：Message
    - [Name] Message
    """
    messages = []
    pattern = re.compile(r"^([^\n:：]{1,30})[：:]\s*(.+)$", re.MULTILINE)

    for match in pattern.finditer(text):
        name = match.group(1).strip()
        msg = match.group(2).strip()
        if msg:
            messages.append({
                "timestamp": "",
                "name": name,
                "message": msg,
                "is_target": target_name and (target_name in name),
            })

    return messages


def parse_social_text(text: str) -> dict:
    """
    Parse social media content (posts, captions, etc.).
    Extracts stylistic markers: emojis, hashtags, mention patterns.
    """
    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
        r"\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
        r"☀-⛿✀-➿️]"
    )
    hashtag_pattern = re.compile(r"#\w+")
    mention_pattern = re.compile(r"@\w+")
    url_pattern = re.compile(r"https?://\S+")

    emojis = emoji_pattern.findall(text)
    hashtags = hashtag_pattern.findall(text)
    mentions = mention_pattern.findall(text)
    urls = url_pattern.findall(text)

    return {
        "char_count": len(text),
        "line_count": len(text.split("\n")),
        "emojis": Counter(emojis).most_common(10),
        "hashtags": hashtags,
        "mentions": mentions,
        "urls": urls,
        "has_emojis": len(emojis) > 0,
        "emoji_density": round(len(emojis) / max(len(text), 1) * 100, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="QQ & chat log parser for now-skill")
    parser.add_argument("--file", help="Path to chat log file")
    parser.add_argument("--text", help="Pasted chat text (from /now-feed)")
    parser.add_argument("--target", default="", help="Target person's display name")
    parser.add_argument("--output", default="/tmp/qq_out.txt", help="Output file path (when using --file)")

    args = parser.parse_args()

    if args.text:
        # Paste mode
        messages = parse_pasted_chat(args.text, args.target)
        analysis = {
            "source": "pasted_chat",
            "total_messages": len(messages),
            "target_messages": len([m for m in messages if m.get("is_target")]),
            "messages": messages,
        }
        print(json.dumps(analysis, indent=2, ensure_ascii=True))
        return

    if args.file and os.path.exists(args.file):
        messages = parse_qq_txt(args.file, args.target)

        if not messages:
            # Try as generic pasted text
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            messages = parse_pasted_chat(content, args.target)

        target_msgs = [m for m in messages if m.get("is_target")]

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"# Chat Analysis\n\n")
            f.write(f"Target: {args.target or '(auto-detect)'}\n")
            f.write(f"Total messages: {len(messages)}\n")
            f.write(f"Target messages: {len(target_msgs)}\n\n")
            f.write("## Messages\n")
            for m in messages[:50]:
                f.write(f"- [{m['name']}] {m['message'][:200]}\n")

        result = {
            "total_messages": len(messages),
            "target_messages": len(target_msgs),
            "sample": [m["message"][:200] for m in target_msgs[:20]],
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Error: Provide --file or --text")
        sys.exit(1)


if __name__ == "__main__":
    main()
