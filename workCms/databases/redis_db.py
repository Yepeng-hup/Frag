from flask import render_template, Blueprint, request, jsonify
from workCms.core.auxiliay import session_zsq
from workCms.status_restful_api import HttpCode
from workCms.modeCls.redisModule import Redis_str, Redis_list

redisx = Blueprint('redisx', __name__)

cmdFileDir = "workCms/serviceall/txt/redisResult.txt"

@redisx.route('/redisx/index', endpoint='/redisx/index')
@session_zsq
def redis_index():
    return render_template('rs.html')


@redisx.route('/redisx/rel', endpoint='/redisx/rel')
@session_zsq
def rel():
    f = open(cmdFileDir, 'r', encoding='utf8')
    cmdRes_all_text = f.read()
    f.close()
    return render_template('cmdRes.html', cmdResInfo=cmdRes_all_text)


@redisx.route('/redisx/str', endpoint='/redisx/str', methods=['POST', 'GET'])
@session_zsq
def str():
    if request.method == "POST":
        cmd = request.form.get('cmd')
        k = request.form.get('k')
        v = request.form.get('v')
        k_time = request.form.get('k_time')
        if cmd == "set":
            rs = Redis_str(k=k, v=v)
            rel = rs.r_set()
            if rel == HttpCode.success:
                return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
            return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
        elif cmd == "del":
            rs = Redis_str(k=k)
            rel = rs.r_del()
            if rel == HttpCode.success:
                return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
            return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
        elif cmd == "append":
            rs = Redis_str(k=k, v=v)
            rel = rs.r_append()
            if rel == HttpCode.success:
                return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
            return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
        elif cmd == "get":
            rs = Redis_str(k=k)
            rel = rs.r_get()
            if rel == HttpCode.serverError:
                return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
            with open(cmdFileDir, 'w', encoding='utf8') as f:
                f.write("return value:  \n" + rel)
                f.close()
            return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
        elif cmd == "strlen":
            rs = Redis_str(k=k)
            rel = rs.r_strlen()
            if rel == HttpCode.serverError:
                return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
            with open(cmdFileDir, 'w', encoding='utf8') as f:
                f.write(f"return value: {rel}")
                f.close()
            return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
        else:
            rs = Redis_str(k=k, v=v, k_time=k_time)
            rel = rs.r_setex()
            if rel == HttpCode.success:
                return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
            return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
    else:
        return render_template('rs.html')


@redisx.route('/redisx/list', endpoint='/redisx/list', methods=['POST'])
@session_zsq
def lists():
    cmd = request.form.get('cmd')
    k = request.form.get('k')
    v = request.form.get('v')
    index_s = request.form.get('index_s')
    index_end = request.form.get('index_end')
    if cmd == "lpush":
        rs = Redis_list(k=k)
        rel = rs.r_lpush(v)
        if rel == HttpCode.success:
            return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
        return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})

    elif cmd == "lindex":
        rs = Redis_list(k=k)
        rel = rs.r_lindex(index_s)
        if rel == HttpCode.serverError:
            return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
        with open(cmdFileDir, 'w', encoding='utf8') as f:
            f.write(f"return value: {rel}")
            f.close()
        return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
    elif cmd == "lpop":
        rs = Redis_list(k=k)
        rel = rs.r_lpop()
        if rel == HttpCode.success:
            return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
        return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
    else:
        rs = Redis_list(k=k)
        rel = rs.r_lrange(index_s, index_end)
        if rel == HttpCode.serverError:
            return jsonify({"code": HttpCode.serverError, "message": "命令执行失败!"})
        with open(cmdFileDir, 'w', encoding='utf8') as f:
            f.write(f"return value: {rel}")
            f.close()
        return jsonify({"code": HttpCode.success, "message": "命令执行成功!"})
