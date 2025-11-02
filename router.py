from fastapi import APIRouter, Depends
from shemas import Registration
from midleware import user
from repo import Repo

router = APIRouter()


@router.post("/sign-up")
async def sign_up(r: Registration = Depends(user)):
    await Repo.add_user(r)
    return {"success": "success"}