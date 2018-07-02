import datetime

import pytest
import pytz
from freezegun import freeze_time

from middle.dtutils import convert_to_utc
from middle.dtutils import dt_from_iso_string
from middle.dtutils import dt_from_timestamp
from middle.dtutils import dt_to_iso_string


def test_datetime_with_tzinfo_to_iso_string():
    dt = datetime.datetime(2018, 7, 2, 8, 30, 0, 0, datetime.timezone.utc)
    assert dt_to_iso_string(dt) == "2018-07-02T08:30:00+00:00"


def test_datetime_no_tzinfo_to_iso_string():
    tz = datetime.datetime.now(datetime.timezone.utc).astimezone()
    utc_offset = tz.tzinfo.utcoffset(tz).total_seconds() / 3600
    with freeze_time(
        "2018-07-02 08:30:00", tz_offset=datetime.timedelta(hours=utc_offset)
    ):
        dt = datetime.datetime.now()
        assert dt.tzinfo is None
        assert dt_to_iso_string(dt) == "2018-07-02T08:30:00+00:00"


def test_datetime_with_tzinfo_nonutc_to_iso_string():
    dt = datetime.datetime(2018, 7, 2, 8, 30, 0, 0, pytz.timezone("CET"))
    assert dt_to_iso_string(dt) == "2018-07-02T08:30:00+01:00"


def test_dt_withtz_from_iso_string():
    assert dt_from_iso_string(
        "2018-07-02T08:30:00+01:00"
    ) == datetime.datetime(2018, 7, 2, 7, 30, 0, 0, datetime.timezone.utc)


def dt_withouttz_from_iso_string():
    with freeze_time(
        "2018-07-02 08:30:00", tz_offset=-datetime.timedelta(hours=3)
    ):
        assert dt_from_iso_string("2018-07-02T08:30:00") == datetime.datetime(
            2018, 7, 2, 11, 30, 0, 0, datetime.timezone.utc
        )


@pytest.mark.parametrize(
    "value,exc",
    [
        pytest.param(None, TypeError, id="none_dt_input"),
        pytest.param("                    ", TypeError, id="blank_dt_input"),
        pytest.param(
            "            20181335110608-1532        ",
            ValueError,
            id="invalid_dt_input",
        ),
        pytest.param("foobarbaz", ValueError, id="invalid_dt_input_2"),
    ],
)
def test_dt_from_iso_string_error(value, exc):
    with pytest.raises(exc):
        dt_from_iso_string(value)


def test_dt_from_timestamp():
    tz = datetime.timezone.utc
    assert dt_from_timestamp(1530520200) == datetime.datetime(
        2018, 7, 2, 8, 30, 0, 0, tz
    )
    assert dt_from_timestamp(1530520200.000123) == datetime.datetime(
        2018, 7, 2, 8, 30, 0, 123, tz
    )


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(None, id="none_dt_input"),
        pytest.param("1530520200", id="blank_dt_input"),
        pytest.param(b"testing", id="invalid_dt_input"),
    ],
)
def test_dt_from_timestamp_error(value):
    with pytest.raises(TypeError):
        dt_from_timestamp(value)


def test_convert_to_utc():
    assert convert_to_utc(
        datetime.datetime(2018, 7, 2, 8, 30, 0, 0, pytz.timezone("CET"))
    ) == datetime.datetime(2018, 7, 2, 7, 30, 0, 0, datetime.timezone.utc)

    assert convert_to_utc(
        datetime.datetime(2018, 7, 2, 8, 30, 0, 0)
    ) == datetime.datetime(2018, 7, 2, 9, 30, 0, 0, pytz.timezone("CET"))


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(None, id="none_dt_input"),
        pytest.param("", id="blank_dt_input"),
        pytest.param(object(), id="invalid_dt_input"),
        pytest.param(datetime.datetime.now().date, id="invalid_dt_input_2"),
    ],
)
def test_convert_to_utc_error(value):
    with pytest.raises(TypeError):
        convert_to_utc(value)
