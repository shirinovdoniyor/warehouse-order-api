from datetime import datetime, timezone
from automation.schedule import daily_slots, decide


def test_daily_plan_is_stable_bounded_and_changes():
    seen = set()
    for day in range(1, 29):
        date = f"2026-11-{day:02}"
        slots = daily_slots(date, "owner/repo")
        assert slots == daily_slots(date, "owner/repo")
        assert 5 <= len(slots) <= 10
        assert len(set(slots)) == len(slots)
        assert all(487 <= x < 1320 for x in slots)
        seen.add(tuple(slots))
    assert len(seen) > 1


def test_cap_and_manual_run():
    now = datetime(2026, 11, 1, 0, tzinfo=timezone.utc)
    target = len(daily_slots("2026-11-01", "o/r"))
    assert decide(now, "o/r", [], manual=True)["run"] == "true"
    assert decide(now, "o/r", [{"day": "2026-11-01"}] * target, True)["run"] == "false"
    assert decide(now, "o/r", [])["run"] == "false"


def test_due_slot_and_timezone_boundary():
    now = datetime(2026, 11, 1, 16, 59, tzinfo=timezone.utc)
    assert decide(now, "o/r", [])["run"] == "true"
    after_midnight = datetime(2026, 11, 1, 20, tzinfo=timezone.utc)
    result = decide(after_midnight, "o/r", [])
    assert result["day"] == "2026-11-02"
    assert result["run"] == "false"
