#!/usr/bin/env python3
"""Create a deterministic inventory of every repository-owned profile asset."""
from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from PIL import Image

ROOT = Path("assets")
JSON_OUT = Path("docs/profile-audit/asset-inventory.json")
MD_OUT = Path("docs/profile-audit/asset-inventory.md")


def describe(path: Path) -> dict:
    raw = path.read_bytes()
    item = {
        "path": path.as_posix(),
        "kind": path.suffix.lower().lstrip(".") or "file",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    suffix = path.suffix.lower()
    if suffix in {".gif", ".png", ".webp", ".jpg", ".jpeg"}:
        with Image.open(path) as image:
            item["format"] = image.format
            item["width"], item["height"] = image.size
            item["frames"] = int(getattr(image, "n_frames", 1))
            if item["frames"] > 1:
                durations = []
                for frame in range(item["frames"]):
                    image.seek(frame)
                    durations.append(int(image.info.get("duration", 0) or 0))
                item["duration_ms_min"] = min(durations)
                item["duration_ms_max"] = max(durations)
                item["loop"] = image.info.get("loop")
    elif suffix == ".svg":
        root = ET.fromstring(raw)
        item["width"] = root.attrib.get("width")
        item["height"] = root.attrib.get("height")
        item["viewBox"] = root.attrib.get("viewBox")
    elif suffix == ".json":
        json.loads(raw.decode("utf-8"))
        item["valid_json"] = True
    return item


def human_bytes(value: int) -> str:
    if value < 1024:
        return f"{value} B"
    if value < 1024**2:
        return f"{value/1024:.1f} KB"
    return f"{value/1024**2:.2f} MB"


def render_markdown(items: list[dict], duplicates: list[list[str]]) -> str:
    counts = defaultdict(int)
    total = 0
    for item in items:
        counts[item["kind"]] += 1
        total += item["bytes"]
    lines = [
        "# Profile asset inventory",
        "",
        "Generated deterministically by scripts/audit_profile_assets.py from every file under assets/.",
        "",
        f"- Files: **{len(items)}**",
        f"- Combined asset size: **{human_bytes(total)}**",
        "- Types: " + ", ".join(f"{kind}: {count}" for kind, count in sorted(counts.items())),
        "",
        "| Asset | Type | Size | Dimensions | Frames | Timing | Loop | SHA-256 |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in items:
        dimensions = ""
        if item.get("width") is not None and item.get("height") is not None:
            dimensions = f'{item["width"]} × {item["height"]}'
        elif item.get("viewBox"):
            dimensions = f'viewBox {item["viewBox"]}'
        frames = str(item.get("frames", "—"))
        timing = "—"
        if "duration_ms_min" in item:
            timing = str(item["duration_ms_min"])
            if item["duration_ms_min"] != item["duration_ms_max"]:
                timing += f'–{item["duration_ms_max"]}'
            timing += " ms"
        loop = str(item.get("loop", "—"))
        lines.append(f'| {item["path"]} | {item["kind"]} | {human_bytes(item["bytes"])} | {dimensions or "—"} | {frames} | {timing} | {loop} | {item["sha256"][:12]} |')
    lines.extend(["", "## Duplicate content", ""])
    if duplicates:
        for group in duplicates:
            lines.append("- " + ", ".join(paths))
    else:
        lines.append("No byte-identical duplicate files detected.")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- GIF frame count and duration are read from the actual file, not inferred from its extension.",
        "- SVG dimensions and viewBox are read from parsed XML.",
        "- SHA-256 values make changes and byte-identical duplicates auditable.",
        "- This inventory records technical properties; it does not replace visual design review.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed inventory is stale")
    args = parser.parse_args()
    if not ROOT.is_dir():
        raise SystemExit("assets/ directory is missing")

    items = [describe(path) for path in sorted(ROOT.rglob("*")) if path.is_file()]
    if any(item["bytes"] == 0 for item in items):
        raise SystemExit("An empty asset file was found.")
    by_hash = defaultdict(list)
    for item in items:
        by_hash[item["sha256"]].append(item["path"])
    duplicates = [paths for paths in by_hash.values() if len(paths) > 1]
    json_text = json.dumps({
        "schema_version": 1,
        "asset_count": len(items),
        "total_bytes": sum(item["bytes"] for item in items),
        "assets": items,
        "duplicate_groups": duplicates,
    }, indent=2, ensure_ascii=False) + "\n"
    md_text = render_markdown(items, duplicates)

    if args.check:
        if not JSON_OUT.is_file() or JSON_OUT.read_text(encoding="utf-8") != json_text:
            raise SystemExit("Asset inventory JSON is stale; regenerate and commit it.")
        if not MD_OUT.is_file() or MD_OUT.read_text(encoding="utf-8") != md_text:
            raise SystemExit("Asset inventory Markdown is stale; regenerate and commit it.")
        print(f"PASS: inventory matches all {len(items)} assets ({human_bytes(sum(i['bytes'] for i in items))}).")
        return 0

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json_text, encoding="utf-8")
    MD_OUT.write_text(md_text, encoding="utf-8")
    print(f"Generated {JSON_OUT} and {MD_OUT}: {len(items)} assets, {human_bytes(sum(i['bytes'] for i in items))}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
