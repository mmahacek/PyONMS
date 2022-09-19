# utils.__init__.py

from datetime import datetime


def convert_time(time: int) -> datetime:
    if type(time) == int:
        return datetime.utcfromtimestamp(time / 1000)
    else:
        return None
