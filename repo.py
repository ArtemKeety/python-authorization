import asyncpg
from db import Database
from shemas import Registration
from utils import Password


class Repo:

    @staticmethod
    @Database.get()
    async def check_user(r: Registration, conn: asyncpg.Connection):
        if _ := await conn.fetch("SELECT * FROM users WHERE email = $1 or login =$2", r.email, r.login):
            return True
        return False


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