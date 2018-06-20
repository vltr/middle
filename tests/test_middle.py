from enum import Enum
from enum import IntEnum
from enum import unique
from typing import Dict
from typing import List
from typing import Set

from middle import schema
from middle import utils


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


class City(schema.Model):
    name = schema.field(type=str, description="The city name")
    region = schema.field(
        type=CityRegionEnum, description="The region this city is located"
    )


class Game(schema.Model):
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
    awesome_city: City = schema.field(description="One awesome city built")


def test_instance():
    game = Game(
        name="Cities: Skylines",
        platform="PC",
        score=9.0,
        resolution_tested="1920x1080",
        genre=["Simulators", "City Building"],
        rating={"IGN": 8.5, "Gamespot": 8.0, "Steam": 4.5},
        players=["Flux", "strictoaster"],
        language=1,
        awesome_city=City(name="Blumenau", region=CityRegionEnum.TEMPERATE),
    )

    assert isinstance(game, Game)


def test_instance_to_dict():
    game = Game(
        name="Cities: Skylines",
        platform="PC",
        score=9.0,
        resolution_tested="1920x1080",
        genre=["Simulators", "City Building"],
        rating={"IGN": 8.5, "Gamespot": 8.0, "Steam": 4.5},
        players=["Flux", "strictoaster"],
        language=1,
        awesome_city=City(name="Blumenau", region=CityRegionEnum.TEMPERATE),
    )

    data = utils.asdict(game)
    assert isinstance(data, dict)
    assert isinstance(data.get("awesome_city", None), dict)
    assert data.get("awesome_city").get("region") == "TEMPERATE"


def test_dict_to_instance():
    data = {
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

    game = Game(**data)
    assert isinstance(game, Game)
    assert isinstance(game.awesome_city, City)
    assert game.platform == PlatformEnum.PC
