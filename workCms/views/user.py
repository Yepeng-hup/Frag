from flask import render_template, request, redirect, session, Blueprint, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import traceback

from .auxiliay import session_zsq
from .database import cursor, conn
from .deleteApi import idSort
from workCms import status_restful_api

user = Blueprint('user', __name__)


def db_passwd(user: str):
    lists = list()
    cursor.execute("select user_name,user_passwd from users where user_name=%(name)s", {"name": user})
    results = cursor.fetchall()
    for i in results:
        for _, v in i.items():
            lists.append(v)
    return lists


@user.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = request.form.get('Name')
        passwd = request.form.get('Password')
        hash_pwd = db_passwd(user)
        if hash_pwd == []:
            return render_template('login.html', errorMgs='用户名不存在!')
        code = check_password_hash(hash_pwd[1], passwd)
        db_usre = hash_pwd[0]
        if user == db_usre and code == True:
            session['user_info'] = user
            return render_template('index.html')
        else:
            return render_template('login.html', errorMgs='用户名或密码输入错误！')


@user.route('/logout')
def logout():
    del session['user_info']
    return redirect('/')


@user.route("/user/usercreate", endpoint='/user/usercreate', methods=['POST', 'GET'])
@session_zsq
def userCreate():
    if request.method == 'GET':
        return render_template('userCreate.html')
    else:
        user = request.form.get('user')
        passwd = request.form.get('passwd')
        authority = request.form.get('authority')
        hash_pwd = generate_password_hash(passwd)
        cursor.execute("INSERT INTO users (user_name,user_passwd,user_identity) "
                       "VALUES (%(name)s,%(passwd)s,%(identity)s)", {"name": user, "passwd": hash_pwd, "identity": authority})
        conn.commit()
        return jsonify({"code": status_restful_api.HttpCode.success, "message": "用户创建成功!"})



@user.route("/user/userlist", endpoint='/user/userlist')
@session_zsq
def userlist():
    cursor.execute("select user_name,user_datetime from users order by user_id desc")
    rel = cursor.fetchall()
    return render_template('userlist.html', userName=rel)


@user.route('/user/delete', endpoint='/user/delete', methods=['POST'])
@session_zsq
def delete():
    userInfo = request.form.get('name')
    userList = userInfo.split('\t')
    deleteUser = userList[1]
    try:
        cursor.execute("delete from users where user_name=%(name)s", {"name": deleteUser})
        conn.commit()
        idSort("user", "user_id")
    except:
        traceback.format_exc()


@user.route('/user/update', endpoint='/user/update', methods=['POST'])
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