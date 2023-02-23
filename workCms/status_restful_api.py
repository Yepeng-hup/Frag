from flask import jsonify


class HttpCode(object):
    # code status
    success = 200
    serverError = 500
    serverOn = 404


def _statusApi(code, message, data):
    return jsonify({"message": message or "", "data": data or {}, "code": code})


def success(message=None, data=None):
    return _statusApi(code=HttpCode.success, message=message, data=data)


def serverError(message="服务器错误"):
    return _statusApi(code=HttpCode.serverError, message=message, data=None)


def serverOn(message="服务器没有这个"):
    return _statusApi(code=HttpCode.serverOn, message=message, data=None)
