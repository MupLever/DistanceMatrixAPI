import re
import time
from random import random
from typing import Optional, Tuple

from scrapy import Selector
from selenium import webdriver
from selenium.webdriver import Firefox
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
    def get_driver(cls) -> Firefox:
        return cls.driver

    @classmethod
    def open_url(cls, url: str) -> None:
        try:
            cls.driver.get(url)
        except WebDriverException as exc:
            logger.error(f"Can't get {url}: {exc}")

        time.sleep(1.5)

    @classmethod
    def close(cls) -> None:
        cls.driver.close()

    @classmethod
    async def parse_duration(cls, address_from: str, address_to: str) -> Tuple[str, Optional[str]]:
        msg = ""
        from_input_xpath = "//span[@class='input__context']/input[@placeholder='Откуда']"
        to_input_xpath = "//span[@class='input__context']/input[@placeholder='Куда']"

        try:
            WebDriverWait(cls.driver, settings.SECOND_TO_WAIT).until(
                EC.presence_of_element_located((By.XPATH, from_input_xpath))
            )
        except TimeoutException:
            msg = "Timeout waiting for input to appear"
            return msg, None

        field = cls.driver.find_element(by="xpath", value=from_input_xpath)
        field.clear()
        field.send_keys(address_from)

        field = cls.driver.find_element(by="xpath", value=to_input_xpath)
        field.clear()
        field.send_keys(address_to)

        timeout = random() * 1.5
        time.sleep(timeout)

        data = Selector(text=cls.driver.page_source)
        duration = re.sub(r"[ |\xa0]", " ", data.xpath("//div[@class='auto-route-snippet-view__route-duration']/text()").get())
        # distance = data.xpath("//div[@class='auto-route-snippet-view__route-subtitle']/text()").get()

        return msg, duration
