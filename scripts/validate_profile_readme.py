from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
APPROVED_HERO = """<p align="center"><img src="./assets/hero/engineering-hero.svg" width="100%" alt="Engineering mindset, software building and practical technology with a precision mechanical rotor illustration" /></p>

<h1 align="center">Mohammed Thuhidul Islam Shovo</h1>
<p align="center"><strong>Engineering Mindset · Software Building · AI & Automation · Practical Technology</strong></p>
<p align="center">Dhaka, Bangladesh · <a href="https://github.com/shovo127">GitHub</a> · <a href="https://lernedeutschmittechnologie.tech">Lerne Deutsch Mit Technologie</a></p>

---
"""
APPROVED_HERO_BLOB = "f988a3193de32412396a760fee2cf46d7de771e4"

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.remote_images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            src = (attrs.get("src") or "").strip()
            if src.startswith(("http://", "https://", "//")):
                self.remote_images.append(src)
            elif src:
                self.images.append(src)
        if tag == "a":
            href = (attrs.get("href") or "").strip()
            if href:
                self.links.append(href)

def local_target(value):
    value = value.strip().split()[0].strip("<>")
    if not value or value.startswith(("#", "http://", "https://", "mailto:", "tel:", "//")):
        return None
    return value.split("#", 1)[0].split("?", 1)[0]

readme = README.read_text(encoding="utf-8")
assert readme.startswith(APPROVED_HERO), "Approved Hero block changed; stop and review before merging."
hero_blob = subprocess.check_output(
    ["git", "hash-object", "assets/hero/engineering-hero.svg"], cwd=ROOT, text=True
).strip()
assert hero_blob == APPROVED_HERO_BLOB, "Approved Hero SVG changed; stop and review before merging."

parser = References()
parser.feed(readme)
assert not parser.remote_images, f"External image dependency found: {parser.remote_images}"

targets = set(parser.images)
targets.update(parser.links)
targets.update(re.findall(r"!??\[[^\]]*\]\(([^)]+)\)", readme))
missing = []
for raw in targets:
    target = local_target(raw)
    if not target:
        continue
    path = (ROOT / target).resolve()
    if ROOT.resolve() not in path.parents and path != ROOT.resolve():
        missing.append(raw)
    elif not path.is_file():
        missing.append(raw)
assert not missing, f"Broken or case-mismatched local references: {sorted(missing)}"

svg_files = sorted((ROOT / "assets").rglob("*.svg"))
for svg in svg_files:
    assert svg.stat().st_size <= 64 * 1024, f"SVG exceeds 64 KB: {svg.relative_to(ROOT)}"
    tree = ET.parse(svg)
    for node in tree.iter():
        tag = node.tag.rsplit("}", 1)[-1].lower()
        assert tag not in {"script", "foreignobject"}, f"Unsupported active SVG content in {svg}"
        for key, value in node.attrib.items():
            if key.rsplit("}", 1)[-1].lower() in {"href", "src"}:
                assert not value.strip().startswith(("http://", "https://", "//")), f"Remote SVG dependency in {svg}"

asset_bytes = sum(p.stat().st_size for p in (ROOT / "assets").rglob("*") if p.is_file())
assert asset_bytes <= 200 * 1024, f"Profile assets exceed 200 KB: {asset_bytes}"

print("PASS: approved Hero block + SVG blob locked.")
print(f"PASS: {len(parser.images)} README images, {len(parser.links)} HTML links, local references resolved.")
print(f"PASS: {len(svg_files)} SVG files parse; no remote SVG dependencies or active embedded content.")
print(f"PASS: total assets {asset_bytes:,} bytes (budget 204,800 bytes).")
