from flask import redirect, session
import time

dates = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_size(bytes, suffix="B"):
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
