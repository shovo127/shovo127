from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from html import escape
import os, sys

url=os.environ.get("BLOG_FEED_URL","").strip()
if not url:
    print("BLOG_FEED_URL is not configured; leaving the README feed unchanged.")
    sys.exit(0)

req=Request(url,headers={"User-Agent":"ShovoProfileBlogFeed/1.0","Accept":"application/atom+xml,application/rss+xml,application/xml,text/xml"})
with urlopen(req,timeout=25) as response:
    root=ET.fromstring(response.read())

def local(tag):
    return tag.rsplit("}",1)[-1].lower()

entries=[node for node in root.iter() if local(node.tag) in ("item","entry")]
posts=[]
for entry in entries[:10]:
    values={}
    for child in list(entry):
        key=local(child.tag)
        if key=="link":
            value=child.attrib.get("href") or (child.text or "").strip()
        else:
            value=(child.text or "").strip()
        if key not in values and value:
            values[key]=value
    title=values.get("title","").strip()
    link=values.get("link","").strip()
    date=values.get("pubdate") or values.get("published") or values.get("updated") or ""
    if title and link.startswith(("https://","http://")):
        label=escape(title)
        suffix=f" — {escape(date[:10])}" if date else ""
        posts.append(f"- [{label}]({link}){suffix}")
    if len(posts)==5:
        break

if not posts:
    print("Feed contained no valid public entries; leaving the README unchanged.")
    sys.exit(0)

readme=Path("README.md")
text=readme.read_text(encoding="utf-8")
start="<!-- BLOG-POST-LIST:START -->"
end="<!-- BLOG-POST-LIST:END -->"
if start not in text or end not in text:
    raise SystemExit("README blog markers are missing.")
before,tail=text.split(start,1)
_,after=tail.split(end,1)
updated=before+start+"\n"+"\n".join(posts)+"\n"+end+after
if updated!=text:
    readme.write_text(updated,encoding="utf-8")
    print(f"Updated README with {len(posts)} feed entries.")
else:
    print("Blog feed is already current.")
