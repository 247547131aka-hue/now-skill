#!/usr/bin/env python3
"""
Version Manager for now-skill.

Handles timeline snapshots, version backups, and rollbacks.
Now-skill uses a timeline-based approach (not just backup/restore)
to track the evolution of the relationship over time.
"""

import json
import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path


def create_timeline_snapshot(slug: str, base_dir: str, delta: dict, summary: str = ""):
    """
    Append a new snapshot to the timeline.
    Does NOT delete old data — timeline is cumulative.
    """
    timeline_path = os.path.join(base_dir, slug, "timeline.json")

    # Load existing timeline
    if os.path.exists(timeline_path):
        with open(timeline_path, "r", encoding="utf-8") as f:
            timeline = json.load(f)
    else:
        timeline = {"slug": slug, "snapshots": []}

    snapshot = {
        "id": len(timeline["snapshots"]) + 1,
        "timestamp": datetime.now().isoformat(),
        "source": delta.get("source", "unknown"),
        "delta": {
            "new_facts": delta.get("new_facts", []),
            "behavior_changes": delta.get("behavior_changes", []),
            "emotions": delta.get("emotions", {}),
            "topics": delta.get("topics", {}),
        },
        "summary": summary or f"Snapshot {len(timeline['snapshots']) + 1}",
    }

    timeline["snapshots"].append(snapshot)

    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=2, ensure_ascii=True)

    return snapshot["id"]


def backup_version(slug: str, base_dir: str):
    """
    Create a full version backup before a major update.
    Backs up: memory.md, persona.md, SKILL.md, meta.json
    """
    now_dir = os.path.join(base_dir, slug)
    versions_dir = os.path.join(now_dir, "versions")

    if not os.path.exists(now_dir):
        print(f"Error: now-skill '{slug}' not found at {now_dir}")
        return None

    os.makedirs(versions_dir, exist_ok=True)

    # Generate version name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_name = f"v_{timestamp}"
    version_dir = os.path.join(versions_dir, version_name)
    os.makedirs(version_dir)

    # Copy files
    for fname in ["memory.md", "persona.md", "SKILL.md", "meta.json"]:
        src = os.path.join(now_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(version_dir, fname))

    print(f"Backed up '{slug}' -> versions/{version_name}")
    return version_name


def rollback(slug: str, base_dir: str, version: str = None):
    """
    Rollback to a specific version or the latest backup.
    """
    versions_dir = os.path.join(base_dir, slug, "versions")

    if not os.path.exists(versions_dir):
        print(f"No versions found for '{slug}'")
        return False

    # List available versions
    versions = sorted(os.listdir(versions_dir), reverse=True)

    if not versions:
        print(f"No versions found for '{slug}'")
        return False

    if version:
        if version not in versions:
            print(f"Version '{version}' not found. Available: {', '.join(versions)}")
            return False
        target = version
    else:
        target = versions[0]  # Latest

    version_dir = os.path.join(versions_dir, target)
    now_dir = os.path.join(base_dir, slug)

    # Restore files
    for fname in ["memory.md", "persona.md", "SKILL.md", "meta.json"]:
        src = os.path.join(version_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(now_dir, fname))

    print(f"Rolled back '{slug}' -> {target}")
    return True


def list_versions(slug: str, base_dir: str):
    """List all versions for a now-skill."""
    versions_dir = os.path.join(base_dir, slug, "versions")

    if not os.path.exists(versions_dir):
        print(f"No versions for '{slug}'")
        return

    versions = sorted(os.listdir(versions_dir), reverse=True)
    print(f"\nVersions for '{slug}':")
    print("-" * 40)
    for v in versions:
        vpath = os.path.join(versions_dir, v)
        size = sum(
            os.path.getsize(os.path.join(vpath, f))
            for f in os.listdir(vpath)
            if os.path.isfile(os.path.join(vpath, f))
        )
        print(f"  {v}  ({size:,} bytes)")
    print()


def list_nows(base_dir: str):
    """List all now-skills."""
    if not os.path.exists(base_dir):
        print("No now-skills found.")
        return

    nows = [
        d for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
        and os.path.exists(os.path.join(base_dir, d, "SKILL.md"))
    ]

    if not nows:
        print("No now-skills found.")
        return

    print(f"\nAll now-skills ({len(nows)}):")
    print("-" * 50)

    for slug in sorted(nows):
        meta_path = os.path.join(base_dir, slug, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            name = meta.get("profile", {}).get("name", meta.get("name", slug))
            created = meta.get("created_at", "?")[:10]
            updated = meta.get("updated_at", "?")[:10]
            print(f"  /{slug}  — {name}  (created: {created}, updated: {updated})")
        else:
            print(f"  /{slug}  — (no metadata)")


def main():
    parser = argparse.ArgumentParser(description="now-skill Version Manager")
    parser.add_argument("--action", choices=["backup", "rollback", "list", "snapshot"],
                        default="list", help="Action to perform")
    parser.add_argument("--slug", help="Skill slug")
    parser.add_argument("--version", help="Version to rollback to")
    parser.add_argument("--source", help="Delta source (for snapshot)")
    parser.add_argument("--delta", help="Delta JSON string (for snapshot)")
    parser.add_argument("--summary", help="Snapshot summary")
    parser.add_argument("--base-dir", default="./nows", help="Base directory for now-skills")

    args = parser.parse_args()

    if args.action == "list":
        if args.slug:
            list_versions(args.slug, args.base_dir)
        else:
            list_nows(args.base_dir)
    elif args.action == "backup":
        if not args.slug:
            print("Error: --slug required for backup")
            sys.exit(1)
        backup_version(args.slug, args.base_dir)
    elif args.action == "rollback":
        if not args.slug:
            print("Error: --slug required for rollback")
            sys.exit(1)
        rollback(args.slug, args.base_dir, args.version)
    elif args.action == "snapshot":
        if not args.slug:
            print("Error: --slug required for snapshot")
            sys.exit(1)
        delta = json.loads(args.delta) if args.delta else {}
        create_timeline_snapshot(args.slug, args.base_dir, delta, args.summary or "")


if __name__ == "__main__":
    main()
