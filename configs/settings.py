import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    GECKODRIVER_PATH: str = os.getenv("GECKODRIVER_PATH")
    SECOND_TO_WAIT: int = 20


settings = Settings()
