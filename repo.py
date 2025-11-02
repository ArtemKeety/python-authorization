import asyncpg
from db import Database
from shemas import Registration, DBUser
from utils import Password
from typing import Optional


class Repo:

    @staticmethod
    @Database.get()
    async def check_user(r: Registration, conn: asyncpg.Connection) -> Optional[DBUser]:
        if data := await conn.fetchrow("SELECT * FROM users WHERE email = $1 or login =$2", r.email, r.login):
            return DBUser(**data)
        return None


    @staticmethod
    @Database.get()
    async def add_user(r: Registration, conn: asyncpg.Connection) -> int:
        password = Password.hash_password(r.password)
        res = await conn.fetchval(
            "INSERT INTO users (email, login, password) VALUES ($1, $2, $3) RETURNING id",
            r.email, r.login, password,
            timeout=10,
        )
        return res