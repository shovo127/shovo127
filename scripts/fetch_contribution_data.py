import datetime as dt
import html
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USERNAME = os.environ.get("GITHUB_USERNAME", "shovo127")
TOKEN = os.environ.get("PROFILE_READ_TOKEN", "").strip()
OUT_JSON = Path("assets/contribution-calendar.json")
OUT_SVG = Path("assets/contribution-city-data.svg")

def empty(reason):
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    return {
        "schema_version": 1,
        "status": "unavailable",
        "username": USERNAME,
        "source": "GitHub GraphQL contributionCalendar",
        "generated_at": now.isoformat(),
        "reason": reason,
        "private_visibility_note": "Private contribution counts require the account's profile setting and a token with read:user scope.",
        "total_contributions": None,
        "weeks": [],
        "days": [],
    }

def fetch():
    if not TOKEN:
        return empty("PROFILE_READ_TOKEN is not configured; neutral empty state.")
    end = dt.datetime.now(dt.timezone.utc).replace(hour=23, minute=59, second=59, microsecond=0)
    start = end - dt.timedelta(days=365)
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          hasAnyRestrictedContributions
          restrictedContributionsCount
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                weekday
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    payload = json.dumps({
        "query": query,
        "variables": {
            "login": USERNAME,
            "from": start.isoformat(),
            "to": end.isoformat(),
        },
    }).encode("utf-8")
    req = Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": "Bearer " + TOKEN,
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "shovo127-profile-contribution-city",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=30) as response:
            result = json.load(response)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        return empty("GitHub GraphQL request unavailable: " + type(exc).__name__)
    if result.get("errors"):
        return empty("GitHub GraphQL rejected the contribution query or token permissions.")
    user = result.get("data", {}).get("user")
    if not user:
        return empty("GitHub did not return the requested public user.")
    collection = user.get("contributionsCollection", {})
    calendar = collection.get("contributionCalendar", {})
    weeks = calendar.get("weeks", [])
    if not weeks:
        return empty("GitHub returned no contribution calendar weeks.")
    days = []
    for week_index, week in enumerate(weeks):
        for day in week.get("contributionDays", []):
            days.append({
                "week": week_index,
                "weekday": int(day.get("weekday", 0)) % 7,
                "date": day["date"],
                "count": int(day.get("contributionCount", 0)),
            })
    return {
        "schema_version": 1,
        "status": "available",
        "username": USERNAME,
        "source": "GitHub GraphQL contributionCalendar",
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "period_start": start.date().isoformat(),
        "period_end": end.date().isoformat(),
        "total_contributions": int(calendar.get("totalContributions", 0)),
        "private_contributions_visible": bool(collection.get("hasAnyRestrictedContributions")),
        "restricted_contributions_count": int(collection.get("restrictedContributionsCount", 0)),
        "private_visibility_note": "Private contribution counts appear only when enabled in GitHub profile settings and authorized by read:user scope.",
        "weeks": [{"index": i} for i in range(len(weeks))],
        "days": days,
    }

def render_svg(data):
    width, height = 1240, 470
    available = data.get("status") == "available"
    weeks = max(1, len(data.get("weeks", []))) if available else 52
    max_count = max((d["count"] for d in data.get("days", [])), default=0)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Shovo GitHub contribution city</title>',
        '<desc id="desc">Isometric calendar city generated from GitHub contribution counts. A neutral empty grid is shown when contribution data is unavailable.</desc>',
        '<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#071321"/><stop offset="1" stop-color="#102A43"/></linearGradient></defs>',
        '<rect width="1240" height="470" rx="26" fill="url(#bg)"/>',
        '<text x="54" y="58" fill="#5EEAD4" font-family="Arial,sans-serif" font-size="15" letter-spacing="3">GITHUB CONTRIBUTION CALENDAR</text>',
        '<text x="54" y="103" fill="#F8FAFC" font-family="Arial,sans-serif" font-size="31" font-weight="700">Isometric contribution city</text>',
    ]
    if available:
        subtitle = f'{data["total_contributions"]:,} contributions · {data["period_start"]} to {data["period_end"]} · GitHub GraphQL'
    else:
        subtitle = "Contribution data unavailable · neutral empty state · no activity fabricated"
    parts.append(f'<text x="56" y="135" fill="#AFC4D8" font-family="Arial,sans-serif" font-size="14">{html.escape(subtitle)}</text>')
    days = {(d["week"], d["weekday"]): d["count"] for d in data.get("days", [])}
    max_count = max(1, max_count)
    cell_w, cell_h = 9.5, 5.0
    origin_x, origin_y = 620, 145
    for week in range(weeks):
        for weekday in range(7):
            count = days.get((week, weekday), 0) if available else 0
            level = min(4, (count * 4 + max_count - 1) // max_count) if count else 0
            x = origin_x + (week - weekday) * cell_w
            y = origin_y + (week + weekday) * cell_h
            lift = level * 8
            top = f"{x},{y-lift} {x+cell_w*.75},{y+cell_h*.45-lift} {x},{y+cell_h*.9-lift} {x-cell_w*.75},{y+cell_h*.45-lift}"
            left = f"{x-cell_w*.75},{y+cell_h*.45-lift} {x},{y+cell_h*.9-lift} {x},{y+cell_h*.9} {x-cell_w*.75},{y+cell_h*.45}"
            right = f"{x},{y+cell_h*.9-lift} {x+cell_w*.75},{y+cell_h*.45-lift} {x+cell_w*.75},{y+cell_h*.45} {x},{y+cell_h*.9}"
            colors = [("#233746","#1B2B38","#152431"),("#2A827A","#20645F","#174D4A"),("#25A99A","#1D837B","#17645F"),("#36C5B0","#259A8D","#1B746B"),("#60A5FA","#3F7FC1","#2B5D94")]
            top_c,left_c,right_c=colors[level]
            parts.extend([
                f'<polygon points="{left}" fill="{left_c}"/>',
                f'<polygon points="{right}" fill="{right_c}"/>',
                f'<polygon points="{top}" fill="{top_c}" stroke="#9BCBCB" stroke-opacity=".16" stroke-width=".6"/>',
            ])
    parts.append('<text x="54" y="430" fill="#819DB4" font-family="Arial,sans-serif" font-size="12">Height and colour represent daily contribution counts; zero-count days remain at ground level.</text>')
    parts.append('</svg>')
    OUT_SVG.write_text("".join(parts), encoding="utf-8")

data = fetch()
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
render_svg(data)
print("Contribution calendar status:", data["status"])
print("Contribution calendar days:", len(data.get("days", [])))
print("Contribution city SVG:", OUT_SVG)
