from flask import render_template, request, jsonify
from collections import Counter
from flask import Blueprint

from workCms.databases.mysql_db import cursor, conn
from workCms.core.auxiliay import session_zsq

deployJL = Blueprint('deploy', __name__)


@deployJL.route('/deploy_data_handle', endpoint='deploy_data_handle')
@session_zsq
def deploy_data_handle():
    conn.ping(reconnect=True)
    cursor.execute("select * from maintain order by maintain_id desc limit 100")
    results = cursor.fetchall()

    date = []
    for i in results:
        for k, v in i.items():
            if k == "maintain_date":
                date.append(v)
    deployAndDate = dict(Counter(date))
    # 返回json数据
    return jsonify(
        dates=[k for k, _ in deployAndDate.items()],
        deploy_num=[v for _, v in deployAndDate.items()],
    )


@deployJL.route('/deploy_w', endpoint='deploy_w', methods=['GET'])
@session_zsq
def deploy_w():
    return render_template('deploy_w.html')


@deployJL.route('/deploy_w_database', endpoint='deploy_w_database', methods=['POST'])
@session_zsq
def deploy_w_database():
    deploy_date = request.form.get('date')
    deploy_time = request.form.get('time')
    deploy_info = request.form.get('info')
    deploy_name = request.form.get('deployName')

    cursor.execute(
        "INSERT INTO maintain (maintain_date, maintain_time, maintain_info, maintain_name)VALUES (%(maintain_date)s, %(maintain_time)s, %(maintain_info)s, %(maintain_name)s)",
        {
            "maintain_date": deploy_date,
            "maintain_time": deploy_time,
            "maintain_info": deploy_info,
            "maintain_name": deploy_name
        })
    conn.commit()
    return 'ok'


@deployJL.route('/deploy_zs', endpoint='deploy_zs', methods=['GET', 'POST'])
@session_zsq
def deploy_zs():
    conn.ping(reconnect=True)
    cursor.execute("select * from maintain order by maintain_id desc limit 200")
    results = cursor.fetchall()
    return render_template('deploy_zs.html', data=results)

@deployJL.route('/deploy_sx', endpoint='deploy_sx', methods=['POST'])
@session_zsq
def deploy_sx():
        start_num = request.form.get('start_num')
        stop_num = request.form.get('stop_num')
        if start_num == '' or stop_num == '':
            return render_template('deploy_zs.html')
        sql = """
            select * from maintain limit {s},{e}
        """.format(s=start_num, e=stop_num)
        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template('deploy_zs.html', data=results)

@deployJL.route('/deploy_search', endpoint='deploy_search', methods=['GET', 'POST'])
@session_zsq
def deploy_search():
    search = request.form['search']
    if search == '':
        return render_template('deploy_zs.html')
    conn.ping(reconnect=True)
    sql = """
            select * from maintain where maintain_info like '%{name}%'  order by maintain_id desc
        """.format(name=search)
    cursor.execute(sql)
    conn.commit()
    results = cursor.fetchall()
    return render_template('deploy_zs.html', data=results)
