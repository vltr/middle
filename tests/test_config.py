import datetime

import pytest

import middle


def test_config_keys():
    class TestModel(middle.Model):
        name: str = middle.field()
        when: datetime.datetime = middle.field()

    assert middle.config.str_method is True
    assert middle.config.force_str is False
    assert middle.config.force_datetime_utc is False

    dt = datetime.datetime.now()
    current_tz = (
        datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    )

    inst = TestModel(name=1, when=dt)
    assert isinstance(inst, TestModel)
    assert inst.name == "1"
    assert inst.when == dt.replace(tzinfo=current_tz)

    middle.config.str_method = False

    with pytest.raises(TypeError):
        TestModel(name=1, when=dt)

    middle.config.force_str = True
    assert TestModel(name=1, when=dt).name == "1"

    assert middle.config.str_method is False
    assert middle.config.force_str is True

    # reset
    middle.config.str_method = True
    middle.config.force_str = False
    middle.config.force_datetime_utc = False

    assert middle.config.str_method is True
    assert middle.config.force_str is False
    assert middle.config.force_datetime_utc is False


def test_invalid_config_keys():
    assert middle.config.str_method is True
    assert middle.config.force_str is False
    assert middle.config.force_datetime_utc is False

    middle.config.str_method = "foo"
    middle.config.force_str = "bar"
    middle.config.force_datetime_utc = "baz"

    assert middle.config.str_method is True
    assert middle.config.force_str is False
    assert middle.config.force_datetime_utc is False


def test_contextmanager_config_keys():
    pass


def test_contextmanager_invalid_config_keys():
    with middle.config.temp(
        force_str=1, str_method="a", force_datetime_utc={}
    ):
        assert middle.config.force_str is False
        assert middle.config.str_method is True
        assert middle.config.force_datetime_utc is False
