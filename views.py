from random import randint

from fastapi import APIRouter

from configs.logger import logger
from schemas import Geocoordinates
from utils.parse import Driver

router = APIRouter(tags=["Addresses"], prefix="/api/v1/distance_matrix")


# @router.post("/")
async def get_duration_random(source: Geocoordinates, destination: Geocoordinates):
    return {
        "source_coordinates": source.model_dump(),
        "destination_coordinates": destination.model_dump(),
        "duration": randint(1, 100)
    }


@router.post("/")
async def get_duration_selenium(source: Geocoordinates, destination: Geocoordinates):
    src: str = ",".join(source.model_dump().values())
    dst: str = ",".join(destination.model_dump().values())

    url = f"https://yandex.ru/maps/213/moscow/?mode=routes&rtext={src}~{dst}&rtt=auto&ruri=~&z=12.84"
    msg, duration = await Driver.parse_duration(url=url)
    logger.info(msg=msg + f" {duration=}")

    return {
        "source_coordinates": source.model_dump(),
        "destination_coordinates": destination.model_dump(),
        "duration": duration
    }
