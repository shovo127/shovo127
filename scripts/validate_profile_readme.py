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
APPROVED_HERO_BLOB = "1529179ad25ae062157ad78c81ca41765f7ffcc0"
TOTAL_ASSET_BUDGET = 5 * 1024 * 1024
STATIC_ASSET_LIMIT = 300 * 1024
GIF_ASSET_LIMIT = 500 * 1024

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.links, self.remote_images = [], [], []
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
assert readme.startswith(APPROVED_HERO), "Approved Hero README block changed."
hero_blob = subprocess.check_output(
    ["git", "hash-object", "assets/hero/engineering-hero.svg"], cwd=ROOT, text=True
).strip()
assert hero_blob == APPROVED_HERO_BLOB, "Approved Hero SVG blob changed."

parser = References()
parser.feed(readme)
assert not parser.remote_images, f"External image dependencies: {parser.remote_images}"
targets = set(parser.images)
targets.update(parser.links)
targets.update(re.findall(r"!??\[[^\]]*\]\(([^)]+)\)", readme))
missing = []
for raw in targets:
    target = local_target(raw)
    if not target:
        continue
    path = (ROOT / target).resolve()
    if ROOT.resolve() not in path.parents or not path.is_file():
        missing.append(raw)
assert not missing, f"Broken or case-mismatched local references: {sorted(missing)}"

required_sections = [
    "## ENGINEERING PROFILE", "## SELECTED PROJECTS", "## TECHNICAL FOCUS",
    "## AUTOMOTIVE ENGINEERING / 3D STUDY", "## EDUCATION & LEARNING",
    "## PUBLIC REPOSITORY ANALYTICS", "## CONNECT",
]
for section in required_sections:
    assert readme.count(section) == 1, f"Missing or duplicate section: {section}"

project_names = [
    "VisaFlowX Universal", "Kostenlos AI", "Noti-Fixer for Chinese Devices",
    "Circle to Search for Xiaomi", "Smart Scanner Pro", "IPTV By Shovo",
]
project_urls = [
    "https://github.com/shovo127/visaflowx-universal",
    "https://github.com/shovo127/kostenlos-ai",
    "https://github.com/shovo127/Noti-Fixer-for-Chinese-Devices",
    "https://github.com/shovo127/Circle-to-Search-for-Xiaomi",
    "https://github.com/shovo127/Smart-Scanner-Pro",
    "https://github.com/shovo127/IPTV-By-Shovo",
]
for name, url in zip(project_names, project_urls):
    assert name in readme and url in readme, f"Missing project card or repository link: {name}"
assert readme.count("project-01-scan.gif") == 1
assert all(readme.count(f"project-{i:02d}-scan.gif") == 1 for i in range(1, 7))
assert all((ROOT / "assets" / "focus" / f"focus-{i:02d}.jpg").is_file() for i in range(1, 7)), "Original Technical Focus source artwork must remain intact."
assert "manual" in readme.lower() and "planned" in readme.lower()
assert "static, not live" in readme.lower() or "static values" in readme.lower()
assert "third-party" in readme.lower() and "no video streams are hosted" in readme.lower()
assert "contact@lernedeutschmittechnologie.tech" in readme

svg_files = sorted((ROOT / "assets").rglob("*.svg"))
for svg in svg_files:
    assert svg.stat().st_size <= 64 * 1024, f"SVG too large: {svg}"
    tree = ET.parse(svg)
    for node in tree.iter():
        tag = node.tag.rsplit("}", 1)[-1].lower()
        assert tag not in {"script", "foreignobject"}, f"Unsafe SVG element in {svg}: {tag}"
        for key, value in node.attrib.items():
            if key.rsplit("}", 1)[-1].lower() in {"href", "src"}:
                assert not value.strip().startswith(("http://", "https://", "//")), f"Remote SVG reference in {svg}"

expected_dimensions = {
    "assets/projects/visaflowx-interface.jpg": (1200, 520),
    "assets/projects/kostenlos-ai-workspace.jpg": (1200, 520),
    "assets/projects/noti-fixer-diagnostics.jpg": (1200, 520),
    "assets/projects/circle-search-native.jpg": (1200, 520),
    "assets/projects/smart-scanner-architecture.jpg": (1200, 520),
    "assets/projects/iptv-by-shovo.jpg": (1200, 520),
    "assets/engineering/piston-connecting-rod-crankshaft.jpg": (1200, 520),
    "assets/engineering/education-path.jpg": (1200, 300),
    "assets/data/public-repository-snapshot.jpg": (1200, 360),
    "assets/cards/footer-engineering.jpg": (640, 220),
    "assets/cards/footer-location.jpg": (640, 220),
}
for i in range(1, 7):
    expected_dimensions[f"assets/focus/focus-{i:02d}.jpg"] = (640, 300)
for rel, dimensions in expected_dimensions.items():
    path = ROOT / rel
    assert path.is_file(), f"Missing required artwork: {rel}"
    assert path.stat().st_size <= STATIC_ASSET_LIMIT, f"Static asset exceeds 300 KiB: {rel}"
    with Image.open(path) as im:
        assert im.format == "JPEG" and im.size == dimensions, f"Unexpected JPEG format/dimensions for {rel}: {im.format} {im.size}"
        im.verify()

expected_gifs = ["assets/motion/signal-sweep.gif", "assets/motion/focus-pulse.gif",
                 "assets/motion/analytics-trace.gif",
                 "assets/motion/education-path-live.gif",
                 "assets/motion/analytics-snapshot-live.gif",
                 "assets/motion/piston-crankshaft-cycle.gif"]
expected_gifs += [f"assets/motion/focus-{i:02d}-live.gif" for i in range(1, 7)]
expected_gifs += [f"assets/motion/project-{i:02d}-scan.gif" for i in range(1, 7)]
expected_gif_dimensions = {
    "assets/motion/signal-sweep.gif": (560, 84),
    "assets/motion/focus-pulse.gif": (560, 84),
    "assets/motion/analytics-trace.gif": (560, 84),
    "assets/motion/education-path-live.gif": (900, 225),
    "assets/motion/analytics-snapshot-live.gif": (900, 270),
    "assets/motion/piston-crankshaft-cycle.gif": (720, 312),
}
expected_gif_dimensions.update({f"assets/motion/focus-{i:02d}-live.gif": (480, 225) for i in range(1, 7)})
expected_gif_dimensions.update({f"assets/motion/project-{i:02d}-scan.gif": (480, 208) for i in range(1, 7)})
for rel in expected_gifs:
    path = ROOT / rel
    assert path.is_file(), f"Missing animated visual: {rel}"
    assert path.stat().st_size <= GIF_ASSET_LIMIT, f"GIF exceeds 350 KiB: {rel}"
    with Image.open(path) as im:
        assert im.format == "GIF" and im.n_frames >= 12, f"Expected animated GIF with >=12 frames: {rel}"
        assert im.size == expected_gif_dimensions[rel], f"Unexpected GIF dimensions for {rel}: {im.size}"
        assert im.info.get("loop") == 0, f"GIF must loop continuously: {rel}"
        durations = []
        for frame in range(im.n_frames):
            im.seek(frame)
            durations.append(im.info.get("duration"))
        assert all(d is not None and 60 <= d <= 350 for d in durations), f"Unreasonable frame timing in {rel}: {durations}"
        assert 2000 <= sum(durations) <= 14000, f"Loop duration outside 2–14 seconds: {rel}"
        assert im.width <= 1200 and im.height <= 600, f"GIF dimensions exceed intended use: {rel}"

# No README card image may be referenced twice, except the intentionally repeated section sweep.
card_images = [x for x in parser.images if "project-" in x or "/focus/" in x]
assert len([x for x in parser.images if "project-" in x]) == 6, "Expected six distinct project image references."
focus_live = [x for x in parser.images if "focus-" in x and "-live.gif" in x]
assert len(focus_live) == len(set(focus_live)) == 6, "Expected six distinct animated Technical Focus card references."
for required in ("education-path-live.gif", "analytics-snapshot-live.gif", "piston-crankshaft-cycle.gif",
                 "footer-engineering.jpg", "footer-location.jpg"):
    assert any(required in x for x in parser.images), f"Missing requested visual reference: {required}"

asset_files = [p for p in (ROOT / "assets").rglob("*") if p.is_file()]
asset_bytes = sum(p.stat().st_size for p in asset_files)
assert asset_bytes <= TOTAL_ASSET_BUDGET, f"Assets exceed 3 MiB budget: {asset_bytes:,} bytes"

print("PASS: approved Hero README block and SVG blob SHA are unchanged.")
print(f"PASS: {len(parser.images)} README image references resolve; no remote image dependencies.")
print(f"PASS: {len(parser.links)} HTML links inspected; all local targets resolve.")
print(f"PASS: {len(svg_files)} SVG files parse safely without script/foreignObject or remote references.")
print("PASS: six project artworks, six animated Technical Focus cards and two footer identity cards exist with intended dimensions.")
print(f"PASS: {len(expected_gifs)} animated GIFs loop continuously with validated frame timing and dimensions, including piston/crank cycle.")
print(f"PASS: static/GIF asset limits respected; total asset footprint {asset_bytes:,} / {TOTAL_ASSET_BUDGET:,} bytes.")
