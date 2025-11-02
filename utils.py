import jwt
from passlib.hash import bcrypt



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
