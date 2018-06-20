from datetime import date
from datetime import datetime
from datetime import timezone
from enum import Enum
from enum import IntEnum
from enum import unique

import pytest

from middle import schema
from middle import utils

# from enum import EnumMeta
# from functools import partial, singledispatch
# from typing import (
#     Collection,
#     Dict,
#     FrozenSet,
#     GenericMeta,
#     Iterable,
#     List,
#     Mapping,
#     MutableMapping,
#     MutableSequence,
#     MutableSet,
#     Sequence,
#     Set,
# )


# #############################################################################
# str


def test_str_working():
    class TestModel(schema.Model):
        name: str = schema.field()

    inst = TestModel(name="some str")

    assert isinstance(inst, TestModel)
    assert inst.name == "some str"

    data = utils.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("name", None) == "some str"


def test_str_converter():
    class TestModel(schema.Model):
        name: str = schema.field()

    inst = TestModel(name=1)
    assert isinstance(inst, TestModel)
    assert inst.name == "1"


# #############################################################################
# int


def test_int_working():
    class TestModel(schema.Model):
        age: int = schema.field()

    inst = TestModel(age=42)

    assert isinstance(inst, TestModel)
    assert inst.age == 42

    data = utils.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("age", None) == 42


def test_int_converter():
    class TestModel(schema.Model):
        age: int = schema.field()

    inst = TestModel(age="42")
    assert isinstance(inst, TestModel)
    assert inst.age == 42


# #############################################################################
# float


def test_float_working():
    class TestModel(schema.Model):
        const: float = schema.field()

    inst = TestModel(const=3.14)

    assert isinstance(inst, TestModel)
    assert inst.const == 3.14

    data = utils.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("const", None) == 3.14


def test_float_converter():
    class TestModel(schema.Model):
        const: float = schema.field()

    inst = TestModel(const="3.14")
    assert isinstance(inst, TestModel)
    assert inst.const == 3.14


# #############################################################################
# bool


def test_bool_working():
    class TestModel(schema.Model):
        broken: bool = schema.field()

    inst = TestModel(broken=True)

    assert isinstance(inst, TestModel)
    assert inst.broken is True

    data = utils.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("broken", False) is True


def test_bool_converter():
    class TestModel(schema.Model):
        broken: bool = schema.field()

    # everything must be true
    assert TestModel(broken="True").broken is True
    assert TestModel(broken="true").broken is True
    assert TestModel(broken="yes").broken is True
    assert TestModel(broken="TRUE").broken is True
    assert TestModel(broken="YES").broken is True
    assert TestModel(broken=1).broken is True
    assert TestModel(broken=10).broken is True
    assert TestModel(broken=1.5).broken is True
    assert TestModel(broken=3.14).broken is True

    # now, everything must be false
    assert TestModel(broken="foo").broken is False
    assert TestModel(broken="BAR").broken is False
    assert TestModel(broken="False").broken is False
    assert TestModel(broken="NO").broken is False
    assert TestModel(broken=0).broken is False
    assert TestModel(broken=-1).broken is False
    assert TestModel(broken=-1.5).broken is False
    assert TestModel(broken=0.0).broken is False

    with pytest.raises(TypeError):
        TestModel(broken={"hello": "world"})


# #############################################################################
# date


def test_date_working():
    class TestModel(schema.Model):
        created_on: date = schema.field()

    inst = TestModel(created_on="2018-06-18")

    assert isinstance(inst, TestModel)
    assert inst.created_on == date(2018, 6, 18)

    data = utils.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("created_on", None) == "2018-06-18"


def test_date_converter():
    class TestModel(schema.Model):
        created_on: date = schema.field()

    test_date = date(2018, 6, 18)

    assert TestModel(created_on="2018-06-18").created_on == test_date
    assert TestModel(created_on=date(2018, 6, 18)).created_on == test_date
    assert TestModel(created_on=[2018, 6, 18]).created_on == test_date
    assert TestModel(created_on=[2018, 6, 18, 4, 3, 2]).created_on == test_date
    assert TestModel(created_on=(2018, 6, 18)).created_on == test_date
    assert TestModel(created_on=(2018, 6, 18, 4, 3, 2)).created_on == test_date
    assert TestModel(created_on=1529290800).created_on == test_date
    assert TestModel(created_on=1529290800.0).created_on == test_date

    with pytest.raises(TypeError):
        TestModel(created_on={"date": "2018-06-18", "format": "iso"})


# #############################################################################
# datetime


def test_datetime_working():
    class TestModel(schema.Model):
        ts: datetime = schema.field()

    inst = TestModel(ts="2018-06-18T13:30:00.123456+00:00")

    assert isinstance(inst, TestModel)
    assert inst.ts == datetime(2018, 6, 18, 13, 30, 0, 123456, timezone.utc)

    data = utils.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("ts", None) == "2018-06-18T13:30:00.123456+00:00"


def test_datetime_converter():
    class TestModel(schema.Model):
        ts: datetime = schema.field()

    test_datetime = datetime(2018, 6, 18, 13, 30, 0, 0, timezone.utc)

    assert TestModel(ts="2018-06-18T13:30:00.000000+00:00").ts == test_datetime
    assert (
        TestModel(ts=datetime(2018, 6, 18, 13, 30, 0, 0, timezone.utc)).ts
        == test_datetime
    )
    assert TestModel(ts=[2018, 6, 18, 13, 30, 0, 0]).ts == test_datetime
    assert TestModel(ts=(2018, 6, 18, 13, 30, 0, 0)).ts == test_datetime
    assert TestModel(ts=1529328600).ts == test_datetime
    assert TestModel(ts=1529328600.0).ts == test_datetime

    with pytest.raises(TypeError):
        TestModel(
            ts={"datetime": "2018-06-18T13:30:00.000000+0000", "format": "iso"}
        )


# #############################################################################
# enum


def test_enum_working():
    @unique
    class TestStrEnum(str, Enum):
        TEST_1 = "TEST1"
        TEST_2 = "TEST2"
        TEST_3 = "TEST3"

    @unique
    class TestIntEnum(IntEnum):
        TEST_1 = 1
        TEST_2 = 2
        TEST_3 = 3

    class TestModel(schema.Model):
        str_enum: TestStrEnum = schema.field()
        int_enum: TestIntEnum = schema.field()

    inst = TestModel(str_enum="TEST2", int_enum=3)

    assert isinstance(inst, TestModel)
    assert inst.str_enum == TestStrEnum.TEST_2
    assert inst.int_enum == TestIntEnum.TEST_3

    data = utils.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("str_enum", None) == "TEST2"
    assert data.get("int_enum", None) == 3


def test_enum_converter():
    @unique
    class TestStrEnum(str, Enum):
        TEST_1 = "TEST1"
        TEST_2 = "TEST2"
        TEST_3 = "TEST3"

    @unique
    class TestIntEnum(IntEnum):
        TEST_1 = 1
        TEST_2 = 2
        TEST_3 = 3

    class TestStrModel(schema.Model):
        str_enum: TestStrEnum = schema.field()

    class TestIntModel(schema.Model):
        int_enum: TestIntEnum = schema.field()

    test_str_enum = TestStrEnum.TEST_1
    test_int_enum = TestIntEnum.TEST_2

    assert TestStrModel(str_enum="TEST1").str_enum == test_str_enum
    assert TestStrModel(str_enum=TestStrEnum.TEST_1).str_enum == test_str_enum
    assert TestIntModel(int_enum=2).int_enum == test_int_enum
    assert TestIntModel(int_enum=TestIntEnum.TEST_2).int_enum == test_int_enum

    with pytest.raises(ValueError):
        TestStrModel(str_enum="FOO")

    with pytest.raises(ValueError):
        TestIntModel(int_enum=99)


# #############################################################################
# Model

# #############################################################################
# List

# #############################################################################
# Set

# #############################################################################
# MutableSet

# #############################################################################
# Sequence

# #############################################################################
# Collection

# #############################################################################
# Iterable

# #############################################################################
# MutableSequence

# #############################################################################
# FrozenSet

# #############################################################################
# Dict

# #############################################################################
# Mapping

# #############################################################################
# MutableMapping
