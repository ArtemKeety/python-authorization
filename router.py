from fastapi import APIRouter, Depends, HTTPException

from shemas import Registration, Login, DBUser
from repo import Repo
from utils import Token
from utils import Password
from midleware import checkRole, Role, get_user_id

router = APIRouter()

COMMENTS = [
    {"text": "first comment", "author": "admin"},
]


@router.post("/sign-up")
async def sign_up(r: Registration):

    if await Repo.get_user(r.login, r.email):
        raise HTTPException(status_code=400, detail="Username already exists")

    r.password = Password.hash_password(r.password)
    user_id: int = await Repo.add_user(r)
    token = Token.encode_token(user_id)
    return {"token": token}

@router.post("/sign-in")
async def sign_in(u: Login):
    if not (db_user := await Repo.get_user(u.login, None)):
        raise HTTPException(status_code=404, detail="User not found")

    if not Password.verify_password(u.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = Token.encode_token(db_user.id)
    return {"token": token}

@router.post("/logout")
async def logout():
    pass

@router.get("/comment")
async def get_comment():
    return COMMENTS

@router.post("/comment")
async def add_comment(text: str, user: DBUser = Depends(checkRole([Role.user, Role.admin]))):
    COMMENTS.append({"text": text, "author": user.login})

# @router.post("/moc")
# async def moc(user_id = Depends(get_user_id)):
#     pass