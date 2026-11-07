from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image

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

expected_images = {
    "assets/projects/visaflowx-interface.jpg": (1200, 520),
    "assets/projects/kostenlos-ai-workspace.jpg": (1200, 520),
    "assets/projects/noti-fixer-diagnostics.jpg": (1200, 520),
    "assets/projects/circle-search-native.jpg": (1200, 520),
    "assets/projects/smart-scanner-architecture.jpg": (1200, 520),
    "assets/engineering/piston-connecting-rod-crankshaft.jpg": (1200, 520),
    "assets/engineering/technical-focus.jpg": (1200, 360),
    "assets/engineering/education-path.jpg": (1200, 300),
    "assets/data/public-repository-snapshot.jpg": (1200, 360),
    "assets/motion/signal-sweep.gif": (560, 84),
}
for relative, dimensions in expected_images.items():
    path = ROOT / relative
    assert path.is_file(), f"Required generated asset missing: {relative}"
    assert path.stat().st_size <= 150 * 1024, f"Asset exceeds 150 KB: {relative}"
    with Image.open(path) as image:
        if dimensions is not None:
            assert image.size == dimensions, f"Unexpected dimensions for {relative}: {image.size}"
        if relative.endswith(".gif"):
            assert image.format == "GIF", "Motion asset is not a GIF."
            assert image.n_frames == 24, f"Expected 24 motion frames, found {image.n_frames}."
            assert image.info.get("loop") == 0, "GIF must loop continuously."
            durations = []
            for frame in range(image.n_frames):
                image.seek(frame)
                durations.append(image.info.get("duration"))
            assert all(duration == 220 for duration in durations), f"Unexpected GIF frame timing: {durations}"
        image.verify()

asset_bytes = sum(p.stat().st_size for p in (ROOT / "assets").rglob("*") if p.is_file())
assert asset_bytes <= 800 * 1024, f"Profile assets exceed 800 KiB: {asset_bytes}"

print("PASS: approved Hero README block + original SVG Git blob locked.")
print(f"PASS: {len(parser.images)} README images and {len(parser.links)} HTML links resolve locally.")
print(f"PASS: {len(svg_files)} SVG files parse; no active embedded content or remote SVG references.")
print(f"PASS: {len(expected_images)} generated raster/animation assets have verified formats and dimensions.")
print("PASS: 24-frame, 220 ms/frame looping GIF verified.")
print(f"PASS: total assets {asset_bytes:,} bytes (budget 819,200 bytes).")
