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
        },
        "file": {
            "class": 'logging.FileHandler',
            "level": "DEBUG",
            "formatter": "simple",
            "filename": "calc.log",
            "mode": "a"
        },
        "httpserver": {
            "()": "logging.handlers.HTTPHandler",
            "level": "DEBUG",
            "host": "127.0.0.1:5555",
            "url": "/log",
            "method": "POST"
        }
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["screen", "file", "httpserver"],
            "propagate": False
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["screen", "file", "httpserver"],
            "propagate": False
        }
    }
}
