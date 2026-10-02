from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


def stamp_created(updated: dict | None = None) -> dict:
    now = utc_now().isoformat()
    data = {"created_at": now, "updated_at": now}
    if updated:
        data.update(updated)
    return data


def touch_updated(data: dict) -> dict:
    data["updated_at"] = utc_now().isoformat()
    return data
