"""Trusted script: run a copy captured BEFORE the AI edits the checkout."""
from pathlib import Path
import re
import subprocess
import sys


def git(*args):
    return subprocess.check_output(["git", *args])


base = sys.argv[1]
assert git("rev-parse", "HEAD").decode().strip() == base, "AI changed HEAD"
# Include newly added files; never trust the AI's staging choices.
subprocess.run(["git", "add", "-A"], check=True)
paths = git("diff", "--cached", "--name-only", "-z", base).decode().split("\0")
paths = [p for p in paths if p]
if not paths:
    raise SystemExit("No changes; nothing to publish")
allowed = ("app/", "tests/", "migrations/", "docs/learning/")
for p in paths:
    assert p in ("TASKS.md", "README.md") or p.startswith(allowed), f"Forbidden path: {p}"
    assert not Path(p).is_symlink(), f"Symlink forbidden: {p}"
    assert ".." not in Path(p).parts
assert any(p.startswith("app/") for p in paths), "A real application change is required"
assert any(p.startswith("tests/") for p in paths), "Feature tests are required"
assert any(p.startswith("docs/learning/") for p in paths), "Learning note required"
old = git("show", f"{base}:TASKS.md").decode()
new = Path("TASKS.md").read_text()
match = re.search(r"^- \[ \] (.+)$", old, re.M)
assert match, "Roadmap complete"
expected = old[:match.start()] + old[match.start():].replace("- [ ] ", "- [x] ", 1)
assert new == expected, "Only the first pending checkbox can be completed"
# Reject new symlinks/submodules, even if their targets are missing.
for line in git("diff", "--cached", "--raw", base).decode().splitlines():
    assert line.split()[1] not in ("120000", "160000")
Path("/tmp/feature.patch").write_bytes(git("diff", "--cached", "--binary", base))
Path("/tmp/commit-message.txt").write_text("feat: " + match.group(1) + "\n\nAI-assisted implementation using OpenAI Codex.\n")
