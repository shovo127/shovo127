from pathlib import Path
from PIL import Image
import os

src=Path(os.environ.get("PROFILE_RENDER_DIR","/tmp/profile-render"))
dst=Path("assets/3d"); dst.mkdir(parents=True,exist_ok=True)
for prefix in ("00-hero","01-about","02-engineering-focus","03-featured-work","04-technology","05-command-center","06-achievements","07-contribution-city","09-coding-habits","10-learning-loop","11-beyond-code","12-connect"):
    files=sorted(src.glob(prefix+"_*.png"))
    if len(files)!=12:
        raise SystemExit(f"{prefix}: expected 12 rendered frames, found {len(files)}")
    frames=[Image.open(p).convert("RGB").quantize(colors=128,method=Image.Quantize.MEDIANCUT) for p in files]
    out=dst/(prefix+".gif")
    frames[0].save(out,save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True,disposal=2)
    with Image.open(out) as im:
        if im.format!="GIF" or im.n_frames!=12:
            raise SystemExit(f"Invalid animation output: {out}")
    print(f"PACKED {out} ({out.stat().st_size} bytes)")
