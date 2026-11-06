from pathlib import Path
import re
import subprocess
import sys

# Conservative checks for common high-confidence credential formats.
PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    re.compile(r"\bsk-proj-[A-Za-z0-9_-]{30,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"),
    re.compile(r"\b xox[baprs]-[A-Za-z0-9-]{10,}\b"),
]
FORBIDDEN_NAMES = {
    ".env", ".env.local", ".env.production", "credentials.json",
    "token.json", "id_rsa", "id_ed25519",
}
ALLOWLIST = {"scripts/check_public_leaks.py"}

tracked = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
problems = []
for raw in filter(None, tracked):
    path = Path(raw)
    if path.name in FORBIDDEN_NAMES or path.suffix.lower() in {".pem", ".p12", ".pfx", ".keystore"}:
        problems.append(f"Forbidden sensitive filename tracked: {raw}")
        continue
    if raw in ALLOWLIST or not path.is_file():
        continue
    try:
        data = path.read_bytes()
        if b"\0" in data:
            continue
        text = data.decode("utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for pattern in PATTERNS:
        if pattern.search(text):
            problems.append(f"Possible credential pattern in tracked file: {raw}")
            break

if problems:
    print("PUBLIC REPOSITORY SECURITY CHECK FAILED:")
    for problem in problems:
        print(f"- {problem}")
    sys.exit(1)

print(f"PASS: checked {len([x for x in tracked if x])} tracked files; no common credential patterns or forbidden secret files detected.")
