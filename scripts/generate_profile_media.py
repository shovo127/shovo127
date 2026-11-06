from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
from urllib.request import Request, urlopen
import json, os, math, random

OUT = Path("assets")
OUT.mkdir(exist_ok=True)
W, H, FRAMES = 1100, 120, 24
BG1, BG2 = (7, 19, 33), (14, 54, 69)
MINT, BLUE, VIOLET, GOLD = (67, 224, 190), (92, 165, 255), (174, 145, 255), (248, 195, 78)

def background():
    im = Image.new("RGB", (W, H))
    px = im.load()
    for x in range(W):
        t=x/(W-1)
        c=tuple(int(BG1[i]*(1-t)+BG2[i]*t) for i in range(3))
        for y in range(H): px[x,y]=c
    return im.convert("RGBA")

def save_gif(name, painter, size=(W,H), frames=FRAMES, duration=110):
    result=[]
    for i in range(frames):
        im=Image.new("RGBA",size,(7,19,33,255))
        painter(im,i,frames)
        result.append(im.convert("P",palette=Image.Palette.ADAPTIVE))
    result[0].save(OUT/name,save_all=True,append_images=result[1:],duration=duration,loop=0,optimize=True,disposal=2)

def about(im,i,n):
    im.alpha_composite(background())
    d=ImageDraw.Draw(im)
    d.text((30,20),"IDEAS  /  SYSTEMS  /  BUILDING",fill=(170,210,220))
    cx,cy=840,62
    for r in (24,43,61):
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(63,145,157,100),width=2)
    for k,col in enumerate((MINT,BLUE,VIOLET)):
        a=2*math.pi*i/n+k*2*math.pi/3
        x=cx+61*math.cos(a); y=cy+61*math.sin(a)
        d.line((cx,cy,x,y),fill=(*col,150),width=2)
        d.ellipse((x-6,y-6,x+6,y+6),fill=(*col,255))
    d.ellipse((cx-9,cy-9,cx+9,cy+9),fill=(*MINT,255))
    for k in range(9):
        x=(k*127+i*4)%W; y=25+(k*19)%75
        d.ellipse((x-2,y-2,x+2,y+2),fill=(110,190,220,150))
    d.line((30,96,1070,96),fill=(74,125,145,100),width=1)
    x=30+(i/n)*1040
    d.ellipse((x-3,93,x+3,99),fill=(*MINT,255))

def focus(im,i,n):
    im.alpha_composite(background()); d=ImageDraw.Draw(im)
    xs=[150,420,690,960]; cols=[MINT,BLUE,VIOLET,GOLD]
    d.text((30,18),"CONNECTED DISCIPLINES  /  ONE ENGINEERING MINDSET",fill=(170,210,220))
    d.line((xs[0],67,xs[-1],67),fill=(76,131,150,170),width=3)
    for j,(x,c) in enumerate(zip(xs,cols)):
        d.ellipse((x-17,50,x+17,84),fill=(18,52,68,255),outline=(*c,255),width=2)
        d.ellipse((x-5,62,x+5,72),fill=(*c,255))
        pulse=(i+j*6)%n
        radius=22+int(5*(1+math.sin(pulse*2*math.pi/n))/2)
        d.ellipse((x-radius,67-radius,x+radius,67+radius),outline=(*c,90),width=2)

def projects(im,i,n):
    im.alpha_composite(background()); d=ImageDraw.Draw(im)
    d.text((30,18),"SELECTED BUILDS  /  EXPERIMENTS THAT SOLVE REAL PROBLEMS",fill=(170,210,220))
    pts=[(150,78),(310,48),(470,78),(630,48),(790,78),(950,48)]
    for a,b in zip(pts,pts[1:]): d.line((*a,*b),fill=(65,160,170,130),width=2)
    head=(i*len(pts)//n)%len(pts)
    for j,(x,y) in enumerate(pts):
        c=MINT if j==head else (70,125,150)
        r=10 if j==head else 6
        d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,255),outline=(190,245,240,160),width=1)
    x=30+(i/n)*1040
    d.line((x,108,x+40,108),fill=(*MINT,210),width=3)

def tech(im,i,n):
    im.alpha_composite(background()); d=ImageDraw.Draw(im)
    d.text((30,16),"TOOLS ARE MEANS  /  USEFUL OUTCOMES ARE THE GOAL",fill=(170,210,220))
    for row in range(2):
        for col in range(12):
            x=30+col*88; y=42+row*35
            d.rounded_rectangle((x,y,x+70,y+22),radius=6,fill=(17,49,65,255),outline=(57,105,128,190),width=1)
    x=20+(i/n)*1050
    d.rounded_rectangle((x,38,x+54,101),radius=8,outline=(*MINT,220),width=3)

def dashboard(im,i,n):
    im.alpha_composite(background()); d=ImageDraw.Draw(im)
    d.text((30,18),"PUBLIC GITHUB DATA  /  AUTOMATICALLY REFRESHED",fill=(170,210,220))
    vals=[68,56,72,48,60,34,53,25,46,20,39,16,29,12,25,18]
    pts=[]
    for j,v in enumerate(vals):
        x=35+j*67; y=96-v
        pts.append((x,y))
    d.line(pts,fill=(66,145,177,150),width=3)
    x=pts[int(i/ n*(len(pts)-1))][0]; y=pts[int(i/n*(len(pts)-1))][1]
    d.ellipse((x-7,y-7,x+7,y+7),fill=(*MINT,255),outline=(235,255,250,255),width=2)

def achievement(im,i,n):
    im.alpha_composite(background()); d=ImageDraw.Draw(im)
    d.text((30,18),"MILESTONES  /  PRACTICE  /  SHARED LEARNING",fill=(170,210,220))
    for j in range(18):
        x=70+j*56; y=70+int(8*math.sin(j*.8+i*2*math.pi/n))
        r=3+(j%3)
        c=[MINT,BLUE,VIOLET,GOLD][j%4]
        d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,220))
    x=35+(i/n)*1030
    d.line((x,103,x+50,103),fill=(*GOLD,210),width=3)

def city(im,i,n):
    im.alpha_composite(background()); d=ImageDraw.Draw(im)
    d.text((30,16),"A CITY BUILT ONE CONTRIBUTION AT A TIME",fill=(170,210,220))
    base=103
    for j in range(18):
        x=40+j*58; h=20+(j*17)%58
        d.rectangle((x,base-h,x+35,base),fill=(15,73,81,255),outline=(49,151,139,255))
        for yy in range(base-h+7,base-4,12):
            for xx in (x+7,x+21):
                lit=(j*3+yy+i//3)%7==0
                d.rectangle((xx,yy,xx+5,yy+5),fill=(* (GOLD if lit else (37,91,105)),255))
    x=30+(i/n)*1040
    d.line((x,112,x+55,112),fill=(*MINT,180),width=2)

def habits(im,i,n):
    im.alpha_composite(background()); d=ImageDraw.Draw(im)
    labels=["PLAN","BUILD","TEST","IMPROVE"]
    xs=[150,420,690,960]; cols=[MINT,BLUE,VIOLET,GOLD]
    d.text((30,16),"SMALL ITERATIONS  /  BETTER ENGINEERING",fill=(170,210,220))
    d.line((xs[0],69,xs[-1],69),fill=(68,124,148,180),width=3)
    active=(i//6)%4
    for j,(x,label,c) in enumerate(zip(xs,labels,cols)):
        r=17 if j==active else 11
        d.ellipse((x-r,69-r,x+r,69+r),fill=(*c,220 if j==active else 100))
        d.text((x-22,98),label,fill=(230,243,248))
    x=xs[active]
    d.ellipse((x-25,44,x+25,94),outline=(*cols[active],110),width=2)

def snake_data():
    login=os.environ.get("GITHUB_USERNAME","shovo127")
    token=os.environ.get("GITHUB_TOKEN","")
    query={"query":"query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}","variables":{"login":login}}
    try:
        req=Request("https://api.github.com/graphql",data=json.dumps(query).encode(),headers={"Authorization":f"Bearer {token}","Content-Type":"application/json","User-Agent":"self-hosted-profile-media"})
        with urlopen(req,timeout=20) as response: data=json.load(response)
        weeks=data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        days=[day for week in weeks for day in week["contributionDays"]]
        return days
    except Exception as exc:
        print(f"Contribution calendar unavailable; using honest illustrative fallback: {type(exc).__name__}")
        return []

def snake_gif():
    days=snake_data()
    cols=max(1,len(days)//7)
    cell,gap=13,5
    width=cols*(cell+gap)+50; height=7*(cell+gap)+55
    result=[]
    for frame in range(28):
        im=Image.new("RGBA",(width,height),(7,19,33,255)); d=ImageDraw.Draw(im)
        d.text((22,12),"GITHUB CONTRIBUTION TRAIL",fill=(130,210,205))
        vals=[x.get("contributionCount",0) for x in days] if days else [((i*7)%5 if i%11==0 else 0) for i in range(cols*7)]
        maxv=max(vals or [1]) or 1
        points=[]
        for idx,v in enumerate(vals):
            col=idx//7; row=idx%7
            x=22+col*(cell+gap); y=38+row*(cell+gap)
            intensity=v/maxv
            color=(22,55,68,255) if v==0 else (31+int(25*intensity),105+int(110*intensity),92+int(95*intensity),255)
            d.rounded_rectangle((x,y,x+cell,y+cell),radius=3,fill=color)
            points.append((x+cell//2,y+cell//2))
        if points:
            head=(frame*5)%len(points)
            trail=[points[(head-k)%len(points)] for k in range(min(12,len(points)))]
            if len(trail)>1: d.line(trail,fill=(81,236,203,210),width=4)
            hx,hy=points[head]
            d.ellipse((hx-7,hy-7,hx+7,hy+7),fill=(220,255,247,255),outline=(39,190,164,255),width=2)
        result.append(im.convert("P",palette=Image.Palette.ADAPTIVE))
    result[0].save(OUT/"contribution-snake.gif",save_all=True,append_images=result[1:],duration=115,loop=0,optimize=True,disposal=2)

for name, painter in [
    ("about-motion.gif",about),("focus-motion.gif",focus),("projects-motion.gif",projects),
    ("technology-motion.gif",tech),("dashboard-motion.gif",dashboard),
    ("achievement-motion.gif",achievement),("city-motion.gif",city),("habits-motion.gif",habits)
]:
    save_gif(name,painter)
    print("Generated",name)
snake_gif()
print("Generated contribution-snake.gif")
