import pytest

import middle


def test_config_keys():
    class TestModel(middle.Model):
        name: str = middle.field()

    assert middle.config.str_method is True
    assert middle.config.force_str is False

    inst = TestModel(name=1)
    assert isinstance(inst, TestModel)
    assert inst.name == "1"

    middle.config.str_method = False

    with pytest.raises(TypeError):
        TestModel(name=1)

    middle.config.force_str = True
    assert TestModel(name=1).name == "1"

    assert middle.config.str_method is False
    assert middle.config.force_str is True

    # reset
    middle.config.str_method = True
    middle.config.force_str = False

    assert middle.config.str_method is True
    assert middle.config.force_str is False


def test_invalid_config_keys():
    assert middle.config.str_method is True
    assert middle.config.force_str is False

    middle.config.str_method = "foo"
    middle.config.force_str = "bar"

    assert middle.config.str_method is True
    assert middle.config.force_str is False
