from fastapi import HTTPException, Response, Request
from repo import Repo
from shemas import Registration


async def user_exists(r: Registration):
    if await Repo.get_user(r):
        raise HTTPException(status_code=400, detail="Username already exists")
    return r