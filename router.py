from fastapi import APIRouter, Depends, HTTPException

from shemas import Registration, Login, DBUser, UpdateRole, Role
from repo import Repo
from utils import Token
from utils import Password
from midleware import checkRole, get_user_id

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

@router.delete("/delete")
async def del_acc(user: DBUser = Depends(checkRole([Role.user]))):
    await Repo.update_active(user.id, False)
    return {"message": "Account deleted"}

@router.get("/comment")
async def get_comment():
    return COMMENTS

@router.post("/comment")
async def add_comment(text: str, user: DBUser = Depends(checkRole([Role.user, Role.admin]))):
    COMMENTS.append({"text": text, "author": user.login})
    return {"message": "Comment added"}

@router.put("/role", dependencies=[Depends(checkRole([Role.admin]))])
async def update_role(u: UpdateRole = Depends()):
    await Repo.update_role(u.user_id, u.role)
    return {"message": "Role updated"}






