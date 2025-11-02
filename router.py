from fastapi import APIRouter, Depends
from shemas import Registration
from midleware import user
from repo import Repo
from utils import Token
router = APIRouter()


@router.post("/sign-up")
async def sign_up(r: Registration = Depends(user)):
    user_id: int = await Repo.add_user(r)
    token = Token.encode_token(user_id)
    return {"token": token}