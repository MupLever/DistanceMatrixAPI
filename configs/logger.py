import logging
from datetime import datetime
logging.basicConfig(
    level=logging.INFO,
    filename=f"{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("Geocoder")
