import datetime

import pytest

import middle


def test_config_keys():
    class TestModel(middle.Model):
        name = middle.field(type=str)
        when = middle.field(type=datetime.datetime)

    # ------------------------- #
    # defaults

    assert middle.config.str_method is True
    assert middle.config.force_str is False
    assert middle.config.no_transit_local_dtime is False

    tz = datetime.datetime.now(datetime.timezone.utc).astimezone()
    dt = datetime.datetime(2018, 7, 10, 10, 30)

    inst = TestModel(name=1, when=dt)
    assert isinstance(inst, TestModel)
    assert inst.name == "1"
    assert inst.when == dt.replace(tzinfo=tz.tzinfo).astimezone(
        datetime.timezone.utc
    )

    # ------------------------- #
    # str_method

    middle.config.str_method = False

    with pytest.raises(TypeError):
        TestModel(name=1, when=dt)

    # ------------------------- #
    # force_str

    middle.config.force_str = True
    assert TestModel(name=1, when=dt).name == "1"

    assert middle.config.str_method is False
    assert middle.config.force_str is True

    # ------------------------- #
    # no_transit_local_dtime

    middle.config.no_transit_local_dtime = True
    inst = TestModel(name=1, when=dt)
    assert inst.when == dt.replace(tzinfo=datetime.timezone.utc)

    # ------------------------- #
    # reset

    middle.config.str_method = True
    middle.config.force_str = False
    middle.config.no_transit_local_dtime = False

    assert middle.config.str_method is True
    assert middle.config.force_str is False
    assert middle.config.no_transit_local_dtime is False


def test_invalid_config_keys():
    assert middle.config.str_method is True
    assert middle.config.force_str is False
    assert middle.config.no_transit_local_dtime is False

    middle.config.str_method = "foo"
    middle.config.force_str = "bar"
    middle.config.no_transit_local_dtime = "baz"

    assert middle.config.str_method is True
    assert middle.config.force_str is False
    assert middle.config.no_transit_local_dtime is False


def test_contextmanager_config_keys():
    class TestModel(middle.Model):
        name = middle.field(type=str)
        when = middle.field(type=datetime.datetime)

    class Foo:
        def __init__(self, *args, **kwargs):
            pass

        def __str__(self):
            return "foo instance"

    dt = datetime.datetime(2018, 7, 10, 10, 30)

    # ------------------------- #
    # str_method

    with middle.config.temp(str_method=False):
        assert middle.config.str_method is False

        with pytest.raises(TypeError):
            TestModel(name=1)

    assert middle.config.str_method is True

    # ------------------------- #
    # force_str

    with middle.config.temp(force_str=True):
        assert middle.config.force_str is True
        assert TestModel(name=Foo(), when=dt).name == "foo instance"

    assert middle.config.force_str is False

    # ------------------------- #
    # no_transit_local_dtime

    with middle.config.temp(no_transit_local_dtime=True):
        assert middle.config.no_transit_local_dtime is True
        assert TestModel(name="foo", when=dt).when == dt.replace(
            tzinfo=datetime.timezone.utc
        )

    assert middle.config.no_transit_local_dtime is False


def test_contextmanager_invalid_config_keys():
    with middle.config.temp(
        force_str=1, str_method="a", no_transit_local_dtime=object()
    ):
        assert middle.config.force_str is False
        assert middle.config.str_method is True
        assert middle.config.no_transit_local_dtime is False
