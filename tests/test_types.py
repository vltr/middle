from datetime import date
from datetime import datetime
from datetime import timezone
from enum import Enum
from enum import IntEnum
from enum import unique
from typing import Collection
from typing import Dict
from typing import FrozenSet
from typing import Iterable
from typing import List
from typing import Mapping
from typing import MutableMapping
from typing import MutableSequence
from typing import MutableSet
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Union

import pytest

import middle

# #############################################################################
# str


def test_str_working():
    class TestModel(middle.Model):
        name: str = middle.field()

    inst = TestModel(name="some str")

    assert isinstance(inst, TestModel)
    assert inst.name == "some str"

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("name", None) == "some str"


def test_str_converter():
    class TestModel(middle.Model):
        name: str = middle.field()

    inst = TestModel(name=1)
    assert isinstance(inst, TestModel)
    assert inst.name == "1"

    with middle.config.temp(str_method=False):
        with pytest.raises(TypeError):
            TestModel(name=1)

    with middle.config.temp(str_method=False, force_str=True):
        assert TestModel(name=1).name == "1"


# #############################################################################
# int


def test_int_working():
    class TestModel(middle.Model):
        const: int = middle.field()

    inst = TestModel(const=42)

    assert isinstance(inst, TestModel)
    assert inst.const == 42

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("const", None) == 42


def test_int_converter():
    class TestModel(middle.Model):
        const: int = middle.field()

    inst = TestModel(const="42")
    assert isinstance(inst, TestModel)
    assert inst.const == 42

    with middle.config.temp():
        pass

    assert TestModel(const="-42").const == -42


# #############################################################################
# float


def test_float_working():
    class TestModel(middle.Model):
        const: float = middle.field()

    inst = TestModel(const=3.14)

    assert isinstance(inst, TestModel)
    assert inst.const == 3.14

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("const", None) == 3.14


def test_float_converter():
    class TestModel(middle.Model):
        const: float = middle.field()

    inst = TestModel(const="3.14")
    assert isinstance(inst, TestModel)
    assert inst.const == 3.14

    assert TestModel(const="-3.14").const == -3.14
    assert TestModel(const="+3.14").const == 3.14
    assert TestModel(const=".14").const == 0.14
    assert TestModel(const="1.").const == 1.0
    assert TestModel(const="-.3").const == -0.3


# #############################################################################
# bool


def test_bool_working():
    class TestModel(middle.Model):
        broken: bool = middle.field()

    inst = TestModel(broken=True)

    assert isinstance(inst, TestModel)
    assert inst.broken is True

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("broken", False) is True


def test_bool_converter():
    class TestModel(middle.Model):
        broken: bool = middle.field()

    # everything must be true
    assert TestModel(broken="True").broken is True
    assert TestModel(broken="true").broken is True
    assert TestModel(broken="yes").broken is True
    assert TestModel(broken="on").broken is True
    assert TestModel(broken="On").broken is True
    assert TestModel(broken="TRUE").broken is True
    assert TestModel(broken="YES").broken is True
    assert TestModel(broken="ON").broken is True
    assert TestModel(broken=1).broken is True
    assert TestModel(broken=10).broken is True
    assert TestModel(broken=1.5).broken is True
    assert TestModel(broken=3.14).broken is True

    # now, everything must be false
    assert TestModel(broken="foo").broken is False
    assert TestModel(broken="BAR").broken is False
    assert TestModel(broken="False").broken is False
    assert TestModel(broken="NO").broken is False
    assert TestModel(broken="off").broken is False
    assert TestModel(broken="Off").broken is False
    assert TestModel(broken="OFF").broken is False
    assert TestModel(broken=0).broken is False
    assert TestModel(broken=-1).broken is False
    assert TestModel(broken=-1.5).broken is False
    assert TestModel(broken=0.0).broken is False

    with pytest.raises(TypeError):
        TestModel(broken={"hello": "world"})


# #############################################################################
# date


def test_date_working():
    class TestModel(middle.Model):
        created_on: date = middle.field()

    inst = TestModel(created_on="2018-06-18")

    assert isinstance(inst, TestModel)
    assert inst.created_on == date(2018, 6, 18)

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("created_on", None) == "2018-06-18"


def test_date_converter():
    class TestModel(middle.Model):
        created_on: date = middle.field()

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
    class TestModel(middle.Model):
        ts: datetime = middle.field()

    inst = TestModel(ts="2018-06-18T13:30:00.123456+00:00")

    assert isinstance(inst, TestModel)
    assert inst.ts == datetime(2018, 6, 18, 13, 30, 0, 123456, timezone.utc)

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("ts", None) == "2018-06-18T13:30:00.123456+00:00"


def test_datetime_converter():
    class TestModel(middle.Model):
        ts: datetime = middle.field()

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

    class TestModel(middle.Model):
        str_enum: TestStrEnum = middle.field()
        int_enum: TestIntEnum = middle.field()

    inst = TestModel(str_enum="TEST2", int_enum=3)

    assert isinstance(inst, TestModel)
    assert inst.str_enum == TestStrEnum.TEST_2
    assert inst.int_enum == TestIntEnum.TEST_3

    data = middle.asdict(inst)

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

    class TestStrModel(middle.Model):
        str_enum: TestStrEnum = middle.field()

    class TestIntModel(middle.Model):
        int_enum: TestIntEnum = middle.field()

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


def test_model_working():
    class ColorEnum(IntEnum):
        RED = 1
        GREEN = 2
        BLUE = 3
        YELLOW = 4
        PINK = 5
        BLACK = 6

    class ChildModel(middle.Model):
        name: str = middle.field()
        age: int = middle.field()
        favourite_color: ColorEnum = middle.field()

    class PersonModel(middle.Model):
        name: str = middle.field()
        age: int = middle.field()
        children: List[ChildModel] = middle.field()

    class CompanyModel(middle.Model):
        name: str = middle.field()
        manager: PersonModel = middle.field()
        employees: List[PersonModel] = middle.field()

    inst = CompanyModel(
        {
            "name": "My Company Ltd",
            "manager": {"name": "John", "age": 42, "children": []},
            "employees": [
                {
                    "name": "Jane",
                    "age": 35,
                    "children": [
                        {"name": "Clarice", "age": 5, "favourite_color": 4},
                        {"name": "Robert", "age": 8, "favourite_color": 1},
                    ],
                },
                {"name": "Carl", "age": 22, "children": []},
            ],
        }
    )

    assert isinstance(inst, CompanyModel)
    assert isinstance(inst.manager, PersonModel)
    assert isinstance(inst.employees[0], PersonModel)
    assert isinstance(inst.employees[1], PersonModel)
    assert isinstance(inst.employees[0].children[0], ChildModel)
    assert isinstance(inst.employees[0].children[1], ChildModel)

    assert inst.name == "My Company Ltd"
    assert inst.manager.name == "John"
    assert inst.manager.age == 42
    assert inst.manager.children == []
    assert inst.employees[0].name == "Jane"
    assert inst.employees[0].age == 35
    assert inst.employees[0].children[0].name == "Clarice"
    assert inst.employees[0].children[0].age == 5
    assert inst.employees[0].children[0].favourite_color == ColorEnum.YELLOW
    assert inst.employees[0].children[1].name == "Robert"
    assert inst.employees[0].children[1].age == 8
    assert inst.employees[0].children[1].favourite_color == ColorEnum.RED
    assert inst.employees[1].name == "Carl"
    assert inst.employees[1].age == 22
    assert inst.employees[1].children == []

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert (
        data.get("employees")[0].get("children")[0].get("favourite_color") == 4
    )


def test_model_converter():
    class ChildModel(middle.Model):
        __attr_s_kwargs__ = {"cmp": True}
        name: str = middle.field()
        age: int = middle.field()

    class PersonModel(middle.Model):
        name: str = middle.field()
        age: int = middle.field()
        children: List[ChildModel] = middle.field()

    test_child = ChildModel(name="Robert", age=10)

    assert (
        PersonModel(name="foo", age=1, children=[test_child]).children[0]
        == test_child
    )
    assert (
        PersonModel(
            name="foo", age=1, children=[{"name": "Robert", "age": 10}]
        ).children[0]
        == test_child
    )

    with pytest.raises(TypeError):
        PersonModel(name="foo", age=1, children=[{}])

    with pytest.raises(TypeError):
        PersonModel(name="foo", age="!", children=[])


# #############################################################################
# List, Sequence, Collection, Iterable, MutableSequence


@pytest.mark.parametrize(
    "list_type",
    [
        pytest.param(Collection, id="Collection"),
        pytest.param(Iterable, id="Iterable"),
        pytest.param(List, id="List"),
        pytest.param(MutableSequence, id="MutableSequence"),
        pytest.param(Sequence, id="Sequence"),
    ],
)
def test_list_working(list_type):
    class TestModel(middle.Model):
        names: list_type[str] = middle.field()

    inst = TestModel(names=["foo", "bar"])

    assert isinstance(inst, TestModel)
    assert inst.names == ["foo", "bar"]

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("names", None) == ["foo", "bar"]


@pytest.mark.parametrize(
    "list_type",
    [
        pytest.param(Collection, id="Collection"),
        pytest.param(Iterable, id="Iterable"),
        pytest.param(List, id="List"),
        pytest.param(MutableSequence, id="MutableSequence"),
        pytest.param(Sequence, id="Sequence"),
    ],
)
def test_list_converter(list_type):
    class SomeJunk:
        def __str__(self):
            return "hello"

    class TestModel(middle.Model):
        names: list_type[str] = middle.field()

    with middle.config.temp(str_method=False):
        with pytest.raises(TypeError):
            TestModel(names=[1, SomeJunk()])

    with middle.config.temp(str_method=False, force_str=True):
        assert TestModel(names=[1, SomeJunk()]) is not None

    inst = TestModel(names=[1, SomeJunk()])
    assert isinstance(inst, TestModel)
    assert inst.names[0] == "1"
    assert inst.names[1] == "hello"


# #############################################################################
# Set, MutableSet, FrozenSet


@pytest.mark.parametrize(
    "set_type",
    [
        pytest.param(Set, id="Set"),
        pytest.param(FrozenSet, id="FrozenSet"),
        pytest.param(MutableSet, id="MutableSet"),
    ],
)
def test_set_working(set_type):
    class TestModel(middle.Model):
        names: set_type[str] = middle.field()

    inst = TestModel(names=["foo", "bar"])

    assert isinstance(inst, TestModel)
    assert inst.names == {"bar", "foo"}

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("names", None) == {"bar", "foo"}


@pytest.mark.parametrize(
    "set_type",
    [
        pytest.param(Set, id="Set"),
        pytest.param(FrozenSet, id="FrozenSet"),
        pytest.param(MutableSet, id="MutableSet"),
    ],
)
def test_set_converter(set_type):
    class SomeJunk:
        def __str__(self):
            return "hello"

    class TestModel(middle.Model):
        names: set_type[str] = middle.field()

    inst = TestModel(names=[1, SomeJunk()])
    assert isinstance(inst, TestModel)
    assert inst.names == {"1", "hello"}


# #############################################################################
# Dict, Mapping, MutableMapping


@pytest.mark.parametrize(
    "dict_type",
    [
        pytest.param(Dict, id="Dict"),
        pytest.param(Mapping, id="Mapping"),
        pytest.param(MutableMapping, id="MutableMapping"),
    ],
)
def test_dict_working(dict_type):
    class TestModel(middle.Model):
        ratings: dict_type[str, float] = middle.field()

    inst = TestModel(
        ratings={"contender1": 4.2, "contender2": 3.9, "contender3": 3.4}
    )

    assert isinstance(inst, TestModel)
    assert list(inst.ratings.keys()) == [
        "contender1",
        "contender2",
        "contender3",
    ]
    assert list(inst.ratings.values()) == [4.2, 3.9, 3.4]

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("ratings", None) == {
        "contender1": 4.2,
        "contender2": 3.9,
        "contender3": 3.4,
    }


@pytest.mark.parametrize(
    "dict_type",
    [
        pytest.param(Dict, id="Dict"),
        pytest.param(Mapping, id="Mapping"),
        pytest.param(MutableMapping, id="MutableMapping"),
    ],
)
def test_dict_converter(dict_type):
    class SomeJunk:
        def __str__(self):
            return "hello"

    class TestModel(middle.Model):
        ratings: dict_type[str, float] = middle.field()

    inst = TestModel(ratings={SomeJunk(): 5.0})
    assert isinstance(inst, TestModel)
    assert inst.ratings == {"hello": 5.0}


# #############################################################################
# Optional


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("foo", "foo", id="value_str"),
        pytest.param(None, None, id="value_none"),
        pytest.param(1, "1", id="value_str_from_int"),
    ],
)
def test_optional_working(value, expected):
    class TestModel(middle.Model):
        name: Optional[str] = middle.field()

    inst = TestModel(name=value)
    assert isinstance(inst, TestModel)
    assert inst.name == expected

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("name", None) == expected


# #############################################################################
# Union


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("foo", "foo", id="value_str"),
        pytest.param(3.14, 3.14, id="value_float"),
        pytest.param(-1, -1, id="value_int"),
    ],
)
def test_union_working(value, expected):
    class TestModel(middle.Model):
        value: Union[str, int, float] = middle.field()

    inst = TestModel(value=value)
    assert isinstance(inst, TestModel)
    assert inst.value == expected

    data = middle.asdict(inst)

    assert isinstance(data, dict)
    assert data.get("value", None) == expected
