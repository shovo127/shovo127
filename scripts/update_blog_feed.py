#!/usr/bin/env python3
"""Update an optional README writing list from an RSS or Atom feed."""

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import escape
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MAX_FEED_BYTES = 2 * 1024 * 1024
MAX_ITEMS = 5
START = "<!-- BLOG_POSTS_START -->"
END = "<!-- BLOG_POSTS_END -->"


def local_name(tag):
    return tag.rsplit("}", 1)[-1].lower()


def child_text(element, names):
    names = set(names)
    for child in element:
        if local_name(child.tag) in names:
            value = "".join(child.itertext()).strip()
            if value:
                return value
    return ""


def safe_http_url(value):
    try:
        parsed = urlparse(value.strip())
    except ValueError:
        return ""
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        return ""
    return value.strip()


def parse_date(value):
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        try:
            parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except (TypeError, ValueError, OverflowError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_feed(xml_bytes):
    """Return up to five safe, newest-first entries from RSS or Atom XML."""
    root = ET.fromstring(xml_bytes)
    entries = [node for node in root.iter() if local_name(node.tag) in {"item", "entry"}]
    results = []
    for entry in entries:
        title = child_text(entry, {"title"})
        if not title:
            continue

        link = ""
        for child in entry:
            if local_name(child.tag) != "link":
                continue
            attrs = {local_name(k): v for k, v in child.attrib.items()}
            rel = attrs.get("rel", "alternate")
            candidate = attrs.get("href", "") if rel in {"alternate", ""} else ""
            if not candidate:
                candidate = (child.text or "").strip()
            link = safe_http_url(candidate)
            if link:
                break
        if not link:
            continue

        raw_date = child_text(entry, {"pubdate", "published", "updated", "date"})
        published = parse_date(raw_date)
        results.append({
            "title": title,
            "url": link,
            "date": published,
            "date_label": published.strftime("%Y-%m-%d") if published else "",
        })

    results.sort(key=lambda item: item["date"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return results[:MAX_ITEMS]


def markdown_title(value):
    value = re.sub(r"\s+", " ", value).strip()
    for char in "\\[]()":
        value = value.replace(char, "\\" + char)
    return value


def render_items(items):
    lines = []
    for item in items:
        line = f"- [{markdown_title(item['title'])}]({item['url']})"
        if item["date_label"]:
            line += f" — {item['date_label']}"
        lines.append(line)
    return "\n".join(lines)


def update_readme(readme_text, items):
    """Insert or replace the optional writing block; no-op for an empty feed."""
    if not items:
        return readme_text
    rendered = START + "\n" + render_items(items) + "\n" + END
    has_start = START in readme_text
    has_end = END in readme_text
    if has_start != has_end:
        raise ValueError("README contains only one blog feed marker.")
    if has_start:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
        return pattern.sub(lambda _: rendered, readme_text, count=1)

    anchor = "\n## Connect\n"
    if anchor not in readme_text:
        raise ValueError("README has no '## Connect' insertion point.")
    section = "\n## Latest writing\n\n" + rendered + "\n"
    return readme_text.replace(anchor, section + anchor, 1)


def fetch_feed(url):
    safe_url = safe_http_url(url)
    if not safe_url:
        raise ValueError("BLOG_FEED_URL must be a public HTTP(S) URL.")
    request = Request(safe_url, headers={"User-Agent": "shovo127-profile-feed/1.0", "Accept": "application/atom+xml, application/rss+xml, application/xml, text/xml"})
    with urlopen(request, timeout=15) as response:
        data = response.read(MAX_FEED_BYTES + 1)
    if len(data) > MAX_FEED_BYTES:
        raise ValueError("Feed exceeds the 2 MiB size limit.")
    return data


def main():
    feed_url = os.environ.get("BLOG_FEED_URL", "").strip()
    if not feed_url:
        print("BLOG_FEED_URL is unset; no README changes.")
        return 0
    items = parse_feed(fetch_feed(feed_url))
    if not items:
        print("No valid public RSS/Atom entries found; README unchanged.")
        return 0
    original = README.read_text(encoding="utf-8")
    updated = update_readme(original, items)
    if updated == original:
        print("Latest writing block is already current.")
        return 0
    README.write_text(updated, encoding="utf-8")
    print(f"Updated Latest writing with {len(items)} verified feed links.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Blog feed update failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
