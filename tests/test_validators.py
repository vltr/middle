# from typing import Collection
# from typing import Mapping
# from typing import MutableMapping
# from typing import MutableSequence
# from typing import MutableSet
# from typing import Sequence
# from typing import FrozenSet
# from typing import Iterable
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


# #############################################################################
# List, Sequence, Collection, Iterable, MutableSequence


@pytest.mark.parametrize(
    "list_types,test_values,error_values,kwargs",
    [
        pytest.param(
            [
                # Collection[int],
                # Iterable[int],
                List[int],
                # MutableSequence[int],
                # Sequence[int],
            ],
            [0, 1, 2, 3],
            [[0, 1], []],
            {"min_items": 3},
            id="list_min_items",
        ),
        pytest.param(
            [
                # Collection[str],
                # Iterable[str],
                List[str],
                # MutableSequence[str],
                # Sequence[str],
            ],
            ["foo", "bar"],
            [["foo", "bar", "baz", "wee"]],
            {"max_items": 3},
            id="list_max_items",
        ),
        pytest.param(
            [
                # Collection[float],
                # Iterable[float],
                List[float],
                # MutableSequence[float],
                # Sequence[float],
            ],
            [1.0, 1.5, 2.0],
            [[1.0, 1.2, 1.4, 1.2, 1.5]],
            {"unique_items": True},
            id="list_unique_items",
        ),
        pytest.param(
            [
                # Collection[float],
                # Iterable[float],
                List[float],
                # MutableSequence[float],
                # Sequence[float],
            ],
            [1.0, 1.5, 2.0],
            [],
            {"unique_items": False},
            id="list_unique_items_false",
        ),
        pytest.param(
            [
                # Collection[str],
                # Iterable[str],
                List[str],
                # MutableSequence[str],
                # Sequence[str],
            ],
            ["foo", "bar", "baz"],
            [["foo", "bar"], ["foo", "bar", "baz", "FOO", "BAR"]],
            {"min_items": 3, "max_items": 4},
            id="list_min_max_items",
        ),
    ],
)
def test_list(list_types, test_values, error_values, kwargs):
    for list_type in list_types:

        class TestModel(middle.Model):
            values = middle.field(type=list_type, **kwargs)

        inst = TestModel(values=test_values)

        assert isinstance(inst, TestModel)
        assert inst.values == test_values

        for ev in error_values:
            with pytest.raises(ValidationError):
                TestModel(values=ev)


# #############################################################################
# Set, MutableSet, FrozenSet


@pytest.mark.parametrize(
    "set_types,test_values,error_values,kwargs",
    [
        pytest.param(
            [Set[int]],  # MutableSet[int], FrozenSet[int]],
            {0, 1, 2, 3},
            [{0, 1}, {}],
            {"min_items": 3},
            id="set_min_items",
        ),
        pytest.param(
            [Set[str]],  # MutableSet[str], FrozenSet[str]],
            {"foo", "bar"},
            [{"foo", "bar", "baz", "wee"}],
            {"max_items": 3},
            id="set_max_items",
        ),
        pytest.param(
            [Set[float]],  # MutableSet[float], FrozenSet[float]],
            {1.0, 1.5, 2.0},
            [],
            {"unique_items": True},
            id="set_unique_items",
        ),
        pytest.param(
            [Set[str]],  # MutableSet[str], FrozenSet[str]],
            {"foo", "bar", "baz"},
            [{"foo", "bar"}, {"foo", "bar", "baz", "FOO", "BAR"}],
            {"min_items": 3, "max_items": 4},
            id="set_min_max_items",
        ),
    ],
)
def test_set(set_types, test_values, error_values, kwargs):
    for set_type in set_types:

        class TestModel(middle.Model):
            values = middle.field(type=set_type, **kwargs)

        inst = TestModel(values=test_values)

        assert isinstance(inst, TestModel)
        assert inst.values == test_values

        for ev in error_values:
            with pytest.raises(ValidationError):
                TestModel(values=ev)


# #############################################################################
# Dict, Mapping, MutableMapping


@pytest.mark.parametrize(
    "dict_types,test_values,error_values,kwargs",
    [
        pytest.param(
            [Dict[int, str]],  # Mapping[int, str], MutableMapping[int, str]],
            {0: "hello", 1: "world", 2: "foo", 3: "bar"},
            [{0: "hello", 1: "world"}, {}],
            {"min_properties": 3},
            id="dict_min_properties",
        ),
        pytest.param(
            [Dict[str, int]],  # Mapping[str, int], MutableMapping[str, int]],
            {"foo": 1, "bar": 2},
            [{"foo": 1, "bar": 2, "baz": 3, "wee": 4}],
            {"max_properties": 3},
            id="dict_max_properties",
        ),
        pytest.param(
            [
                Dict[str, float],
                # Mapping[str, float],
                # MutableMapping[str, float],
            ],
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
def test_dict(dict_types, test_values, error_values, kwargs):
    for dict_type in dict_types:

        class TestModel(middle.Model):
            values = middle.field(type=dict_type, **kwargs)

        inst = TestModel(values=test_values)

        assert isinstance(inst, TestModel)
        assert inst.values == test_values

        for ev in error_values:
            with pytest.raises(ValidationError):
                TestModel(values=ev)
