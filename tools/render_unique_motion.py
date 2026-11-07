#!/usr/bin/env python3
"""Render a premium, GitHub-safe profile motion system with distinct motion per component."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, colorsys
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/"assets"; M=A/"motion"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
TEAL=(62,198,181); ICE=(186,220,231); GOLD=(218,177,113); WHITE=(235,243,246); MUTED=(155,177,188)
BG=(9,17,27); PANEL=(17,30,43); LINE=(36,58,72)
def font(sz,b=False,m=False): return ImageFont.truetype(MONO if m else BOLD if b else FONT,sz)
def quant(im,n=64): return im.convert("RGB").quantize(colors=n,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
def save(frames,path,delay=90,n=64):
    q=[quant(x,n) for x in frames]
    q[0].save(path,save_all=True,append_images=q[1:],duration=delay,loop=0,optimize=True,disposal=2)
def text(d,xy,s,sz=16,fill=WHITE,b=False,m=False,anchor=None): d.text(xy,s,font=font(sz,b,m),fill=fill,anchor=anchor)
def recolor(im):
    im=im.convert("RGB"); px=im.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b=px[x,y]
            mx=max(r,g,b); mn=min(r,g,b)
            if mx-mn<12: continue
            # Re-map bright red accents and dark-red grid lines; preserve neutral metals.
            if r>g*1.15 and r>b*1.10 and r>24:
                v=mx/255
                if g<r*.34: hue=0.49 # teal
                else: hue=0.105 # restrained champagne
                sat=min(.72,max(.24,(mx-mn)/max(1,mx)*1.15))
                rr,gg,bb=colorsys.hsv_to_rgb(hue,sat,v)
                px[x,y]=(int(rr*255),int(gg*255),int(bb*255))
    return im
def recolor_sources():
    for folder in ("projects","focus","engineering","data","cards"):
        p=A/folder
        if not p.exists(): continue
        for f in p.glob("*.jpg"):
            im=Image.open(f); recolor(im).save(f,"JPEG",quality=90,optimize=True,progressive=True)
def typewriter(label,path,accent=TEAL,width=560,height=58,size=25):
    # Each character is revealed in sequence; the cursor remains alive after the line completes.
    im=Image.new("RGB",(width,height),BG); d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,width-2,height-2),radius=10,fill=PANEL,outline=LINE,width=1)
    d.rectangle((12,12,15,height-12),fill=accent)
    f=font(size,True)
    maxw=width-48
    while d.textbbox((0,0),label,font=f)[2]>maxw and size>14:
        size-=1; f=font(size,True)
    count=len(label); frames=[]
    # Initial cursor blink, then progressive typing.
    for i in range(count+1):
        frame=im.copy(); dr=ImageDraw.Draw(frame); shown=label[:i]
        dr.text((28,(height-size)//2-2),shown,font=f,fill=WHITE)
        tw=dr.textbbox((28,0),shown,font=f)[2] if shown else 28
        if i%2==0: dr.rounded_rectangle((tw+2,17,tw+5,height-17),radius=1,fill=accent)
        frames.append(frame)
    for j in range(10):
        frame=im.copy(); dr=ImageDraw.Draw(frame); dr.text((28,(height-size)//2-2),label,font=f,fill=WHITE)
        tw=dr.textbbox((28,0),label,font=f)[2]
        if j%2==0: dr.rounded_rectangle((tw+2,17,tw+5,height-17),radius=1,fill=accent)
        frames.append(frame)
    save(frames,path,95,32)
def title_assets():
    labels=[
      ("hero-name.gif","MOHAMMED THUHIDUL ISLAM SHOVO",GOLD,880,62,28),
      ("hero-tagline.gif","ENGINEERING MINDSET · SOFTWARE BUILDING · AI & AUTOMATION · PRACTICAL TECHNOLOGY",TEAL,1050,52,17),
      ("section-profile.gif","ENGINEERING PROFILE",TEAL,560,54,22),
      ("section-projects.gif","SELECTED PROJECTS",GOLD,560,54,22),
      ("section-focus.gif","TECHNICAL FOCUS",TEAL,560,54,22),
      ("section-engine.gif","AUTOMOTIVE ENGINEERING / 3D STUDY",GOLD,720,54,21),
      ("section-education.gif","EDUCATION & LEARNING",TEAL,560,54,22),
      ("section-analytics.gif","PUBLIC REPOSITORY ANALYTICS",GOLD,620,54,22),
      ("section-connect.gif","CONNECT",TEAL,420,54,22),
    ]
    for name,label,col,w,h,sz in labels: typewriter(label,M/name,col,w,h,sz)
    projects=["VisaFlowX Universal","Kostenlos AI","Noti-Fixer for Chinese Devices","Circle to Search for Xiaomi","Smart Scanner Pro","IPTV By Shovo"]
    focus=["Software Engineering","AI & Automation","Android Systems","Automotive Engineering","Learning Technology","Mechanical Visualisation"]
    for i,s in enumerate(projects,1): typewriter(s,M/f"title-project-{i:02d}.gif",GOLD if i%2==0 else TEAL,480,50,18)
    for i,s in enumerate(focus,1): typewriter(s,M/f"title-focus-{i:02d}.gif",TEAL if i%2==0 else GOLD,480,50,18)
    typewriter("Diploma in Automobile Engineering",M/"title-education-01.gif",GOLD,480,50,18)
    typewriter("TELC Deutsch B2",M/"title-education-02.gif",TEAL,480,50,18)
    typewriter("ENGINEERING · SOFTWARE · SYSTEMS",M/"title-footer.gif",GOLD,600,54,20)
    typewriter("GITHUB",M/"title-connect-github.gif",TEAL,320,48,18)
    typewriter("LEARNING PROJECT",M/"title-connect-learning.gif",GOLD,420,48,18)
    typewriter("EMAIL",M/"title-connect-email.gif",TEAL,320,48,18)
def unique_project_motion():
    names=["visaflowx-interface","kostenlos-ai-workspace","noti-fixer-diagnostics","circle-search-native","smart-scanner-architecture","iptv-by-shovo"]
    for idx,name in enumerate(names):
        base=recolor(Image.open(A/"projects"/(name+".jpg"))).resize((480,208),Image.Resampling.LANCZOS)
        frames=[]; n=24
        for i in range(n):
            im=base.copy(); d=ImageDraw.Draw(im); t=i/n
            if idx==0: # sequential route nodes
                pts=[(85,150),(185,80),(300,130),(405,65)]
                for a,b in zip(pts,pts[1:]): d.line((a,b),fill=(68,122,134),width=2)
                upto=min(3,int(t*4))
                for j,(x,y) in enumerate(pts):
                    rad=7 if j<=upto else 4; col=GOLD if j<=upto else (70,96,110)
                    d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=col)
                seg=min(2,int(t*3)); frac=t*3-seg
                x=int(pts[seg][0]+(pts[seg+1][0]-pts[seg][0])*frac)
                y=int(pts[seg][1]+(pts[seg+1][1]-pts[seg][1])*frac)
                pulse=9+int(4*(.5+.5*math.sin(2*math.pi*t*3)))
                d.ellipse((x-pulse,y-pulse,x+pulse,y+pulse),outline=TEAL,width=2)
                d.ellipse((x-4,y-4,x+4,y+4),fill=GOLD)
            elif idx==1: # AI chat: response text types in
                msg="Routing to the best available model..."
                k=min(len(msg),int(t*len(msg)*1.35))
                d.rounded_rectangle((100,130,455,183),radius=9,fill=(13,30,42),outline=TEAL,width=1)
                text(d,(114,145),msg[:k],11,WHITE)
                if i%2==0: d.rectangle((116+d.textbbox((0,0),msg[:k],font=font(11))[2],145,119+d.textbbox((0,0),msg[:k],font=font(11))[2],160),fill=GOLD)
            elif idx==2: # notification bell pulse / vibration
                x,y=360,92; r=18+int(14*(.5+.5*math.sin(2*math.pi*t*2)))
                d.arc((x-r,y-r,x+r,y+r),200,340,fill=GOLD,width=3); d.arc((x-r-12,y-r-12,x+r+12,y+r+12),210,330,fill=TEAL,width=2)
                dx=int(3*math.sin(t*2*math.pi*8)); d.ellipse((x-9+dx,y-8,x+9+dx,y+10),fill=GOLD)
            elif idx==3: # expanding target reticle
                x,y=240,104; r=12+int(t*75)
                d.ellipse((x-r,y-r,x+r,y+r),outline=TEAL,width=2); d.ellipse((x-8,y-8,x+8,y+8),outline=GOLD,width=2)
                d.line((x-100,y,x-18,y),fill=ICE,width=1); d.line((x+18,y,x+100,y),fill=ICE,width=1)
                d.line((x,y-100,x,y-18),fill=ICE,width=1); d.line((x,y+18,x,y+100),fill=ICE,width=1)
            elif idx==4: # document feed / vertical scan, with page corners
                y=int(28+t*155)
                d.line((110,y,430,y),fill=TEAL,width=3); d.line((110,y+4,430,y+4),fill=(80,155,160),width=1)
                for x0,y0,sx,sy in [(110,28,1,1),(430,28,-1,1),(110,180,1,-1),(430,180,-1,-1)]:
                    d.line((x0,y0,x0+sx*22,y0),fill=GOLD,width=3); d.line((x0,y0,x0,y0+sy*22),fill=GOLD,width=3)
            else: # playlist equaliser, each channel has a distinct amplitude
                for j in range(12):
                    x=75+j*29; h=8+int((.5+.5*math.sin(t*2*math.pi+j*.8))*38)
                    d.rounded_rectangle((x,170-h,x+12,170),radius=4,fill=TEAL if j%3 else GOLD)
            frames.append(im.resize((360,156),Image.Resampling.LANCZOS))
        save(frames,M/f"project-{idx+1:02d}-kinetic-v2.gif",120,32)
def unique_focus_motion():
    for idx in range(1,7):
        base=recolor(Image.open(A/"focus"/f"focus-{idx:02d}.jpg")).resize((480,225),Image.Resampling.LANCZOS)
        frames=[]
        for i in range(24):
            im=base.copy(); d=ImageDraw.Draw(im); t=i/24
            if idx==1: # terminal typing
                msg="git commit -m \"verified build\""; k=min(len(msg),int(t*len(msg)*1.2))
                d.rounded_rectangle((220,195,468,220),radius=4,fill=(8,18,27))
                text(d,(228,201),msg[:k],9,TEAL,m=True)
                if i%2==0: d.rectangle((230+d.textbbox((0,0),msg[:k],font=font(9,m=True))[2],201,232+d.textbbox((0,0),msg[:k],font=font(9,m=True))[2],212),fill=GOLD)
            elif idx==2: # neural graph: sequential node activation
                pts=[(275,45),(330,82),(390,48),(440,100),(370,158),(285,170)]
                for j in range(len(pts)-1): d.line((pts[j],pts[j+1]),fill=(54,93,106),width=2)
                for j,(x,y) in enumerate(pts):
                    r=5+int(4*(.5+.5*math.sin(t*2*math.pi+j)))
                    d.ellipse((x-r,y-r,x+r,y+r),fill=GOLD if (i//4)%6==j else TEAL)
            elif idx==3: # android notification concentric ripple
                x,y=365,110; r=8+int((i%16)*6)
                d.ellipse((x-r,y-r,x+r,y+r),outline=TEAL,width=2); d.ellipse((x-7,y-7,x+7,y+7),fill=GOLD)
            elif idx==4: # automotive piston motion
                y=105+int(22*math.sin(2*math.pi*t))
                d.rectangle((350,y-28,382,y+28),fill=(150,176,185),outline=TEAL,width=2)
                d.line((366,y+28,366,190),fill=GOLD,width=5)
                d.ellipse((353,177,379,203),outline=TEAL,width=3)
            elif idx==5: # learning book page flip + progress
                x=290+int(45*math.sin(2*math.pi*t))
                d.polygon([(285,62),(x,55),(x,174),(285,180)],fill=(19,47,58),outline=TEAL)
                d.polygon([(x,55),(450,62),(450,180),(x,174)],fill=(24,37,50),outline=GOLD)
                d.line((300,193,450,193),fill=(55,75,86),width=5); d.line((300,193,300+int(150*t),193),fill=TEAL,width=5)
            else: # 3D wireframe orbital rotation
                cx,cy=365,112; a=t*2*math.pi
                for k in range(3):
                    r=22+k*20; pts=[]
                    for q in range(48):
                        ang=q*2*math.pi/48+a*(1 if k%2 else -1)
                        pts.append((cx+int(r*math.cos(ang)),cy+int(r*.45*math.sin(ang))))
                    d.line(pts+[pts[0]],fill=TEAL if k%2 else GOLD,width=2)
                d.ellipse((cx-6,cy-6,cx+6,cy+6),fill=WHITE)
            frames.append(im.resize((360,169),Image.Resampling.LANCZOS))
        save(frames,M/f"focus-{idx:02d}-motion-v2.gif",120,32)
def education_motion():
    base=recolor(Image.open(A/"engineering/education-path.jpg")).resize((900,225),Image.Resampling.LANCZOS)
    frames=[]
    for i in range(24):
        im=base.copy(); d=ImageDraw.Draw(im); t=i/23
        d.line((60,195,840,195),fill=(52,76,89),width=3)
        x1=60+int(780*min(1,t*1.4)); x2=60+int(780*max(0,(t-.25)*1.34))
        d.line((60,195,x1,195),fill=TEAL,width=3)
        for x,on in [(60,t>.1),(840,t>.78)]:
            r=8+int(4*(.5+.5*math.sin(i*.35)))
            d.ellipse((x-r,195-r,x+r,195+r),fill=GOLD if on else PANEL,outline=TEAL,width=2)
        frames.append(im.resize((640,160),Image.Resampling.LANCZOS))
    save(frames,M/"education-path-v2.gif",120,32)
def analytics_motion():
    base=recolor(Image.open(A/"data/public-repository-snapshot.jpg")).resize((720,216),Image.Resampling.LANCZOS)
    frames=[]
    for i in range(24):
        im=base.copy(); d=ImageDraw.Draw(im); t=i/23
        # Values remain the dated snapshot; bars/counts animate to those exact values.
        for x,y,w,val,col in [(145,150,70,7,TEAL),(285,150,130,13,GOLD),(425,150,40,4,ICE)]:
            d.rectangle((x,y,x+w,y+8),fill=(25,43,55))
            d.rectangle((x,y,x+int(w*min(1,t*1.5)),y+8),fill=col)
        d.arc((620,24,690,94),start=int(i*9),end=int(i*9+230),fill=TEAL,width=2)
        frames.append(im.resize((640,192),Image.Resampling.LANCZOS))
    save(frames,M/"analytics-data-v2.gif",120,32)
def hero_motion():
    w,h=1200,420; frames=[]
    for i in range(32):
        im=Image.new("RGB",(w,h),BG); d=ImageDraw.Draw(im)
        # Layered graphite blueprint field and restrained teal/brass accents.
        for x in range(0,w,32): d.line((x,0,x,h),fill=(17,34,47),width=1)
        for y in range(0,h,32): d.line((0,y,w,y),fill=(17,34,47),width=1)
        d.line((70,108,600,108),fill=TEAL,width=1); d.line((70,344,600,344),fill=(43,75,87),width=1)
        # Rotor has a continuous, mechanically readable rotation.
        cx,cy=950,210; d.ellipse((cx-145,cy-145,cx+145,cy+145),outline=(50,83,96),width=2)
        d.ellipse((cx-124,cy-124,cx+124,cy+124),outline=TEAL,width=2)
        d.ellipse((cx-78,cy-78,cx+78,cy+78),outline=GOLD,width=3)
        for j in range(8):
            a=2*math.pi*j/8+2*math.pi*i/32; x1=cx+int(96*math.cos(a)); y1=cy+int(96*math.sin(a))
            x2=cx+int(72*math.cos(a)); y2=cy+int(72*math.sin(a))
            d.polygon([(x1,y1),(x1+int(10*math.cos(a+1.57)),y1+int(10*math.sin(a+1.57))),(x2,y2)],fill=TEAL)
        d.ellipse((cx-28,cy-28,cx+28,cy+28),fill=(18,43,54),outline=GOLD,width=2)
        text(d,(70,82),"ENGINEERING / SOFTWARE / SYSTEMS",13,TEAL,True,True)
        text(d,(72,320),"PRECISION · SYSTEMS · PRACTICAL TECHNOLOGY",15,ICE)
        text(d,(72,372),"DHAKA, BANGLADESH",12,TEAL,True,True)
        frames.append(im.resize((840,294),Image.Resampling.LANCZOS))
    save(frames,M/"hero-engineering-v2.gif",120,32)
def recolor_existing_gifs():
    # Convert unused-but-retained motion assets too; nothing is removed from the repository.
    for p in [M/"signal-sweep.gif", M/"focus-pulse.gif", M/"analytics-trace.gif", M/"piston-crankshaft-cycle.gif"]:
        if not p.is_file(): continue
        try:
            im=Image.open(p); frames=[]
            for i in range(im.n_frames):
                im.seek(i); fr=im.convert("RGB"); frames.append(recolor(fr))
            if frames:
                if p.name == "piston-crankshaft-cycle.gif":
                    frames=[fr.resize((640,277),Image.Resampling.LANCZOS) for fr in frames]
                    save(frames,M/"piston-cycle-v2.gif",120,32)
                else:
                    save(frames,p,im.info.get("duration",120),48)
        except Exception as e: print("SKIP_RECOLOR",p.name,str(e))
def render_dividers():
    specs=[("divider-profile-v2.gif","wave"),("divider-projects-v2.gif","orbit"),("divider-focus-v2.gif","nodes"),("divider-analytics-v2.gif","chart"),("divider-footer-v2.gif","rotor")]
    for filename,kind in specs:
        frames=[]; w,h=560,64
        for i in range(36):
            im=Image.new("RGB",(w,h),BG); d=ImageDraw.Draw(im)
            for x in range(0,w,28): d.line((x,0,x,h),fill=(20,39,51),width=1)
            for y in range(0,h,16): d.line((0,y,w,y),fill=(20,39,51),width=1)
            t=2*math.pi*i/36
            if kind=="wave":
                pts=[(x,32+int(12*math.sin(x*.035-t))) for x in range(0,w,4)]
                d.line(pts,fill=TEAL,width=2); x=275+int(80*math.sin(t)); d.ellipse((x-5,27,x+5,37),fill=GOLD)
            elif kind=="orbit":
                cx,cy=280,32; d.ellipse((cx-35,cy-18,cx+35,cy+18),outline=(63,101,112),width=1)
                for j in range(4):
                    a=t+j*math.pi/2; x=cx+int(35*math.cos(a)); y=cy+int(18*math.sin(a))
                    d.ellipse((x-5,y-5,x+5,y+5),fill=GOLD if j==int(i/9)%4 else TEAL)
            elif kind=="nodes":
                pts=[(170,32),(230,12),(280,32),(330,12),(390,32)]
                for a,b in zip(pts,pts[1:]): d.line((a,b),fill=(59,91,104),width=2)
                for j,(x,y) in enumerate(pts):
                    r=4+int(3*(.5+.5*math.sin(t*2+j)))
                    d.ellipse((x-r,y-r,x+r,y+r),fill=GOLD if j==int(i/7)%5 else TEAL)
            elif kind=="chart":
                pts=[(x,48-int(22*(.5+.5*math.sin(x*.03-t)))) for x in range(0,w,5)]
                d.line(pts,fill=TEAL,width=2); x=int((i/36)*w); yy=pts[min(len(pts)-1,int(x/5))][1]
                d.ellipse((x-4,yy-4,x+4,yy+4),fill=GOLD)
            else:
                cx,cy=280,32
                for j in range(3):
                    a=t*(1 if j%2==0 else -1)
                    d.arc((cx-12-j*10,cy-12-j*7,cx+12+j*10,cy+12+j*7),start=int(a*180/math.pi),end=int(a*180/math.pi+260),fill=TEAL if j%2==0 else GOLD,width=2)
            frames.append(im)
        save(frames,M/filename,100,48)

def main():
    recolor_sources()
    unique_project_motion()
    unique_focus_motion()
    education_motion()
    analytics_motion()
    hero_motion()
    title_assets()
    render_dividers()
    recolor_existing_gifs()
    total=sum(p.stat().st_size for p in A.rglob("*") if p.is_file())
    print("TOTAL_ASSETS",total)
    for p in sorted(M.glob("*.gif")): print(p.name,p.stat().st_size)
if __name__=="__main__": main()
