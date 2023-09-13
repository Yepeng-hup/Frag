import logging
import os
import psutil
from flask import render_template

from workCms import app
from workCms import scheduler
from workCms.core.conf import cron
from workCms.views.user import file
from workCms.core.auxiliay import session_zsq, authority_check
from workCms.databases.mysql_db import cursor, conn
from workCms.core.conf import flask_host, flask_port, flask_debug, log_dir
from workCms.core.syslog import zip_logs


logging.basicConfig(filename=log_dir + "/" + "frag_local.log", format='%(levelname)s - %(message)s')


@app.route('/home', endpoint='home')
@session_zsq
@authority_check
def home():
    # now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # cursor.execute("select COUNT(user_name) from users")
    # rel = cursor.fetchall()
    # rel = rel[0]
    # rel = rel['COUNT(user_name)']
    f = open(file + "login_logout.txt", 'r', encoding='utf-8')
    try:
        login_all_text = f.read()
        loginAll = reversed(login_all_text.split('\n'))
    finally:
        f.close()
    # return render_template('index_l.html', rel=rel, date=now_time, loginLog=loginAll)
    return render_template('index_l.html', loginLog=loginAll)


def deleteLog():
    deleteLogDir = "workCms/serviceall/txt/"

    def ck_dbUser():
        dbUserList = []
        cursor.execute(" select user_name from users")
        results = cursor.fetchall()
        for i in results:
            for _, v in i.items():
                dbUserList.append(v)
        return dbUserList

    def deleteLoginFileNotUser(userList: list(), dbUserList: list()):
        d = list()
        for i in userList:
            if i not in dbUserList:
                d.append(i)
        for user in d:
            if os.path.exists(deleteLogDir + user + "@loginErrNum.txt"):
                os.remove(deleteLogDir + user + "@loginErrNum.txt")
                print(f"无效用户文件已被删除 --> {user}@loginErrNum.txt")
        return

    dbUserList = ck_dbUser()
    file_user = []
    fileList = os.listdir(deleteLogDir)
    for txt in fileList:
        start = txt.find("@")
        if start > 0:
            s = txt[:start]
            file_user.append(s)
    deleteLoginFileNotUser(file_user, dbUserList)
    return


# 每隔40秒执行一次函数
# h = hours
@scheduler.task('interval', id='system_w_databaseJOB', seconds=40, misfire_grace_time=700, jitter=2)
def system_w_database():
    svmem = psutil.virtual_memory()
    memFree = svmem.used / 1024 / 1024
    cpu_res = psutil.cpu_percent()
    cursor.execute("INSERT INTO system (system_ResourcesName, system_ResourcesNum) VALUES (%(cpu)s, %(use_num)s)",
                   {"use_num": cpu_res, "cpu": "CPU"})
    cursor.execute("INSERT INTO system (system_ResourcesName, system_ResourcesNum) VALUES (%(mem)s, %(mem_num)s)",
                   {"mem_num": memFree, "mem": "MEM"})
    conn.commit()


# 创建一个定时任务，该任务在每天的1点10分10秒执行, *是通配符
@scheduler.task('cron', day_of_week='*', hour=1, minute='10', second='10')
def zip_log_cron():
    zip_logs(log_dir)


if __name__ == "__main__":
    deleteLog()
    if cron:
        scheduler.start()
    app.run(debug=flask_debug, host=flask_host, port=flask_port)

