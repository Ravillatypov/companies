from datetime import datetime, timedelta, timezone


def utcnow() -> datetime:
    """Get UTC now with tz."""
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def after(
        days: float = 0,
        seconds: float = 0,
        minutes: float = 0,
        hours: float = 0,
        weeks: float = 0,
) -> datetime:
    """Get datetime with offset."""
    return utcnow() + timedelta(
        days=days,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
    )
