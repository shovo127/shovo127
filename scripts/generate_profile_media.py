from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from urllib.request import Request, urlopen
import os, json, math, numpy as np

OUT=Path("assets"); OUT.mkdir(exist_ok=True)
W,H=1200,300
BG=(9,15,20); BG2=(22,34,42); WHITE=(235,240,242); MUTED=(145,160,168)
TEAL=(91,190,172); ICE=(137,171,190); BRASS=(170,143,101)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
def f(n,b=False,m=False): return ImageFont.truetype(MONO if m else (BOLD if b else FONT),n)
def base():
    x=np.linspace(0,1,W,dtype=np.float32)[None,:,None]
    a=np.array(BG,dtype=np.float32)[None,None,:]*(1-x)+np.array(BG2,dtype=np.float32)[None,None,:]*x
    a=np.repeat(a,H,axis=0).astype("uint8")
    im=Image.fromarray(a,"RGB").convert("RGBA"); d=ImageDraw.Draw(im,"RGBA")
    for xx in range(590,W,48): d.line((xx,18,xx,H-18),fill=(95,123,135,18),width=1)
    for yy in range(24,H,24): d.line((585,yy,W-18,yy),fill=(95,123,135,16),width=1)
    d.rounded_rectangle((12,12,W-12,H-12),radius=10,outline=(126,151,162,42),width=1)
    d.line((570,28,570,H-28),fill=(91,190,172,65),width=1)
    return im
def title(d,num,kicker,name,sub):
    d.text((46,32),f"{num:02d} / {kicker.upper()}",font=f(12,m=True),fill=TEAL)
    d.text((46,76),name,font=f(29,True),fill=WHITE)
    d.text((48,124),sub,font=f(12),fill=MUTED)
    d.line((48,170,520,170),fill=(*TEAL,105),width=1)
    d.text((48,190),"MOHAMMED THUHIDUL ISLAM SHOVO",font=f(9,m=True),fill=(116,135,145))
def metallic(d,x,y,r,col=TEAL):
    d.ellipse((x-r+4,y-r+6,x+r+4,y+r+6),fill=(0,0,0,90))
    d.ellipse((x-r,y-r,x+r,y+r),fill=(39,59,67,255),outline=(*ICE,180),width=2)
    d.arc((x-r+4,y-r+4,x+r-4,y+r-4),195,300,fill=(225,240,240,150),width=2)
    d.ellipse((x-r*.56,y-r*.56,x+r*.56,y+r*.56),fill=(17,31,38,255),outline=(*col,190),width=2)
    d.ellipse((x-r*.22,y-r*.22,x+r*.22,y+r*.22),fill=(10,19,24,255),outline=(*ICE,170),width=2)
def chip(d,x,y,r,col=TEAL):
    d.rounded_rectangle((x-r+4,y-r+6,x+r+4,y+r+6),radius=7,fill=(0,0,0,90))
    d.rounded_rectangle((x-r,y-r,x+r,y+r),radius=7,fill=(37,54,63,255),outline=(*ICE,200),width=2)
    d.rounded_rectangle((x-r+7,y-r+7,x+r-7,y+r-7),radius=4,fill=(12,24,31,255),outline=(*col,190),width=1)
    for q in range(-2,3):
        xx=x+q*r*.28
        d.line((xx,y-r-8,xx,y-r),fill=(*ICE,190),width=2); d.line((xx,y+r,xx,y+r+8),fill=(*ICE,190),width=2)
        yy=y+q*r*.28
        d.line((x-r-8,yy,x-r,yy),fill=(*ICE,190),width=2); d.line((x+r,yy,x+r+8,yy),fill=(*ICE,190),width=2)
    d.ellipse((x-r*.27,y-r*.27,x+r*.27,y+r*.27),fill=(33,69,69,255),outline=(*col,220),width=2)
def phone(d,x,y,r):
    d.rounded_rectangle((x-r*.7+4,y-r*1.35+6,x+r*.7+4,y+r*1.35+6),radius=12,fill=(0,0,0,90))
    d.rounded_rectangle((x-r*.7,y-r*1.35,x+r*.7,y+r*1.35),radius=12,fill=(35,50,59,255),outline=(*ICE,210),width=2)
    d.rounded_rectangle((x-r*.55,y-r*1.18,x+r*.55,y+r*1.13),radius=7,fill=(9,19,26,255),outline=(105,132,143,140),width=1)
    for q in range(3): d.line((x-r*.4,y-r*.7+q*18,x+r*.4,y-r*.7+q*18),fill=(*TEAL,130),width=2)
def book(d,x,y,r):
    d.polygon([(x-r,y-r),(x-2,y-r+8),(x-2,y+r),(x-r,y+r-8)],fill=(28,44,52,255),outline=(*ICE,190))
    d.polygon([(x+2,y-r+8),(x+r,y-r),(x+r,y+r-8),(x+2,y+r)],fill=(42,57,64,255),outline=(*ICE,190))
    d.line((x,y-r+6,x,y+r),fill=(*TEAL,210),width=2)
    for q in range(3): d.line((x-r*.7,y-r*.35+q*15,x-r*.2,y-r*.35+q*15),fill=(170,190,192,130),width=1)
def render(i,n):
    im=base(); d=ImageDraw.Draw(im,"RGBA")
    titles=[
      (1,"ABOUT / IDENTITY","Shovo — engineer & builder","Automobile engineering  ·  Software products  ·  Practical problem-solving"),
      (2,"ENGINEERING FOCUS","Connected disciplines","AI applications  ·  Automation  ·  Android systems  ·  Learning technology"),
      (3,"FEATURED WORK","Selected projects","AI tools  ·  Browser automation  ·  Android  ·  Learning technology"),
      (4,"TECHNOLOGY","Technology stack","Technologies I use or explore — not a proficiency ranking"),
      (5,"GITHUB COMMAND CENTER","Public engineering data","Live repository metrics generated from GitHub public data"),
      (6,"MILESTONES","Learning through delivery","Engineering practice  ·  Open-source work  ·  Automation  ·  Continuous learning"),
      (7,"CONTRIBUTION CITY","A landscape of consistent work","An original isometric interpretation of contribution activity"),
      (9,"CODING HABITS","A disciplined build cycle","Plan carefully  ·  Build in increments  ·  Verify behaviour  ·  Improve with evidence"),
      (10,"RECENT WRITING","Notes from the workbench","Research notes  ·  Technical experiments  ·  Lessons learned  ·  Documentation"),
      (11,"BEYOND CODE","Curiosity beyond the screen","Automotive  ·  German language  ·  Hardware  ·  Creative work"),
      (12,"CONTACT","Open to thoughtful collaboration","GitHub  ·  Lerne Deutsch Mit Technologie  ·  MailMerge by Shovo")
    ]
    num,kicker,name,sub=next(x for x in titles if x[0]==i); title(d,num,kicker,name,sub)
    xs=[660,800,940,1080]
    if i==1:
        metallic(d,900,143,76); d=ImageDraw.Draw(im,"RGBA")
        for r,ry,a in [(104,42,i*180/n),(128,52,55-i*180/n)]:
            pts=[]
            for q in range(181):
                t=2*math.pi*q/180; ang=math.radians(a)
                xx=r*math.cos(t); yy=ry*math.sin(t)
                pts.append((900+xx*math.cos(ang)-yy*math.sin(ang),143+xx*math.sin(ang)+yy*math.cos(ang)))
            d.line(pts,fill=(*TEAL,145),width=2)
        d.ellipse((887,130,913,156),fill=(13,29,35,255),outline=(*TEAL,220),width=2); d.text((900,143),"S",font=f(17,True),fill=WHITE,anchor="mm")
    elif i==2:
        metallic(d,xs[0],122,34); chip(d,xs[1],122,31); phone(d,xs[2],122,29); book(d,xs[3],122,28)
        for x,l in zip(xs,["AI SYSTEMS","AUTOMATION","ANDROID","EDTECH"]): d.text((x,205),l,font=f(10,True,m=True),fill=WHITE,anchor="mm")
    elif i==3:
        names=["KAI","VFX","VFU","NF","CTS","IPTV"]; xx=[630,730,830,930,1030,1130]
        for j,x in enumerate(xx):
            d.rounded_rectangle((x-30+3,108+5,x+30+3,162+5),radius=4,fill=(0,0,0,90))
            d.rounded_rectangle((x-30,108,x+30,162),radius=4,fill=(29,46,55,255),outline=(*ICE,170),width=1)
            d.line((x-20,118,x+20,118),fill=(*TEAL,130),width=1); d.text((x,137),names[j],font=f(10,True,m=True),fill=WHITE,anchor="mm")
            if j<5: d.line((x+31,137,xx[j+1]-31,137),fill=(*ICE,110),width=1)
    elif i==4:
        for j,(a,b) in enumerate([("WEB","TypeScript · JavaScript · Python · React · Next.js"),("SYSTEMS","Android · Linux · Windows · Git · GitHub"),("CLOUD","Cloudflare · Vercel · Firebase · Appwrite"),("CREATIVE","Photoshop · Illustrator · Premiere · PowerShell")]):
            y=57+j*53; d.text((620,y),a,font=f(10,True,m=True),fill=[TEAL,ICE,BRASS,ICE][j]); d.text((620,y+20),b,font=f(12),fill=WHITE); d.line((620,y+43,1140,y+43),fill=(100,127,138,80),width=1)
    elif i==5:
        for j,x in enumerate([620,795,970]):
            d.rounded_rectangle((x,62,x+150,124),radius=4,fill=(15,27,35,240),outline=(106,133,145,100),width=1)
            d.text((x+13,76),["REPOSITORIES","LANGUAGES","ACTIVITY"][j],font=f(9,m=True),fill=MUTED)
            d.line((x+13,104,x+135,104),fill=[(*TEAL,170),(*ICE,170),(*BRASS,170)][j],width=2)
        d.rounded_rectangle((620,148,1145,250),radius=4,fill=(13,24,32,230),outline=(100,127,139,90),width=1)
        pts=[(635+k*22,218-22*math.sin(k*.39)-10*math.sin(k*.18)) for k in range(23)]
        d.line(pts,fill=(*ICE,175),width=2); x,y=pts[(i*3)%22]; d.ellipse((x-4,y-4,x+4,y+4),fill=(*TEAL,230))
    elif i==6:
        for j,x in enumerate([650,805,960,1115]):
            metallic(d,x,137,13,TEAL); d.text((x,178),["ENGINEERING","OPEN SOURCE","AUTOMATION","LEARNING"][j],font=f(9,True,m=True),fill=WHITE,anchor="mm")
            if j<3: d.line((x+14,137,x+141,137),fill=(*ICE,120),width=2)
    elif i==7:
        for j in range(8):
            x=620+j*66; h=30+(j*19)%82; top=[(x,216-h),(x+22,204-h),(x+62,216-h),(x+40,228-h)]
            d.polygon([top[0],top[3],(x+40,216),(x,204)],fill=(26,47,56,255),outline=(99,136,147,155))
            d.polygon([top[3],top[2],(x+62,216),(x+40,216)],fill=(17,32,40,255),outline=(99,136,147,155))
            d.polygon(top,fill=(45,70,79,255),outline=(*TEAL,110))
    elif i==9:
        labels=["PLAN","BUILD","VERIFY","REFINE"]
        d.line((650,138,1100,138),fill=(*ICE,120),width=2)
        for j,x in enumerate(xs):
            d.ellipse((x-18,120,x+18,156),fill=(21,36,44,255),outline=(*TEAL if j==(i//5)%4 else ICE,210),width=2)
            d.text((x,138),str(j+1),font=f(11,True,m=True),fill=WHITE,anchor="mm"); d.text((x,185),labels[j],font=f(10,True,m=True),fill=WHITE,anchor="mm")
    elif i==10:
        book(d,880,142,58); d.text((1000,95),"FIELD NOTES",font=f(10,True,m=True),fill=TEAL)
        for j,t in enumerate(["RESEARCH","BUILD","REFINE"]): d.text((1000,125+j*22),t,font=f(10,m=True),fill=WHITE)
        d.line((1000,195,1138,195),fill=(*BRASS,130),width=1)
    elif i==11:
        x=665; d.line((x-43,142,x-28,125,x+25,125,x+42,143,x+48,151,x-50,151,x-43,142),fill=(*ICE,220),width=3)
        d.arc((x-36,135,x-15,164),180,360,fill=(*TEAL,220),width=3); d.arc((x+15,135,x+36,164),180,360,fill=(*TEAL,220),width=3)
        d.text((820,140),"Aä",font=f(38,True),fill=ICE,anchor="mm"); chip(d,975,140,28); d.ellipse((1095,110,1155,170),outline=(*BRASS,210),width=2); d.line((1105,158,1145,122),fill=(*BRASS,210),width=3)
        for x,l in zip(xs,["AUTOMOTIVE","LANGUAGE","HARDWARE","DESIGN"]): d.text((x,205),l,font=f(9,True,m=True),fill=WHITE,anchor="mm")
    elif i==12:
        d.line((680,143,1135,143),fill=(*ICE,110),width=2)
        for j,x in enumerate(xs):
            metallic(d,x,143,18,TEAL); d.text((x,198),["GITHUB","LEARNING","MAILMERGE","CONTACT"][j],font=f(9,True,m=True),fill=WHITE,anchor="mm")
    return im
def save(name,fn,frames=20,duration=90):
    fs=[fn(i,frames).convert("P",palette=Image.Palette.ADAPTIVE) for i in range(frames)]
    fs[0].save(OUT/name,save_all=True,append_images=fs[1:],duration=duration,loop=1,optimize=True,disposal=2)
def contributions():
    token=os.environ.get("GITHUB_TOKEN",""); user=os.environ.get("GITHUB_USERNAME","shovo127")
    if not token: return []
    q={"query":"query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{contributionCount}}}}}}","variables":{"login":user}}
    req=Request("https://api.github.com/graphql",data=json.dumps(q).encode(),headers={"Authorization":"Bearer "+token,"Content-Type":"application/json","User-Agent":"shovo-profile-snake"})
    try:
        with urlopen(req,timeout=30) as r: data=json.load(r)
        return [day for week in data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"] for day in week["contributionDays"]]
    except Exception as e:
        print("Contribution data unavailable; grid remains neutral:",type(e).__name__); return []
def snake():
    days=contributions(); cols,rows,cell,gap,ox,oy=53,7,15,5,70,66
    vals=[int(x.get("contributionCount",0)) for x in days[-cols*rows:]]; vals=[0]*(cols*rows-len(vals))+vals; mx=max(vals) if vals else 0
    path=[]; grid=Image.new("RGBA",(W,H),(0,0,0,0)); g=ImageDraw.Draw(grid,"RGBA")
    pal=[(25,37,44),(32,63,59),(37,91,76),(47,132,103),(74,177,137)]
    for c in range(cols):
        for r in range(rows):
            v=vals[c*rows+r]; level=0 if not v or not mx else min(4,1+int(3*v/mx))
            x=ox+c*(cell+gap); y=oy+r*(cell+gap); g.rounded_rectangle((x,y,x+cell,y+cell),radius=2,fill=(*pal[level],245))
    for r in range(rows):
        for c in (range(cols) if r%2==0 else range(cols-1,-1,-1)): path.append((ox+c*(cell+gap)+cell/2,oy+r*(cell+gap)+cell/2))
    frames=[]
    for frame in range(40):
        im=base(); im.alpha_composite(grid); d=ImageDraw.Draw(im,"RGBA")
        d.text((35,25),"08 / CONTRIBUTION SNAKE",font=f(11,m=True),fill=TEAL); d.text((760,27),"GITHUB CONTRIBUTION CALENDAR · SELF-HOSTED",font=f(9,m=True),fill=MUTED)
        head=round(frame/39*(len(path)-1))
        for k in range(9,0,-1):
            x,y=path[max(0,head-k)]; rr=5.4-k*.12
            d.ellipse((x-rr+1,y-rr+2,x+rr+1,y+rr+2),fill=(0,0,0,95)); d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(36+int(16*(1-k/9)),112+int(48*(1-k/9)),91+int(40*(1-k/9)),255),outline=(153,219,194,210),width=1)
        hx,hy=path[head]; d.ellipse((hx-6,hy-6,hx+6,hy+6),fill=(113,217,184,255),outline=(229,255,243,240),width=1)
        d.text((35,250),"Contribution intensity reflects GitHub data; unavailable data is never fabricated.",font=f(9),fill=MUTED)
        frames.append(im.convert("P",palette=Image.Palette.ADAPTIVE))
    frames[0].save(OUT/"section-08-contribution-snake.gif",save_all=True,append_images=frames[1:],duration=60,loop=1,optimize=True,disposal=2)
for i in [1,2,3,4,5,6,7,9,10,11,12]: save(f"section-{i:02d}.gif",lambda frame,total:render(i,frame,total))
snake()
print("Generated twelve self-hosted section animations.")
