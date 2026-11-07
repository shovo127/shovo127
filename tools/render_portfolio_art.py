#!/usr/bin/env python3
"""Generate self-hosted cyberpunk portfolio artwork using Pillow only.

The project interfaces are stylised visual interpretations of documented public
project behaviour, not screenshots or claims that a mock interface is live.
The mechanical study uses a triangle-mesh renderer with face lighting and depth
sorting. No external image assets or network calls are used.
"""
from pathlib import Path
from math import sin, cos, pi, sqrt
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "assets" / "projects"
ENGINEERING = ROOT / "assets" / "engineering"
MOTION = ROOT / "assets" / "motion"
DATA = ROOT / "assets" / "data"
for folder in (PROJECTS, ENGINEERING, MOTION, DATA):
    folder.mkdir(parents=True, exist_ok=True)

W, H = 1200, 520
TEXT = (242, 245, 250)
MUTED = (165, 176, 192)
DIM = (105, 121, 143)
CYAN = (200, 16, 46)
VIOLET = (143, 0, 26)
MAGENTA = (255, 48, 79)
LIME = (255, 82, 104)
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(size, bold=False, mono=False):
    name = "DejaVuSansMono-Bold.ttf" if mono and bold else "DejaVuSansMono.ttf" if mono else "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = FONT_DIR / name
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def txt(draw, xy, value, size=16, color=TEXT, bold=False, mono=False, anchor=None):
    draw.text(xy, value, font=font(size, bold, mono), fill=color, anchor=anchor)


def rounded(draw, box, radius=12, fill=(11, 15, 22), outline=(37, 51, 68), width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def base_canvas(kicker, accent=CYAN, seed=0):
    im = Image.new("RGB", (W, H), (3, 3, 3))
    p = im.load()
    for y in range(H):
        for x in range(W):
            v = max(0.0, 1 - abs(x - (790 + seed * 13)) / 900)
            p[x, y] = (5 + int(v * 2), 6 + int(v * 4), 9 + int(v * 8))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(0, W, 40):
        d.line((x, 0, x, H), fill=(80, 18, 30, 24), width=1)
    for y in range(0, H, 40):
        d.line((0, y, W, y), fill=(80, 18, 30, 24), width=1)
    d.line((44, 78, 1156, 78), fill=(*accent, 110), width=1)
    d.line((44, 476, 1156, 476), fill=(*accent, 75), width=1)
    d.rectangle((44, 102, 48, 442), fill=(*accent, 230))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((650, 70, 1320, 700), fill=(*accent, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(105))
    im = Image.alpha_composite(im.convert("RGBA"), glow)
    im = Image.alpha_composite(im, overlay)
    d = ImageDraw.Draw(im)
    txt(d, (70, 38), kicker.upper(), 13, accent, True, True)
    txt(d, (1148, 490), "SHOVO127  /  ENGINEERING PORTFOLIO", 10, DIM, False, True, "ra")
    return im


def save(im, name):
    path = PROJECTS / name
    im.convert("RGB").save(path, "JPEG", quality=88, optimize=True, progressive=True, subsampling=1)
    return path


def visa():
    im = base_canvas("01 / browser automation / manifest v3", CYAN, 1)
    d = ImageDraw.Draw(im)
    rounded(d, (82, 105, 1116, 435), 18, (8, 12, 18), (55, 18, 25), 2)
    d.rounded_rectangle((82, 105, 1116, 147), radius=18, fill=(20, 10, 13), outline=(55, 18, 25), width=1)
    d.rectangle((82, 130, 1116, 147), fill=(20, 10, 13))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse((102 + i * 19, 121, 111 + i * 19, 130), fill=c)
    rounded(d, (190, 114, 660, 138), 8, (7, 11, 17), (34, 49, 64))
    txt(d, (210, 120), "chrome-extension://visaflowx/popup.html", 10, DIM, False, True)
    d.rectangle((83, 148, 285, 434), fill=(8, 7, 8))
    txt(d, (105, 169), "VFX / UNIVERSAL", 13, CYAN, True, True)
    for y, label, active in [(207, "Overview", True), (248, "Site profiles", False), (289, "Monitor rules", False), (330, "Scheduler", False), (371, "Activity log", False)]:
        if active:
            rounded(d, (96, y-8, 270, y+23), 7, (48, 8, 18), (150, 10, 35))
        d.ellipse((110, y+1, 117, y+8), fill=CYAN if active else (72, 89, 106))
        txt(d, (128, y-2), label, 13, TEXT if active else MUTED)
    txt(d, (316, 169), "Workflow overview", 22, TEXT, True)
    txt(d, (316, 199), "Profile-driven monitoring · user-controlled actions", 12, MUTED)
    rounded(d, (916, 165, 1088, 198), 8, (45, 8, 18), (145, 12, 35))
    d.ellipse((931, 177, 940, 186), fill=LIME)
    txt(d, (950, 174), "MONITORING", 11, LIME, True, True)
    cards = [("ACTIVE SITE", "IVAC profile", CYAN), ("WORKFLOW", "Monitoring", VIOLET), ("RETRY TIMER", "Backoff ready", MAGENTA)]
    for i, (label, value, accent) in enumerate(cards):
        x = 316 + i * 250
        rounded(d, (x, 220, x+232, 292), 10, (15, 21, 30), (50, 18, 24))
        txt(d, (x+16, 236), label, 10, DIM, True, True)
        txt(d, (x+16, 260), value, 16, TEXT, True)
        d.rectangle((x+16, 282, x+65, 284), fill=accent)
    rounded(d, (316, 308, 820, 415), 10, (13, 19, 27), (50, 18, 24))
    txt(d, (336, 324), "MONITOR RULES", 11, CYAN, True, True)
    for i, (label, detail) in enumerate([("Text appears", "Availability signal"), ("Selector exists", "Target control"), ("Wait / retry", "Backoff with recovery")]):
        y = 352 + i * 21
        d.ellipse((337, y+2, 344, y+9), fill=(64, 198, 177))
        txt(d, (356, y), label, 12, TEXT, True)
        txt(d, (540, y), detail, 11, MUTED)
    rounded(d, (842, 308, 1088, 415), 10, (35, 8, 13), (145, 12, 35))
    txt(d, (862, 325), "HUMAN VERIFICATION", 10, MAGENTA, True, True)
    txt(d, (862, 351), "Detected → wait", 15, TEXT, True)
    txt(d, (862, 376), "Complete protected checks", 10, MUTED)
    txt(d, (862, 393), "manually; no bypass.", 10, MUTED)
    txt(d, (82, 452), "SITE PROFILES  /  DOM OBSERVER  /  RULE ENGINE  /  SCHEDULER", 11, DIM, False, True)
    return save(im, "visaflowx-interface.jpg")


def kostenlos():
    im = base_canvas("02 / multi-model chat / bring your own key", VIOLET, 2)
    d = ImageDraw.Draw(im)
    rounded(d, (82, 105, 1116, 435), 18, (8, 12, 18), (48, 54, 82), 2)
    d.rectangle((83, 106, 284, 434), fill=(11, 15, 23))
    txt(d, (106, 128), "KOSTENLOS", 17, TEXT, True)
    txt(d, (106, 151), "AI WORKSPACE", 10, VIOLET, True, True)
    rounded(d, (100, 177, 266, 212), 8, (20, 28, 40), (52, 64, 85))
    txt(d, (116, 187), "+  New chat", 12, TEXT, True)
    for y, label in [(238, "Recent chats"), (275, "Model routing"), (312, "API keys"), (349, "Settings")]:
        txt(d, (112, y), label, 12, MUTED)
    d.line((285, 106, 285, 434), fill=(42, 52, 69), width=1)
    txt(d, (316, 129), "A conversation, not a provider lock-in.", 18, TEXT, True)
    txt(d, (316, 156), "Your keys stay yours. Routing can fall back when a provider fails.", 11, MUTED)
    rounded(d, (600, 181, 1068, 229), 11, (25, 23, 43), (81, 61, 126))
    txt(d, (620, 195), "Compare the approaches and explain the trade-offs.", 12, TEXT)
    rounded(d, (316, 247, 1068, 337), 11, (14, 22, 30), (43, 58, 74))
    d.ellipse((334, 263, 351, 280), fill=VIOLET)
    txt(d, (362, 260), "Assistant response", 12, TEXT, True)
    txt(d, (362, 286), "The request is routed through the configured provider chain.", 11, MUTED)
    txt(d, (362, 307), "If a provider fails, the service can attempt the next eligible route.", 11, MUTED)
    txt(d, (316, 358), "PROVIDER ROUTING", 10, CYAN, True, True)
    providers = [("GROQ", CYAN), ("GEMINI", VIOLET), ("OPENAI", MAGENTA), ("MISTRAL", LIME)]
    for i, (name, col) in enumerate(providers):
        x = 316 + i * 143
        rounded(d, (x, 378, x+132, 414), 7, (17, 24, 34), (48, 62, 80))
        d.ellipse((328+i*143, 391, 336+i*143, 399), fill=col)
        txt(d, (344+i*143, 387), name, 10, TEXT, True, True)
    txt(d, (82, 452), "REACT  /  TYPESCRIPT  /  APPWRITE AUTH + DATABASE  /  CLOUDFLARE PAGES FUNCTION", 10, DIM, False, True)
    return save(im, "kostenlos-ai-workspace.jpg")


def noti():
    im = base_canvas("03 / android diagnostics / wireless adb", CYAN, 3)
    d = ImageDraw.Draw(im)
    rounded(d, (116, 111, 358, 434), 30, (12, 17, 24), (84, 102, 122), 3)
    rounded(d, (131, 135, 343, 410), 18, (4, 10, 17), (30, 55, 70), 1)
    d.rounded_rectangle((204, 119, 270, 126), radius=4, fill=(55, 69, 84))
    txt(d, (151, 155), "Wireless debugging", 15, TEXT, True)
    txt(d, (151, 182), "Connected to a network", 10, MUTED)
    rounded(d, (148, 205, 326, 254), 8, (13, 29, 39), (0, 105, 126))
    txt(d, (162, 216), "IP address & port", 10, CYAN, True)
    txt(d, (162, 235), "192.168.x.x : 37xxx", 10, TEXT, False, True)
    rounded(d, (148, 267, 326, 319), 8, (14, 20, 29), (43, 58, 73))
    txt(d, (162, 279), "Pair with code", 11, TEXT, True)
    txt(d, (162, 299), "Pairing port is temporary", 9, MUTED)
    d.ellipse((218, 388, 255, 425), outline=(62, 83, 101), width=2)
    rounded(d, (395, 111, 1088, 435), 14, (8, 12, 18), (55, 18, 25), 2)
    d.rectangle((396, 112, 1087, 147), fill=(20, 10, 13))
    txt(d, (420, 124), "ADB SESSION  /  NOTI-FIXER", 11, CYAN, True, True)
    d.ellipse((1040, 124, 1049, 133), fill=LIME)
    txt(d, (1060, 121), "PAIRED", 10, LIME, True, True)
    txt(d, (425, 174), "$ adb pair <device-ip>:<pairing-port>", 13, TEXT, False, True)
    txt(d, (425, 204), "$ adb connect <device-ip>:<connect-port>", 13, TEXT, False, True)
    txt(d, (425, 244), "[scan]  detect_device.py", 12, CYAN, True, True)
    txt(d, (425, 269), "[scan]  audit_fcm_doze.py", 12, CYAN, True, True)
    rounded(d, (422, 298, 1060, 344), 8, (23, 19, 32), (116, 56, 121))
    txt(d, (442, 310), "READ-ONLY DIAGNOSTICS", 11, VIOLET, True, True)
    txt(d, (442, 328), "Review findings before any setting is changed.", 10, MUTED)
    rounded(d, (422, 360, 1060, 410), 8, (13, 35, 30), (45, 115, 83))
    txt(d, (442, 373), "USER APPROVAL REQUIRED", 11, LIME, True, True)
    txt(d, (442, 392), "Back up first · reversible changes · no root", 10, MUTED)
    txt(d, (82, 452), "PYTHON TOOLING  /  ADB  /  READ-ONLY AUDIT  /  CONFIRM BEFORE APPLY", 11, DIM, False, True)
    return save(im, "noti-fixer-diagnostics.jpg")


def circle():
    im = base_canvas("04 / android system integration / native search", MAGENTA, 4)
    d = ImageDraw.Draw(im)
    rounded(d, (130, 112, 430, 430), 36, (13, 18, 27), (77, 91, 117), 3)
    rounded(d, (145, 130, 415, 410), 25, (5, 10, 17), (34, 55, 74), 1)
    d.rounded_rectangle((235, 118, 325, 126), radius=5, fill=(63, 74, 91))
    d.ellipse((190, 175, 380, 365), fill=(14, 35, 51), outline=(0, 107, 130), width=2)
    d.ellipse((223, 206, 347, 330), fill=(24, 28, 52), outline=(111, 69, 163), width=2)
    d.polygon([(210, 345), (275, 240), (350, 345)], fill=(18, 56, 67))
    d.arc((207, 198, 363, 354), start=205, end=510, fill=CYAN, width=5)
    d.line((330, 320, 375, 365), fill=CYAN, width=7)
    d.ellipse((264, 254, 310, 300), outline=(242, 245, 250), width=2)
    txt(d, (280, 378), "DOUBLE BACK TAP", 9, CYAN, True, True, "mm")
    rounded(d, (500, 120, 1088, 426), 16, (9, 14, 22), (49, 62, 82), 2)
    txt(d, (530, 148), "NATIVE GOOGLE CIRCLE TO SEARCH", 12, CYAN, True, True)
    txt(d, (530, 188), "Trigger path", 22, TEXT, True)
    stages = [("01", "HyperOS Back Tap", CYAN), ("02", "Launch transparent activity", VIOLET), ("03", "Voice Interaction Manager", MAGENTA), ("04", "Google native search surface", LIME)]
    for i, (num, label, col) in enumerate(stages):
        y = 230 + i * 42
        rounded(d, (530, y, 1055, y+32), 7, (15, 22, 32), (41, 55, 74))
        txt(d, (548, y+8), num, 10, col, True, True)
        txt(d, (590, y+7), label, 12, TEXT, True)
    txt(d, (530, 404), "Google must be the default assistant; device eligibility still applies.", 10, MUTED)
    txt(d, (82, 452), "ANDROID  /  HYPEROS  /  VIS ENTRY POINT  /  NO OVERLAY OR ACCESSIBILITY SERVICE", 10, DIM, False, True)
    return save(im, "circle-search-native.jpg")


def scanner():
    im = base_canvas("05 / windows scanning platform / architecture concept", VIOLET, 5)
    d = ImageDraw.Draw(im)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((130, 330, 610, 460), fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    im = Image.alpha_composite(im, shadow)
    d = ImageDraw.Draw(im)
    d.polygon([(150, 240), (400, 155), (635, 236), (382, 326)], fill=(34, 45, 61), outline=(109, 127, 149))
    d.polygon([(150, 240), (382, 326), (382, 390), (150, 300)], fill=(15, 22, 31), outline=(69, 86, 106))
    d.polygon([(382, 326), (635, 236), (635, 302), (382, 390)], fill=(22, 31, 43), outline=(77, 94, 114))
    d.polygon([(188, 239), (402, 169), (594, 238), (380, 307)], fill=(7, 14, 22), outline=CYAN)
    d.polygon([(260, 236), (402, 190), (526, 234), (384, 280)], fill=(218, 225, 232), outline=(165, 176, 192))
    for y in (236, 248, 260):
        d.line((293, y, 420, y-42), fill=(108, 125, 146), width=2)
    d.line((202, 246, 382, 309), fill=CYAN, width=3)
    rounded(d, (690, 124, 1090, 420), 13, (9, 14, 22), (55, 65, 88), 2)
    txt(d, (718, 148), "DOCUMENTED ARCHITECTURE", 11, VIOLET, True, True)
    txt(d, (718, 178), "Smart Scanner Pro", 22, TEXT, True)
    modules = [("DOMAIN", "Entities · value objects"), ("APPLICATION", "CQRS · service interfaces"), ("DRIVERS", "TWAIN · WIA · eSCL planned"), ("PROCESSING", "Image · OCR · PDF planned"), ("DESKTOP UI", "WPF · MVVM")]
    for i, (a, b) in enumerate(modules):
        y = 218 + i * 37
        d.rectangle((718, y, 724, y+22), fill=CYAN if i in (0, 1) else VIOLET)
        txt(d, (738, y), a, 9, DIM, True, True)
        txt(d, (850, y-1), b, 10, TEXT)
    rounded(d, (718, 397, 1060, 417), 5, (37, 25, 45), (119, 61, 125))
    txt(d, (889, 401), "PLANNED / ARCHITECTURE", 9, MAGENTA, True, True, "mm")
    txt(d, (82, 452), "WINDOWS  /  .NET 9  /  WPF  /  FEATURE IMPLEMENTATION STATUS: PLANNED", 11, DIM, False, True)
    return save(im, "smart-scanner-architecture.jpg")


def vadd(a, b): return tuple(x+y for x, y in zip(a, b))
def vsub(a, b): return tuple(x-y for x, y in zip(a, b))
def vmul(a, s): return tuple(x*s for x in a)
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a):
    n = sqrt(dot(a, a)) or 1
    return tuple(x/n for x in a)


class Mesh:
    def __init__(self):
        self.vertices, self.faces, self.colors = [], [], []

    def add(self, vertices, faces, color):
        off = len(self.vertices)
        self.vertices.extend(vertices)
        for face in faces:
            self.faces.append(tuple(off+i for i in face))
            self.colors.append(color)


def cylinder(mesh, center, radius, length, axis=(0, 0, 1), color=(120, 145, 164), segments=56):
    axis = norm(axis)
    helper = (0, 1, 0) if abs(axis[1]) < .9 else (1, 0, 0)
    u, v = norm(cross(axis, helper)), norm(cross(axis, norm(cross(axis, helper))))
    verts = []
    for side in (-.5, .5):
        for i in range(segments):
            a = 2*pi*i/segments
            p = vadd(vadd(center, vmul(axis, side*length)), vadd(vmul(u, radius*cos(a)), vmul(v, radius*sin(a))))
            verts.append(p)
    faces = []
    for i in range(segments):
        j = (i+1) % segments
        faces.append((i, j, segments+j, segments+i))
    faces.extend([tuple(reversed(range(segments))), tuple(range(segments, 2*segments))])
    mesh.add(verts, faces, color)


def torus(mesh, center, major, minor, color=(0, 210, 240), axis=(0, 0, 1), seg1=72, seg2=12):
    axis = norm(axis)
    helper = (0, 1, 0) if abs(axis[1]) < .9 else (1, 0, 0)
    u = norm(cross(axis, helper))
    v = norm(cross(axis, u))
    verts = []
    for i in range(seg1):
        a = 2*pi*i/seg1
        radial = vadd(vmul(u, cos(a)), vmul(v, sin(a)))
        for j in range(seg2):
            b = 2*pi*j/seg2
            verts.append(vadd(center, vadd(vmul(radial, major+minor*cos(b)), vmul(axis, minor*sin(b)))))
    faces = []
    for i in range(seg1):
        for j in range(seg2):
            i2, j2 = (i+1) % seg1, (j+1) % seg2
            faces.append((i*seg2+j, i2*seg2+j, i2*seg2+j2, i*seg2+j2))
    mesh.add(verts, faces, color)


def sphere(mesh, center, radius, color=(140, 155, 170), seg1=36, seg2=18):
    verts, faces = [], []
    for j in range(seg2+1):
        phi = pi*j/seg2
        for i in range(seg1):
            theta = 2*pi*i/seg1
            verts.append((center[0]+radius*sin(phi)*cos(theta), center[1]+radius*sin(phi)*sin(theta), center[2]+radius*cos(phi)))
    for j in range(seg2):
        for i in range(seg1):
            i2 = (i+1) % seg1
            faces.append((j*seg1+i, j*seg1+i2, (j+1)*seg1+i2, (j+1)*seg1+i))
    mesh.add(verts, faces, color)


def rod(mesh, start, end, width, depth, color=(95, 120, 142)):
    axis = norm(vsub(end, start))
    helper = (0, 1, 0) if abs(axis[1]) < .9 else (1, 0, 0)
    u, v = norm(cross(axis, helper)), norm(cross(axis, norm(cross(axis, helper))))
    verts = []
    for pt in (start, end):
        for su, sv in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            verts.append(vadd(pt, vadd(vmul(u, su*width/2), vmul(v, sv*depth/2))))
    faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    mesh.add(verts, faces, color)


def render_engine():
    mesh = Mesh()
    cylinder(mesh, (0, 0, 1.20), .70, 1.02, (0, 0, 1), (112, 133, 153))
    cylinder(mesh, (0, 0, 1.77), .75, .26, (0, 0, 1), (166, 178, 190))
    for z in (1.36, 1.48, 1.60):
        torus(mesh, (0, 0, z), .705, .025, (0, 205, 240))
    torus(mesh, (0, 0, 1.91), .59, .035, (175, 190, 204))
    cylinder(mesh, (0, 0, 1.12), .18, 1.55, (1, 0, 0), (73, 91, 110))
    cylinder(mesh, (-.57, 0, 1.12), .25, .22, (1, 0, 0), (147, 162, 177))
    cylinder(mesh, (.57, 0, 1.12), .25, .22, (1, 0, 0), (147, 162, 177))
    rod(mesh, (0, 0, .92), (.10, 0, -1.13), .26, .24, (86, 108, 130))
    torus(mesh, (0, 0, .92), .23, .055, (0, 205, 240))
    torus(mesh, (.10, 0, -1.13), .38, .07, (0, 205, 240))
    cylinder(mesh, (.10, 0, -1.13), .30, .50, (0, 1, 0), (102, 121, 141))
    sphere(mesh, (.10, 0, -1.13), .18, (151, 165, 178))
    cylinder(mesh, (-.40, 0, -1.58), .48, .25, (0, 1, 0), (65, 82, 101))
    cylinder(mesh, (.55, 0, -1.58), .48, .25, (0, 1, 0), (65, 82, 101))
    cylinder(mesh, (0, 0, -1.84), .22, 2.10, (1, 0, 0), (131, 148, 164))
    cylinder(mesh, (.10, 0, -1.13), .19, 1.30, (1, 0, 0), (178, 188, 198))
    for x in (-.90, .90):
        cylinder(mesh, (x, 0, -1.84), .29, .17, (1, 0, 0), (175, 187, 199))
    yaw, pitch = 34*pi/180, 22*pi/180

    def camera(p):
        x, y, z = p
        xr = cos(yaw)*x - sin(yaw)*y
        yr = sin(yaw)*x + cos(yaw)*y
        yr2 = cos(pitch)*yr - sin(pitch)*z
        depth = sin(pitch)*yr + cos(pitch)*z
        return xr, yr2, depth

    projected = []
    light = norm((-.45, -.65, .75))
    for face, color in zip(mesh.faces, mesh.colors):
        pts = [camera(mesh.vertices[i]) for i in face]
        n = norm(cross(vsub(pts[1], pts[0]), vsub(pts[2], pts[0])))
        lum = max(.16, .30 + .70*abs(dot(n, light)))
        spec = max(0, dot(n, norm((-.25, -.8, .55))))**18*.32
        col = tuple(min(255, int(c*lum+255*spec)) for c in color)
        depth = sum(p[2] for p in pts)/len(pts)
        projected.append((depth, [(830+p[0]*108, 260+p[1]*108) for p in pts], col))
    projected.sort(key=lambda q: q[0])
    scale = 2
    im = Image.new("RGBA", (W*scale, H*scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _, pts, col in projected:
        d.polygon([(int(x*scale), int(y*scale)) for x, y in pts], fill=(*col, 255), outline=(35, 58, 75, 255))
    im = im.resize((W, H), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (W, H), (5, 7, 11, 255))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((580, 90, 1180, 500), fill=(0, 160, 220, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(75))
    canvas = Image.alpha_composite(canvas, glow)
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 40): gd.line((x, 0, x, H), fill=(29, 55, 73, 30), width=1)
    for y in range(0, H, 40): gd.line((0, y, W, y), fill=(29, 55, 73, 30), width=1)
    gd.line((44, 88, 1156, 88), fill=(0, 229, 255, 100), width=1)
    gd.line((44, 475, 1156, 475), fill=(0, 229, 255, 65), width=1)
    canvas = Image.alpha_composite(canvas, grid)
    canvas.alpha_composite(im, (0, 0))
    d = ImageDraw.Draw(canvas)
    txt(d, (70, 39), "ENGINEERING / MECHANICAL SYSTEMS", 13, CYAN, True, True)
    txt(d, (70, 145), "PRECISION", 48, TEXT, True)
    txt(d, (70, 203), "IN MOTION.", 48, TEXT, True)
    txt(d, (72, 280), "Piston · connecting rod · crankshaft", 17, MUTED)
    txt(d, (72, 312), "Original 3D mesh study · metallic materials", 13, DIM)
    d.rectangle((70, 370, 73, 430), fill=LIME)
    txt(d, (88, 374), "AUTOMOTIVE ENGINEERING", 12, LIME, True, True)
    txt(d, (72, 449), "RENDERED FROM PARAMETRIC GEOMETRY", 10, DIM, False, True)
    path = ENGINEERING / "piston-connecting-rod-crankshaft.jpg"
    canvas.convert("RGB").save(path, "JPEG", quality=90, optimize=True, progressive=True, subsampling=1)
    return path


def render_focus():
    im = Image.new("RGB", (1200, 360), (3, 3, 3))
    d = ImageDraw.Draw(im)
    for x in range(0, 1200, 40): d.line((x, 0, x, 360), fill=(55, 15, 24), width=1)
    for y in range(0, 360, 40): d.line((0, y, 1200, y), fill=(55, 15, 24), width=1)
    txt(d, (48, 28), "TECHNICAL FOCUS / FIVE CONNECTED DISCIPLINES", 13, CYAN, True, True)
    items = [
        ("01", "SOFTWARE", "Web apps · browser extensions", CYAN, "</>"),
        ("02", "AI + AUTOMATION", "Provider routing · workflow rules", VIOLET, "AI"),
        ("03", "ANDROID SYSTEMS", "ADB · HyperOS · diagnostics", MAGENTA, "ADB"),
        ("04", "AUTOMOTIVE", "Mechanical systems · diagnostics", LIME, "ENG"),
        ("05", "LEARNING TECH", "Multilingual · German learning", (181, 181, 181), "DE"),
    ]
    for i, (num, title, desc, col, mark) in enumerate(items):
        x, y = 48+i*224, 84
        d.rounded_rectangle((x, y, x+202, y+224), radius=10, fill=(12, 8, 9), outline=(50, 18, 24), width=1)
        d.rectangle((x, y, x+202, y+3), fill=col)
        txt(d, (x+16, y+18), num, 10, col, True, True)
        d.ellipse((x+16, y+50, x+66, y+100), outline=col, width=2)
        txt(d, (x+41, y+75), mark, 13, TEXT, True, True, "mm")
        txt(d, (x+16, y+124), title, 12, TEXT, True, True)
        if "browser" in desc: lines = ("Web apps · browser", "extensions")
        elif "workflow" in desc: lines = ("Provider routing ·", "workflow rules")
        elif "HyperOS" in desc: lines = ("ADB · HyperOS ·", "device diagnostics")
        elif "Mechanical" in desc: lines = ("Mechanical systems ·", "diagnostics")
        else: lines = ("Multilingual · German", "learning experiences")
        txt(d, (x+16, y+158), lines[0], 9, MUTED)
        txt(d, (x+16, y+176), lines[1], 9, MUTED)
        d.line((x+16, y+207, x+70, y+207), fill=col, width=2)
    path = ENGINEERING / "technical-focus.jpg"
    im.save(path, "JPEG", quality=88, optimize=True, progressive=True, subsampling=1)
    return path


def render_education():
    im = Image.new("RGB", (1200, 300), (3, 3, 3))
    d = ImageDraw.Draw(im)
    for x in range(0, 1200, 40): d.line((x, 0, x, 300), fill=(55, 15, 24), width=1)
    for y in range(0, 300, 40): d.line((0, y, 1200, y), fill=(55, 15, 24), width=1)
    txt(d, (48, 26), "EDUCATION / CONTINUOUS LEARNING", 13, CYAN, True, True)
    panels = [(48, "01 / COMPLETED", "DIPLOMA IN AUTOMOBILE ENGINEERING", "Dhaka Polytechnic Institute", CYAN),
              (618, "02 / CURRENT", "TELC DEUTSCH B2", "German language preparation", VIOLET)]
    for x, kicker, title, detail, col in panels:
        d.rounded_rectangle((x, 76, x+534, 258), radius=12, fill=(12, 8, 9), outline=(50, 18, 24), width=1)
        d.rectangle((x, 76, x+4, 258), fill=col)
        txt(d, (x+24, 98), kicker, 10, col, True, True)
        txt(d, (x+24, 139), title, 19, TEXT, True)
        txt(d, (x+24, 178), detail, 13, MUTED)
        d.line((x+24, 222, x+112, 222), fill=col, width=2)
    path = ENGINEERING / "education-path.jpg"
    im.save(path, "JPEG", quality=88, optimize=True, progressive=True, subsampling=1)
    return path


SNAPSHOT = {
    "as_of": "2026-11-07",
    "source": "GitHub REST API: public owner repositories and repository metadata",
    "scope": "Seven public project repositories; excludes the profile repository and all private repositories.",
    "repositories": 7, "stars": 13, "forks": 4,
    "primary_languages": {"JavaScript": 2, "TypeScript": 2, "C#": 1, "PowerShell": 1, "Python": 1},
    "repositories_detail": [
        {"name": "visaflowx", "language": "JavaScript", "stars": 0, "forks": 1},
        {"name": "visaflowx-universal", "language": "JavaScript", "stars": 0, "forks": 0},
        {"name": "kostenlos-ai", "language": "TypeScript", "stars": 0, "forks": 0},
        {"name": "Smart-Scanner-Pro", "language": "C#", "stars": 0, "forks": 0},
        {"name": "IPTV-By-Shovo", "language": "TypeScript", "stars": 12, "forks": 3},
        {"name": "Circle-to-Search-for-Xiaomi", "language": "PowerShell", "stars": 0, "forks": 0},
        {"name": "Noti-Fixer-for-Chinese-Devices", "language": "Python", "stars": 1, "forks": 0},
    ],
}


def render_analytics():
    (DATA / "public-repositories.json").write_text(json.dumps(SNAPSHOT, indent=2)+"\n", encoding="utf-8")
    im = Image.new("RGB", (1200, 360), (3, 3, 3))
    d = ImageDraw.Draw(im)
    for x in range(0, 1200, 40): d.line((x, 0, x, 360), fill=(55, 15, 24), width=1)
    for y in range(0, 360, 40): d.line((0, y, 1200, y), fill=(55, 15, 24), width=1)
    txt(d, (48, 32), "PUBLIC REPOSITORY SNAPSHOT", 14, CYAN, True, True)
    txt(d, (48, 69), "7", 48, TEXT, True); txt(d, (48, 124), "PUBLIC PROJECT REPOS", 10, MUTED, True, True)
    txt(d, (280, 69), "13", 48, TEXT, True); txt(d, (280, 124), "STARS", 10, MUTED, True, True)
    txt(d, (480, 69), "4", 48, TEXT, True); txt(d, (480, 124), "FORKS", 10, MUTED, True, True)
    d.line((680, 30, 680, 320), fill=(75, 24, 34), width=1)
    txt(d, (720, 34), "PRIMARY LANGUAGE BY REPOSITORY", 12, VIOLET, True, True)
    langs = list(SNAPSHOT["primary_languages"].items())
    colors = [CYAN, VIOLET, MAGENTA, LIME, (181, 181, 181)]
    y = 82
    for (name, count), color in zip(langs, colors):
        txt(d, (720, y), name, 12, TEXT, True)
        d.rounded_rectangle((860, y+1, 1095, y+15), radius=6, fill=(35, 12, 17))
        d.rounded_rectangle((860, y+1, 860+235*count/2, y+15), radius=6, fill=color)
        txt(d, (1120, y), str(count), 11, MUTED, False, True, "ra")
        y += 42
    txt(d, (48, 205), "A dated public-data snapshot, not a live counter.", 14, MUTED)
    txt(d, (48, 236), "Language labels describe each repository's primary language — not skill or proficiency.", 11, DIM)
    txt(d, (48, 307), "SOURCE: GITHUB REST API  /  2026-11-07", 10, DIM, False, True)
    path = DATA / "public-repository-snapshot.jpg"
    im.save(path, "JPEG", quality=88, optimize=True, progressive=True, subsampling=1)
    return path


def render_motion():
    frames = []
    fw, fh = 560, 84
    for i in range(36):
        im = Image.new("RGB", (fw, fh), (3, 3, 3))
        d = ImageDraw.Draw(im)
        for x in range(0, fw, 32): d.line((x, 0, x, fh), fill=(55, 15, 24), width=1)
        for y in range(0, fh, 21): d.line((0, y, fw, y), fill=(55, 15, 24), width=1)
        d.line((0, fh//2, fw, fh//2), fill=(90, 24, 38), width=1)
        cx = int(i*fw/36)
        glow = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.polygon([(cx-30, 0), (cx-5, 0), (cx+30, fh), (cx+5, fh)], fill=(200, 16, 46, 45))
        gd.line((cx, 0, cx+30, fh), fill=(255, 48, 79, 190), width=2)
        if cx < 40: gd.line((cx+fw, 0, cx+fw+30, fh), fill=(255, 48, 79, 55), width=1)
        elif cx > fw-40: gd.line((cx-fw, 0, cx-fw+30, fh), fill=(255, 48, 79, 55), width=1)
        glow = glow.filter(ImageFilter.GaussianBlur(4))
        im = Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB")
        d = ImageDraw.Draw(im)
        txt(d, (18, 12), "SYSTEMS / ENGINEERING", 11, CYAN, True, True)
        txt(d, (18, 43), "SIGNAL PATH", 16, TEXT, True)
        txt(d, (fw-18, 15), "LIVE TRACE / 01", 9, MUTED, False, True, "ra")
        txt(d, (fw-18, 48), "MONITOR → VERIFY → ACT", 9, MUTED, False, True, "ra")
        frames.append(im.quantize(colors=32, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE))
    path = MOTION / "signal-sweep.gif"
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=160, loop=0, optimize=True, disposal=2)
    return path



def render_focus_cards():
    items = [
        ("01", "SOFTWARE ENGINEERING", "Web applications · browser extensions", "API", "STRUCTURE / SYSTEMS"),
        ("02", "AI & AUTOMATION", "Provider routing · workflow rules", "AI", "ROUTING / FAILOVER"),
        ("03", "ANDROID SYSTEMS", "ADB · HyperOS · notification diagnostics", "ADB", "DEVICE / CONTROL"),
        ("04", "AUTOMOTIVE ENGINEERING", "Mechanical systems · diagnostic thinking", "ENG", "MECHANICAL / TEST"),
        ("05", "LEARNING TECHNOLOGY", "Multilingual tools · German learning", "DE", "LEARN / BUILD"),
        ("06", "MECHANICAL VISUALISATION", "Parametric geometry · assembly studies", "3D", "MODEL / RENDER"),
    ]
    for num, title, desc, mark, foot in items:
        im = Image.new("RGB", (640, 300), (3, 3, 3))
        d = ImageDraw.Draw(im)
        for x in range(0, 640, 32): d.line((x,0,x,300), fill=(30,10,14), width=1)
        for y in range(0, 300, 32): d.line((0,y,640,y), fill=(30,10,14), width=1)
        d.rounded_rectangle((10,10,630,290), radius=12, fill=(8,8,8), outline=(65,18,28), width=2)
        d.rectangle((10,10,630,14), fill=(200,16,46))
        d.rectangle((10,10,15,290), fill=(143,0,26))
        txt(d,(34,32),num+" / SHOVO127",12,(255,48,79),True,True)
        d.ellipse((40,80,180,220), outline=(143,0,26), width=3)
        d.ellipse((58,98,162,202), outline=(200,16,46), width=1)
        d.line((110,68,110,232), fill=(90,24,38), width=2)
        d.line((28,150,192,150), fill=(90,24,38), width=2)
        txt(d,(110,150),mark,22,(245,245,245),True,True,"mm")
        txt(d,(220,95),title,20,(245,245,245),True,True)
        txt(d,(220,137),desc,13,(181,181,181))
        d.line((220,180,570,180), fill=(65,18,28), width=1)
        txt(d,(220,202),foot,11,(255,82,104),True,True)
        txt(d,(590,258),"ENGINEERING / "+num,9,(119,119,119),False,True,"ra")
        out = ROOT/"assets"/"focus"/("focus-"+num+".jpg")
        out.parent.mkdir(parents=True,exist_ok=True)
        im.save(out,"JPEG",quality=88,optimize=True,progressive=True,subsampling=1)

def render_iptv():
    im = base_canvas("06 / PUBLIC PLAYLIST MAINTENANCE / M3U + M3U8", CYAN, 6)
    d = ImageDraw.Draw(im)
    rounded(d,(90,110,1110,420),16,(8,8,8),(65,18,28),2)
    txt(d,(125,142),"PLAYLIST INDEX",15,TEXT,True,True)
    rows=[("SPORTS","M3U8 / PUBLIC SOURCE"),("NEWS","REGIONAL CHANNEL INDEX"),("ENTERTAINMENT","PLAYER-COMPATIBLE PLAYLIST"),("EPG","EXTERNAL PROGRAMME DATA")]
    for i,(a,b) in enumerate(rows):
        y=195+i*48
        d.rectangle((126,y,132,y+25),fill=CYAN)
        txt(d,(150,y+2),a,14,TEXT,True,True)
        txt(d,(430,y+4),b,12,MUTED,False,True)
    txt(d,(126,390),"LINK COLLECTION ONLY  /  THIRD-PARTY STREAMS",11,(255,82,104),True,True)
    return save(im,"iptv-by-shovo.jpg")

def render_project_motion():
    names=["visaflowx-interface","kostenlos-ai-workspace","noti-fixer-diagnostics","circle-search-native","smart-scanner-architecture","iptv-by-shovo"]
    for idx,name in enumerate(names):
        source=PROJECTS/(name+".jpg")
        if not source.exists(): continue
        base=Image.open(source).convert("RGB").resize((480,208),Image.Resampling.LANCZOS)
        frames=[]
        for i in range(18):
            frame=base.copy()
            d=ImageDraw.Draw(frame)
            x=int(i*480/18)
            d.polygon([(x-13,0),(x-7,0),(x+16,208),(x+10,208)],fill=(200,16,46))
            d.line((x,0,x+22,208),fill=(255,82,104),width=2)
            d.rectangle((0,0,600,4),fill=(143,0,26))
            frames.append(frame.quantize(colors=32,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE))
        out=MOTION/("project-"+str(idx+1).zfill(2)+"-scan.gif")
        frames[0].save(out,save_all=True,append_images=frames[1:],duration=160,loop=0,optimize=True,disposal=2)



def render_aux_motion():
    for name, mode in [("focus-pulse.gif","focus"),("analytics-trace.gif","analytics")]:
        frames=[]
        fw,fh=560,84
        for i in range(36):
            im=Image.new("RGB",(fw,fh),(3,3,3))
            d=ImageDraw.Draw(im)
            for x in range(0,fw,32): d.line((x,0,x,fh),fill=(34,10,15),width=1)
            for y in range(0,fh,21): d.line((0,y,fw,y),fill=(34,10,15),width=1)
            if mode=="focus":
                cx=int((1+sin(2*pi*i/36))*0.5*(fw-40))+20
                d.ellipse((cx-19,23,cx+19,61),outline=(143,0,26),width=2)
                d.ellipse((cx-9,33,cx+9,51),fill=(200,16,46))
                txt(d,(18,12),"FOCUS / SIGNAL STATUS",11,(255,48,79),True,True)
                txt(d,(18,44),"DISCIPLINE TRACE",15,(245,245,245),True)
            else:
                txt(d,(18,12),"PUBLIC DATA / SNAPSHOT",11,(255,48,79),True,True)
                txt(d,(18,44),"REPOSITORY METRICS",15,(245,245,245),True)
                x=int(i*fw/36)
                d.line((0,70,x,70),fill=(143,0,26),width=2)
                d.ellipse((x-4,66,x+4,74),fill=(255,82,104))
            txt(d,(fw-18,15),"STATIC VALUES / RED TRACE",9,(181,181,181),False,True,"ra")
            frames.append(im.quantize(colors=32,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE))
        out=MOTION/name
        frames[0].save(out,save_all=True,append_images=frames[1:],duration=160,loop=0,optimize=True,disposal=2)


def main():
    created = [visa(), kostenlos(), noti(), circle(), scanner(), render_iptv(), render_engine(),
               render_focus(), render_focus_cards(), render_education(), render_analytics(), render_motion(), render_project_motion(), render_aux_motion()]
    for path in created:
        if path is not None:
            print(f"{path.relative_to(ROOT)}\t{path.stat().st_size}")
    total = sum(p.stat().st_size for p in (ROOT / "assets").rglob("*") if p.is_file())
    print(f"TOTAL_GENERATED_BYTES\t{total}")


if __name__ == "__main__":
    main()
