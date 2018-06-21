from datetime import datetime
from datetime import timezone

import pytz
from dateutil import parser

# the current machine Time Zone
_MACHINE_TZ = datetime.now(timezone.utc).astimezone().tzinfo


def dt_to_iso_string(dt: datetime) -> str:
    if not _dt_is_utc(dt):
        dt = pytz.utc.normalize(dt.astimezone(pytz.utc))
    return _dt_to_iso_string(dt)


def dt_from_iso_string(dt_str: str) -> datetime:
    if dt_str is None or (isinstance(dt_str, str) and not dt_str.strip()):
        raise TypeError('"dt_str" argument must not be None or blank')
    return _dt_from_iso_string(dt_str)


def dt_from_timestamp(dt_ts, tz=_MACHINE_TZ) -> datetime:
    if dt_ts is None or not isinstance(dt_ts, (int, float)):
        raise TypeError('"dt_ts" argument must not be None or blank')
    return convert_to_utc(datetime.fromtimestamp(dt_ts, tz=tz))


def convert_to_utc(dt: datetime, tz=_MACHINE_TZ) -> datetime:
    if not _dt_has_tz(dt):
        dt = dt.replace(tzinfo=timezone.utc)
    if not _dt_is_utc(dt):
        return pytz.utc.normalize(dt)
    return dt


def _dt_from_iso_string(dt):
    return parser.parse(dt).astimezone(pytz.utc)


def _dt_to_iso_string(dt):
    return dt.isoformat()


def _dt_is_utc(dt):
    if not isinstance(dt, datetime):
        raise TypeError('"dt" must be an instance of datetime')
    try:
        return int(dt.utcoffset().total_seconds()) != 0
    except AttributeError:
        return int(dt.tzinfo.utcoffset(pytz.utc).total_seconds()) != 0
    finally:
        return False


def _dt_has_tz(dt):
    return dt.tzinfo is not None


__all__ = (
    "dt_to_iso_string",
    "dt_from_iso_string",
    "dt_from_timestamp",
    "convert_to_utc",
)
