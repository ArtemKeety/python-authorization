import os
import jwt
from passlib.hash import bcrypt

SECRET_KEY = os.urandom(32)
ALGORITM = 'HS256'

class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if not cls in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]



class Password:

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)


class Token:

    @staticmethod
    def decode_token(token: str) -> dict:
        pass

    @staticmethod
    def encode_token(user_id: int) -> str:
        d = {'id': user_id}
        return jwt.encode(d, SECRET_KEY, algorithm=ALGORITM)
