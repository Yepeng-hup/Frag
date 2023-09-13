from flask import Blueprint
from flask import render_template, request

from workCms.core.auxiliay import session_zsq
from workCms.databases.mysql_db import cursor, conn
from workCms import status_restful_api
from workCms.modeCls.alertModule import Alert

server_check = Blueprint('server_check', __name__)


@server_check.route("/server", endpoint="server")
@session_zsq
def serverCheck():
    return render_template('serverCheck.html')


@server_check.route("/server_w_database", endpoint='server_w_database', methods=['POST'])
@session_zsq
def server_w():
    datatime = request.form.get('datetime')
    serverName = request.form.get('serverName')
    dataBackup = request.form.get('dataBackup')
    serverStatus = request.form.get('serverStatus')
    policeNum = request.form.get('policeNum')
    policeInfo = request.form.get('policeInfo')
    checkName = request.form.get('checkName')
    cursor.execute(
        "INSERT INTO server (server_date, server_name, server_dataBackup, server_status, server_policeNum, server_info, server_userName) VALUES"
        "(%(server_date)s, %(server_name)s, %(server_dataBackup)s, %(server_status)s, %(server_policeNum)s, %(server_info)s,%(checkName)s)",
        {
            "server_date": datatime,
            "server_name": serverName,
            "server_dataBackup": dataBackup,
            "server_status": serverStatus,
            "server_policeNum": policeNum,
            "server_info": policeInfo,
            "checkName": checkName
        })
    conn.commit()
    return status_restful_api.success(message="数据提交成功！")


@server_check.route("/server_zs", endpoint="server_zs")
@session_zsq
def server_zs():
    cursor.execute("select * from server order by server_id desc limit 200")
    server_results = cursor.fetchall()
    return render_template("serverCheck_zs.html", rel=server_results)

@server_check.route('/server_sx', endpoint='server_sx', methods=['POST'])
@session_zsq
def server_sx():
        start_num = request.form.get('start_num')
        stop_num = request.form.get('stop_num')
        if start_num == '' or stop_num == '':
            return render_template('serverCheck_zs.html')
        sql = """
            select * from server limit {s},{e}
        """.format(s=start_num, e=stop_num)
        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template('serverCheck_zs.html', rel=results)


@server_check.route('/server_search', endpoint='server_search', methods=['GET', 'POST'])
@session_zsq
def deploy_search():
    search = request.form['search']
    if search == '':
        return render_template('serverCheck_zs.html')
    sql = """
        select * from server where server_info like '%{name}%'  order by server_id desc
    """.format(name=search)
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('serverCheck_zs.html', rel=results)


@server_check.route('/server/alert', endpoint='/server/alert')
@session_zsq
def alert():
    alerts = Alert()
    all_res = alerts.allAlertResult()
    today_date = alerts.todayDateResult()
    day_res = alerts.alldayAlertResult(today_date)
    alert_str, alert_num = alerts.alertScreen()
    return render_template('alertGather.html', all=all_res, day=day_res, str=alert_str, num=alert_num)
