#!/usr/bin/env python3
"""
Trend Tracker for now-skill.

Tracks emotional trends, topic shifts, and behavior changes
across timeline snapshots.
"""

import json
import os
import sys
import argparse
from datetime import datetime
from collections import Counter
from pathlib import Path


def analyze_trend(slug: str, base_dir: str):
    """
    Compare the latest N snapshots and detect trends.
    """
    timeline_path = os.path.join(base_dir, slug, "timeline.json")

    if not os.path.exists(timeline_path):
        return {
            "error": f"No timeline found for '{slug}'",
            "message": "Import some data first to build a timeline."
        }

    with open(timeline_path, "r", encoding="utf-8") as f:
        timeline = json.load(f)

    snapshots = timeline.get("snapshots", [])

    if len(snapshots) < 2:
        return {
            "error": "Need at least 2 snapshots for trend analysis",
            "message": f"Currently have {len(snapshots)} snapshot(s). Import more data."
        }

    latest = snapshots[-1]
    previous = snapshots[-2]

    analysis = {
        "slug": slug,
        "analyzed_at": datetime.now().isoformat(),
        "compared_snapshots": {
            "latest": {"id": latest["id"], "timestamp": latest["timestamp"]},
            "previous": {"id": previous["id"], "timestamp": previous["timestamp"]},
        },
        "emotions": compare_emotions(previous, latest),
        "topics": compare_topics(previous, latest),
        "behavior": compare_behavior(previous, latest),
        "signals": detect_signals(previous, latest),
    }

    return analysis


def compare_emotions(prev_snapshot, curr_snapshot):
    """Compare emotional states between snapshots."""
    prev_emotions = prev_snapshot.get("delta", {}).get("emotions", {})
    curr_emotions = curr_snapshot.get("delta", {}).get("emotions", {})

    if not prev_emotions or not curr_emotions:
        return {"trend": "insufficient_data", "message": "Not enough emotional data to compare"}

    return {
        "previous": prev_emotions,
        "current": curr_emotions,
        "trend": "stable",
    }


def compare_topics(prev_snapshot, curr_snapshot):
    """Compare topic distributions between snapshots."""
    prev_topics = prev_snapshot.get("delta", {}).get("topics", {})
    curr_topics = curr_snapshot.get("delta", {}).get("topics", {})

    def _flatten_values(d):
        """Extract all topic strings from dict (values may be lists or strings)."""
        out = set()
        if isinstance(d, dict):
            for v in d.values():
                if isinstance(v, list):
                    out.update(v)
                elif isinstance(v, str):
                    out.add(v)
        return out

    prev_set = _flatten_values(prev_topics)
    curr_set = _flatten_values(curr_topics)

    return {
        "new": list(curr_set - prev_set),
        "increased": [],
        "decreased": [],
        "disappeared": list(prev_set - curr_set),
    }


def compare_behavior(prev_snapshot, curr_snapshot):
    """Compare behavior patterns."""
    curr_changes = curr_snapshot.get("delta", {}).get("behavior_changes", [])
    prev_changes = prev_snapshot.get("delta", {}).get("behavior_changes", [])

    return {
        "new_changes": curr_changes or [],
        "previous_changes": prev_changes or [],
        "has_changes": bool(curr_changes),
    }


def detect_signals(prev_snapshot, curr_snapshot):
    """
    Detect warning signs and positive signals.
    Runs basic text analysis as a starting point.
    """
    signals = {
        "warning": [],
        "positive": [],
        "neutral": [],
    }

    curr_facts = curr_snapshot.get("delta", {}).get("new_facts", [])
    curr_changes = curr_snapshot.get("delta", {}).get("behavior_changes", [])

    all_text = " ".join(
        str(item) for item in (curr_facts + curr_changes)
    ).lower()

    warning_keywords = [
        "less", "silent", "distant", "cold", "tired", "whatever",
        "busy", "later", "fine", "k.", "avoid",
    ]

    positive_keywords = [
        "love", "miss", "happy", "excited", "share", "together",
        "future", "plan", "initiative",
    ]

    for kw in warning_keywords:
        if kw in all_text:
            signals["warning"].append(f"Warning keyword detected: '{kw}'")

    for kw in positive_keywords:
        if kw in all_text:
            signals["positive"].append(f"Positive keyword detected: '{kw}'")

    return signals


def main():
    parser = argparse.ArgumentParser(description="now-skill Trend Tracker")
    parser.add_argument("slug", nargs="?", help="Skill slug to analyze")
    parser.add_argument("--base-dir", default="./nows", help="Base directory for now-skills")
    args = parser.parse_args()

    if not args.slug:
        parser.print_help()
        sys.exit(1)

    result = analyze_trend(args.slug, args.base_dir)

    if "error" in result:
        print(f"\n[!] {result['error']}")
        print(result.get("message", ""))
    else:
        print(f"\nTrend Analysis for /{args.slug}")
        snap = result["compared_snapshots"]
        print(f"   Comparing snapshot #{snap['previous']['id']} -> #{snap['latest']['id']}")
        print(f"\n   Topics:")
        new_topics = result["topics"]["new"]
        gone_topics = result["topics"]["disappeared"]
        print(f"     New: {', '.join(new_topics) if new_topics else 'None'}")
        print(f"     Disappeared: {', '.join(gone_topics) if gone_topics else 'None'}")
        print(f"\n   Signals:")
        print(f"     [!] Warning: {len(result['signals']['warning'])}")
        print(f"     [*] Positive: {len(result['signals']['positive'])}")


if __name__ == "__main__":
    main()
