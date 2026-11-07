from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
EXPECTED_OPENING = """<p align="center"><img src="./assets/motion/hero-engineering-v2.gif" width="100%" alt="Animated engineering hero with letter-by-letter name reveal and rotating precision rotor" /></p>

<h1 align="center"><img src="./assets/motion/hero-name.gif" alt="Mohammed Thuhidul Islam Shovo" /></h1>
<p align="center"><img src="./assets/motion/hero-tagline.gif" alt="Engineering Mindset · Software Building · AI and Automation · Practical Technology" /></p>
<p align="center">Dhaka, Bangladesh · <a href="https://github.com/shovo127">GitHub</a> · <a href="https://lernedeutschmittechnologie.tech">Lerne Deutsch Mit Technologie</a></p>

---
"""
TOTAL_ASSET_BUDGET = 12 * 1024 * 1024
STATIC_LIMIT = 300 * 1024
GIF_LIMIT = 750 * 1024

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
assert readme.startswith(EXPECTED_OPENING), "Animated Hero / typewriter opening changed."
parser = References()
parser.feed(readme)
assert not parser.remote_images, f"External image dependencies: {parser.remote_images}"
targets = set(parser.images) | set(parser.links)
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
    "section-profile.gif", "section-projects.gif", "section-focus.gif",
    "section-engine.gif", "section-education.gif", "section-analytics.gif", "section-connect.gif"
]
for item in required_sections:
    assert item in readme, f"Missing animated section heading: {item}"
assert all(f"project-{i:02d}-kinetic-v2.gif" in readme for i in range(1, 7))
assert all(f"focus-{i:02d}-motion-v2.gif" in readme for i in range(1, 7))
assert all(f"title-project-{i:02d}.gif" in readme for i in range(1, 7))
assert all(f"title-focus-{i:02d}.gif" in readme for i in range(1, 7))
assert all(f"divider-{x}-v2.gif" in readme for x in ("profile","projects","focus","analytics","footer"))
assert "manual" in readme.lower() and "planned" in readme.lower()
assert "static, not live" in readme.lower()
assert "third-party" in readme.lower() and "no video streams are hosted" in readme.lower()
assert "contact@lernedeutschmittechnologie.tech" in readme

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
    assert name in readme and url in readme, f"Missing project card or link: {name}"

for i in range(1, 7):
    assert (ROOT / "assets/focus" / f"focus-{i:02d}.jpg").is_file(), "Original focus artwork must remain."
    assert (ROOT / "assets/motion" / f"title-education-{i:02d}.gif").is_file() if i < 3 else True

svg_files = sorted((ROOT / "assets").rglob("*.svg"))
for svg in svg_files:
    assert svg.stat().st_size <= 64 * 1024, f"SVG too large: {svg}"
    tree = ET.parse(svg)
    for node in tree.iter():
        tag = node.tag.rsplit("}", 1)[-1].lower()
        assert tag not in {"script", "foreignobject"}, f"Unsafe SVG element: {tag}"
        for key, value in node.attrib.items():
            if key.rsplit("}", 1)[-1].lower() in {"href", "src"}:
                assert not value.strip().startswith(("http://", "https://", "//")), f"Remote SVG reference: {svg}"

static_files = [
    "assets/projects/visaflowx-interface.jpg", "assets/projects/kostenlos-ai-workspace.jpg",
    "assets/projects/noti-fixer-diagnostics.jpg", "assets/projects/circle-search-native.jpg",
    "assets/projects/smart-scanner-architecture.jpg", "assets/projects/iptv-by-shovo.jpg",
    "assets/engineering/piston-connecting-rod-crankshaft.jpg", "assets/engineering/education-path.jpg",
    "assets/data/public-repository-snapshot.jpg", "assets/cards/footer-engineering.jpg",
    "assets/cards/footer-location.jpg",
]
for i in range(1, 7):
    static_files.append(f"assets/focus/focus-{i:02d}.jpg")
for rel in static_files:
    path = ROOT / rel
    assert path.is_file(), f"Missing source artwork: {rel}"
    assert path.stat().st_size <= STATIC_LIMIT, f"Static artwork exceeds 300 KiB: {rel}"
    with Image.open(path) as im:
        assert im.format == "JPEG", f"Expected JPEG: {rel}"
        im.verify()

gif_refs = sorted({x for x in parser.images if x.lower().endswith(".gif")})
assert len(gif_refs) >= 40, f"Expected a rich animated system, found only {len(gif_refs)} GIF references."
for raw in gif_refs:
    rel = local_target(raw)
    path = ROOT / rel
    assert path.stat().st_size <= GIF_LIMIT, f"GIF exceeds 750 KiB: {rel}"
    with Image.open(path) as im:
        assert im.format == "GIF" and im.n_frames >= 12, f"Expected animated GIF (12+ frames): {rel}"
        assert im.info.get("loop") == 0, f"GIF must loop continuously: {rel}"
        durations = []
        for frame in range(im.n_frames):
            im.seek(frame)
            durations.append(im.info.get("duration"))
        assert all(d is not None and 60 <= d <= 1000 for d in durations), f"Unreasonable frame timing: {rel}"
        assert 1400 <= sum(durations) <= 14000, f"Loop duration outside 1.4–14 seconds: {rel}"
        assert im.width <= 1200 and im.height <= 600, f"GIF dimensions too large: {rel}"

asset_files = [p for p in (ROOT / "assets").rglob("*") if p.is_file()]
asset_bytes = sum(p.stat().st_size for p in asset_files)
assert asset_bytes <= TOTAL_ASSET_BUDGET, f"Assets exceed 12 MiB: {asset_bytes:,} bytes"
print("PASS: animated Hero and letter-by-letter title/tagline block.")
print(f"PASS: {len(parser.images)} README images and {len(parser.links)} HTML links resolve locally.")
print(f"PASS: {len(svg_files)} SVGs parse safely; no script, foreignObject or remote references.")
print(f"PASS: six project motion systems, six unique Technical Focus motions and typewriter headings.")
print(f"PASS: {len(gif_refs)} referenced GIFs loop continuously with valid frame timing and dimensions.")
print(f"PASS: asset budget respected: {asset_bytes:,} / {TOTAL_ASSET_BUDGET:,} bytes.")
