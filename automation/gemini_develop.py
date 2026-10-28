"""One bounded Gemini request; validate all returned files before writing any."""
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import urllib.error
import urllib.request

MODEL = "gemini-3.8-flash"
SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "blocked": {"type": "BOOLEAN"},
        "reason": {"type": "STRING"},
        "files": {"type": "ARRAY", "items": {
            "type": "OBJECT", "properties": {
                "path": {"type": "STRING"}, "content": {"type": "STRING"}},
            "required": ["path", "content"]}},
    },
    "required": ["blocked", "reason", "files"],
}


def allowed(name):
    if not isinstance(name, str) or not name or "\\" in name:
        return False
    p = PurePosixPath(name)
    if p.is_absolute() or str(p) != name or any(x.startswith(".") for x in p.parts):
        return False
    if name in ("README.md", "TASKS.md"):
        return True
    if len(p.parts) < 2 or p.name == "conftest.py":
        return False
    return ((p.parts[0] in ("app", "tests", "migrations") and p.suffix == ".py")
            or (name.startswith("docs/learning/") and p.suffix == ".md"))


def checked_path(root, name):
    p = root / name
    for item in (p, *p.parents):
        if item == root:
            break
        if item.is_symlink():
            raise ValueError("Symlink forbidden: " + name)
    if not p.resolve().is_relative_to(root.resolve()):
        raise ValueError("Path outside repository")
    return p


def validate(root, result, tasks):
    if not isinstance(result, dict) or type(result.get("blocked")) is not bool:
        raise ValueError("Invalid response")
    if result["blocked"]:
        print("Gemini could not complete this task. No changes or push.")
        return {}
    rows = result.get("files")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 16:
        raise ValueError("Expected 1..16 files")
    changes = {}
    for row in rows:
        name, content = row.get("path"), row.get("content")
        if not allowed(name) or name in changes or not isinstance(content, str):
            raise ValueError("Forbidden or duplicate file")
        if len(content.encode()) > 100_000 or "\0" in content:
            raise ValueError("Invalid file content")
        p = checked_path(root, name)
        if p.exists() and name.startswith(("tests/", "docs/learning/", "migrations/")):
            raise ValueError("Existing tests, notes and migrations cannot be replaced")
        if name.endswith(".py"):
            compile(content, name, "exec")
        changes[name] = content
    match = re.search(r"^- \[ \] (.+)$", tasks, re.M)
    if not match:
        raise ValueError("No unfinished task")
    expected = tasks[:match.start()] + tasks[match.start():].replace("- [ ] ", "- [x] ", 1)
    if changes.get("TASKS.md") != expected:
        raise ValueError("Only the first task checkbox may change")
    for prefix in ("app/", "tests/", "docs/learning/"):
        if not any(n.startswith(prefix) and
                   (not (root / n).exists() or (root / n).read_text(encoding="utf-8") != c)
                   for n, c in changes.items()):
            raise ValueError("Missing real change under " + prefix)
    return changes


def context(root):
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    result = {}
    for name in names:
        if allowed(name) or name in ("AGENTS.md", "requirements.txt", "pytest.ini", "tests/conftest.py"):
            p = checked_path(root, name)
            result[name] = p.read_text(encoding="utf-8")
    if len(json.dumps(result)) > 220_000:
        raise ValueError("Repository context exceeds limit; split roadmap/context before continuing")
    return result


def generate(files, key):
    prompt = (
        "Implement ONLY the first unchecked TASKS.md task in this educational repository. "
        "Follow AGENTS.md. Return complete contents of changed/new files, no shell commands. "
        "Preserve existing behavior. No dependency or configuration changes. "
        "Use only app/*.py (including subdirectories), NEW tests/test_*.py, NEW migrations/*.py, "
        "NEW docs/learning/*.md, README.md and TASKS.md. Never replace existing tests, migrations "
        "or learning notes; never create conftest.py. Add meaningful tests and an Uzbek Latin "
        "learning note with interview questions. Mark only the first checkbox done and preserve "
        "the rest of TASKS.md byte for byte. External CI will run tests before publishing; do not "
        "claim you ran them. If unable to fully implement, return blocked=true and files=[]. "
        "Repository files follow as JSON:\n" + json.dumps(files, ensure_ascii=False)
    )
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json",
                                 "responseSchema": SCHEMA, "maxOutputTokens": 16384}}
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as e:
        reasons = {400: "Request/model configuration rejected", 403: "API key or project access denied",
                   404: "Model unavailable", 429: "Free quota/rate limit reached; no changes made"}
        raise RuntimeError(f"Gemini HTTP {e.code}: " + reasons.get(e.code, "API service error")) from None
    candidates = payload.get("candidates", [])
    if not candidates or candidates[0].get("finishReason") != "STOP":
        raise ValueError("Gemini returned a blocked/incomplete response; nothing written")
    content = "".join(p.get("text", "") for p in candidates[0].get("content", {}).get("parts", [])
                      if not p.get("thought"))
    return json.loads(content)


def main():
    root = Path.cwd()
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise ValueError("Add repository secret GEMINI_API_KEY")
    if subprocess.check_output(["git", "status", "--porcelain"]).strip():
        raise ValueError("Checkout must be clean before generation")
    files = context(root)
    if not re.search(r"^- \[ \] ", files["TASKS.md"], re.M):
        print("Roadmap complete; no request sent.")
        return
    changes = validate(root, generate(files, key), files["TASKS.md"])
    for name, content in changes.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="")
    if changes:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("changed=true\n")
        print(f"Prepared {len(changes)} files; tests must pass before publication.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as e:
        # No raw API body, request headers, credentials or generated source in logs.
        print(f"::error::{str(e)}")
        raise SystemExit(1)
