#!/usr/bin/env python3
"""Render a data-driven, non-interactive contribution-calendar snake GIF."""
from __future__ import annotations

import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DATA = Path("assets/contribution-calendar.json")
OUTPUT = Path("assets/contribution-snake-live.gif")
WIDTH, HEIGHT = 800, 280
CELL, GAP = 7, 3
STEP = CELL + GAP
GRID_X, GRID_Y = 140, 150
INITIAL_LENGTH = 5
ADVANCE_PER_FRAME = 6
DURATION_MS = 100
PALETTE = ["#1B2A38", "#155A54", "#1C8276", "#28AE9B", "#55D8C2"]
GOLD = "#F7C66A"
BODY = "#0F887B"
BODY_HIGHLIGHT = "#72E8CF"
HEAD = "#5CE1C1"
INK = "#071321"
TEXT = "#E8F2FA"
MUTED = "#A8BED0"


def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(21, True)
FONT_LABEL = font(10, True)
FONT_SMALL = font(9)


def base_calendar(data: dict) -> tuple[Image.Image, dict, list, dict]:
    weeks = data.get("weeks", [])
    days = data.get("days", [])
    week_count = max(1, len(weeks))
    counts = {(int(d["week"]), int(d["weekday"])): int(d["count"]) for d in days}
    dates = {(int(d["week"]), int(d["weekday"])): d["date"] for d in days}
    max_count = max(counts.values(), default=0)
    image = Image.new("RGB", (WIDTH, HEIGHT), INK)
    pixels = image.load()
    for y in range(HEIGHT):
        t = y / max(1, HEIGHT - 1)
        col = (int(7 + 8*t), int(19 + 14*t), int(33 + 22*t))
        for x in range(WIDTH):
            pixels[x, y] = col
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((18, 14, WIDTH-18, HEIGHT-14), radius=22, outline=(105,151,177,50), width=1)
    draw.text((40, 30), "CONTRIBUTION SNAKE", font=FONT_LABEL, fill="#5EEAD4")
    draw.text((40, 53), "A moving path through real GitHub activity", font=FONT_TITLE, fill=TEXT)
    total = data.get("total_contributions")
    if total is not None:
        subtitle = f"{int(total):,} contributions  ·  {data.get('period_start','')} — {data.get('period_end','')}"
    else:
        subtitle = "Contribution data unavailable — neutral empty state"
    draw.text((42, 82), subtitle, font=FONT_SMALL, fill=MUTED)

    # Month labels are derived from actual dates in the returned contribution grid.
    seen_months = set()
    for (week, weekday), date in sorted(dates.items()):
        month = date[:7]
        if month not in seen_months:
            seen_months.add(month)
            x = GRID_X + week * STEP
            draw.text((x, GRID_Y-27), date[5:7], font=FONT_SMALL, fill="#AFC4D8")

    for week in range(week_count):
        for weekday in range(7):
            x = GRID_X + week * STEP
            y = GRID_Y + weekday * STEP
            count = counts.get((week, weekday), 0)
            if count <= 0 or max_count <= 0:
                level = 0
            else:
                level = min(4, math.ceil(count * 4 / max_count))
            color = PALETTE[level]
            draw.rounded_rectangle((x, y, x+CELL, y+CELL), radius=3, fill=color, outline=(159,190,208,35), width=1)
            if count > 0:
                # A small inset glint makes active calendar cells readable at profile size.
                draw.ellipse((x+3, y+3, x+5, y+5), fill=(220,255,247,150))

    draw.text((42, 242), "Food markers = days with recorded contributions  ·  Snake grows when it reaches an active day", font=FONT_SMALL, fill=MUTED)
    draw.text((42, 258), "Data source: GitHub GraphQL contributionCalendar  ·  GIF animation, not a playable game", font=FONT_SMALL, fill="#7F9AAF")
    return image, counts, dates, {"weeks": week_count, "max_count": max_count}


def build_path(weeks: int, dates: dict) -> list[tuple[int, int]]:
    path = []
    for week in range(weeks):
        rows = range(7) if week % 2 == 0 else range(6, -1, -1)
        for weekday in rows:
            if (week, weekday) in dates:
                path.append((week, weekday))
    for previous, current in zip(path, path[1:]):
        distance = abs(previous[0]-current[0]) + abs(previous[1]-current[1])
        if distance != 1:
            raise ValueError(f"Contribution path is not continuous: {previous} -> {current}")
    if len(set(path)) != len(path):
        raise ValueError("Contribution path contains a collision.")
    return path


def draw_frame(base: Image.Image, path: list[tuple[int, int]], counts: dict, head_index: int, alpha: int) -> Image.Image:
    overlay = Image.new("RGBA", base.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    active = {i for i, pos in enumerate(path) if counts.get(pos, 0) > 0}

    # Uncollected food sits exactly on days with real contribution counts.
    for index in active:
        if index <= head_index:
            continue
        week, weekday = path[index]
        cx = GRID_X + week*STEP + CELL//2
        cy = GRID_Y + weekday*STEP + CELL//2
        count = counts.get((week,weekday), 0)
        radius = 1.8 + min(1.8, math.log2(count+1)*.35)
        draw.ellipse((cx-radius-3,cy-radius-3,cx+radius+3,cy+radius+3), fill=(247,198,106,35))
        draw.ellipse((cx-radius,cy-radius,cx+radius,cy+radius), fill=(247,198,106,alpha), outline=(255,235,187,alpha), width=1)

    growth = sum(1 for index in active if index <= head_index)
    length = min(len(path), INITIAL_LENGTH + growth)
    body_indices = list(range(max(0, head_index-length+1), head_index+1))
    points = []
    for index in body_indices:
        week, weekday = path[index]
        points.append((GRID_X + week*STEP + CELL//2, GRID_Y + weekday*STEP + CELL//2))

    if points:
        # Draw a dark outline first, then a teal inner body with bright dorsal highlights.
        if len(points) > 1:
            draw.line(points, fill=(3,35,42,alpha), width=8, joint="curve")
            draw.line(points, fill=(15,136,123,alpha), width=6, joint="curve")
            draw.line(points, fill=(114,232,207,alpha//2), width=1, joint="curve")
        for i, (cx,cy) in enumerate(points[:-1]):
            radius = 3.0
            draw.ellipse((cx-radius,cy-radius,cx+radius,cy+radius), fill=(15,136,123,alpha), outline=(3,35,42,alpha), width=1)
            if i % 3 == 0:
                draw.ellipse((cx-1.8,cy-2.7,cx+.2,cy-.7), fill=(183,255,239,alpha//2))

        hx,hy = points[-1]
        previous = points[-2] if len(points)>1 else (hx-1,hy)
        dx,dy = hx-previous[0],hy-previous[1]
        magnitude = max(1, math.hypot(dx,dy))
        dx,dy = dx/magnitude,dy/magnitude
        px,py = -dy,dx
        radius = 5.2
        draw.ellipse((hx-radius-2,hy-radius-2,hx+radius+2,hy+radius+2), fill=(3,35,42,alpha))
        draw.ellipse((hx-radius,hy-radius,hx+radius,hy+radius), fill=(92,225,193,alpha), outline=(183,255,239,alpha), width=1)
        for sign in (-1,1):
            ex = hx + dx*1.8 + px*sign*2.5
            ey = hy + dy*1.8 + py*sign*2.5
            draw.ellipse((ex-2,ey-2,ex+2,ey+2), fill=(255,255,255,alpha))
            draw.ellipse((ex-.8,ey-.8,ex+.8,ey+.8), fill=(7,19,33,alpha))
        tx,ty = hx + dx*10, hy + dy*10
        draw.line((hx+dx*6,hy+dy*6,tx,ty), fill=(255,117,128,alpha), width=2)

    return Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")


def make_unavailable(base: Image.Image) -> list[Image.Image]:
    # No snake or food is fabricated when GitHub contribution data is unavailable.
    return [base.copy(), base.copy()]


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    base, counts, dates, meta = base_calendar(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    if data.get("status") != "available" or not dates:
        frames = make_unavailable(base)
    else:
        path = build_path(meta["weeks"], dates)
        if not path:
            frames = make_unavailable(base)
        else:
            active_indices = {i for i,pos in enumerate(path) if counts.get(pos,0)>0}
            positions = list(range(INITIAL_LENGTH-1, len(path), ADVANCE_PER_FRAME))
            if positions[-1] != len(path)-1:
                positions.append(len(path)-1)
            frames = [draw_frame(base,path,counts,positions[0],0),
                      draw_frame(base,path,counts,positions[0],90),
                      draw_frame(base,path,counts,positions[0],180)]
            frames.extend(draw_frame(base,path,counts,index,255) for index in positions[1:])
            last = positions[-1]
            frames.extend([draw_frame(base,path,counts,last,180),
                           draw_frame(base,path,counts,last,90),
                           draw_frame(base,path,counts,last,0)])
            print(f"Contribution snake: {len(path)} calendar cells, {len(active_indices)} food cells, {len(frames)} frames.")

    # One shared palette prevents flicker between the many moving frames.
    sample_w, sample_h = 128, 45
    sheet = Image.new("RGB", (sample_w, sample_h*len(frames)))
    for i, frame in enumerate(frames):
        sheet.paste(frame.resize((sample_w,sample_h),Image.Resampling.LANCZOS),(0,i*sample_h))
    palette = sheet.quantize(colors=64,method=Image.Quantize.MEDIANCUT)
    quantized = [frame.quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG) for frame in frames]
    quantized[0].save(OUTPUT,save_all=True,append_images=quantized[1:],duration=DURATION_MS,loop=0,optimize=True,disposal=2)
    with Image.open(OUTPUT) as result:
        assert result.format=="GIF" and result.size==(WIDTH,HEIGHT)
        assert result.n_frames==len(frames)
        assert result.info.get("loop")==0
        assert OUTPUT.stat().st_size < 3_000_000, f"Snake GIF exceeds 3 MB budget: {OUTPUT.stat().st_size}"
    print(f"Generated {OUTPUT}: {len(frames)} frames, {OUTPUT.stat().st_size} bytes.")


if __name__ == "__main__":
    main()
