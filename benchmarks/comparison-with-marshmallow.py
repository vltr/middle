import cProfile
import sys
from enum import Enum, IntEnum, unique
from typing import Dict, List, Set

# --------------------------------------------------------------- #
# Import boilerplate
# --------------------------------------------------------------- #

try:
    import timy
    from marshmallow import Schema, fields
    from marshmallow.schema import MarshalResult
    from middle import schema
except ImportError:
    print(
        "To run this script, you must install these dependencies:",
        file=sys.stderr,
    )
    print("- marshmallow", file=sys.stderr)
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
# Caja model definition
# --------------------------------------------------------------- #


class MiddleCity(schema.Model):
    name = schema.field(type=str, description="The city name")
    region = schema.field(
        type=CityRegionEnum, description="The region this city is located"
    )


class MiddleGame(schema.Model):
    name: str = schema.field(description="The name of the game")
    platform: PlatformEnum = schema.field(
        description="Which platform it runs on"
    )
    score: float = schema.field(description="The average score of the game")
    resolution_tested: str = schema.field(
        description="The resolution which the game was tested",
        pattern="^\d+x\d+$",
    )
    genre: List[str] = schema.field(
        description="One or more genres this game is part of"
    )
    rating: Dict[str, float] = schema.field(
        description="Ratings given on specialized websites"
    )
    players: Set[str] = schema.field(
        description="Some of the notorious players of this game"
    )
    language: LanguageEnum = schema.field(
        description="The main language of the game"
    )
    awesome_city: MiddleCity = schema.field(
        description="One awesome city built"
    )


# --------------------------------------------------------------- #
# marshmallow model definition
# --------------------------------------------------------------- #


class CitySchema(Schema):
    name = fields.Str()
    region = fields.Str()


class GameSchema(Schema):
    name = fields.Str()
    platform = fields.Str()
    score = fields.Float()
    resolution_tested = fields.Str()
    genre = fields.List(fields.Str())
    rating = fields.Dict(values=fields.Float(), keys=fields.Str())
    players = fields.List(fields.Str())
    language = fields.Integer()
    awesome_city = fields.Nested(CitySchema)


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


def test_marshmallow():
    game = GameSchema().dump(MODEL_INSTANCE)
    assert isinstance(game, MarshalResult)
    assert "awesome_city" in game.data


def test_middle():
    game = MiddleGame(**MODEL_INSTANCE)
    assert isinstance(game, MiddleGame)
    assert isinstance(game.awesome_city, MiddleCity)


# --------------------------------------------------------------- #
# Run tests
# --------------------------------------------------------------- #


def main():
    if "profile" in sys.argv:
        cProfile.run(
            "for i in range({}): test_marshmallow()".format(TOTAL_LOOPS),
            sort="tottime",
        )
        cProfile.run(
            "for i in range({}): test_middle()".format(TOTAL_LOOPS),
            sort="tottime",
        )
    else:
        timy.timer(ident="marshmallow", loops=TOTAL_LOOPS)(
            test_marshmallow
        ).__call__()
        timy.timer(ident="middle", loops=TOTAL_LOOPS)(test_middle).__call__()


if __name__ == "__main__":
    main()
