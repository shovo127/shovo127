from pathlib import Path
import gzip

root = Path(__file__).resolve().parents[1]
source = root / "scripts" / "profile_art_source.py.gz"
code = gzip.decompress(source.read_bytes()).decode("utf-8")
exec(compile(code, str(source), "exec"), {"__name__": "__main__", "__file__": str(source)})
