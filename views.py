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
        "duration": {
            "auto": randint(1, 100),
            "mt": randint(1, 100),
            "bc": randint(1, 100),
            "sc": randint(1, 100),
            "pd": randint(1, 100),
        }
    }


def process(strtime: str) -> int:
    coefficients = {"мин": 1, "ч": 60, "д": 1440}
    times = reversed(strtime.split(" "))
    result = 0
    for time in times:
        if time.isdigit():
            result += coef * int(time)
            continue

        coef = coefficients[time]

    return result


@router.post("/")
async def get_duration_selenium(source: Geocoordinates, destination: Geocoordinates):
    src: str = ",".join(source.model_dump().values())
    dst: str = ",".join(destination.model_dump().values())
    transports = ["auto", "mt", "taxi", "pd", "bc", "sc"]

    url = f"https://yandex.ru/maps/213/moscow/?mode=routes&rtext={src}~{dst}&rtt=comparison&ruri=~&z=12.84"
    msg, durations = await Driver.parse_duration(url=url)
    durations = dict(zip(transports, map(process, durations)))
    del durations["taxi"]
    logger.info(msg=msg + f" {durations=}")

    return {
        "source_coordinates": source.model_dump(),
        "destination_coordinates": destination.model_dump(),
        "duration": durations
    }
