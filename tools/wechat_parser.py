#!/usr/bin/env python3
"""
WeChat chat log parser for now-skill.

Parses exported WeChat chat logs in various formats (txt, csv, html, json)
and extracts messages, patterns, and metadata.
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime
from collections import Counter


def parse_txt(filepath: str, target_name: str) -> list:
    """
    Parse WeChat txt export format.
    Common format: "YYYY-MM-DD HH:MM:SS Name\nMessage"
    or: "Name  MM/DD HH:MM\nMessage"
    """
    messages = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern 1: "YYYY-MM-DD HH:MM:SS Name"
    pattern1 = re.compile(
        r"(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+([^\n]+?)\n(.*?)(?=\n\d{4}-\d{2}-\d{2}|\Z)",
        re.DOTALL
    )
    # Pattern 2: "Name  MM/DD HH:MM"
    pattern2 = re.compile(
        r"([^\n]+?)\s+(\d{1,2}/\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\n(.*?)(?=\n[^\n]+\s+\d{1,2}/\d{1,2}|\Z)",
        re.DOTALL
    )
    # Pattern 3: Simple "Name: Message"
    pattern3 = re.compile(r"^([^:：\n]+)[：:]\s*(.+)$", re.MULTILINE)

    for pattern in [pattern1, pattern2]:
        for match in pattern.finditer(content):
            if pattern is pattern1:
                timestamp_str, name, msg = match.groups()
            else:
                name, timestamp_str, msg = match.groups()

            msg = msg.strip()
            if msg and name.strip():
                messages.append({
                    "timestamp": timestamp_str.strip(),
                    "name": name.strip(),
                    "message": msg,
                    "is_target": target_name and target_name in name.strip(),
                })

    if not messages:
        # Fallback to simple pattern
        for match in pattern3.finditer(content):
            name, msg = match.groups()
            msg = msg.strip()
            if msg and name.strip():
                messages.append({
                    "timestamp": "",
                    "name": name.strip(),
                    "message": msg,
                    "is_target": target_name and target_name in name.strip(),
                })

    return messages


def parse_csv(filepath: str, target_name: str) -> list:
    """Parse WeChat CSV export format."""
    import csv
    messages = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", row.get("sender", row.get("Name", "")))
            msg = row.get("message", row.get("content", row.get("Message", row.get("text", ""))))
            ts = row.get("timestamp", row.get("time", row.get("datetime", row.get("Time", ""))))
            if msg.strip():
                messages.append({
                    "timestamp": str(ts).strip(),
                    "name": str(name).strip(),
                    "message": str(msg).strip(),
                    "is_target": target_name and target_name in str(name),
                })
    return messages


def analyze_messages(messages: list, target_name: str) -> dict:
    """Analyze parsed messages and extract patterns."""
    if not messages:
        return {"error": "No messages found", "message_count": 0}

    target_msgs = [m for m in messages if m.get("is_target")]
    user_msgs = [m for m in messages if not m.get("is_target")]

    # Word frequency
    all_target_words = []
    for m in target_msgs:
        all_target_words.extend(m["message"])

    word_chars = "".join(all_target_words)
    # Simple char-level n-gram detection for catchphrases
    catchphrases_candidates = []
    for length in [2, 3, 4]:
        for i in range(len(word_chars) - length + 1):
            ngram = word_chars[i:i+length]
            if word_chars.count(ngram) >= 5 and ngram not in catchphrases_candidates:
                catchphrases_candidates.append(ngram)

    # Emoji detection
    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
        r"\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
        r"☀-⛿✀-➿️]"
    )
    emojis = []
    for m in target_msgs:
        emojis.extend(emoji_pattern.findall(m["message"]))

    emoji_counter = Counter(emojis)

    # Response time patterns
    avg_length = sum(len(m["message"]) for m in target_msgs) / max(len(target_msgs), 1)

    return {
        "total_messages": len(messages),
        "target_messages": len(target_msgs),
        "user_messages": len(user_msgs),
        "target_ratio": round(len(target_msgs) / max(len(messages), 1) * 100, 1),
        "avg_message_length": round(avg_length, 1),
        "top_emojis": emoji_counter.most_common(10),
        "catchphrase_candidates": catchphrases_candidates[:15],
        "sample_messages": [
            {"name": m["name"], "message": m["message"][:200]}
            for m in target_msgs[:20]
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="WeChat chat log parser for now-skill")
    parser.add_argument("--file", required=True, help="Path to WeChat export file")
    parser.add_argument("--target", default="", help="Target person's display name")
    parser.add_argument("--output", default="/tmp/wechat_out.txt", help="Output file path")
    parser.add_argument("--format", default="auto",
                        choices=["auto", "txt", "csv", "html", "json"],
                        help="Input file format")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    ext = os.path.splitext(args.file)[1].lower()

    if args.format == "auto":
        if ext == ".csv":
            parse_func = parse_csv
        elif ext == ".json":
            parse_func = None  # TODO
        else:
            parse_func = parse_txt
    elif args.format == "csv":
        parse_func = parse_csv
    else:
        parse_func = parse_txt

    if parse_func is None:
        print("Error: Unsupported format")
        sys.exit(1)

    messages = parse_func(args.file, args.target)

    if not messages:
        print("No messages parsed. Trying all available parsers...")
        # Try all parsers
        for func in [parse_txt, parse_csv]:
            messages = func(args.file, args.target)
            if messages:
                break

    analysis = analyze_messages(messages, args.target)

    # Output
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# WeChat Analysis\n\n")
        f.write(f"Target: {args.target or '(auto-detect)'}\n")
        f.write(f"Total messages: {analysis['total_messages']}\n")
        f.write(f"Target messages: {analysis['target_messages']}\n")
        f.write(f"Target ratio: {analysis['target_ratio']}%\n")
        f.write(f"Average message length: {analysis['avg_message_length']} chars\n\n")

        f.write("## Top Emojis\n")
        for emoji, count in analysis.get("top_emojis", []):
            f.write(f"- {emoji}: {count}\n")

        f.write(f"\n## Sample Messages\n")
        for m in analysis.get("sample_messages", []):
            f.write(f"- [{m['name']}] {m['message']}\n")

    print(json.dumps(analysis, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
