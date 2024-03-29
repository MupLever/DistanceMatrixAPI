from pydantic import BaseModel


class Geocoordinates(BaseModel):
    lat: str
    lng: str
