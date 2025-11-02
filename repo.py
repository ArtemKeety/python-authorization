import asyncpg
from db import Database
from shemas import Registration, DBUser
from typing import Optional
from config import DB_TIMEOUT


class Repo:

    @staticmethod
    @Database.get()
    async def get_user(login:str, email:str, conn: asyncpg.Connection) -> Optional[DBUser]:
        if data := await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1 or login =$2",
                email, login,
                timeout=DB_TIMEOUT,
        ):
            return DBUser(**data)
        return None


    @staticmethod
    @Database.get()
    async def add_user(r: Registration, conn: asyncpg.Connection) -> int:
        res = await conn.fetchval(
            "INSERT INTO users (email, login, password) VALUES ($1, $2, $3) RETURNING id",
            r.email, r.login, r.password,
            timeout=DB_TIMEOUT,
        )
        return res