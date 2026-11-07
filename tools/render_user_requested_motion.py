#!/usr/bin/env python3
"""Focused motion derivatives for the five requested README areas."""
from pathlib import Path
import sys, math
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from tools.render_portfolio_art import Mesh,cylinder,torus,rod,norm,cross,dot,vsub
A=ROOT/"assets"; M=A/"motion"; F=A/"focus"; E=A/"engineering"; D=A/"data"; C=A/"cards"
for p in (M,F,E,D,C): p.mkdir(parents=True,exist_ok=True)
RED=(200,16,46); PINK=(255,48,79); WHITE=(245,245,245)

def save_gif(frames,path,delay=180,colors=64):
    q=[im.convert("RGB").quantize(colors=colors,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE) for im in frames]
    q[0].save(path,save_all=True,append_images=q[1:],duration=delay,loop=0,optimize=True,disposal=2)

def scan(src,out,kind,n=24):
    base=Image.open(src).convert("RGB"); w,h=base.size; frames=[]
    for i in range(n):
        im=base.convert("RGBA"); ov=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(ov)
        if kind=="focus":
            x=int(-w*.25+w*1.5*i/n); d.polygon([(x-22,0),(x-8,0),(x+88,h),(x+68,h)],fill=(200,16,46,24)); d.line((x,0,x+76,h),fill=(255,48,79,125),width=2)
            a=int(75+65*(.5+.5*math.sin(2*math.pi*i/n))); d.ellipse((40,80,180,220),outline=(255,48,79,a),width=2)
        elif kind=="education":
            x=int(-80+(w+160)*i/n); d.polygon([(x-24,0),(x-8,0),(x+40,h),(x+18,h)],fill=(200,16,46,22)); d.line((x,0,x+25,h),fill=(255,48,79,105),width=2)
        else:
            x=int(680+500*i/n); d.polygon([(x-30,0),(x-8,0),(x+36,h),(x+12,h)],fill=(200,16,46,22)); d.line((x,0,x+20,h),fill=(255,48,79,110),width=2)
        frames.append(Image.alpha_composite(im,ov).convert("RGB"))
    save_gif(frames,out,180,64)

def footer(path,kicker,title,detail,mark):
    w,h=640,220; im=Image.new("RGB",(w,h),(3,3,3)); d=ImageDraw.Draw(im)
    for x in range(0,w,32): d.line((x,0,x,h),fill=(30,10,14))
    for y in range(0,h,32): d.line((0,y,w,y),fill=(30,10,14))
    d.rounded_rectangle((8,8,w-8,h-8),12,fill=(8,8,8),outline=(65,18,28),width=2); d.rectangle((8,8,w-8,13),fill=RED); d.rectangle((8,8,14,h-8),fill=(143,0,26))
    d.ellipse((34,52,164,182),outline=(143,0,26),width=3); d.ellipse((49,67,149,167),outline=RED,width=1)
    d.line((99,40,99,194),fill=(90,24,38)); d.line((24,117,174,117),fill=(90,24,38))
    d.text((99,117),mark,fill=WHITE,anchor="mm"); d.text((194,42),kicker,fill=PINK); d.text((194,82),title,fill=WHITE)
    d.line((194,126,570,126),fill=(65,18,28)); d.text((194,151),detail,fill=(181,181,181)); d.text((570,188),"SHOVO127 / PROFILE",fill=(119,119,119),anchor="ra")
    im.save(path,"JPEG",quality=90,optimize=True,progressive=True)

def engine_frame(a):
    mesh=Mesh(); cc=-.40; r=.48; L=1.38
    px=r*math.sin(a); pz=cc+r*math.cos(a); pinz=cc+r*math.cos(a)+math.sqrt(L*L-(r*math.sin(a))**2); pc=pinz+.28
    # Open guide rails keep the translating piston visible.
    cylinder(mesh,(-.59,0,.90),.065,2.1,(0,0,1),(83,91,103),28); cylinder(mesh,(.59,0,.90),.065,2.1,(0,0,1),(83,91,103),28)
    torus(mesh,(0,0,1.88),.60,.045,RED); torus(mesh,(0,0,-.12),.60,.045,(105,35,45))
    cylinder(mesh,(0,0,pc),.48,.56,(0,0,1),(139,149,160),48)
    for z in (pc+.17,pc+.08,pc-.01): torus(mesh,(0,0,z),.485,.025,RED)
    cylinder(mesh,(0,0,pc+.285),.44,.055,(0,0,1),(190,198,205),48)
    crank=(px,0,pz); pin=(0,0,pinz); rod(mesh,pin,crank,.23,.20,(108,119,132))
    torus(mesh,pin,.17,.045,RED); torus(mesh,crank,.18,.045,PINK); cylinder(mesh,crank,.13,.58,(0,1,0),(166,174,184),32)
    cylinder(mesh,(0,0,cc),.13,1.75,(1,0,0),(117,130,145),36)
    cylinder(mesh,(-.30,0,cc),.33,.22,(0,1,0),(76,87,101),40); cylinder(mesh,(.30,0,cc),.33,.22,(0,1,0),(76,87,101),40)
    rod(mesh,(-.30,0,cc),crank,.16,.20,(133,143,154)); rod(mesh,(.30,0,cc),crank,.16,.20,(133,143,154))
    for x in (-.86,.86): cylinder(mesh,(x,0,cc),.23,.13,(1,0,0),(173,181,190),40)
    yaw,pitch=34*math.pi/180,22*math.pi/180
    def cam(p):
        x,y,z=p; xr=math.cos(yaw)*x-math.sin(yaw)*y; yr=math.sin(yaw)*x+math.cos(yaw)*y
        return xr,math.cos(pitch)*yr-math.sin(pitch)*z,math.sin(pitch)*yr+math.cos(pitch)*z
    polys=[]; light=norm((-.45,-.65,.75)); specdir=norm((-.25,-.8,.55))
    for face,col in zip(mesh.faces,mesh.colors):
        pts=[cam(mesh.vertices[k]) for k in face]; n=norm(cross(vsub(pts[1],pts[0]),vsub(pts[2],pts[0])))
        lum=max(.18,.34+.66*abs(dot(n,light))); spec=max(0,dot(n,specdir))**18*.26
        c=tuple(min(255,int(v*lum+255*spec)) for v in col); polys.append((sum(p[2] for p in pts)/len(pts),[(830+p[0]*108,260+p[1]*108) for p in pts],c))
    polys.sort(key=lambda z:z[0]); model=Image.new("RGBA",(2400,1040),(0,0,0,0)); md=ImageDraw.Draw(model)
    for _,pts,c in polys: md.polygon([(int(x*2),int(y*2)) for x,y in pts],fill=(*c,255),outline=(50,18,24,255))
    model=model.resize((1200,520),Image.Resampling.LANCZOS)
    base=Image.open(E/"piston-connecting-rod-crankshaft.jpg").convert("RGBA"); d=ImageDraw.Draw(base)
    d.rectangle((560,90,1199,474),fill=(3,3,3,255))
    for x in range(560,1200,40): d.line((x,90,x,474),fill=(30,10,14,255))
    for y in range(90,475,40): d.line((560,y,1199,y),fill=(30,10,14,255))
    d.line((560,88,1156,88),fill=(200,16,46,100)); d.line((560,475,1156,475),fill=(200,16,46,65))
    base.alpha_composite(model); d=ImageDraw.Draw(base)
    d.ellipse((1080,118,1140,178),outline=(90,24,38),width=2); qx=1110+int(24*math.sin(a)); qy=148-int(24*math.cos(a)); d.ellipse((qx-4,qy-4,qx+4,qy+4),fill=(255,82,104))
    return base.convert("RGB").resize((900,390),Image.Resampling.LANCZOS)

def main():
    for i in range(1,7): scan(F/f"focus-{i:02d}.jpg",M/f"focus-{i:02d}-live.gif","focus",18)
    scan(E/"education-path.jpg",M/"education-path-live.gif","education",30)
    scan(D/"public-repository-snapshot.jpg",M/"analytics-snapshot-live.gif","analytics",30)
    footer(C/"footer-engineering.jpg","PROFILE / ENGINEERING","ENGINEERING · SOFTWARE · SYSTEMS","Practical tools, careful implementation.","01")
    footer(C/"footer-location.jpg","INDEPENDENTLY MAINTAINED","DHAKA, BANGLADESH","Designed and maintained independently.","BD")
    save_gif([engine_frame(2*math.pi*i/36) for i in range(36)],M/"piston-crankshaft-cycle.gif",160,96)
    for p in sorted([*M.glob("*-live.gif"),M/"piston-crankshaft-cycle.gif",C/"footer-engineering.jpg",C/"footer-location.jpg"]): print(p.relative_to(ROOT),p.stat().st_size)
    print("TOTAL_ASSETS",sum(p.stat().st_size for p in (A).rglob("*") if p.is_file()))
if __name__=="__main__": main()
