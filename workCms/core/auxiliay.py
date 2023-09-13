from flask import redirect, session, jsonify
from datetime import datetime
from functools import wraps
from workCms.databases.mysql_db import cursor
from workCms.status_restful_api import HttpCode

dates = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
date2 = datetime.now().strftime('%Y-%m-%d')
file = "workCms/serviceall/txt/"


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def session_zsq(func):
    @wraps(func)
    def inner(*args, **kwargs):
        user_info = session.get('user_info')
        if not user_info:
            return redirect('/')
        return func(*args, **kwargs)

    return inner


def execute_time_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        print(exec_time)
        return result

    return wrapper


def authority_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cursor.execute("SELECT user_identity FROM users WHERE user_name=%(name)s", {"name": session['user_info']})
        identity_name = cursor.fetchall()
        # client_ip = request.remote_addr
        # proxy_client_ip = request.headers
        if identity_name[0].get('user_identity', '') != "Admin":
            return jsonify({"msg": {
                "code": HttpCode.serverError,
                "error": "You are not a super administrator,You don't have the right to access this route.",
            }})
        result = func(*args, **kwargs)
        return result

    return wrapper


import time


def climit(s):
    def wapper(func):
        name = func.__name__
        func_identify = {name: 0, 'second': s}

        @wraps(func)
        def inner(*args, **kwargs):
            # use_time需等待这些时间之后才可以再次访问
            use_time = func_identify[name] + func_identify['second']
            now_time = time.time()
            re_time = use_time - now_time
            if now_time > use_time:
                res = func(*args, **kwargs)
                func_identify[name] = now_time
            else:
                print(f"请在{re_time}之后再次访问.")
                res = jsonify({"error": "Too many visits, please try again in 3 seconds!"})
            return res

        return inner

    return wapper


# def test():
#     client_ip = request.remote_addr
# proxy_client_ip = request.headers.get('User-Agent')
# print(client_ip)
