from flask import redirect, session
import time

dates = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def session_zsq(func):
    def inner(*args, **kwargs):
        user_info = session.get('user_info')
        if not user_info:
            return redirect('/')
        return func(*args, **kwargs)

    return inner
