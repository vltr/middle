import datetime
import typing as t

from decimal import Decimal
from enum import Enum, EnumMeta

import pytest

import middle


@pytest.mark.parametrize(
    "type_,expected",
    [
        pytest.param(None, type(None), id="none"),
        pytest.param(str, str, id="str"),
        pytest.param(int, int, id="int"),
        pytest.param(float, float, id="float"),
        pytest.param(bool, bool, id="bool"),
        pytest.param(bytes, bytes, id="bytes"),
        pytest.param(datetime.date, datetime.date, id="datetime_date"),
        pytest.param(
            datetime.datetime, datetime.datetime, id="datetime_datetime"
        ),
        pytest.param(Decimal, Decimal, id="Decimal"),
        pytest.param(t.Dict, t.Dict, id="typing.Dict"),
        pytest.param(t.Dict[str, float], t.Dict, id="typing.Dict[str,float]"),
        pytest.param(t.List, t.List, id="typing.List"),
        pytest.param(t.List[int], t.List, id="typing.List[int]"),
        pytest.param(t.Set, t.Set, id="typing.Set"),
        pytest.param(t.Set[float], t.Set, id="typing.Set[float]"),
        pytest.param(t.Tuple, t.Tuple, id="typing.Tuple"),
        pytest.param(
            t.Tuple[Decimal, float, None, int],
            t.Tuple,
            id="typing.Tuple[Decimal,float,None,int]",
        ),
        pytest.param(t.Union, t.Union, id="typing.Union"),
        pytest.param(t.Union[str, int], t.Union, id="typing.Union[str,int]"),
        pytest.param(t.Optional[str], t.Union, id="typing.Union[str,None]"),
    ],
)
def test_get_type(type_, expected):
    assert middle.get_type(type_) == expected


def test_get_enum():
    class RegionEnum(str, Enum):
        TROPICAL = "TROPICAL"
        TEMPERATE = "TEMPERATE"
        BOREAL = "BOREAL"

    assert middle.get_type(RegionEnum) == EnumMeta


def test_registered_custom_type():
    class Foo:
        pass

    middle.TypeRegistry[Foo] = Foo
    assert middle.get_type(Foo) == Foo


def test_unregistered_custom_type():
    class Bar:
        pass

    assert middle.get_type(Bar) == Bar
