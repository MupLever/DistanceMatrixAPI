import re
import asyncio
from random import random
from typing import Optional, Tuple

from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from configs.logger import logger
from configs.settings import settings


class Driver:
    driver = None

    @classmethod
    def init_driver(cls):
        service = Service(settings.GECKODRIVER_PATH)
        cls.driver = webdriver.Firefox(service=service)
        cls.driver.maximize_window()

    @classmethod
    def close(cls) -> None:
        cls.driver.close()

    @classmethod
    async def parse_duration(cls, url: str) -> Tuple[str, Optional[int]]:
        msg = ""
        timeout = random() * 0.5
        await asyncio.sleep(timeout)

        try:
            cls.driver.get(url)
        except WebDriverException as exc:
            logger.error(f"Can't get {url}: {exc}")
            return msg, None

        from_input_xpath = "//span[@class='input__context']/input[@placeholder='Откуда']"

        try:
            WebDriverWait(cls.driver, settings.SECOND_TO_WAIT).until(
                EC.presence_of_element_located((By.XPATH, from_input_xpath))
            )
        except TimeoutException:
            msg = "Timeout waiting for input to appear"
            return msg, None

        await asyncio.sleep(timeout)
        route_duration_xpath = "//div[@class='auto-route-snippet-view__route-duration']/text()"

        data = Selector(text=cls.driver.page_source)
        duration = re.sub(
            r"[ |\xa0]", " ",
            data.xpath(route_duration_xpath).get()
        )

        return msg, int(duration.split(" ")[0])
