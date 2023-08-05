from datetime import datetime, timedelta, timezone


def add_check_result(watcher, status, response=None, start=None, end=None):
    now = datetime.now(timezone.utc)
    start = start or now - timedelta(seconds=2)
    end = end or now
    response = response or {}
    return watcher.add_check_result(
        status=status, response=response, start=start, end=end)
