import asyncpg
from db import Database
from shemas import Registration, DBUser
from typing import Optional
from config import DB_TIMEOUT
from shemas import Role


class Repo:

    @staticmethod
    @Database.get()
    async def get_user(login:str, email:str, conn: asyncpg.Connection) -> Optional[DBUser]:
        if data := await conn.fetchrow(
                "SELECT * FROM users WHERE (email = $1 or login =$2) and is_active = true",
                email, login,
                timeout=DB_TIMEOUT,
        ):
            return DBUser(**data)
        return None


    @staticmethod
    @Database.get()
    async def get_user_by_id(user_id: int, conn: asyncpg.Connection) -> Optional[DBUser]:
        if data := await conn.fetchrow(
                "SELECT * FROM users WHERE (id = $1) and is_active = true",
                user_id,
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


    @staticmethod
    @Database.get()
    async def update_active(user_id: int, active: bool, conn: asyncpg.Connection) -> None:
        await conn.execute(
            "UPDATE users SET is_active = $1 WHERE id = $2",
            active, user_id,
            timeout=DB_TIMEOUT,
        )


    @staticmethod
    @Database.get()
    async def update_role(user_id: int, role: Role, conn: asyncpg.Connection):
        await conn.execute(
            "UPDATE users SET role_id = $1 WHERE id = $2",
            role.value, user_id,
            timeout=DB_TIMEOUT
        )

