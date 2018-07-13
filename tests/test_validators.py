import re
from typing import Dict
from typing import List
from typing import Set

import pytest

import middle
from middle.exceptions import ValidationError

# #############################################################################
# str


@pytest.mark.parametrize(
    "test_value,error_values,kwargs",
    [
        pytest.param("foo", ["fo", ""], {"min_length": 3}, id="str_min"),
        pytest.param("", [], {"min_length": None}, id="str_min_none"),
        pytest.param(
            "foo", ["foobar", "      "], {"max_length": 5}, id="str_max"
        ),
        pytest.param("", [], {"max_length": None}, id="str_max_none"),
        pytest.param(
            "foo",
            ["fo", "foobar"],
            {"min_length": 3, "max_length": 5},
            id="str_min_max",
        ),
        pytest.param(
            "foo",
            [],
            {"min_length": None, "max_length": None},
            id="str_min_max_none",
        ),
        pytest.param(
            "foo", ["fo1", " foo "], {"pattern": "^[a-z]+$"}, id="str_pattern"
        ),
        pytest.param("foo", [], {"pattern": None}, id="str_pattern_none"),
        pytest.param(
            "foo",
            ["fo1", " foo "],
            {"pattern": re.compile("^[a-z]+$")},
            id="str_re_object",
        ),
    ],
)
def test_str(test_value, error_values, kwargs):
    class TestModel(middle.Model):
        name = middle.field(type=str, **kwargs)

    inst = TestModel(name=test_value)

    assert isinstance(inst, TestModel)
    assert inst.name == test_value

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(name=ev)


@pytest.mark.parametrize(
    "test_value,raised_exc,kwargs",
    [
        pytest.param(
            "foo", TypeError, {"min_length": "foo"}, id="str_min_wrong_type"
        ),
        pytest.param(
            "foo", TypeError, {"max_length": "foo"}, id="str_max_wrong_type"
        ),
        pytest.param(
            "foo", ValueError, {"min_length": -3}, id="str_min_negative"
        ),
        pytest.param(
            "foo", ValueError, {"max_length": -3}, id="str_max_negative"
        ),
        pytest.param(
            "foo",
            ValueError,
            {"min_length": 5, "max_length": 3},
            id="str_max_lt_min",
        ),
        pytest.param(
            "foo", TypeError, {"pattern": object()}, id="str_pattern_none"
        ),
    ],
)
def test_str_errors(test_value, raised_exc, kwargs):
    class TestModel(middle.Model):
        name = middle.field(type=str, **kwargs)

    with pytest.raises(raised_exc):
        TestModel(name=test_value)


# #############################################################################
# int


@pytest.mark.parametrize(
    "test_value,error_values,kwargs",
    [
        pytest.param(20, [19, 18], {"minimum": 20}, id="int_min"),
        pytest.param(
            21,
            [20, 19],
            {"minimum": 20, "exclusive_minimum": True},
            id="int_excl_min",
        ),
        pytest.param(20, [21, 22], {"maximum": 20}, id="int_max"),
        pytest.param(
            19,
            [20, 21],
            {"maximum": 20, "exclusive_maximum": True},
            id="int_excl_max",
        ),
        pytest.param(
            15, [9, 21], {"minimum": 10, "maximum": 20}, id="int_min_max"
        ),
        pytest.param(
            15,
            [10, 21],
            {"minimum": 10, "exclusive_minimum": True, "maximum": 20},
            id="int_excl_min_max",
        ),
        pytest.param(
            15,
            [9, 20],
            {"minimum": 10, "maximum": 20, "exclusive_maximum": True},
            id="int_min_excl_max",
        ),
        pytest.param(
            15,
            [10, 20],
            {
                "minimum": 10,
                "exclusive_minimum": True,
                "maximum": 20,
                "exclusive_maximum": True,
            },
            id="int_excl_min_excl_max",
        ),
        pytest.param(20, [21, 99], {"multiple_of": 5}, id="int_multiple_of"),
    ],
)
def test_int(test_value, error_values, kwargs):
    class TestModel(middle.Model):
        age = middle.field(type=int, **kwargs)

    inst = TestModel(age=test_value)

    assert isinstance(inst, TestModel)
    assert inst.age == test_value

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(age=ev)


@pytest.mark.parametrize(
    "test_value,raised_exc,kwargs",
    [
        pytest.param(
            5, TypeError, {"minimum": "foo"}, id="int_min_wrong_type"
        ),
        pytest.param(
            5, TypeError, {"maximum": "foo"}, id="int_max_wrong_type"
        ),
        pytest.param(
            4, ValueError, {"minimum": 5, "maximum": 3}, id="int_max_lt_min"
        ),
        pytest.param(
            5,
            TypeError,
            {"minimum": 3, "exclusive_minimum": "foo"},
            id="int_min_exclusive_wrong_type",
        ),
        pytest.param(
            5,
            TypeError,
            {"maximum": 6, "exclusive_maximum": "foo"},
            id="int_max_exclusive_wrong_type",
        ),
        pytest.param(
            5,
            TypeError,
            {"maximum": 6, "multiple_of": "foo"},
            id="int_multiple_of_wrong_type",
        ),
        pytest.param(
            5,
            ValueError,
            {"maximum": 6, "multiple_of": -2},
            id="int_multiple_of_negative",
        ),
    ],
)
def test_int_errors(test_value, raised_exc, kwargs):
    class TestModel(middle.Model):
        value = middle.field(type=int, **kwargs)

    with pytest.raises(raised_exc):
        TestModel(value=test_value)


# #############################################################################
# float


@pytest.mark.parametrize(
    "test_value,error_values,kwargs",
    [
        pytest.param(1.0, [0.9, 0.99], {"minimum": 1.0}, id="float_min"),
        pytest.param(
            1.01,
            [1.0, 0.999],
            {"minimum": 1.0, "exclusive_minimum": True},
            id="float_excl_min",
        ),
        pytest.param(1.0, [1.01, 1.1], {"maximum": 1.0}, id="float_max"),
        pytest.param(
            0.999,
            [1.0, 1.001],
            {"maximum": 1.0, "exclusive_maximum": True},
            id="float_excl_max",
        ),
        pytest.param(
            0.5,
            [-0.01, 1.001],
            {"minimum": 0.0, "maximum": 1.0},
            id="float_min_max",
        ),
        pytest.param(
            0.5,
            [-0.01, 0.0, 1.1],
            {"minimum": 0.0, "exclusive_minimum": True, "maximum": 1.0},
            id="float_excl_min_max",
        ),
        pytest.param(
            0.5,
            [-0.01, 1.0, 1.001],
            {"minimum": 0.0, "maximum": 1.0, "exclusive_maximum": True},
            id="float_min_excl_max",
        ),
        pytest.param(
            0.5,
            [0.0, 1.0],
            {
                "minimum": 0.0,
                "exclusive_minimum": True,
                "maximum": 1.0,
                "exclusive_maximum": True,
            },
            id="float_excl_min_excl_max",
        ),
        pytest.param(
            3.3, [2.21, 99.3], {"multiple_of": 1.1}, id="float_multiple_of"
        ),
    ],
)
def test_float(test_value, error_values, kwargs):
    class TestModel(middle.Model):
        age = middle.field(type=float, **kwargs)

    inst = TestModel(age=test_value)

    assert isinstance(inst, TestModel)
    assert inst.age == test_value

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(age=ev)


@pytest.mark.parametrize(
    "test_value,raised_exc,kwargs",
    [
        pytest.param(
            5.4, TypeError, {"minimum": "foo"}, id="float_min_wrong_type"
        ),
        pytest.param(
            5.4, TypeError, {"maximum": "foo"}, id="float_max_wrong_type"
        ),
        pytest.param(
            4.5,
            ValueError,
            {"minimum": 5.5, "maximum": 3.2},
            id="float_max_lt_min",
        ),
        pytest.param(
            5.0,
            TypeError,
            {"minimum": 3.2, "exclusive_minimum": "foo"},
            id="float_min_exclusive_wrong_type",
        ),
        pytest.param(
            5.1,
            TypeError,
            {"maximum": 6.7, "exclusive_maximum": "foo"},
            id="float_max_exclusive_wrong_type",
        ),
        pytest.param(
            5.5,
            TypeError,
            {"maximum": 6.8, "multiple_of": "foo"},
            id="float_multiple_of_wrong_type",
        ),
        pytest.param(
            5.5,
            ValueError,
            {"maximum": 6.9, "multiple_of": -0.5},
            id="float_multiple_of_negative",
        ),
    ],
)
def test_float_errors(test_value, raised_exc, kwargs):
    class TestModel(middle.Model):
        value = middle.field(type=float, **kwargs)

    with pytest.raises(raised_exc):
        TestModel(value=test_value)


# #############################################################################
# List


@pytest.mark.parametrize(
    "list_type,test_values,error_values,kwargs",
    [
        pytest.param(
            List[int],
            [0, 1, 2, 3],
            [[0, 1], []],
            {"min_items": 3},
            id="list_min_items",
        ),
        pytest.param(
            List[str],
            ["foo", "bar"],
            [["foo", "bar", "baz", "wee"]],
            {"max_items": 3},
            id="list_max_items",
        ),
        pytest.param(
            List[float],
            [1.0, 1.5, 2.0],
            [[1.0, 1.2, 1.4, 1.2, 1.5]],
            {"unique_items": True},
            id="list_unique_items",
        ),
        pytest.param(
            List[float],
            [1.0, 1.5, 2.0],
            [],
            {"unique_items": False},
            id="list_unique_items_false",
        ),
        pytest.param(
            List[str],
            ["foo", "bar", "baz"],
            [["foo", "bar"], ["foo", "bar", "baz", "FOO", "BAR"]],
            {"min_items": 3, "max_items": 4},
            id="list_min_max_items",
        ),
    ],
)
def test_list(list_type, test_values, error_values, kwargs):
    class TestModel(middle.Model):
        values = middle.field(type=list_type, **kwargs)

    inst = TestModel(values=test_values)

    assert isinstance(inst, TestModel)
    assert inst.values == test_values

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(values=ev)


@pytest.mark.parametrize(
    "test_value,raised_exc,kwargs",
    [
        pytest.param(
            ["foo", "bar"],
            TypeError,
            {"min_items": "foo"},
            id="list_min_wrong_type",
        ),
        pytest.param(
            ["foo", "bar"],
            TypeError,
            {"max_items": "foo"},
            id="list_max_wrong_type",
        ),
        pytest.param(
            ["foo", "bar"],
            ValueError,
            {"min_items": 5, "max_items": 3},
            id="list_max_lt_min",
        ),
        pytest.param(
            ["foo", "bar"],
            TypeError,
            {"min_items": 1, "unique_items": "foo"},
            id="list_min_unique_wrong_type",
        ),
        pytest.param(
            ["foo", "bar"],
            TypeError,
            {"max_items": 6, "unique_items": "foo"},
            id="list_max_unique_wrong_type",
        ),
        pytest.param(
            ["foo", "bar"],
            ValueError,
            {"min_items": -6},
            id="list_min_negative",
        ),
        pytest.param(
            ["foo", "bar"],
            ValueError,
            {"max_items": -6},
            id="list_max_negative",
        ),
    ],
)
def test_list_errors(test_value, raised_exc, kwargs):
    class TestModel(middle.Model):
        value = middle.field(type=List[str], **kwargs)

    with pytest.raises(raised_exc):
        TestModel(value=test_value)


# #############################################################################
# Set


@pytest.mark.parametrize(
    "set_type,test_values,error_values,kwargs",
    [
        pytest.param(
            Set[int],
            {0, 1, 2, 3},
            [{0, 1}, {}],
            {"min_items": 3},
            id="set_min_items",
        ),
        pytest.param(
            Set[str],
            {"foo", "bar"},
            [{"foo", "bar", "baz", "wee"}],
            {"max_items": 3},
            id="set_max_items",
        ),
        pytest.param(
            Set[float],
            {1.0, 1.5, 2.0},
            [],
            {"unique_items": True},
            id="set_unique_items",
        ),
        pytest.param(
            Set[str],
            {"foo", "bar", "baz"},
            [{"foo", "bar"}, {"foo", "bar", "baz", "FOO", "BAR"}],
            {"min_items": 3, "max_items": 4},
            id="set_min_max_items",
        ),
    ],
)
def test_set(set_type, test_values, error_values, kwargs):
    class TestModel(middle.Model):
        values = middle.field(type=set_type, **kwargs)

    inst = TestModel(values=test_values)

    assert isinstance(inst, TestModel)
    assert inst.values == test_values

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(values=ev)


@pytest.mark.parametrize(
    "test_value,raised_exc,kwargs",
    [
        pytest.param(
            {"bar", "foo"},
            TypeError,
            {"min_items": "foo"},
            id="set_min_wrong_type",
        ),
        pytest.param(
            {"bar", "foo"},
            TypeError,
            {"max_items": "foo"},
            id="set_max_wrong_type",
        ),
        pytest.param(
            {"bar", "foo"},
            ValueError,
            {"min_items": 5, "max_items": 3},
            id="set_max_lt_min",
        ),
        pytest.param(
            {"bar", "foo"},
            TypeError,
            {"min_items": 1, "unique_items": "foo"},
            id="set_min_unique_wrong_type",
        ),
        pytest.param(
            {"bar", "foo"},
            TypeError,
            {"max_items": 6, "unique_items": "foo"},
            id="set_max_unique_wrong_type",
        ),
        pytest.param(
            {"bar", "foo"},
            ValueError,
            {"min_items": -6},
            id="set_min_negative",
        ),
        pytest.param(
            {"bar", "foo"},
            ValueError,
            {"max_items": -6},
            id="set_max_negative",
        ),
    ],
)
def test_set_errors(test_value, raised_exc, kwargs):
    class TestModel(middle.Model):
        value = middle.field(type=Set[str], **kwargs)

    with pytest.raises(raised_exc):
        TestModel(value=test_value)


# #############################################################################
# Dict


@pytest.mark.parametrize(
    "dict_type,test_values,error_values,kwargs",
    [
        pytest.param(
            Dict[int, str],
            {0: "hello", 1: "world", 2: "foo", 3: "bar"},
            [{0: "hello", 1: "world"}, {}],
            {"min_properties": 3},
            id="dict_min_properties",
        ),
        pytest.param(
            Dict[str, int],
            {"foo": 1, "bar": 2},
            [{"foo": 1, "bar": 2, "baz": 3, "wee": 4}],
            {"max_properties": 3},
            id="dict_max_properties",
        ),
        pytest.param(
            Dict[str, float],
            {"foo": 1.0, "bar": 1.1, "baz": 1.2},
            [
                {"foo": 0.0, "bar": 0.2},
                {"foo": 1.1, "bar": 1.3, "baz": 1.7, "FOO": 1.8, "BAR": 2.1},
            ],
            {"min_properties": 3, "max_properties": 4},
            id="dict_min_max_properties",
        ),
    ],
)
def test_dict(dict_type, test_values, error_values, kwargs):
    class TestModel(middle.Model):
        values = middle.field(type=dict_type, **kwargs)

    inst = TestModel(values=test_values)

    assert isinstance(inst, TestModel)
    assert inst.values == test_values

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(values=ev)


@pytest.mark.parametrize(
    "test_value,raised_exc,kwargs",
    [
        pytest.param(
            {"bar": "foo"},
            TypeError,
            {"min_properties": "foo"},
            id="dict_min_wrong_type",
        ),
        pytest.param(
            {"bar": "foo"},
            TypeError,
            {"max_properties": "foo"},
            id="dict_max_wrong_type",
        ),
        pytest.param(
            {"bar": "foo"},
            ValueError,
            {"min_properties": 5, "max_properties": 3},
            id="dict_max_lt_min",
        ),
        pytest.param(
            {"bar": "foo"},
            ValueError,
            {"min_properties": -6},
            id="dict_min_negative",
        ),
        pytest.param(
            {"bar": "foo"},
            ValueError,
            {"max_properties": -6},
            id="dict_max_negative",
        ),
    ],
)
def test_dict_errors(test_value, raised_exc, kwargs):
    class TestModel(middle.Model):
        value = middle.field(type=Dict[str, str], **kwargs)

    with pytest.raises(raised_exc):
        TestModel(value=test_value)
