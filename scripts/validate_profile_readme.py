from html.parser import HTMLParser
from pathlib import Path
import re, subprocess, xml.etree.ElementTree as ET
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
        self.images, self.links, self.remote_images, self.tables = [], [], [], 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table": self.tables += 1
        if tag == "img":
            src = (attrs.get("src") or "").strip()
            if src.startswith(("http://", "https://", "//")): self.remote_images.append(src)
            elif src: self.images.append(src)
        if tag == "a":
            href = (attrs.get("href") or "").strip()
            if href: self.links.append(href)

def local_target(value):
    value = value.strip().split()[0].strip("<>")
    if not value or value.startswith(("#", "http://", "https://", "mailto:", "tel:", "//")): return None
    return value.split("#", 1)[0].split("?", 1)[0]

readme = README.read_text(encoding="utf-8")
assert readme.startswith(APPROVED_HERO), "Approved Hero README block changed."
hero_blob = subprocess.check_output(["git", "hash-object", "assets/hero/engineering-hero.svg"], cwd=ROOT, text=True).strip()
assert hero_blob == APPROVED_HERO_BLOB, "Approved Hero SVG blob changed."

parser = References(); parser.feed(readme)
assert not parser.remote_images, f"External image dependencies: {parser.remote_images}"
targets = set(parser.images); targets.update(parser.links)
targets.update(re.findall(r"!??\[[^\]]*\]\(([^)]+)\)", readme))
missing = []
for raw in targets:
    target = local_target(raw)
    if not target: continue
    path = (ROOT / target).resolve()
    if ROOT.resolve() not in path.parents or not path.is_file(): missing.append(raw)
assert not missing, f"Broken or case-mismatched local refs: {sorted(missing)}"

required = [
    "assets/projects/visaflowx-interface.jpg",
    "assets/projects/kostenlos-ai-workspace.jpg",
    "assets/projects/noti-fixer-diagnostics.jpg",
    "assets/projects/circle-search-native.jpg",
    "assets/projects/smart-scanner-architecture.jpg",
    "assets/engineering/piston-connecting-rod-crankshaft.jpg",
    "assets/engineering/technical-focus.jpg",
    "assets/engineering/education-path.jpg",
    "assets/data/public-repository-snapshot.jpg",
    "assets/motion/signal-sweep.gif",
]
for rel in required:
    assert (ROOT / rel).is_file(), f"Missing required asset: {rel}"
assert readme.count('width="50%"') >= 6, "Expected two-column project and education card cells."
assert readme.count('width="33%"') >= 9, "Expected equal three-column technical focus and contact card cells."
assert readme.count("## SELECTED PROJECTS") == 1 and readme.count("## TECHNICAL FOCUS") == 1
assert readme.count("## EDUCATION & LEARNING") == 1 and readme.count("## CONNECT") == 1
assert readme.count('src="./assets/projects/') == 5, "All five selected project images must be used exactly once."
assert readme.count('src="./assets/motion/signal-sweep.gif"') == 3, "Expected existing signal loop in profile, divider and footer."
assert "contact@lernedeutschmittechnologie.tech" in readme
assert all(link in readme for link in [
    "https://github.com/shovo127/visaflowx-universal",
    "https://github.com/shovo127/kostenlos-ai",
    "https://github.com/shovo127/Noti-Fixer-for-Chinese-Devices",
    "https://github.com/shovo127/Circle-to-Search-for-Xiaomi",
    "https://github.com/shovo127/Smart-Scanner-Pro",
])

svg_files = sorted((ROOT / "assets").rglob("*.svg"))
for svg in svg_files:
    assert svg.stat().st_size <= 64*1024, f"SVG too large: {svg}"
    tree = ET.parse(svg)
    for node in tree.iter():
        assert node.tag.rsplit("}",1)[-1].lower() not in {"script","foreignobject"}, f"Active SVG content: {svg}"
        for key,value in node.attrib.items():
            if key.rsplit("}",1)[-1].lower() in {"href","src"}:
                assert not value.strip().startswith(("http://","https://","//")), f"Remote SVG dependency: {svg}"

expected = {
    "assets/projects/visaflowx-interface.jpg": (1200,520),
    "assets/projects/kostenlos-ai-workspace.jpg": (1200,520),
    "assets/projects/noti-fixer-diagnostics.jpg": (1200,520),
    "assets/projects/circle-search-native.jpg": (1200,520),
    "assets/projects/smart-scanner-architecture.jpg": (1200,520),
    "assets/engineering/piston-connecting-rod-crankshaft.jpg": (1200,520),
    "assets/engineering/technical-focus.jpg": (1200,360),
    "assets/engineering/education-path.jpg": (1200,300),
    "assets/data/public-repository-snapshot.jpg": (1200,360),
    "assets/motion/signal-sweep.gif": (560,84),
}
for rel, dims in expected.items():
    path=ROOT/rel
    assert path.is_file(), f"Missing {rel}"
    assert path.stat().st_size <= 150*1024, f"Asset too large: {rel}"
    with Image.open(path) as image:
        assert image.size == dims, f"Wrong dimensions for {rel}: {image.size}"
        if rel.endswith(".gif"):
            assert image.format == "GIF" and image.n_frames == 24 and image.info.get("loop")==0
            durations=[]
            for frame in range(image.n_frames):
                image.seek(frame); durations.append(image.info.get("duration"))
            assert all(d==220 for d in durations), f"Unexpected GIF timing {durations}"
        image.verify()

asset_bytes=sum(p.stat().st_size for p in (ROOT/"assets").rglob("*") if p.is_file())
assert asset_bytes <= 800*1024, f"Assets exceed budget: {asset_bytes}"
print("PASS: immutable Hero block and SVG blob SHA.")
print(f"PASS: {len(parser.images)} README images and {len(parser.links)} HTML links resolve locally.")
print(f"PASS: {parser.tables} HTML card tables, project/focus/education/contact grid coverage.")
print(f"PASS: {len(svg_files)} SVG files are safe and parse correctly.")
print("PASS: ten reused visual assets have verified formats and dimensions.")
print("PASS: existing 24-frame signal sweep loops at 220 ms/frame.")
print(f"PASS: self-hosted asset total {asset_bytes:,} bytes / 819,200-byte budget.")
