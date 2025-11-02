

class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if not cls in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]
