import os
import traceback
from datetime import datetime
from flask import render_template, request, redirect, session, Blueprint, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from workCms import status_restful_api
from workCms.core.auxiliay import session_zsq, authority_check, climit
from workCms.databases.mysql_db import cursor, conn
from workCms.views.deleteApi import idSort

user = Blueprint('user', __name__)

file = "workCms/serviceall/txt/"
err_maxNum = 5


def db_passwd(user: str):
    lists = list()
    cursor.execute("select user_name,user_passwd from users where user_name=%(name)s", {"name": user})
    results = cursor.fetchall()
    for i in results:
        for _, v in i.items():
            lists.append(v)
    return lists


def check_user_login(error_num: str, user: str):
    with open(file + user + "@loginErrNum.txt", 'a', encoding='utf8') as f:
        f.write(error_num + "\n")


def _check_login_err(user: str):
    if not os.path.exists(file + user + '@loginErrNum.txt'):
        s = open(file + user + '@loginErrNum.txt', 'w')
        s.close()
    with open(file + user + "@loginErrNum.txt", 'r', encoding='utf8') as f:
        lines = f.readlines()
        total_lines = len(lines)
    return total_lines


@user.route('/', methods=['GET', 'POST'])
@climit(3)
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = request.form.get('Name')
        passwd = request.form.get('Password')
        hash_pwd = db_passwd(user)
        err_num = _check_login_err(user)
        if hash_pwd == []:
            if err_num <= err_maxNum:
                check_user_login("1", user)
                num = 6 - err_num
                return render_template('login.html', errorMgs=f'用户名或密码输入错误,输错{num}次账户会被锁定！')
            else:
                cursor.execute(" select user_locks from user_lock where user_name=%(user)s", {"user": user})
                results = cursor.fetchall()
                for i in results:
                    for _, v in i.items():
                        if v == "":
                            cursor.execute(
                                "INSERT INTO  `user_lock` (user_name, user_locks) VALUES (%(name)s, %(lock_status)s) ",
                                {"name": user, "lock_status": "true"})
                            conn.commit()
                            return render_template('login.html', errorMgs='您的账户已被锁定!')
                        elif v == "false":
                            cursor.execute(" UPDATE user_lock SET user_locks=\"true\" where user_name=%(user)s",
                                           {"user": user})
                            conn.commit()
                            return render_template('login.html', errorMgs='您的账户已被锁定!')
                return render_template('login.html', errorMgs='您的账户已被锁定!')

        cursor.execute(" select user_locks from user_lock where user_name=%(user)s",
                       {"user": user})
        results = cursor.fetchall()
        if len(results) == 0:
            cursor.execute(
                "INSERT INTO  `user_lock` (user_name, user_locks) VALUES (%(name)s, %(lock_status)s) ",
                {"name": user, "lock_status": "false"})
            conn.commit()
        cursor.execute(" select user_locks from user_lock where user_name=%(user)s",
                       {"user": user})
        results = cursor.fetchall()
        for i in results:
            for _, v in i.items():
                if v == "false" or v == "":
                    code = check_password_hash(hash_pwd[1], passwd)
                    db_usre = hash_pwd[0]
                    if user == db_usre and code == True:
                        session['user_info'] = user
                        with open(file + user + "@loginErrNum.txt", "r+") as f:
                            f.truncate(0)
                        if user != "admin":
                            with open(file + "login_logout.txt", 'a', encoding='utf8') as f:
                                f.write("登录时间: " + d + " " + "登录用户: " + user + "\n")
                        cursor.execute("SELECT user_identity FROM users WHERE user_name=%(name)s", {"name": user})
                        identity_name = cursor.fetchall()
                        if identity_name[0].get('user_identity', '') != "Admin":
                            newRouet = "/deploy_w"
                        else:
                            newRouet = "/home"
                        return render_template('index.html', loginUser=user,
                                               identity_name=identity_name[0].get('user_identity', ''),
                                               index_r=newRouet,
                                               )
                else:
                    return render_template('login.html', errorMgs='您的账户已被锁定!')

        if err_num <= err_maxNum:
            check_user_login("1", user)
            num = 6 - err_num
            return render_template('login.html', errorMgs=f'用户名或密码输入错误,输错{num}次账户会被锁定！')
        else:
            cursor.execute(" select user_locks from user_lock where user_name=%(user)s", {"user": user})
            results = cursor.fetchall()
            for i in results:
                for _, v in i.items():
                    if v == "":
                        cursor.execute(
                            "INSERT INTO  `user_lock` (user_name, user_locks) VALUES (%(name)s, %(lock_status)s) ",
                            {"name": user, "lock_status": "true"})
                        conn.commit()
                        return render_template('login.html', errorMgs='您的账户已被锁定!')
                    elif v == "false":
                        cursor.execute(" UPDATE user_lock SET user_locks=\"true\" where user_name=%(user)s",
                                       {"user": user})
                        conn.commit()
                        return render_template('login.html', errorMgs='您的账户已被锁定!')
            return render_template('login.html', errorMgs='您的账户已被锁定!')


@user.route("/user/lock/index", endpoint='/user/lock/index')
@session_zsq
@authority_check
def undoLockIndex():
    cursor.execute("select user_datetime,user_name,user_locks from user_lock where user_name not like \"admin\"")
    results = cursor.fetchall()
    cursor.execute("SELECT user_name,user_identity FROM users WHERE user_name NOT LIKE 'admin' ORDER BY user_id DESC")
    rel = cursor.fetchall()
    return render_template("lockIndex.html", lockList=results, userIdentity=rel)


@user.route("/user/lock/undo", endpoint='/user/lock/undo', methods=['POST'])
@session_zsq
def undoLock():
    lock_all = request.form.get('lock_status')
    lists = lock_all.split('\t')
    lock_userName = lists[2]
    lock_status = lists[3]
    if lock_status != "true":
        return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "用户解锁失败!"})
    else:
        try:
            cursor.execute(" UPDATE user_lock SET user_locks=\"false\" where user_name=%(name)s",
                           {"name": lock_userName})
            conn.commit()
        except:
            return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "SQL执行失败!"})
        return jsonify({"code": status_restful_api.HttpCode.success, "message": "用户解锁成功!"})


@user.route("/user/lock/add", endpoint='/user/lock/add', methods=['POST'])
@session_zsq
def addLock():
    lock_all = request.form.get('lock_status')
    lists = lock_all.split('\t')
    lock_userName = lists[2]
    lock_status = lists[3]
    if lock_status != "false":
        return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "用户加锁失败!"})
    else:
        try:
            cursor.execute(" UPDATE user_lock SET user_locks=\"true\" where user_name=%(name)s",
                           {"name": lock_userName})
            conn.commit()
        except:
            return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "SQL执行失败!"})
    return jsonify({"code": status_restful_api.HttpCode.success, "message": "用户加锁成功!"})


@user.route('/logout')
def logout():
    d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if session['user_info'] != "admin":
        with open(file + "login_logout.txt", 'a', encoding='utf8') as f:
            f.write("退出时间: " + d + " " + "退出用户: " + session['user_info'] + "\n")
    del session['user_info']
    return redirect('/')


@user.route("/user/usercreate", endpoint='/user/usercreate', methods=['POST', 'GET'])
@session_zsq
@authority_check
def userCreate():
    if request.method == 'GET':
        return render_template('userCreate.html')
    else:
        user = request.form.get('user')
        passwd = request.form.get('passwd')
        authority = request.form.get('authority')
        hash_pwd = generate_password_hash(passwd)
        try:
            cursor.execute("INSERT INTO users (user_name,user_passwd,user_identity) "
                           "VALUES (%(name)s,%(passwd)s,%(identity)s)",
                           {"name": user, "passwd": hash_pwd, "identity": authority})
            conn.commit()
            return jsonify({"code": status_restful_api.HttpCode.success, "message": "用户创建成功!"})
        except:
            print(traceback.format_exc())
            return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "用户创建失败!"})


@user.route("/user/userlist", endpoint='/user/userlist')
@session_zsq
@authority_check
def userlist():
    cursor.execute("SELECT user_name,user_datetime FROM users WHERE user_name NOT LIKE 'admin' ORDER BY user_id DESC")
    rel = cursor.fetchall()
    return render_template('userlist.html', userName=rel)


@user.route('/user/delete', endpoint='/user/delete', methods=['POST'])
@session_zsq
@authority_check
def delete():
    userInfo = request.form.get('name')
    userList = userInfo.split('\t')
    deleteUser = userList[1]
    try:
        cursor.execute("delete from users where user_name=%(name)s", {"name": deleteUser})
        cursor.execute("delete from user_lock where user_name=%(name)s", {"name": deleteUser})
        conn.commit()
        idSort("user", "user_id")
    except:
        traceback.format_exc()
    return ""


@user.route('/user/update', endpoint='/user/update', methods=['POST'])
@session_zsq
@authority_check
def pwdUpdate():
    try:
        user = request.form.get('user')
        passwd = request.form.get('passwd')
        hash_pwd = generate_password_hash(passwd)
        cursor.execute("UPDATE users SET user_passwd = %(passwd)s WHERE user_name = %(user)s", {
            "user": user,
            "passwd": hash_pwd
        })
        conn.commit()
        return jsonify({"code": status_restful_api.HttpCode.success, "message": "密码修改成功!"})
    except:
        traceback.format_exc()
        return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error,密码修改失败!!!"})
