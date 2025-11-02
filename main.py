import asyncio

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import check
from logger import Logger
from router import router
from uvicorn.config import Config
from uvicorn.server import Server

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

app.include_router(router)

async def main():
    config = Config(app, host="0.0.0.0", port=8000)
    server = Server(config)
    await server.serve()


if __name__ == '__main__':
    #uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)
    asyncio.run(main())