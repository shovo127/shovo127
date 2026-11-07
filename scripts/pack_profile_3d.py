from pathlib import Path
from PIL import Image
import os

src=Path(os.environ.get("PROFILE_RENDER_DIR","/tmp/profile-render"))
dst=Path("assets/3d"); dst.mkdir(parents=True,exist_ok=True)
scenes=("00-hero","01-about","02-engineering-focus","03-featured-work","04-technology","05-command-center","06-precision-tools","07-engineering-city","09-coding-habits","10-learning-loop","11-beyond-code","12-connect")
for prefix in scenes:
    files=sorted(src.glob(prefix+"_*.png"))
    if len(files)!=10:
        raise SystemExit(f"{prefix}: expected 10 rendered frames, found {len(files)}")
    originals=[Image.open(p).convert("RGB") for p in files]
    # Build one shared palette from all frames to prevent colour flicker and reduce GIF size.
    sample_w=min(225, originals[0].width)
    sample_h=min(56, originals[0].height)
    sheet=Image.new("RGB",(sample_w,sample_h*len(originals)))
    for i,frame in enumerate(originals):
        sheet.paste(frame.resize((sample_w,sample_h),Image.Resampling.LANCZOS),(0,i*sample_h))
    palette=sheet.quantize(colors=96,method=Image.Quantize.MEDIANCUT)
    frames=[frame.quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG) for frame in originals]
    out=dst/(prefix+".gif")
    frames[0].save(out,save_all=True,append_images=frames[1:],duration=120,loop=0,optimize=True,disposal=2)
    for frame in originals: frame.close()
    with Image.open(out) as im:
        if im.format!="GIF" or im.n_frames!=10 or im.size!=(900,225):
            raise SystemExit(f"Invalid animation output: {out}")
    print(f"PACKED {out} ({out.stat().st_size} bytes)",flush=True)
