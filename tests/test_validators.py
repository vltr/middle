import re
from typing import Dict
from typing import List
from typing import Set

import attr
import pytest
from attr._make import _AndValidator
from attr.validators import _InstanceOfValidator

import middle
from middle.exceptions import ValidationError
from middle.validators import BaseValidator

# #############################################################################
# str


@pytest.mark.parametrize(
    "test_value,error_values,kwargs,descriptor",
    [
        pytest.param(
            "foo",
            ["fo", ""],
            {"min_length": 3},
            {"min_length": 3},
            id="str_min",
        ),
        pytest.param("", [], {"min_length": None}, {}, id="str_min_none"),
        pytest.param(
            "foo",
            ["foobar", "      "],
            {"max_length": 5},
            {"max_length": 5},
            id="str_max",
        ),
        pytest.param("", [], {"max_length": None}, {}, id="str_max_none"),
        pytest.param(
            "foo",
            ["fo", "foobar"],
            {"min_length": 3, "max_length": 5},
            {"min_length": 3, "max_length": 5},
            id="str_min_max",
        ),
        pytest.param(
            "foo",
            [],
            {"min_length": None, "max_length": None},
            {},
            id="str_min_max_none",
        ),
        pytest.param(
            "foo",
            ["fo1", " foo "],
            {"pattern": "^[a-z]+$"},
            {"pattern": "^[a-z]+$"},
            id="str_pattern",
        ),
        pytest.param("foo", [], {"pattern": None}, {}, id="str_pattern_none"),
        pytest.param(
            "foo",
            ["fo1", " foo "],
            {"pattern": re.compile("^[a-z]+$")},
            {"pattern": "^[a-z]+$"},
            id="str_re_object",
        ),
    ],
)
def test_str(test_value, error_values, kwargs, descriptor):
    class TestModel(middle.Model):
        name = middle.field(type=str, **kwargs)

    inst = TestModel(name=test_value)

    assert isinstance(inst, TestModel)
    assert inst.name == test_value

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(name=ev)

    for field in attr.fields(TestModel):  # noqa
        if field.name == "name":
            if isinstance(field.validator, _AndValidator):
                for validator in field.validator._validators:
                    if isinstance(validator, BaseValidator):
                        assert validator.descriptor == descriptor
                    elif isinstance(validator, _InstanceOfValidator):
                        assert validator.type == str
            else:
                if isinstance(field.validator, BaseValidator):
                    assert field.validator.descriptor == descriptor
                elif (field.validator, _InstanceOfValidator):
                    assert field.validator.type == str


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
    with pytest.raises(raised_exc):

        class TestModel(middle.Model):
            name = middle.field(type=str, **kwargs)


def test_str_with_default():
    class TestModel(middle.Model):
        name = middle.field(type=str, max_length=5, default="Hello")

    class TestNoneModel(middle.Model):
        name = middle.field(type=str, max_length=5, default=None)

    assert TestModel().name == "Hello"
    assert TestModel(name="foo").name == "foo"
    assert TestNoneModel().name is None
    assert TestNoneModel(name="foo").name == "foo"

    with pytest.raises(ValidationError):
        TestModel(name="foobar")

    with pytest.raises(TypeError):
        TestModel(name=None)

    with pytest.raises(ValidationError):
        TestNoneModel(name="foobar")


# #############################################################################
# int


@pytest.mark.parametrize(
    "test_value,error_values,kwargs,descriptor",
    [
        pytest.param(
            20,
            [19, 18],
            {"minimum": 20, "maximum": None},
            {"minimum": 20},
            id="int_min",
        ),
        pytest.param(
            21,
            [20, 19],
            {
                "minimum": 20,
                "exclusive_minimum": True,
                "exclusive_maximum": False,
            },
            {"minimum": 20, "exclusive_minimum": True},
            id="int_excl_min",
        ),
        pytest.param(
            20, [21, 22], {"maximum": 20}, {"maximum": 20}, id="int_max"
        ),
        pytest.param(
            19,
            [20, 21],
            {"maximum": 20, "exclusive_maximum": True, "minimum": None},
            {"maximum": 20, "exclusive_maximum": True},
            id="int_excl_max",
        ),
        pytest.param(
            15,
            [9, 21],
            {
                "minimum": 10,
                "maximum": 20,
                "exclusive_maximum": False,
                "exclusive_minimum": False,
            },
            {"minimum": 10, "maximum": 20},
            id="int_min_max",
        ),
        pytest.param(
            15,
            [10, 21],
            {
                "minimum": 10,
                "exclusive_minimum": True,
                "maximum": 20,
                "exclusive_maximum": False,
            },
            {"minimum": 10, "exclusive_minimum": True, "maximum": 20},
            id="int_excl_min_max",
        ),
        pytest.param(
            15,
            [9, 20],
            {
                "minimum": 10,
                "maximum": 20,
                "exclusive_maximum": True,
                "exclusive_minimum": False,
            },
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
                "multiple_of": None,
            },
            {
                "minimum": 10,
                "exclusive_minimum": True,
                "maximum": 20,
                "exclusive_maximum": True,
            },
            id="int_excl_min_excl_max",
        ),
        pytest.param(
            20,
            [21, 99],
            {"multiple_of": 5},
            {"multiple_of": 5},
            id="int_multiple_of",
        ),
    ],
)
def test_int(test_value, error_values, kwargs, descriptor):
    class TestModel(middle.Model):
        age = middle.field(type=int, **kwargs)

    inst = TestModel(age=test_value)

    assert isinstance(inst, TestModel)
    assert inst.age == test_value

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(age=ev)

    for field in attr.fields(TestModel):  # noqa
        if field.name == "age":
            if isinstance(field.validator, _AndValidator):
                for validator in field.validator._validators:
                    if isinstance(validator, BaseValidator):
                        assert validator.descriptor == descriptor
                    elif isinstance(validator, _InstanceOfValidator):
                        assert validator.type == int
            else:
                if isinstance(field.validator, BaseValidator):
                    assert field.validator.descriptor == descriptor
                elif (field.validator, _InstanceOfValidator):
                    assert field.validator.type == int


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
    with pytest.raises(raised_exc):

        class TestModel(middle.Model):
            value = middle.field(type=int, **kwargs)


def test_int_with_default():
    class TestModel(middle.Model):
        value = middle.field(type=int, maximum=5, default=3)

    class TestNoneModel(middle.Model):
        value = middle.field(type=int, maximum=5, default=None)

    assert TestModel().value == 3
    assert TestModel(value=2).value == 2
    assert TestNoneModel().value is None
    assert TestNoneModel(value=2).value == 2

    with pytest.raises(ValidationError):
        TestModel(value=6)

    with pytest.raises(TypeError):
        TestModel(value=None)

    with pytest.raises(ValidationError):
        TestNoneModel(value=6)


# #############################################################################
# float


@pytest.mark.parametrize(
    "test_value,error_values,kwargs,descriptor",
    [
        pytest.param(
            1.0,
            [0.9, 0.99],
            {"minimum": 1.0, "maximum": None, "exclusive_minimum": False},
            {"minimum": 1.0},
            id="float_min",
        ),
        pytest.param(
            1.01,
            [1.0, 0.999],
            {"minimum": 1.0, "exclusive_minimum": True, "maximum": None},
            {"minimum": 1.0, "exclusive_minimum": True},
            id="float_excl_min",
        ),
        pytest.param(
            1.0,
            [1.01, 1.1],
            {"maximum": 1.0, "minimum": None, "exclusive_maximum": False},
            {"maximum": 1.0},
            id="float_max",
        ),
        pytest.param(
            0.999,
            [1.0, 1.001],
            {
                "maximum": 1.0,
                "exclusive_maximum": True,
                "exclusive_minimum": False,
            },
            {"maximum": 1.0, "exclusive_maximum": True},
            id="float_excl_max",
        ),
        pytest.param(
            0.5,
            [-0.01, 1.001],
            {"minimum": 0.0, "maximum": 1.0, "multiple_of": None},
            {"minimum": 0.0, "maximum": 1.0},
            id="float_min_max",
        ),
        pytest.param(
            0.5,
            [-0.01, 0.0, 1.1],
            {
                "minimum": 0.0,
                "exclusive_minimum": True,
                "maximum": 1.0,
                "exclusive_maximum": False,
            },
            {"minimum": 0.0, "exclusive_minimum": True, "maximum": 1.0},
            id="float_excl_min_max",
        ),
        pytest.param(
            0.5,
            [-0.01, 1.0, 1.001],
            {
                "minimum": 0.0,
                "maximum": 1.0,
                "exclusive_maximum": True,
                "exclusive_minimum": False,
                "multiple_of": None,
            },
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
                "multiple_of": None,
            },
            {
                "minimum": 0.0,
                "exclusive_minimum": True,
                "maximum": 1.0,
                "exclusive_maximum": True,
            },
            id="float_excl_min_excl_max",
        ),
        pytest.param(
            3.3,
            [2.21, 99.3],
            {"multiple_of": 1.1, "exclusive_minimum": False},
            {"multiple_of": 1.1},
            id="float_multiple_of",
        ),
    ],
)
def test_float(test_value, error_values, kwargs, descriptor):
    class TestModel(middle.Model):
        age = middle.field(type=float, **kwargs)

    inst = TestModel(age=test_value)

    assert isinstance(inst, TestModel)
    assert inst.age == test_value

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(age=ev)

    for field in attr.fields(TestModel):  # noqa
        if field.name == "age":
            if isinstance(field.validator, _AndValidator):
                for validator in field.validator._validators:
                    if isinstance(validator, BaseValidator):
                        assert validator.descriptor == descriptor
                    elif isinstance(validator, _InstanceOfValidator):
                        assert validator.type == float
            else:
                if isinstance(field.validator, BaseValidator):
                    assert field.validator.descriptor == descriptor
                elif (field.validator, _InstanceOfValidator):
                    assert field.validator.type == float


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
    with pytest.raises(raised_exc):

        class TestModel(middle.Model):
            value = middle.field(type=float, **kwargs)


def test_float_with_default():
    class TestModel(middle.Model):
        value = middle.field(type=float, maximum=5.8, default=4.9)

    class TestNoneModel(middle.Model):
        value = middle.field(type=float, maximum=5.8, default=None)

    assert TestModel().value == 4.9
    assert TestModel(value=2.5).value == 2.5
    assert TestNoneModel().value is None
    assert TestNoneModel(value=2.5).value == 2.5

    with pytest.raises(ValidationError):
        TestModel(value=5.9)

    with pytest.raises(TypeError):
        TestModel(value=None)

    with pytest.raises(ValidationError):
        TestNoneModel(value=5.9)


# #############################################################################
# List


@pytest.mark.parametrize(
    "list_type,test_values,error_values,kwargs,descriptor",
    [
        pytest.param(
            List[int],
            [0, 1, 2, 3],
            [[0, 1], []],
            {"min_items": 3, "max_items": None},
            {"min_items": 3},
            id="list_min_items",
        ),
        pytest.param(
            List[str],
            ["foo", "bar"],
            [["foo", "bar", "baz", "wee"]],
            {"max_items": 3, "unique_items": False},
            {"max_items": 3},
            id="list_max_items",
        ),
        pytest.param(
            List[float],
            [1.0, 1.5, 2.0],
            [[1.0, 1.2, 1.4, 1.2, 1.5]],
            {"unique_items": True, "max_items": None, "min_items": None},
            {"unique_items": True},
            id="list_unique_items",
        ),
        pytest.param(
            List[float],
            [1.0, 1.5, 2.0],
            [],
            {"unique_items": False},
            {},
            id="list_unique_items_false",
        ),
        pytest.param(
            List[str],
            ["foo", "bar", "baz"],
            [["foo", "bar"], ["foo", "bar", "baz", "FOO", "BAR"]],
            {"min_items": 3, "max_items": 4, "unique_items": False},
            {"min_items": 3, "max_items": 4},
            id="list_min_max_items",
        ),
    ],
)
def test_list(list_type, test_values, error_values, kwargs, descriptor):
    class TestModel(middle.Model):
        values = middle.field(type=list_type, **kwargs)

    inst = TestModel(values=test_values)

    assert isinstance(inst, TestModel)
    assert inst.values == test_values

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(values=ev)

    for field in attr.fields(TestModel):  # noqa
        if field.name == "values":
            if isinstance(field.validator, _AndValidator):
                for validator in field.validator._validators:
                    if isinstance(validator, BaseValidator):
                        assert validator.descriptor == descriptor
                    elif isinstance(validator, _InstanceOfValidator):
                        assert validator.type == list
            else:
                if isinstance(field.validator, BaseValidator):
                    assert field.validator.descriptor == descriptor
                elif (field.validator, _InstanceOfValidator):
                    assert field.validator.type == list


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
    with pytest.raises(raised_exc):

        class TestModel(middle.Model):
            value = middle.field(type=List[str], **kwargs)


def test_list_with_default():
    class TestModel(middle.Model):
        value = middle.field(type=List[int], max_items=3, default=[2, 3])

    class TestNoneModel(middle.Model):
        value = middle.field(type=List[int], max_items=3, default=None)

    assert TestModel().value == [2, 3]
    assert TestModel(value=[3, 4]).value == [3, 4]
    assert TestNoneModel().value is None
    assert TestNoneModel(value=[3, 4]).value == [3, 4]

    with pytest.raises(ValidationError):
        TestModel(value=[2, 3, 4, 5, 6])

    with pytest.raises(TypeError):
        TestModel(value=None)

    with pytest.raises(ValidationError):
        TestNoneModel(value=[2, 3, 4, 5, 6])


# #############################################################################
# Set


@pytest.mark.parametrize(
    "set_type,test_values,error_values,kwargs,descriptor",
    [
        pytest.param(
            Set[int],
            {0, 1, 2, 3},
            [{0, 1}, {}],
            {"min_items": 3, "max_items": None},
            {"min_items": 3},
            id="set_min_items",
        ),
        pytest.param(
            Set[str],
            {"foo", "bar"},
            [{"foo", "bar", "baz", "wee"}],
            {"max_items": 3, "min_items": None},
            {"max_items": 3},
            id="set_max_items",
        ),
        pytest.param(
            Set[float],
            {1.0, 1.5, 2.0},
            [],
            {"unique_items": True, "max_items": None},
            {"unique_items": True},
            id="set_unique_items",
        ),
        pytest.param(
            Set[str],
            {"foo", "bar", "baz"},
            [{"foo", "bar"}, {"foo", "bar", "baz", "FOO", "BAR"}],
            {"min_items": 3, "max_items": 4, "unique_items": False},
            {"min_items": 3, "max_items": 4},
            id="set_min_max_items",
        ),
    ],
)
def test_set(set_type, test_values, error_values, kwargs, descriptor):
    class TestModel(middle.Model):
        values = middle.field(type=set_type, **kwargs)

    inst = TestModel(values=test_values)

    assert isinstance(inst, TestModel)
    assert inst.values == test_values

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(values=ev)

    for field in attr.fields(TestModel):  # noqa
        if field.name == "values":
            if isinstance(field.validator, _AndValidator):
                for validator in field.validator._validators:
                    if isinstance(validator, BaseValidator):
                        assert validator.descriptor == descriptor
                    elif isinstance(validator, _InstanceOfValidator):
                        assert validator.type == set
            else:
                if isinstance(field.validator, BaseValidator):
                    assert field.validator.descriptor == descriptor
                elif (field.validator, _InstanceOfValidator):
                    assert field.validator.type == set


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
    with pytest.raises(raised_exc):

        class TestModel(middle.Model):
            value = middle.field(type=Set[str], **kwargs)


def test_set_with_default():
    class TestModel(middle.Model):
        value = middle.field(type=Set[int], max_items=3, default={2, 3})

    class TestNoneModel(middle.Model):
        value = middle.field(type=Set[int], max_items=3, default=None)

    assert TestModel().value == {2, 3}
    assert TestModel(value=[3, 4]).value == {3, 4}
    assert TestNoneModel().value is None
    assert TestNoneModel(value=[3, 4]).value == {3, 4}

    with pytest.raises(ValidationError):
        TestModel(value=[2, 3, 4, 5, 6])

    with pytest.raises(TypeError):
        TestModel(value=None)

    with pytest.raises(ValidationError):
        TestNoneModel(value=[2, 3, 4, 5, 6])


# #############################################################################
# Dict


@pytest.mark.parametrize(
    "dict_type,test_values,error_values,kwargs,descriptor",
    [
        pytest.param(
            Dict[int, str],
            {0: "hello", 1: "world", 2: "foo", 3: "bar"},
            [{0: "hello", 1: "world"}, {}],
            {"min_properties": 3, "max_properties": None},
            {"min_properties": 3},
            id="dict_min_properties",
        ),
        pytest.param(
            Dict[str, int],
            {"foo": 1, "bar": 2},
            [{"foo": 1, "bar": 2, "baz": 3, "wee": 4}],
            {"max_properties": 3, "min_properties": None},
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
            {"min_properties": 3, "max_properties": 4},
            id="dict_min_max_properties",
        ),
    ],
)
def test_dict(dict_type, test_values, error_values, kwargs, descriptor):
    class TestModel(middle.Model):
        values = middle.field(type=dict_type, **kwargs)

    inst = TestModel(values=test_values)

    assert isinstance(inst, TestModel)
    assert inst.values == test_values

    for ev in error_values:
        with pytest.raises(ValidationError):
            TestModel(values=ev)

    for field in attr.fields(TestModel):  # noqa
        if field.name == "values":
            if isinstance(field.validator, _AndValidator):
                for validator in field.validator._validators:
                    if isinstance(validator, BaseValidator):
                        assert validator.descriptor == descriptor
                    elif isinstance(validator, _InstanceOfValidator):
                        assert validator.type == dict
            else:
                if isinstance(field.validator, BaseValidator):
                    assert field.validator.descriptor == descriptor
                elif (field.validator, _InstanceOfValidator):
                    assert field.validator.type == dict


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
    with pytest.raises(raised_exc):

        class TestModel(middle.Model):
            value = middle.field(type=Dict[str, str], **kwargs)


def test_dict_with_default():
    class TestModel(middle.Model):
        value = middle.field(
            type=Dict[str, int],
            min_properties=1,
            max_properties=2,
            default={"hello": 1},
        )

    class TestNoneModel(middle.Model):
        value = middle.field(
            type=Dict[str, int],
            min_properties=1,
            max_properties=2,
            default=None,
        )

    assert TestModel().value == {"hello": 1}
    assert TestModel(value={"bar": 2, "baz": 3}).value == {"bar": 2, "baz": 3}
    assert TestNoneModel().value is None
    assert TestNoneModel(value={"bar": 2, "baz": 3}).value == {
        "bar": 2,
        "baz": 3,
    }

    with pytest.raises(ValidationError):
        TestModel(value={"bar": 2, "baz": 3, "foo": 4})

    with pytest.raises(TypeError):
        TestModel(value=None)

    with pytest.raises(ValidationError):
        TestNoneModel(value={"bar": 2, "baz": 3, "foo": 4})
