import asyncpg
from contextlib import asynccontextmanager
from functools import wraps
from utils import Singleton
from logger import Logger




class Database(metaclass=Singleton):
    _pool = None

    @classmethod
    async def _connection(cls):
        cls._pool = await asyncpg.create_pool(
            user='postgres',
            password='Yjdsqgfhjkm10',
            database='postgres',
            port=5432
        )


    @classmethod
    @asynccontextmanager
    async def execute(cls):
        if cls._pool is None:
            await cls._connection()

        async with cls._pool.acquire() as conn:
            try:
                yield conn
            finally:
                pass

    @classmethod
    def get(cls):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                async with cls.execute() as conn:
                    return await func(*args, **kwargs, conn=conn)
            return wrapper
        return decorator



@Database.get()
async def check(conn):
    res = await conn.fetch('SELECT 1')
    Logger.info(f'success-connet')
