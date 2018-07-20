import datetime

import pytest
import pytz
from freezegun import freeze_time

import middle
from middle.dtutils import dt_convert_to_utc
from middle.dtutils import dt_from_iso_string
from middle.dtutils import dt_from_timestamp
from middle.dtutils import dt_to_iso_string


def test_datetime_with_tzinfo_to_iso_string():
    dt = datetime.datetime(2018, 7, 2, 8, 30, 0, 0, datetime.timezone.utc)
    assert dt_to_iso_string(dt) == "2018-07-02T08:30:00+00:00"

    with middle.config.temp(no_transit_local_dtime=True):
        assert (
            dt_to_iso_string(datetime.datetime(2018, 7, 2, 8, 30))
            == "2018-07-02T08:30:00+00:00"
        )


def test_datetime_no_tzinfo_to_iso_string():
    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    with freeze_time(datetime.datetime(2018, 7, 2, 8, 30, tzinfo=tz)):
        dt = datetime.datetime.now()
        assert dt.tzinfo is None
        assert dt_to_iso_string(dt) == dt_to_iso_string(
            datetime.datetime.utcnow()
        )


def test_datetime_with_tzinfo_nonutc_to_iso_string():
    dt = datetime.datetime(
        2018, 7, 2, 8, 30, 0, 0, tzinfo=pytz.timezone("Etc/GMT+5")
    )
    assert dt_to_iso_string(dt) == "2018-07-02T13:30:00+00:00"


def test_dt_withtz_from_iso_string():
    assert dt_from_iso_string(
        "2018-07-02T08:30:00+01:00"
    ) == datetime.datetime(2018, 7, 2, 7, 30, 0, 0, datetime.timezone.utc)


def test_dt_withouttz_from_iso_string(local_tz):
    assert dt_from_iso_string("2018-07-02T08:30:00") == datetime.datetime(
        2018, 7, 2, 8, 30, 0, 0, tzinfo=local_tz
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


def test_dt_convert_to_utc():
    assert dt_convert_to_utc(
        datetime.datetime(2018, 7, 2, 8, 30, 0, 0, tzinfo=pytz.timezone("CET"))
    ) == datetime.datetime(
        2018, 7, 2, 7, 30, 0, 0, tzinfo=datetime.timezone.utc
    )

    assert dt_convert_to_utc(
        datetime.datetime(
            2018, 7, 2, 8, 30, 0, 0, tzinfo=datetime.timezone.utc
        )
    ) == dt_convert_to_utc(
        datetime.datetime(2018, 7, 2, 9, 30, 0, 0, tzinfo=pytz.timezone("CET"))
    )


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(None, id="none_dt_input"),
        pytest.param("", id="blank_dt_input"),
        pytest.param(object(), id="invalid_dt_input"),
        pytest.param(datetime.datetime.now().date, id="invalid_dt_input_2"),
    ],
)
def test_dt_convert_to_utc_error(value):
    with pytest.raises(TypeError):
        dt_convert_to_utc(value)
