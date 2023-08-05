from datetime import datetime, time, timezone

from freezegun import freeze_time
from watchghost.config import Server
from watchghost.services import Service
from watchghost.watchers import Watcher

UTC = timezone.utc
SERVER = Server('server', {})
SERVICE = Service('network.Ping')


def test_is_in_checking_period():
    config = {'before': time(16), 'after': time(12)}
    watcher = Watcher(SERVER, SERVICE, config, [])

    # Checking period is local time, not UTC
    with freeze_time('2018-01-01 14:00:00'):
        # 14:00 UTC, 14:00 local time
        assert watcher.is_in_checking_period() is True
    with freeze_time('2018-01-01 15:30:00', tz_offset=1):
        # 15:30 UTC, 16:30 local time
        assert watcher.is_in_checking_period() is False
    with freeze_time('2018-01-01 15:30:00', tz_offset=5):
        # 15:30 UTC, 20:30 local time
        assert watcher.is_in_checking_period() is False
    with freeze_time('2018-01-01 17:30:00', tz_offset=-3):
        # 17:30 UTC, 14:30 local time
        assert watcher.is_in_checking_period() is True
    with freeze_time('2018-01-01 17:30:00', tz_offset=-8):
        # 17:30 UTC, 09:30 local time
        assert watcher.is_in_checking_period() is False


def test_next_check_hour_in_checking_period_long_repeat():
    config = {
        'after': time(12),
        'before': time(16),
        'repeat': 24 * 60 * 60,
    }
    watcher = Watcher(SERVER, SERVICE, config, [])

    with freeze_time('2018-01-01 13:30:00', tz_offset=1):
        # 14:30 UTC, 14:30 local time
        assert watcher.next_check_hour == datetime.now(tz=UTC)

        start = end = datetime(2018, 1, 1, 13, tzinfo=UTC)
        watcher.add_check_result(response={}, status=0, start=start, end=end)
        assert watcher.next_check_hour == datetime(2018, 1, 2, 13, tzinfo=UTC)


def test_next_check_hour_in_checking_period_short_repeat():
    config = {
        'after': time(12),
        'before': time(16),
        'repeat': 1 * 60 * 60,
    }
    watcher = Watcher(SERVER, SERVICE, config, [])

    with freeze_time('2018-01-01 14:30:00'):
        # 14:30 UTC, 14:30 local time
        # We can't use tz_offset for this test because of
        # https://github.com/spulec/freezegun/issues/89
        assert watcher.next_check_hour == datetime.now(tz=UTC)

        start = end = datetime(2018, 1, 1, 12, tzinfo=UTC)
        watcher.add_check_result(response={}, status=0, start=start, end=end)
        assert watcher.next_check_hour == datetime.now(tz=UTC)

        start = end = datetime(2018, 1, 1, 14, tzinfo=UTC)
        watcher.add_check_result(response={}, status=0, start=start, end=end)
        assert watcher.next_check_hour == datetime(2018, 1, 1, 15, tzinfo=UTC)


def test_next_check_hour_not_in_checking_period():
    config = {
        'after': time(12),
        'before': time(16),
        'repeat': 24 * 60 * 60,
    }
    watcher = Watcher(SERVER, SERVICE, config, [])

    with freeze_time('2018-01-01 05:30:00', tz_offset=1):
        # 05:30 UTC, 06:30 local time
        assert watcher.next_check_hour == datetime(2018, 1, 1, 12, tzinfo=UTC)

    with freeze_time('2018-01-01 15:30:00', tz_offset=1):
        # 15:30 UTC, 16:30 local time
        assert watcher.next_check_hour == datetime(2018, 1, 2, 12, tzinfo=UTC)
