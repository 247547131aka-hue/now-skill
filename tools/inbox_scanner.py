#!/usr/bin/env python3
"""
Inbox scanner for now-skill.

Scans nows/{slug}/inbox/ for new files, identifies their types,
and calls appropriate parsers. Frictionless data import.

Usage:
  python inbox_scanner.py --slug <slug> --base-dir ./nows
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path


# File type detection
FILE_TYPE_MAP = {
    ".txt": "text",
    ".csv": "csv",
    ".json": "json",
    ".html": "html",
    ".htm": "html",
    ".mht": "mht",
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".bmp": "image",
    ".gif": "image",
    ".webp": "image",
    ".md": "markdown",
    ".pdf": "pdf",
    ".docx": "word",
}


def scan_inbox(slug: str, base_dir: str = "./nows"):
    """
    Scan inbox directory and return list of new files.
    """
    inbox_path = os.path.join(base_dir, slug, "inbox")

    if not os.path.exists(inbox_path):
        return {"files": [], "message": f"Inbox not found: {inbox_path}. Create it with mkdir -p nows/{slug}/inbox/"}

    files = []
    for fname in os.listdir(inbox_path):
        fpath = os.path.join(inbox_path, fname)

        # Skip processed directory and hidden files
        if fname == "processed" or fname.startswith("."):
            continue

        if os.path.isfile(fpath):
            ext = Path(fname).suffix.lower()
            ftype = FILE_TYPE_MAP.get(ext, "unknown")
            files.append({
                "name": fname,
                "path": fpath,
                "type": ftype,
                "ext": ext,
                "size": os.path.getsize(fpath),
            })

    return {
        "files": files,
        "count": len(files),
        "inbox_path": inbox_path,
        "message": f"Found {len(files)} file(s) in inbox" if files else "Inbox is empty",
    }


def move_to_processed(slug: str, fname: str, base_dir: str = "./nows"):
    """Move a processed file to inbox/processed/."""
    inbox_path = os.path.join(base_dir, slug, "inbox")
    processed_path = os.path.join(inbox_path, "processed")
    os.makedirs(processed_path, exist_ok=True)

    src = os.path.join(inbox_path, fname)
    dst = os.path.join(processed_path, fname)

    # Avoid overwriting — append timestamp if conflict
    if os.path.exists(dst):
        name, ext = os.path.splitext(fname)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = os.path.join(processed_path, f"{name}_{timestamp}{ext}")

    shutil.move(src, dst)
    return dst


def classify_content(file_info: dict) -> str:
    """
    Guess content type based on filename and extension.
    Returns: 'wechat_chat', 'qq_chat', 'social_media', 'photo', 'text', 'unknown'
    """
    name = file_info["name"].lower()

    # WeChat patterns
    if any(kw in name for kw in ["微信", "wechat", "wx", "聊天记录"]):
        return "wechat_chat"

    # QQ patterns
    if any(kw in name for kw in ["qq", "QQ"]):
        return "qq_chat"

    # Screenshot patterns
    if file_info["type"] == "image":
        if any(kw in name for kw in ["朋友圈", "微博", "moment", "post", "weibo", "ins", "story"]):
            return "social_media"
        if any(kw in name for kw in ["聊天", "chat", "对话", "conversation", "msg"]):
            return "chat_screenshot"
        return "photo"

    return "unknown"


def parse_chat_text(content: str, target_name: str) -> dict:
    """
    Simple chat text parser.
    Recognizes lines like 'Name: message' or 'Name：message'.
    """
    import re

    messages = []
    lines = content.strip().split("\n")

    # Pattern: "Name: message" or "Name：message"
    pattern = re.compile(r"^(.+?)[：:]\s*(.+)")

    for line in lines:
        match = pattern.match(line.strip())
        if match:
            name = match.group(1).strip()
            msg = match.group(2).strip()
            if msg:
                messages.append({"name": name, "message": msg, "is_target": name == target_name})

    # Extract target's messages
    target_msgs = [m for m in messages if m["is_target"]]
    other_msgs = [m for m in messages if not m["is_target"]]

    return {
        "total_messages": len(messages),
        "target_messages": len(target_msgs),
        "target_sample": [m["message"] for m in target_msgs[:20]],
        "all_messages": messages,
    }


def main():
    parser = argparse.ArgumentParser(description="now-skill Inbox Scanner")
    parser.add_argument("--slug", required=True, help="Skill slug")
    parser.add_argument("--base-dir", default="./nows", help="Base directory")
    parser.add_argument("--process", action="store_true", help="Move files to processed after scanning")
    parser.add_argument("--target-name", default="", help="Target person's name for chat parsing")

    args = parser.parse_args()

    result = scan_inbox(args.slug, args.base_dir)

    if result["count"] == 0:
        print(result["message"])
        return

    print(f"\n[inbox] Inbox scan for /{args.slug}")
    print(f"   Found {result['count']} file(s):\n")

    parsed_results = []

    for file_info in result["files"]:
        content_type = classify_content(file_info)
        print(f"   [file] {file_info['name']}")
        print(f"      Type: {file_info['type']} ({content_type})")
        print(f"      Size: {file_info['size']:,} bytes")

        # Try to parse text-based files
        if file_info["type"] in ("text", "csv", "markdown"):
            try:
                with open(file_info["path"], "r", encoding="utf-8") as f:
                    content = f.read()
                if args.target_name:
                    parsed = parse_chat_text(content, args.target_name)
                    print(f"      Messages: {parsed['total_messages']} total, {parsed['target_messages']} from target")
                    parsed_results.append(parsed)
            except Exception as e:
                print(f"      [WARN] Could not read: {e}")

        print()

    # Output JSON for downstream processing
    if parsed_results:
        print("---PARSED_JSON---")
        print(json.dumps(parsed_results, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
