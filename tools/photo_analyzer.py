#!/usr/bin/env python3
"""
Photo metadata analyzer for now-skill.

Extracts EXIF data from photo directories and builds a timeline
of locations and dates.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from collections import defaultdict


def try_extract_exif(filepath: str) -> dict:
    """
    Try to extract EXIF data from an image file.
    Uses stdlib only — no external dependencies.
    For full EXIF support, install: pip install Pillow
    """
    info = {
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "size_bytes": os.path.getsize(filepath),
        "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat(),
        "has_exif": False,
        "date_taken": None,
        "gps": None,
        "camera": None,
    }

    # Try to read basic EXIF from file bytes (minimal stdlib approach)
    try:
        with open(filepath, "rb") as f:
            header = f.read(12)

        # Check for JPEG
        if header[:3] == b"\xff\xd8\xff":
            info["format"] = "JPEG"
            # Try to find EXIF marker
            with open(filepath, "rb") as f:
                data = f.read(65536)  # Read first 64KB for EXIF

            # Look for DateTimeOriginal in EXIF
            # This is a rough approach; Pillow is recommended for production
            exif_marker = b"DateTimeOriginal"
            idx = data.find(exif_marker)
            if idx > 0:
                try:
                    # EXIF datetime format: "YYYY:MM:DD HH:MM:SS"
                    date_bytes = data[idx+len(exif_marker)+2:idx+len(exif_marker)+21]
                    date_str = date_bytes.decode("ascii", errors="ignore").strip("\x00")
                    if date_str:
                        info["date_taken"] = date_str
                        info["has_exif"] = True
                except Exception:
                    pass

            # GPS marker
            gps_marker = b"GPSLatitude"
            if data.find(gps_marker) > 0:
                info["gps"] = "present (requires Pillow for full extraction)"

            # Camera make/model
            make_marker = b"Make"
            model_marker = b"Model"
            for marker, key in [(make_marker, "make"), (model_marker, "model")]:
                idx = data.find(marker)
                if idx > 0:
                    try:
                        val_bytes = data[idx+6:idx+30]
                        val = val_bytes.decode("ascii", errors="ignore").split("\x00")[0]
                        if val:
                            info["camera"] = (info.get("camera") or "") + val + " "
                    except Exception:
                        pass

        elif header[:8] == b"\x89PNG\r\n\x1a\n":
            info["format"] = "PNG"
        elif header[:4] == b"RIFF":
            info["format"] = "WEBP"
        elif header[:2] == b"BM":
            info["format"] = "BMP"
        else:
            info["format"] = "unknown"

    except Exception as e:
        info["error"] = str(e)

    return info


def build_timeline(photos: list) -> dict:
    """Build a chronological timeline from photo metadata."""
    dated = [p for p in photos if p.get("date_taken")]
    dated.sort(key=lambda p: p["date_taken"] or "")

    timeline = []
    for p in dated:
        timeline.append({
            "date": p["date_taken"],
            "file": p["filename"],
            "location": p.get("gps", "unknown"),
        })

    date_counts = defaultdict(int)
    for p in photos:
        mod_date = p.get("modified", "")[:10]
        if mod_date:
            date_counts[mod_date] += 1

    busiest_days = sorted(date_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "timeline": timeline,
        "total_photos": len(photos),
        "photos_with_dates": len(dated),
        "busiest_days": [{"date": d, "count": c} for d, c in busiest_days],
    }


def main():
    parser = argparse.ArgumentParser(description="Photo metadata analyzer for now-skill")
    parser.add_argument("--dir", required=True, help="Directory containing photos")
    parser.add_argument("--output", default="/tmp/photo_out.txt", help="Output file path")

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"Error: Directory not found: {args.dir}")
        sys.exit(1)

    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".tiff", ".tif"}

    photos = []
    for fname in sorted(os.listdir(args.dir)):
        ext = os.path.splitext(fname)[1].lower()
        if ext in image_extensions:
            fpath = os.path.join(args.dir, fname)
            info = try_extract_exif(fpath)
            photos.append(info)

    if not photos:
        print(json.dumps({"error": "No image files found", "dir": args.dir}, indent=2))
        return

    timeline = build_timeline(photos)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# Photo Analysis\n\n")
        f.write(f"Total photos: {timeline['total_photos']}\n")
        f.write(f"Photos with dates: {timeline['photos_with_dates']}\n\n")
        f.write("## Timeline\n")
        for t in timeline["timeline"]:
            f.write(f"- {t['date']}: {t['file']}\n")
        f.write("\n## Busiest Days\n")
        for d in timeline["busiest_days"]:
            f.write(f"- {d['date']}: {d['count']} photos\n")

    result = {
        "total_photos": timeline["total_photos"],
        "photos_with_dates": timeline["photos_with_dates"],
        "timeline": timeline["timeline"][:30],
        "busiest_days": timeline["busiest_days"],
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
