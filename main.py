from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from views import router
from utils.parse import Driver


@asynccontextmanager
async def get_driver(app: FastAPI):
    Driver.init_driver()

    yield

    Driver.close()

app = FastAPI(lifespan=get_driver)

app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8002)
