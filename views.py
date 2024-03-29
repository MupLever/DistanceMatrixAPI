from json import JSONDecodeError
from random import randint

import requests
from fastapi import APIRouter

from configs.headers import headers
from configs.logger import logger
from configs.params import params
from schemas import Geocoordinates
from utils.parse import Driver

router = APIRouter(tags=["Addresses"], prefix="/api/v1/distance_matrix")


# @router.post("/")
# async def get_duration_aor(source: Geocoordinates, destination: Geocoordinates):
#     url = "https://yandex.ru/maps/api/router/buildRoute?"
#     params["rll"] = (f"{round(source.lng, 6)}%2C{round(source.lat, 6)}~"
#                      f"{round(destination.lng, 6)}%2C{round(destination.lat, 6)}"),
#
#     url += "&".join(
#         [f"{param}={value}" for param, value in params.items()]
#     )
#
#     response = requests.get(url, headers=headers)
#     try:
#         duration = response.json().get("data").get("routes")[0].get("duration")
#         logger.info(f"Received from the Yandex API {duration=}")
#     except JSONDecodeError:
#         duration = randint(1, 100)
#     except AttributeError:
#         duration = randint(1, 100)
#     except IndexError:

#     duration = randint(1, 100)
#
#     return {
#         "source_coordinates": source.model_dump(),
#         "destination_coordinates": destination.model_dump(),
#         "duration": duration
#     }


@router.post("/")
async def get_duration_s(source: Geocoordinates, destination: Geocoordinates):
    src: str = ",".join(source.model_dump().values())
    dst: str = ",".join(destination.model_dump().values())
    url = f"https://yandex.ru/maps/213/moscow/?mode=routes&rtext={src}~{dst}&rtt=auto&ruri=~&z=12.84"
    Driver.open_url(url=url)
    msg, duration = await Driver.parse_duration(src, dst)
    logger.info(msg=msg + f" {duration=}")

    return {
        "source_coordinates": source.model_dump(),
        "destination_coordinates": destination.model_dump(),
        "duration": int(duration.split(" ")[0])
    }
