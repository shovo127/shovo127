import html
import json
from pathlib import Path

DASHBOARD = Path("assets/github-dashboard-data.json")
CONTRIBUTIONS = Path("assets/contribution-calendar.json")
OUTPUT = Path("assets/metrics-city.svg")

def load_json(path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return fallback

dashboard = load_json(DASHBOARD, {})
contributions = load_json(CONTRIBUTIONS, {"status": "unavailable", "total_contributions": None})
metrics = dashboard.get("metrics", {})
languages = dashboard.get("language_bytes", [])[:5]
contribution_available = contributions.get("status") == "available" and contributions.get("total_contributions") is not None

W, H = 1400, 860
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
    '<title id="title">Shovo127 isometric engineering metrics city</title>',
    '<desc id="desc">An isometric city visualizing verified public GitHub repository metrics, repository language byte distribution and project categories. Language blocks show code volume, not skill.</desc>',
    '<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#071321"/><stop offset="1" stop-color="#102A43"/></linearGradient><linearGradient id="glow"><stop stop-color="#2DD4BF" stop-opacity=".16"/><stop offset="1" stop-color="#60A5FA" stop-opacity="0"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/>',
    '<circle cx="1160" cy="120" r="330" fill="url(#glow)"/>',
    '<g stroke="#8BB5C8" stroke-opacity=".10" stroke-width="1"><path d="M0 180H1400M0 360H1400M0 540H1400M0 720H1400"/><path d="M140 0V800M280 0V800M420 0V800M560 0V800M700 0V800M840 0V800M980 0V800M1120 0V800M1260 0V800"/></g>',
    '<text x="64" y="62" fill="#5EEAD4" font-family="Arial,sans-serif" font-size="14" letter-spacing="4">DATA-DRIVEN ENGINEERING MAP</text>',
    '<text x="64" y="112" fill="#F8FAFC" font-family="Arial,sans-serif" font-size="36" font-weight="700">The Engineering Metrics City</text>',
    '<text x="66" y="145" fill="#AFC4D8" font-family="Arial,sans-serif" font-size="15">Verified public data · no invented achievements · no skill rankings</text>',
]

def polygon(points, fill, stroke="#A7C5D8"):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x,y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-opacity=".24" stroke-width="1.2"/>'

def building(cx, base, width, depth, height, color, label, value):
    top = [(cx,base-height),(cx+width/2,base-height+depth/2),(cx,base-height+depth),(cx-width/2,base-height+depth/2)]
    left = [(cx-width/2,base-height+depth/2),(cx,base-height+depth),(cx,base+depth),(cx-width/2,base+depth/2)]
    right = [(cx,base-height+depth),(cx+width/2,base-height+depth/2),(cx+width/2,base+depth/2),(cx,base+depth)]
    left_color = color
    right_color = color
    top_color = "#6DE5D0" if color != "#60A5FA" else "#A9D2FF"
    out = [polygon(left,left_color),polygon(right,right_color),polygon(top,top_color)]
    out.append(f'<text x="{cx}" y="{base-height-30}" text-anchor="middle" fill="#F1F7FF" font-family="Arial,sans-serif" font-size="24" font-weight="700">{html.escape(str(value))}</text>')
    out.append(f'<text x="{cx}" y="{base+depth+30}" text-anchor="middle" fill="#C4D7E8" font-family="Arial,sans-serif" font-size="14" font-weight="700">{html.escape(label)}</text>')
    return "".join(out)

stats = [
    ("PUBLIC REPOSITORIES", metrics.get("public_repositories"), "#167F78"),
    ("REPOSITORY STARS", metrics.get("public_repository_stars"), "#235F9B"),
    ("FOLLOWERS", metrics.get("public_followers"), "#62529C"),
    ("FOLLOWING", metrics.get("public_following"), "#946B36"),
    ("CONTRIBUTIONS", contributions.get("total_contributions") if contribution_available else None, "#1D877F"),
]
numeric = [float(value) for _,value,_ in stats if isinstance(value,(int,float))]
maximum = max(numeric, default=1)
for index,(label,value,color) in enumerate(stats):
    cx = 170 + index*265
    height = 48 + (min(1.0,float(value)/maximum)*112 if isinstance(value,(int,float)) else 0)
    shown = f"{int(value):,}" if isinstance(value,(int,float)) else "—"
    parts.append(building(cx,370,112,52,height,color,label,shown))

parts.append('<text x="64" y="485" fill="#5EEAD4" font-family="Arial,sans-serif" font-size="13" letter-spacing="3">LANGUAGE CODE VOLUME</text>')
if languages:
    max_share = max(float(item.get("share",0)) for item in languages) or 1
    for index,item in enumerate(languages):
        cx = 190 + index*245
        share = float(item.get("share",0))
        height = 26 + share/max_share*74
        label = str(item.get("name","Unknown"))
        pct = f"{share*100:.1f}%"
        parts.append(building(cx,630,78,36,height,("#167F78","#235F9B","#62529C","#946B36","#287C8A")[index%5],label,pct))
else:
    parts.append('<text x="70" y="570" fill="#AFC4D8" font-family="Arial,sans-serif" font-size="18">Language data unavailable</text>')

parts.append('<text x="64" y="755" fill="#5EEAD4" font-family="Arial,sans-serif" font-size="13" letter-spacing="3">VERIFIED PROJECT CATEGORIES</text>')
categories = ["AI applications","Browser automation","Android tooling","German learning","Gmail productivity"]
for index,label in enumerate(categories):
    x = 64 + index*260
    parts.append(f'<rect x="{x}" y="773" width="236" height="34" rx="12" fill="#FFFFFF" fill-opacity=".055" stroke="#8BB5C8" stroke-opacity=".22"/>')
    parts.append(f'<text x="{x+118}" y="795" text-anchor="middle" fill="#DCEAF5" font-family="Arial,sans-serif" font-size="13">{html.escape(label)}</text>')

generated = dashboard.get("generated_at","timestamp unavailable")
parts.append(f'<text x="64" y="735" fill="#8FA8BC" font-family="Arial,sans-serif" font-size="12">GitHub REST data generated {html.escape(generated)} · Contribution total shown only when GraphQL data is available.</text>')
parts.append('<text x="64" y="835" fill="#8FA8BC" font-family="Arial,sans-serif" font-size="11">Language proportions represent repository bytes, not proficiency. Repository metrics use public data; contribution totals follow GitHub visibility settings and token scope.</text>')
parts.append('</svg>')
OUTPUT.write_text("".join(parts), encoding="utf-8")
print("Generated", OUTPUT, "from public repository metrics and verified project categories.")
