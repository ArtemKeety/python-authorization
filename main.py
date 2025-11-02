import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import check
from logger import Logger

@asynccontextmanager
async def start_upp(app: FastAPI):
    Logger.set_logger()
    Logger.set_lvl(Logger.Level.debug)
    await check()
    yield

app = FastAPI(
    title="Auth web-app",
    lifespan=start_upp,
)





if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)