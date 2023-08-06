import time
from datetime import datetime


def roughly_now():
    tm = datetime.now()
    return f'{tm:%H:%M:%S}.{int(tm.microsecond / 1000):03d}'


def now():
    return time.asctime()
