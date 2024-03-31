import logging.handlers
import sys


class CustomHandler(logging.Handler):
    def __init__(self, file_name='', mode='a'):
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        with open(self.file_name + record.levelname + '.log', mode=self.mode) as file:
            file.write(message + '\n')


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
        }
    },
    "handlers": {
        "screen": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": sys.stdout
        },
        "file": {
            "()": CustomHandler,
            "level": "DEBUG",
            "formatter": "simple",
            "file_name": "calc_",
            "mode": "a"
        }
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["screen", "file"],
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["screen", "file"],
        }
    },
}