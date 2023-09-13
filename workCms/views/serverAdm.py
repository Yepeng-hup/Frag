from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import traceback
from werkzeug.security import check_password_hash, generate_password_hash

from workCms.databases.mysql_db import conn, cursor
from workCms.core.auxiliay import session_zsq
from workCms.status_restful_api import HttpCode

serveradm = Blueprint("serveradm", __name__)
d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@serveradm.route('/server/list/index', endpoint='/server/list/index')
@session_zsq
def serveradm_index():
    cursor.execute("SELECT ssh_list_hostname,ssh_list_hostip,ssh_list_port,ssh_list_user FROM server_ssh_list ORDER BY ssh_list_id DESC")
    rel = cursor.fetchall()
    return render_template("sshserver.html", rel=rel)


@serveradm.route('/server/list/create', endpoint='/server/list/create', methods=['GET', 'POST'])
@session_zsq
def serveradm_index():
    if request.method == 'GET':
        return render_template("servercreate.html")
    else:
        hostname = request.form.get("hostname")
        ipaddr = request.form.get("ipaddr")
        port = request.form.get("port")
        user = request.form.get("user")
        passwd = request.form.get("passwd")
        sys_user = request.form.get("user_xz")
        hash_passwd = generate_password_hash(passwd)
        print(hostname, ipaddr, port, user, hash_passwd, sys_user)
        try:
            cursor.execute(
                "INSERT INTO server_ssh_list (ssh_list_hostname,ssh_list_hostip,ssh_list_port,ssh_list_user,ssh_list_password,ssh_list_system_user) "
                "VALUES (%(hostname)s,%(ipaddr)s,%(port)s,%(user)s,%(passwd)s,%(sys_user)s)",
                {"hostname": hostname, "ipaddr": ipaddr, "port": port, "user": user, "passwd": hash_passwd,
                 "sys_user": sys_user})
            conn.commit()
            return jsonify({"code": HttpCode.success, "message": "主机创建成功."})
        except:
            print(traceback.format_exc())
            return jsonify({"code": HttpCode.serverError, "message": "主机创建失败!"})
