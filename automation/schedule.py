"""Deterministic daily slots; successful publishes are recorded by publish job."""
import hashlib
import json
import os
import random
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def daily_slots(day: str, repository: str) -> list[int]:
    seed = int.from_bytes(hashlib.sha256(f"{repository}:{day}".encode()).digest(), "big")
    rng = random.Random(seed)
    # 08:07 through 21:47, checked by Actions every 20 minutes.
    return sorted(rng.sample(list(range(8 * 60 + 7, 22 * 60, 20)), rng.randint(5, 10)))


def decide(now, repository, runs, manual=False):
    local = now.astimezone(ZoneInfo("Asia/Tashkent"))
    day = local.date().isoformat()
    slots = daily_slots(day, repository)
    done = sum(x["day"] == day for x in runs)
    due = sum(t <= local.hour * 60 + local.minute for t in slots)
    allowed = done < len(slots) and (manual or (8 <= local.hour < 22 and done < due))
    return {"run": str(allowed).lower(), "day": day, "target": len(slots), "done": done,
            "slots": [f"{t // 60:02}:{t % 60:02}" for t in slots]}


if __name__ == "__main__":
    state = json.loads(Path("automation/state.json").read_text())
    result = decide(datetime.now(ZoneInfo("Asia/Tashkent")), os.environ["GITHUB_REPOSITORY"],
                    state["runs"], os.getenv("GITHUB_EVENT_NAME") == "workflow_dispatch")
    if "- [ ] " not in Path("TASKS.md").read_text():
        result["run"] = "false"
    if os.getenv("AI_ENABLED", "true").lower() == "false":
        result["run"] = "false"
    print(json.dumps(result))
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        for key in ("run", "day", "target"):
            print(f"{key}={result[key]}", file=f)
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        print("## Today's plan (Asia/Tashkent)\n" + json.dumps(result), file=f)
