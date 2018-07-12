from enum import Enum
from enum import unique

import middle


def test_inheritance():
    @unique
    class CityRegionEnum(str, Enum):
        TROPICAL = "TROPICAL"
        TEMPERATE = "TEMPERATE"
        BOREAL = "BOREAL"

    class BaseCity(middle.Model):
        name = middle.field(type=str)
        region = middle.field(type=CityRegionEnum)

    class City(BaseCity):
        population = middle.field(type=int)
        latitude = middle.field(type=float)
        longitude = middle.field(type=float)

    base_city = BaseCity(name="London", region="TEMPERATE")

    city = City(
        name="London",
        region="TEMPERATE",
        population=8787892,
        latitude=51.507222,
        longitude=-0.1275,
    )

    assert isinstance(base_city, BaseCity)
    assert isinstance(city, BaseCity)
    assert isinstance(city, City)

    assert isinstance(city.name, str)
    assert isinstance(city.region, CityRegionEnum)
    assert isinstance(city.population, int)
    assert isinstance(city.latitude, float)
    assert isinstance(city.longitude, float)

    data = middle.asdict(city)

    assert isinstance(data.get("name"), str)
    assert isinstance(data.get("region"), str)
    assert isinstance(data.get("population"), int)
    assert isinstance(data.get("latitude"), float)
    assert isinstance(data.get("longitude"), float)
