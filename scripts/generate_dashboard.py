import json, os, urllib.request, datetime, html
from pathlib import Path

user = os.environ["GITHUB_USERNAME"]
token = os.environ["GITHUB_TOKEN"]

def api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "profile-dashboard-workflow",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

profile = api(f"/users/{user}")
repos = []
page = 1
while True:
    batch = api(f"/users/{user}/repos?per_page=100&page={page}&sort=updated")
    if not batch:
        break
    repos.extend(batch)
    if len(batch) < 100:
        break
    page += 1
public_repos = [r for r in repos if not r.get("fork") and not r.get("archived")]
generated_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
langs = {}
for repo in public_repos:
    data = api(f"/repos/{user}/{repo['name']}/languages")
    for name, size in data.items():
        langs[name] = langs.get(name, 0) + size

lang_rows = sorted(langs.items(), key=lambda item: item[1], reverse=True)[:6]
total = sum(langs.values()) or 1
dashboard_data = {
    "schema_version": 1,
    "username": user,
    "source": "GitHub public REST API",
    "generated_at": generated_at,
    "definitions": {
        "public_repositories": "GitHub users.public_repos field.",
        "public_followers": "GitHub users.followers field.",
        "public_following": "GitHub users.following field.",
        "public_repository_stars": "Sum of stargazers_count across all public repositories returned by the users repositories endpoint.",
        "language_bytes": "Sum of GitHub language API byte counts across public repositories excluding forks and archived repositories.",
        "recently_updated_projects": "Non-fork, non-archived public repositories sorted by repository updated_at metadata.",
    },
    "metrics": {
        "public_repositories": profile.get("public_repos"),
        "public_followers": profile.get("followers"),
        "public_following": profile.get("following"),
        "public_repository_stars": sum(r.get("stargazers_count", 0) for r in repos),
    },
    "language_bytes": [{"name": name, "bytes": size, "share": round(size / total, 6)} for name, size in sorted(langs.items(), key=lambda item: item[1], reverse=True)],
    "repositories": [{
        "name": r["name"], "url": r.get("html_url"), "description": r.get("description"),
        "stars": r.get("stargazers_count", 0), "language": r.get("language"),
        "created_at": r.get("created_at"), "updated_at": r.get("updated_at"),
        "fork": r.get("fork", False), "archived": r.get("archived", False)
    } for r in sorted(repos, key=lambda item: item.get("updated_at", ""), reverse=True)],
}
Path("assets/github-dashboard-data.json").write_text(json.dumps(dashboard_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
pieces = []
def add(s): pieces.append(s)
add('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="690" viewBox="0 0 1200 690" role="img" aria-labelledby="title desc">')
add('<title id="title">GitHub Engineering Dashboard</title><desc id="desc">Live public GitHub repository, follower, star, language and recent project data for '+html.escape(user)+'.</desc>')
add('''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#071321"/><stop offset="1" stop-color="#102A43"/></linearGradient>
<linearGradient id="aqua"><stop stop-color="#2DD4BF"/><stop offset="1" stop-color="#60A5FA"/></linearGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#A7C5DD" stroke-opacity=".07"/></pattern>
</defs>''')
add('<rect width="1200" height="690" rx="30" fill="url(#bg)"/><rect width="1200" height="690" rx="30" fill="url(#grid)"/>')
add('<circle cx="1080" cy="70" r="240" fill="#0D9488" opacity=".08"/>')
add('<text x="54" y="62" font-family="Arial,sans-serif" font-size="17" letter-spacing="4" fill="#5EEAD4">ENGINEERING SNAPSHOT</text>')
add('<text x="54" y="112" font-family="Arial,sans-serif" font-size="38" font-weight="800" fill="#F8FAFC">GitHub Command Center</text>')
add('<text x="56" y="147" font-family="Arial,sans-serif" font-size="17" fill="#AFC4D8">@'+html.escape(user)+'  ·  '+datetime.datetime.fromisoformat(generated_at).strftime('%d %b %Y %H:%M UTC')+'</text>')
metrics = [
    ("PUBLIC REPOSITORIES", str(profile.get("public_repos") if profile.get("public_repos") is not None else "—"), "#2DD4BF"),
    ("FOLLOWERS", str(profile.get("followers") if profile.get("followers") is not None else "—"), "#60A5FA"),
    ("FOLLOWING", str(profile.get("following") if profile.get("following") is not None else "—"), "#A78BFA"),
    ("PUBLIC REPOSITORY STARS", str(sum(r.get("stargazers_count",0) for r in repos)), "#FBBF24"),
]
for i,(label,value,color) in enumerate(metrics):
    x=54+i*284
    add(f'<rect x="{x}" y="190" width="260" height="128" rx="20" fill="#FFFFFF" fill-opacity=".055" stroke="#B8D3E8" stroke-opacity=".13"/>')
    add(f'<rect x="{x}" y="190" width="260" height="5" rx="2.5" fill="{color}"/>')
    add(f'<text x="{x+22}" y="235" font-family="Arial,sans-serif" font-size="13" letter-spacing="1.5" fill="#B0C4D8">{label}</text>')
    add(f'<text x="{x+22}" y="291" font-family="Arial,sans-serif" font-size="44" font-weight="800" fill="#F8FAFC">{value}</text>')
add('<rect x="54" y="350" width="540" height="280" rx="22" fill="#FFFFFF" fill-opacity=".045" stroke="#B8D3E8" stroke-opacity=".13"/>')
add('<text x="82" y="395" font-family="Arial,sans-serif" font-size="21" font-weight="700" fill="#F8FAFC">Language footprint</text>')
y=445
for name,size in lang_rows[:5]:
    pct=size/total
    add(f'<text x="82" y="{y}" font-family="Arial,sans-serif" font-size="15" fill="#D7E5F3">{html.escape(name)}</text>')
    add(f'<text x="554" y="{y}" font-family="Arial,sans-serif" font-size="14" fill="#AFC4D8" text-anchor="end">{pct*100:.1f}%</text>')
    add(f'<rect x="82" y="{y+12}" width="472" height="9" rx="4.5" fill="#FFFFFF" fill-opacity=".09"/>')
    add(f'<rect x="82" y="{y+12}" width="{472*pct:.1f}" height="9" rx="4.5" fill="url(#aqua)"/>')
    y+=43
if not lang_rows:
    add('<text x="82" y="455" font-family="Arial,sans-serif" font-size="15" fill="#AFC4D8">Language data is not available yet.</text>')
add('<rect x="620" y="350" width="526" height="280" rx="22" fill="#FFFFFF" fill-opacity=".045" stroke="#B8D3E8" stroke-opacity=".13"/>')
add('<text x="650" y="395" font-family="Arial,sans-serif" font-size="21" font-weight="700" fill="#F8FAFC">Recently updated projects</text>')
y=442
featured_repos = [r for r in public_repos if r.get("name") != user]
for repo in sorted(featured_repos,key=lambda r:r.get("updated_at",""),reverse=True)[:5]:
    name=html.escape(repo["name"])
    desc=html.escape((repo.get("description") or "Open repository").strip())
    if len(desc)>48: desc=desc[:45]+"..."
    stars=repo.get("stargazers_count",0)
    add(f'<circle cx="660" cy="{y-5}" r="5" fill="#2DD4BF"/>')
    url = html.escape(repo.get("html_url") or ("https://github.com/" + user + "/" + repo["name"]), quote=True)
    add(f'<a href="{url}"><text x="679" y="{y}" font-family="Arial,sans-serif" font-size="16" font-weight="700" fill="#EAF4FF">{name}</text></a>')
    add(f'<text x="679" y="{y+21}" font-family="Arial,sans-serif" font-size="12" fill="#9FB6CB">{desc}</text>')
    add(f'<text x="1110" y="{y}" font-family="Arial,sans-serif" font-size="13" fill="#FBBF24" text-anchor="end">★ {stars}</text>')
    y+=42
add('<text x="54" y="662" font-family="Arial,sans-serif" font-size="12" fill="#7F9AB2">Source: GitHub public REST API  ·  Language shares represent repository code volume, not proficiency.</text>')
add('</svg>')
Path("assets/github-dashboard.svg").write_text("".join(pieces),encoding="utf-8")
import cairosvg
cairosvg.svg2png(url="assets/github-dashboard.svg", write_to="assets/github-dashboard.png", output_width=1200, output_height=690)
print(f"Generated self-hosted SVG, PNG and JSON dashboard for {len(repos)} public repositories; {len(public_repos)} non-fork, non-archived repositories used for language shares.")
