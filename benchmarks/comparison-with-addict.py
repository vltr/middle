import cProfile
import sys
from enum import Enum
from enum import IntEnum
from enum import unique
from typing import Dict
from typing import List
from typing import Set

# --------------------------------------------------------------- #
# Import boilerplate
# --------------------------------------------------------------- #

try:
    import timy
    import middle
    from addict import Dict as ADict
except ImportError:
    print(
        "To run this script, you must install these dependencies:",
        file=sys.stderr,
    )
    print("- addict", file=sys.stderr)
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
# Enum definition
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


# --------------------------------------------------------------- #
# middle model definition
# --------------------------------------------------------------- #


class MiddleCity(middle.Model):
    name: str = middle.field()
    region: CityRegionEnum = middle.field()


class MiddleGame(middle.Model):
    name: str = middle.field()
    platform: PlatformEnum = middle.field()
    score: float = middle.field()
    resolution_tested: str = middle.field()
    genre: List[str] = middle.field()
    rating: Dict[str, float] = middle.field()
    players: Set[str] = middle.field()
    language: LanguageEnum = middle.field()
    awesome_city: MiddleCity = middle.field()


# --------------------------------------------------------------- #
# Test variable
# --------------------------------------------------------------- #

MODEL_INSTANCE = {
    "name": "Cities: Skylines",
    "platform": "PC",
    "score": 9.0,
    "resolution_tested": "1920x1080",
    "genre": ["Simulators", "City Building"],
    "rating": {"IGN": 8.5, "Gamespot": 8.0, "Steam": 4.5},
    "players": ["Flux", "strictoaster"],
    "language": 1,
    "awesome_city": {"name": "Blumenau", "region": "TEMPERATE"},
}

# --------------------------------------------------------------- #
# Test runnable
# --------------------------------------------------------------- #


def test_addict():
    game = ADict(MODEL_INSTANCE)
    assert isinstance(game.name, str)
    assert isinstance(game.platform, str)
    assert isinstance(game.score, float)
    assert isinstance(game.resolution_tested, str)
    assert isinstance(game.genre, list)
    assert isinstance(game.rating, dict)
    assert isinstance(game.players, list)
    assert isinstance(game.language, int)
    assert isinstance(game.awesome_city, dict)
    assert isinstance(game.awesome_city.name, str)
    assert isinstance(game.awesome_city.region, str)


def test_middle():
    game = MiddleGame(**MODEL_INSTANCE)
    assert isinstance(game, MiddleGame)
    assert isinstance(game.name, str)
    assert isinstance(game.platform, PlatformEnum)
    assert isinstance(game.score, float)
    assert isinstance(game.resolution_tested, str)
    assert isinstance(game.genre, list)
    assert isinstance(game.rating, dict)
    assert isinstance(game.players, set)
    assert isinstance(game.language, LanguageEnum)
    assert isinstance(game.awesome_city, MiddleCity)
    assert isinstance(game.awesome_city.name, str)
    assert isinstance(game.awesome_city.region, CityRegionEnum)


# --------------------------------------------------------------- #
# Run tests
# --------------------------------------------------------------- #


def main():
    if "profile" in sys.argv:
        cProfile.run(
            "for i in range({}): test_addict()".format(TOTAL_LOOPS),
            sort="tottime",
        )
        cProfile.run(
            "for i in range({}): test_middle()".format(TOTAL_LOOPS),
            sort="tottime",
        )
    else:
        timy.timer(ident="addict", loops=TOTAL_LOOPS)(test_addict).__call__()
        timy.timer(ident="middle", loops=TOTAL_LOOPS)(test_middle).__call__()


if __name__ == "__main__":
    main()
