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


@Database.get()
async def initialize_database(conn: asyncpg.Connection):
    """
    Полная инициализация базы данных: создание таблиц и начальных данных
    """

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS role(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            login VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email TEXT NOT NULL,
            is_active BOOLEAN DEFAULT true,
            role_id INTEGER DEFAULT 1,
            FOREIGN KEY (role_id) REFERENCES role(id)
        )
    """)

    await conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_user_status 
        ON users(LOWER(login)) WHERE is_active = true
    """)


    await conn.execute("""
           INSERT INTO role (id, name) 
           VALUES 
               (1, 'user'),
               (2, 'admin')
           ON CONFLICT (id) DO NOTHING
       """)

    user_count = await conn.fetchval("SELECT COUNT(*) FROM users")
    if user_count == 0:
        from utils import Password
        hashed_password = Password.hash_password("admin123")

        await conn.execute("""
               INSERT INTO users (login, password, email, role_id) 
               VALUES ($1, $2, $3, $4)
           """, "admin", hashed_password, "admin@example.com", 2)

        Logger.info("Created default admin user: admin / admin123")
