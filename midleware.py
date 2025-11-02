from fastapi import HTTPException, Response, Request, Depends
from repo import Repo
from utils import Token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from enum import Enum
from shemas import Role



secure = HTTPBearer(auto_error=True)


def get_user_id(c: HTTPAuthorizationCredentials = Depends(secure)) -> int:
    if not (c and c.scheme.lower() == 'bearer'):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    data: int = Token.decode_token(c.credentials)

    return data



def checkRole(allowed_roles: list[Role]):

    async def dependency(user_id: int = Depends(get_user_id)):
        if not (user := await Repo.get_user_by_id(user_id)):
            raise HTTPException(status_code=404, detail="User not found")

        if not Role(user.role_id) in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")

        return user

    return dependency