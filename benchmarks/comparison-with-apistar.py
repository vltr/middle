import cProfile
import sys
from enum import Enum
from enum import IntEnum
from enum import unique
from typing import List

# --------------------------------------------------------------- #
# Import boilerplate
# --------------------------------------------------------------- #

try:
    import timy
    import middle
    from apistar import types
    from apistar import validators
except ImportError:
    print(
        "To run this script, you must install these dependencies:",
        file=sys.stderr,
    )
    print("- apistar", file=sys.stderr)
    print("- middle", file=sys.stderr)
    print("- timy", file=sys.stderr)
    sys.exit(1)

# --------------------------------------------------------------- #
# Fixed variables
# --------------------------------------------------------------- #

TOTAL_LOOPS = 1_000_000

if "short" in sys.argv:
    TOTAL_LOOPS = 1


# --------------------------------------------------------------- #
# Object definition
# --------------------------------------------------------------- #


@unique
class PlatformEnum(str, Enum):
    XBOX1 = "XBOX1"
    PLAYSTATION4 = "PLAYSTATION4"
    PC = "PC"


@unique
class LanguageEnum(IntEnum):
    ENGLISH = 1
    JAPANESE = 2
    SPANISH = 3
    GERMAN = 4
    PORTUGUESE = 5


@unique
class CityRegionEnum(str, Enum):
    TROPICAL = "TROPICAL"
    TEMPERATE = "TEMPERATE"
    BOREAL = "BOREAL"


class City(middle.Model):
    name = middle.field(type=str)
    region = middle.field(type=CityRegionEnum)


class CityType(types.Type):
    name = validators.String()
    region = validators.String()


class Game(middle.Model):
    name: str = middle.field()
    platform: PlatformEnum = middle.field()
    score: float = middle.field()
    resolution_tested: str = middle.field(pattern="^\d+x\d+$")
    genre: List[str] = middle.field()
    players: List[str] = middle.field()
    language: LanguageEnum = middle.field()
    awesome_city: City = middle.field()


class GameType(types.Type):
    name = validators.String()
    platform = validators.String()
    score = validators.Number()
    resolution_tested = validators.String(pattern="^\d+x\d+$")
    genre = validators.Array()
    players = validators.Array()
    language = validators.Number()
    awesome_city = CityType


# --------------------------------------------------------------- #
# Test variable
# --------------------------------------------------------------- #

MODEL_INSTANCE = {
    "name": "Cities: Skylines",
    "platform": "PC",
    "score": 9.0,
    "resolution_tested": "1920x1080",
    "genre": ["Simulators", "City Building"],
    "players": ["Flux", "strictoaster"],
    "language": 1,
    "awesome_city": {
        "name": "Blumenau",
        "region": "TEMPERATE",
    },
}

# --------------------------------------------------------------- #
# Test runnable
# --------------------------------------------------------------- #


def test_apistar():
    game = GameType(**MODEL_INSTANCE)
    assert isinstance(game, GameType)
    assert isinstance(game.awesome_city, CityType)
    p = dict(game)
    assert isinstance(p, dict)


def test_middle():
    game = Game(**MODEL_INSTANCE)
    assert isinstance(game, Game)
    assert isinstance(game.awesome_city, City)
    p = middle.asdict(game)
    assert isinstance(p, dict)


# --------------------------------------------------------------- #
# Run tests
# --------------------------------------------------------------- #


def main():
    if "profile" in sys.argv:
        cProfile.run(
            "for i in range({}): test_apistar()".format(TOTAL_LOOPS),
            sort="tottime",
        )
        cProfile.run(
            "for i in range({}): test_middle()".format(TOTAL_LOOPS),
            sort="tottime",
        )
    else:
        timy.timer(ident="apistar", loops=TOTAL_LOOPS)(test_apistar).__call__()
        timy.timer(ident="middle", loops=TOTAL_LOOPS)(test_middle).__call__()


if __name__ == "__main__":
    main()
