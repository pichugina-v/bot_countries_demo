from pydantic import BaseModel


class CityCoordinatesSchema(BaseModel):
    name: str
    longitude: float
    latitude: float
