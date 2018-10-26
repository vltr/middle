from enum import Enum
from enum import IntEnum
from enum import unique
from typing import Dict
from typing import List
from typing import Set

import middle


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
    name = {"type": str}
    region = {"type": CityRegionEnum}


class Game(middle.Model):
    name = {"type": str}
    platform = {"type": PlatformEnum}
    score = {"type": float}
    resolution_tested = {"pattern": r"^\d+x\d+$", "type": str}
    genre = {"type": List[str]}
    rating = {"type": Dict[str, float]}
    players = {"type": Set[str]}
    language = {"type": LanguageEnum}
    awesome_city = {"type": City}


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
    assert isinstance(game.platform, PlatformEnum)
    assert isinstance(game.language, LanguageEnum)
    assert isinstance(game.awesome_city, City)
    assert isinstance(game.awesome_city.region, CityRegionEnum)


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

    data = middle.asdict(game)
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
