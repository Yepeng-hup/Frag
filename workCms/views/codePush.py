import paramiko
import traceback
import logging
from flask import Blueprint, render_template, request, jsonify, session

from workCms.core.auxiliay import session_zsq, dates
from workCms import status_restful_api
from workCms.core.conf import ssh_port
from workCms.modeCls.securityModule import Security

codepush = Blueprint('codepush', __name__)

auditFileDir = "workCms/serviceall/txt/commandAudit.txt"
cmdFileDir = "workCms/serviceall/txt/cmdResult.txt"


def linuxAudit(ipAndHostname: str, code: str):
    s = '，'
    with open(auditFileDir, 'a', encoding='utf8') as f:
        f.write(f"平台执行用户: {session['user_info']}{s} 执行时间: {dates}{s}远程服务器地址: [{ipAndHostname}]{s}执行代码: [{code}]\n")
        f.close()


def sshConnServer(serverIp: str, user: str, passwd: str, port: int, code: str):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=serverIp, port=port, username=user, password=passwd)
        stdin, stdout, stderr = ssh.exec_command(code)
        res = stdout.read()
        err = stderr.read()
        ssh.close()
        if res.decode() == '':
            return err.decode()
        else:
            return res.decode()
    except:
        print(traceback.format_exc())


@codepush.route('/data/audit', endpoint='/data/audit')
@session_zsq
def catAudit():
    f = open(auditFileDir, 'r', encoding='utf8')
    audit_all_text = f.read()
    auditAll = audit_all_text.split('\n')
    # 列表反转
    auditAll.reverse()
    f.close()
    return render_template('audit.html', auditInfo=auditAll)


@codepush.route('/data/res', endpoint='/data/res')
@session_zsq
def catCmdRes():
    f = open(cmdFileDir, 'r', encoding='utf8')
    cmdRes_all_text = f.read()
    f.close()
    return render_template('codepush.html', cmdResInfo=cmdRes_all_text)


@codepush.route('/data/linux', endpoint='/data/linux', methods=['POST', 'GET'])
@session_zsq
def linuxHandle():
    if request.method == 'GET':
        return render_template('codepush.html')
    else:
        serverIp = request.form.get('serverIp')
        user = request.form.get('user')
        passwd = request.form.get('passwd')
        code = request.form.get('code')

        if user == '':
            user = 'root'
        if serverIp == '':
            serverIp = '127.0.0.1'

        obj = Security(code)
        errCode = obj.cmdSecurity()
        if errCode == True:
            logging.error('Execute login user: '+session['user_info']+' '+dates + ' Code has been blocked from executing -> ' + code)
            return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error,代码执行失败！"})
        else:
            res = sshConnServer(serverIp, user, passwd, ssh_port, code)
            with open(cmdFileDir, 'w', encoding='utf8') as f:
                f.write(res)
                f.close()
        linuxAudit(serverIp, code)
        return jsonify({"code": status_restful_api.HttpCode.success, "message": "代码执行成功！"})


# @codepush.route('/data/linuxcp', endpoint='/data/linuxcp', methods=['POST'])
# @session_zsq
# def linuxCpHandle():
#     src = request.form.get('src')
#     dest = request.form.get('dest')
#     linuxCmd = '\cp -rf' + ' ' + src + ' ' + dest
#     obj_s = Security(src)
#     errCode = obj_s.cmdSpecialStrSecurity()
#     if errCode == True:
#         print('代码已被阻止执行 -> ', src)
#         return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error,代码执行失败！"})
#     obj_d = Security(dest)
#     errCode = obj_d.cmdSpecialStrSecurity()
#     if errCode == True:
#         print('代码已被阻止执行 -> ', dest)
#         return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error,代码执行失败！"})
#     try:
#         res = os.system(linuxCmd)
#         if res != 1:
#             return jsonify({"code": status_restful_api.HttpCode.success, "message": "拷贝成功!"})
#         else:
#             return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error,执行拷贝失败!!!"})
#     except:
#         return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error,执行拷贝失败!!!"})
