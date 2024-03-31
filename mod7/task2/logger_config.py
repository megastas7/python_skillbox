import logging
import sys

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
        }
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["screen"],
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["screen"],
        }
    },
}