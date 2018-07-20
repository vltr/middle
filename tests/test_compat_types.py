import datetime
import typing
from decimal import Decimal
from enum import Enum
from enum import EnumMeta

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
        pytest.param(typing.Dict, typing.Dict, id="typing.Dict"),
        pytest.param(
            typing.Dict[str, float], typing.Dict, id="typing.Dict[str,float]"
        ),
        pytest.param(typing.List, typing.List, id="typing.List"),
        pytest.param(typing.List[int], typing.List, id="typing.List[int]"),
        pytest.param(typing.Set, typing.Set, id="typing.Set"),
        pytest.param(typing.Set[float], typing.Set, id="typing.Set[float]"),
        pytest.param(typing.Tuple, typing.Tuple, id="typing.Tuple"),
        pytest.param(
            typing.Tuple[Decimal, float, None, int],
            typing.Tuple,
            id="typing.Tuple[Decimal,float,None,int]",
        ),
        pytest.param(typing.Union, typing.Union, id="typing.Union"),
        pytest.param(
            typing.Union[str, int], typing.Union, id="typing.Union[str,int]"
        ),
        pytest.param(
            typing.Optional[str], typing.Union, id="typing.Union[str,None]"
        ),
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
