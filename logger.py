import sys
import logging
from utils import Singleton
from enum import Enum


class Logger(metaclass=Singleton):
    __logger = logging.getLogger('logger')

    @classmethod
    def set_logger(cls):
        """Настройка логгера с обработчиками"""
        cls.__logger.handlers.clear()

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        cls.__logger.addHandler(console_handler)

        cls.__logger.setLevel(logging.DEBUG)
        cls.__logger.propagate = False


    class Level(Enum):
        debug = logging.DEBUG
        info = logging.INFO
        warning = logging.WARNING
        error = logging.ERROR
        critical = logging.CRITICAL

    @classmethod
    def set_lvl(cls, lvl: 'Level'):
        cls.__logger.setLevel(lvl.value)

    @classmethod
    def info(cls, s: str):
        cls.__logger.info(s)

    @classmethod
    def debug(cls, s: str):
        cls.__logger.debug(s)

    @classmethod
    def warning(cls, s: str):
        cls.__logger.warning(s)

    @classmethod
    def error(cls, s: str):
        cls.__logger.error(s)

    @classmethod
    def critical(cls, s: str):
        cls.__logger.critical(s)
