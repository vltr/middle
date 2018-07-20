from datetime import datetime
from datetime import timezone

from dateutil import parser

from .config import config

# the current machine Time Zone
_current_tz = datetime.now(timezone.utc).astimezone().tzinfo


def dt_to_iso_string(dt: datetime, tz=_current_tz) -> str:
    _check_dt_instance(dt)
    if not _dt_has_tz(dt):
        dt = dt_convert_to_utc(dt)
    if not _dt_is_utc(dt):
        dt = dt.astimezone(timezone.utc)
    return _dt_to_iso_string(dt)


def dt_from_iso_string(dt_str: str) -> datetime:
    if dt_str is None:
        raise TypeError('"dt_str" argument must not be None')
    elif isinstance(dt_str, str) and dt_str.strip() == "":
        raise TypeError('"dt_str" argument must not be blank')
    return _dt_from_iso_string(dt_str)


def dt_from_timestamp(dt_ts, tz=_current_tz) -> datetime:
    if dt_ts is None or not isinstance(dt_ts, (int, float)):
        raise TypeError('"dt_ts" argument must not be None or blank')
    return dt_convert_to_utc(datetime.fromtimestamp(dt_ts, tz=tz))


def dt_convert_to_utc(dt: datetime, tz=_current_tz) -> datetime:
    _check_dt_instance(dt)
    if not _dt_has_tz(dt):
        if not config.no_transit_local_dtime:
            dt = dt.replace(tzinfo=tz)
        else:
            dt = dt.replace(tzinfo=timezone.utc)
    if not _dt_is_utc(dt):
        return dt.astimezone(timezone.utc)
    return dt


def _dt_from_iso_string(dt_str):
    dt = parser.parse(dt_str)
    return dt_convert_to_utc(dt)


def _dt_to_iso_string(dt):
    return dt.isoformat()


def _dt_is_utc(dt: datetime):
    return dt.utcoffset().total_seconds() == 0


def _dt_has_tz(dt: datetime):
    """From the Python docs: https://docs.python.org/3/library/datetime.html

    An object of type time or datetime may be naive or aware. A datetime object
    d is aware if d.tzinfo is not None and d.tzinfo.utcoffset(d) does not
    return None. If d.tzinfo is None, or if d.tzinfo is not None but
    d.tzinfo.utcoffset(d) returns None, d is naive. A time object t is aware if
    t.tzinfo is not None and t.tzinfo.utcoffset(None) does not return None.
    Otherwise, t is naive.
    """
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def _check_dt_instance(dt):
    if not isinstance(dt, datetime):
        raise TypeError('"dt" must be an instance of datetime')


__all__ = (
    "dt_convert_to_utc",
    "dt_from_iso_string",
    "dt_from_timestamp",
    "dt_to_iso_string",
)
