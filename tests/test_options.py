import re

import pytest

from middle.options import metadata_options


def _get_option(name):
    return next(filter(lambda o: o.name == name, metadata_options))


@pytest.mark.parametrize(
    "option_name",
    [
        pytest.param("description", id="description_str"),
        pytest.param("format", id="format_str"),
    ],
)
def test_metadata_option_str(option_name):
    option = _get_option(option_name)
    assert option("hello, world") == "hello, world"

    with pytest.raises(TypeError):
        assert option(3.14)

    assert set(option.keys) == {option_name}


def test_metadata_option_minimum():
    minimum = _get_option("minimum")
    assert minimum(10) == 10
    assert minimum(-2.5) == -2.5

    assert minimum.check_upper_range(50) == 50
    assert minimum.check_upper_range(-5.0) == -5.0

    with pytest.raises(TypeError):
        assert minimum("hello")

    with pytest.raises(ValueError):
        minimum.check_upper_range(50, 60)

    with pytest.raises(ValueError):
        minimum.check_upper_range(-5.0, -4.0)

    assert set(minimum.keys) == {"minimum", "maximum"}


@pytest.mark.parametrize(
    "option_name",
    [
        pytest.param("exclusive_minimum", id="exclusive_minimum_bool"),
        pytest.param("exclusive_maximum", id="exclusive_maximum_bool"),
        pytest.param("unique_items", id="unique_items_bool"),
    ],
)
def test_metadata_option_bool(option_name):
    option = _get_option(option_name)
    assert option(True) is True
    assert option(False) is False

    with pytest.raises(TypeError):
        assert option(8)

    assert set(option.keys) == {option_name}


def test_metadata_option_exclusive_maximum():
    exclusive_maximum = _get_option("exclusive_maximum")
    assert exclusive_maximum(True) is True
    assert exclusive_maximum(False) is False

    with pytest.raises(TypeError):
        assert exclusive_maximum(8)

    assert set(exclusive_maximum.keys) == {"exclusive_maximum"}


def test_metadata_option_multiple_of():
    multiple_of = _get_option("multiple_of")
    assert multiple_of(10) == 10
    assert multiple_of(2.5) == 2.5

    with pytest.raises(TypeError):
        assert multiple_of("hello")

    with pytest.raises(ValueError):
        multiple_of(-10)

    with pytest.raises(ValueError):
        multiple_of(-5.0)

    assert set(multiple_of.keys) == {"multiple_of"}


def test_metadata_option_pattern():
    pattern = _get_option("pattern")
    assert pattern("^[a-z]+$") == re.compile("^[a-z]+$")

    with pytest.raises(TypeError):
        assert pattern(20)

    assert set(pattern.keys) == {"pattern"}


@pytest.mark.parametrize(
    "option_name,keys",
    [
        pytest.param(
            "min_length", {"min_length", "max_length"}, id="min_length_range"
        ),
        pytest.param(
            "min_items", {"min_items", "max_items"}, id="min_items_range"
        ),
        pytest.param(
            "min_properties",
            {"min_properties", "max_properties"},
            id="min_properties_range",
        ),
    ],
)
def test_metadata_option_ranges(option_name, keys):
    option = _get_option(option_name)
    assert option(10) == 10

    assert option.check_upper_range(50) == 50

    with pytest.raises(TypeError):
        assert option(3.14)

    with pytest.raises(ValueError):
        option.check_upper_range(0, 1)

    with pytest.raises(ValueError):
        option(-5)

    with pytest.raises(ValueError):
        option(-5, -2)

    assert set(option.keys) == keys
