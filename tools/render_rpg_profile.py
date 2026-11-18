#!/usr/bin/env python3
"""Render the self-hosted RPG-style profile artwork with Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "game"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1200, 520
PALE = (247, 238, 240)
HOT = (255, 55, 82)
MUTED = (157, 145, 151)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False, sans=False):
    return ImageFont.truetype(BOLD if bold else (SANS if sans else MONO), size)

def gradient(size, top=(8, 9, 14), bottom=(24, 8, 15)):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] * (1-t) + bottom[i] * t) for i in range(3))
        for x in range(w):
            glow = max(0, 1 - abs(x - w*.52)/(w*.65)) * max(0, t-.28) * 7
            px[x, y] = tuple(min(255, int(v + glow*(1 if i == 0 else .25))) for i, v in enumerate(c))
    return im

def panel(d, box, fill=(14, 13, 19), outline=(91, 30, 48), radius=12, width=2):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def label(d, xy, text, size=15, color=HOT, bold=False):
    d.text(xy, text, font=font(size, bold), fill=color)

def draw_building(d, x, y, title, code, kind):
    d.polygon([(x-65,y+35),(x,y+5),(x+70,y+35),(x,y+66)], fill=(18,12,18), outline=(95,34,51))
    d.polygon([(x-53,y+8),(x,y-20),(x+53,y+8),(x,y+38)], fill=(31,16,24), outline=(151,39,63))
    d.polygon([(x-53,y+8),(x,y+38),(x,y+89),(x-53,y+59)], fill=(18,15,21), outline=(99,37,53))
    d.polygon([(x,y+38),(x+53,y+8),(x+53,y+59),(x,y+89)], fill=(26,13,21), outline=(115,34,54))
    if kind == "screen":
        panel(d,(x-30,y-4,x+30,y+36),fill=(5,14,19),outline=(205,43,67),radius=4)
        for k in range(3):
            d.line((x-20,y+6+k*9,x+20-k*4,y+6+k*9),fill=(255,75,99),width=3)
    elif kind == "tower":
        d.rectangle((x-24,y-18,x+24,y+56),fill=(17,16,24),outline=(185,42,67),width=3)
        for yy in (-8,8,24,40):
            d.rectangle((x-14,y+yy,x-4,y+yy+6),fill=(255,57,85))
            d.rectangle((x+5,y+yy,x+15,y+yy+6),fill=(130,34,54))
    elif kind == "gear":
        d.ellipse((x-17,y+3,x+17,y+37),outline=HOT,width=4)
        d.ellipse((x-6,y+14,x+6,y+26),fill=HOT)
        for a in range(0,360,45):
            r=23; cx=x+math.cos(math.radians(a))*r; cy=y+20+math.sin(math.radians(a))*r
            d.line((cx,cy,cx+math.cos(math.radians(a))*7,cy+math.sin(math.radians(a))*7),fill=HOT,width=4)
    elif kind == "garage":
        d.rectangle((x-29,y+1,x+29,y+42),fill=(10,12,17),outline=HOT,width=3)
        d.arc((x-22,y+5,x+22,y+43),180,355,fill=(255,75,96),width=4)
        d.line((x-14,y+24,x+14,y+24),fill=HOT,width=3)
    elif kind == "book":
        d.polygon([(x-28,y+5),(x-2,y+14),(x-2,y+47),(x-28,y+38)],fill=(47,21,34),outline=HOT)
        d.polygon([(x+28,y+5),(x+2,y+14),(x+2,y+47),(x+28,y+38)],fill=(25,18,25),outline=HOT)
        d.line((x,y+14,x,y+48),fill=(255,116,131),width=3)
    d.text((x,y+102),code,font=font(11),fill=HOT,anchor="mm")
    d.text((x,y+120),title,font=font(12,True),fill=PALE,anchor="mm")

def world_base():
    im=gradient((W,H))
    d=ImageDraw.Draw(im)
    random.seed(127)
    for _ in range(110):
        x=random.randrange(20,W-20); y=random.randrange(15,240); r=random.choice([1,1,2])
        d.ellipse((x-r,y-r,x+r,y+r),fill=random.choice([(95,40,55),(137,47,65),(70,50,61)]))
    d.polygon([(0,265),(85,220),(160,253),(260,190),(355,258),(465,206),(560,252),(680,190),(780,247),(910,188),(1010,252),(1110,210),(1200,245),(1200,520),(0,520)],fill=(14,13,20))
    for yy in range(290,540,35): d.line((0,yy,W,yy),fill=(34,19,28),width=1)
    for xx in range(-300,1500,90): d.line((600,280,xx,520),fill=(34,19,28),width=1)
    route=[(160,345),(340,305),(510,370),(690,310),(870,360),(1040,300)]
    d.line(route,fill=(95,24,43),width=12,joint="curve")
    d.line(route,fill=(218,39,69),width=3,joint="curve")
    for x,y in route: d.ellipse((x-7,y-7,x+7,y+7),fill=(255,74,97),outline=(255,180,188),width=2)
    draw_building(d,160,210,"BROWSER OUTPOST","01 / AUTOMATION","screen")
    draw_building(d,340,185,"AI LAB","02 / INTELLIGENCE","screen")
    draw_building(d,510,225,"ANDROID TOWER","03 / SYSTEMS","tower")
    draw_building(d,690,185,"WINDOWS WORKSHOP","04 / ARCHITECTURE","gear")
    draw_building(d,870,225,"AUTOMOTIVE GARAGE","05 / MECHANICAL","garage")
    draw_building(d,1040,185,"LEARNING CAMP","06 / STUDY","book")
    d.ellipse((548,390,652,494),fill=(30,12,22),outline=(157,31,56),width=3)
    d.rounded_rectangle((582,414,618,463),radius=7,fill=(28,28,34),outline=HOT,width=3)
    d.ellipse((586,390,614,420),fill=(202,147,138),outline=(250,192,186),width=2)
    d.rectangle((580,386,620,398),fill=(12,10,15))
    d.line((590,464,583,485),fill=(167,39,61),width=8)
    d.line((610,464,617,485),fill=(167,39,61),width=8)
    panel(d,(26,22,1174,112),fill=(8,9,14),outline=(117,34,54),radius=12)
    label(d,(50,40),"SHOVO127  /  ENGINEERING FRONTIER",15,PALE,True)
    label(d,(50,72),"WORLD MAP  ·  SELECT A MISSION  ·  REAL PROJECTS",11,MUTED)
    panel(d,(890,43,1147,89),fill=(24,10,17),outline=(162,37,60),radius=7)
    label(d,(914,57),"QUEST LOG  /  OPEN",12,HOT,True)
    panel(d,(26,465,1174,505),fill=(8,9,14),outline=(91,30,48),radius=8)
    label(d,(48,478),"MISSION ROUTE",10,MUTED)
    label(d,(210,478),"AUTOMATION  →  AI  →  ANDROID  →  SYSTEMS  →  GARAGE  →  STUDY",10,PALE)
    return im

def render_world():
    base=world_base()
    frames=[]
    route=[(160,345),(340,305),(510,370),(690,310),(870,360),(1040,300)]
    for f in range(20):
        im=base.convert("RGBA")
        overlay=Image.new("RGBA",im.size,(0,0,0,0))
        d=ImageDraw.Draw(overlay)
        node=(f//3)%len(route); x,y=route[node]
        pulse=18+int(7*(1+math.sin(f*math.pi/5)))
        d.ellipse((x-pulse,y-pulse,x+pulse,y+pulse),outline=(255,63,91,210),width=4)
        d.ellipse((x-3,y-3,x+3,y+3),fill=(255,226,231,255))
        t=(f/20)*(len(route)-1); idx=min(int(t),len(route)-2); frac=t-idx
        px=int(route[idx][0]*(1-frac)+route[idx+1][0]*frac)
        py=int(route[idx][1]*(1-frac)+route[idx+1][1]*frac)
        d.ellipse((px-10,py-10,px+10,py+10),fill=(255,51,82,120),outline=(255,170,183,255),width=2)
        frames.append(Image.alpha_composite(im,overlay).convert("RGB"))
    frames[0].save(OUT/"quest-world.gif",save_all=True,append_images=frames[1:],duration=120,loop=0,optimize=True,disposal=2)

def save_card(name,title,subtitle,draw_fn,height):
    im=gradient((W,height),(8,9,14),(18,8,14))
    d=ImageDraw.Draw(im)
    for x in range(20,W,40): d.line((x,0,x,height),fill=(22,18,25),width=1)
    d.rounded_rectangle((10,10,W-10,height-10),radius=14,outline=(90,28,47),width=2)
    label(d,(38,26),title,14,HOT,True)
    label(d,(38,54),subtitle,11,MUTED)
    draw_fn(im,d)
    im.save(OUT/name,optimize=True)

def skill_card(im,d):
    nodes=[(600,120,"ENGINEERING CORE"),(220,235,"SOFTWARE"),(405,235,"AI / AUTOMATION"),(600,235,"ANDROID"),(795,235,"AUTOMOTIVE"),(980,235,"LEARNING / 3D")]
    for x,y,_ in nodes[1:]:
        d.line((600,140,x,y-20),fill=(132,33,56),width=5)
        d.line((600,140,x,y-20),fill=(255,49,80),width=1)
    for i,(x,y,t) in enumerate(nodes):
        r=34 if i==0 else 25
        d.ellipse((x-r,y-r,x+r,y+r),fill=(33,13,23),outline=(255,62,91) if i==0 else (167,43,65),width=4)
        d.ellipse((x-8,y-8,x+8,y+8),fill=(222,49,77))
        d.text((x,y+r+12),t,font=font(13,True),fill=PALE,anchor="mm")
    d.text((600,300),"SKILLS GROW THROUGH STUDY, BUILDS AND VERIFICATION",font=font(12),fill=MUTED,anchor="mm")

def boss_card(im,d):
    cx,cy=260,190
    for r,col,w in [(100,(96,27,46),12),(76,(159,35,58),8),(45,(229,48,75),5)]:
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=col,width=w)
    d.ellipse((cx-22,cy-22,cx+22,cy+22),fill=(255,49,78))
    for a in range(0,360,45):
        x1=cx+math.cos(math.radians(a))*98; y1=cy+math.sin(math.radians(a))*98
        x2=cx+math.cos(math.radians(a))*126; y2=cy+math.sin(math.radians(a))*126
        d.line((x1,y1,x2,y2),fill=(177,38,62),width=14)
    d.line((cx-80,cy-65,cx-125,cy-112),fill=HOT,width=14)
    d.line((cx+80,cy-65,cx+125,cy-112),fill=HOT,width=14)
    d.text((260,295),"THE COMPLEXITY ENGINE",font=font(14,True),fill=PALE,anchor="mm")
    steps=[("01","OBSERVE","Understand the real problem"),("02","MODEL","Map boundaries and failure cases"),("03","BUILD","Implement a focused solution"),("04","VERIFY","Test behaviour and regressions")]
    for i,(num,name,desc) in enumerate(steps):
        y=100+i*52
        panel(d,(520,y,1145,y+42),fill=(15,12,18),outline=(114,31,51),radius=7)
        d.text((545,y+11),num,font=font(14,True),fill=HOT)
        d.text((600,y+10),name,font=font(14,True),fill=PALE)
        d.text((760,y+12),desc,font=font(11),fill=MUTED)

def character_card(im,d):
    d.ellipse((70,110,260,300),fill=(24,13,22),outline=(194,39,65),width=4)
    d.ellipse((128,143,202,217),fill=(203,150,140),outline=(255,190,190),width=3)
    d.rectangle((119,133,211,155),fill=(10,10,14))
    d.rounded_rectangle((108,218,220,291),radius=22,fill=(25,26,34),outline=HOT,width=4)
    d.line((145,285,130,310),fill=(170,35,61),width=12)
    d.line((185,285,200,310),fill=(170,35,61),width=12)
    rows=[("CLASS","AUTOMOBILE ENGINEERING DIPLOMA GRADUATE"),
          ("ROLE","INDEPENDENT SOFTWARE BUILDER"),
          ("HOME BASE","DHAKA, BANGLADESH"),
          ("CURRENT QUEST","TELC DEUTSCH B2 PREPARATION")]
    for i,(k,v) in enumerate(rows):
        x=330+(i%2)*420; y=105+(i//2)*92
        panel(d,(x,y,x+390,y+66),fill=(14,12,18),outline=(107,31,50),radius=8)
        d.text((x+18,y+10),k,font=font(11,True),fill=HOT)
        d.text((x+18,y+34),v,font=font(12,True),fill=PALE)

def save_card_art(im,d):
    panel(d,(50,90,245,260),fill=(13,12,18),outline=(174,38,62),radius=12,width=4)
    d.rectangle((70,110,225,224),fill=(5,12,16),outline=(103,35,52),width=3)
    d.text((87,130),"> SAVE",font=font(17,True),fill=HOT)
    d.text((87,164),"> EXPLORE",font=font(13),fill=PALE)
    d.text((87,190),"> CONNECT",font=font(13),fill=PALE)
    d.line((95,242,200,242),fill=HOT,width=5)
    d.text((330,115),"QUEST LOG SAVED",font=font(27,True,sans=True),fill=PALE)
    d.text((330,165),"REAL PROJECTS. CONTINUOUS LEARNING. BETTER SYSTEMS.",font=font(15),fill=HOT)
    d.text((330,215),"GITHUB  /  LEARNING PROJECT  /  EMAIL",font=font(13),fill=MUTED)

def inventory_card(im,d):
    items=[("WEB","JavaScript · React · TypeScript"),("AI / BACKEND","Appwrite · Cloudflare · LLM APIs"),
           ("ANDROID","Kotlin · Android SDK · ADB"),("AUTOMATION","Python · Shell · PowerShell"),
           ("DESKTOP STUDY","C# · .NET · WPF*"),("PLAYLISTS","M3U · M3U8")]
    for i,(k,v) in enumerate(items):
        x=35+(i%2)*575; y=98+(i//2)*62
        panel(d,(x,y,x+540,y+48),fill=(14,12,18),outline=(98,29,47),radius=7)
        d.text((x+16,y+7),k,font=font(10,True),fill=HOT)
        d.text((x+165,y+13),v,font=font(12),fill=PALE)
    d.text((40,294),"* C# / .NET / WPF ARE LISTED FOR SMART SCANNER PRO; INTEGRATIONS REMAIN PLANNED WHERE NOT IMPLEMENTED.",font=font(10),fill=MUTED)

def main():
    render_world()
    save_card("skill-tree.png","SKILL TREE  /  SIX CONNECTED PATHS","Areas explored through study and real projects.",skill_card,340)
    save_card("boss-arena.png","BOSS FIGHT  /  DEBUG THE SYSTEM","Complexity is the challenge. The method is repeatable.",boss_card,340)
    save_card("character-sheet.png","CHARACTER FILE  /  VERIFIED PROFILE","Real background and current learning — no invented XP or achievements.",character_card,330)
    save_card("inventory.png","WORKSHOP INVENTORY  /  TOOLS IN USE","Technologies shown in the context of linked repositories.",inventory_card,340)
    save_card("save-point.png","SAVE POINT  /  END OF THE QUEST LOG","Pick a project, inspect the source, or get in touch.",save_card_art,330)
    print("Rendered RPG profile assets into assets/game/")

if __name__ == "__main__":
    main()
