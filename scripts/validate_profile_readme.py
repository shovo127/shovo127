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
STATIC_LIMIT = 300 * 1024
GIF_LIMIT = 500 * 1024

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
hero_blob = subprocess.check_output(["git", "hash-object", "assets/hero/engineering-hero.svg"], cwd=ROOT, text=True).strip()
assert hero_blob == APPROVED_HERO_BLOB, "Approved Hero SVG blob changed."

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
    "## 01 / QUEST WORLD", "## 02 / MISSION SELECT", "## 03 / SKILL TREE",
    "## 04 / WORKSHOP LOADOUT", "## 05 / BOSS FIGHT",
    "## 06 / AUTOMOTIVE GARAGE", "## 07 / SAVE POINT"
]
for section in required_sections:
    assert readme.count(section) == 1, f"Missing or duplicate game section: {section}"
for stale in (
    "PUBLIC REPOSITORY ANALYTICS", "PROGRESS LOG / VERIFIED MILESTONES",
    "FIELD GUIDE / FAQ", "TECHNICAL FOCUS /", "ENGINEERING PROFILE / PLAYER PROFILE",
    "assets/motion/focus-01-live.gif", "analytics-snapshot-live.gif",
    "education-path-live.gif", "focus-pulse.gif", "signal-sweep.gif"
):
    assert stale not in readme, f"Old layered portfolio content remains: {stale}"

projects = {
    "VisaFlowX Universal": "https://github.com/shovo127/visaflowx-universal",
    "Kostenlos AI": "https://github.com/shovo127/kostenlos-ai",
    "Noti-Fixer for Chinese Devices": "https://github.com/shovo127/Noti-Fixer-for-Chinese-Devices",
    "Circle to Search for Xiaomi": "https://github.com/shovo127/Circle-to-Search-for-Xiaomi",
    "Smart Scanner Pro": "https://github.com/shovo127/Smart-Scanner-Pro",
    "IPTV By Shovo": "https://github.com/shovo127/IPTV-By-Shovo"
}
for name, url in projects.items():
    assert name in readme and url in readme, f"Missing real project: {name}"
for i in range(1, 7):
    path = f"assets/projects/{['visaflowx-interface.jpg','kostenlos-ai-workspace.jpg','noti-fixer-diagnostics.jpg','circle-search-native.jpg','smart-scanner-architecture.jpg','iptv-by-shovo.jpg'][i-1]}"
    assert readme.count(path) == 1, f"Static project artwork must appear once: {path}"
    image_path = ROOT / path
    with Image.open(image_path) as im:
        assert im.format == "JPEG" and im.size == (1200, 520), f"Wrong project art format or dimensions: {path}"
        im.verify()
assert "planned" in readme.lower() and "no video streams" in readme.lower()
assert "contact@lernedeutschmittechnologie.tech" in readme

required_game = {
    "assets/game/quest-world.gif": ("GIF", (1200, 520)),
    "assets/game/skill-tree.png": ("PNG", (1200, 340)),
    "assets/game/boss-arena.png": ("PNG", (1200, 340)),
    "assets/game/character-sheet.png": ("PNG", (1200, 330)),
    "assets/game/inventory.png": ("PNG", (1200, 340)),
    "assets/game/save-point.png": ("PNG", (1200, 330))
}
for rel, (fmt, size) in required_game.items():
    p = ROOT / rel
    assert p.is_file(), f"Missing generated game asset: {rel}"
    assert p.stat().st_size <= (GIF_LIMIT if fmt == "GIF" else STATIC_LIMIT), f"Game asset too large: {rel}"
    with Image.open(p) as im:
        assert im.format == fmt and im.size == size, f"Wrong format/dimensions: {rel} ({im.format}, {im.size})"
        if fmt == "GIF":
            assert im.n_frames >= 16 and im.info.get("loop") == 0, "Quest world must be an animated infinite loop."
            durations = []
            for frame in range(im.n_frames):
                im.seek(frame)
                durations.append(im.info.get("duration"))
            assert all(d is not None and 80 <= d <= 300 for d in durations)
            assert 1800 <= sum(durations) <= 10000
        im.verify()

for rel in (ROOT / "assets").rglob("*.svg"):
    assert rel.stat().st_size <= 64 * 1024
    tree = ET.parse(rel)
    for node in tree.iter():
        tag = node.tag.rsplit("}", 1)[-1].lower()
        assert tag not in {"script", "foreignobject"}, f"Unsafe SVG element in {rel}: {tag}"
        for key, value in node.attrib.items():
            if key.rsplit("}", 1)[-1].lower() in {"href", "src"}:
                assert not value.strip().startswith(("http://", "https://", "//"))

asset_bytes = sum(p.stat().st_size for p in (ROOT / "assets").rglob("*") if p.is_file())
assert asset_bytes <= TOTAL_ASSET_BUDGET, f"Asset budget exceeded: {asset_bytes:,}"
print("PASS: approved hero and SVG blob lock preserved.")
print(f"PASS: {len(parser.images)} local image references resolve; no remote image dependencies.")
print(f"PASS: {len(parser.links)} links inspected; all local targets resolve.")
print("PASS: stale analytics, old focus cards, duplicated FAQ and layered portfolio sections are absent.")
print("PASS: six real projects use six optimized static artwork panels; no looping project-card GIFs remain.")
print("PASS: six original game assets exist; the quest map is an animated looping GIF.")
print("PASS: SVG safety, image dimensions, GIF timing and total asset budget verified.")
