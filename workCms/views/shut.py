from flask import jsonify, render_template, request, Blueprint
from collections import Counter
from workCms.databases.mysql_db import cursor, conn
from workCms.core.auxiliay import session_zsq

hefuJL = Blueprint('hefu', __name__)


@hefuJL.route('/hefu_data_handle', endpoint='hefu_data_handle', methods=['GET', 'POST'])
@session_zsq
def hefu_data_handle():
    conn.ping(reconnect=True)
    print("Connected!")
    cursor.execute("select * from hefu order by hefu_id desc")
    hefu_results = cursor.fetchall()

    date = []
    for i in hefu_results:
        for k, v in i.items():
            if k == "hefu_date":
                date.append(v)
    hefuAndDate = dict(Counter(date))
    return jsonify(
        dates=[k for k, _ in hefuAndDate.items()],
        hefu_num=[v for _, v in hefuAndDate.items()]
    )


@hefuJL.route('/hefu_w', endpoint='hefu_w', methods=['GET', 'POST'])
@session_zsq
def hefu_w():
    return render_template('hefu_w.html')


@hefuJL.route('/hefu_w_database', endpoint='hefu_w_database', methods=['GET', 'POST'])
@session_zsq
def hefu_w_database():
    hefu_date = request.form.get('date')
    hefu_time = request.form.get('time')
    hefu_info = request.form.get('info')
    hefuName = request.form.get('hefuName')

    cursor.execute(
        "INSERT INTO hefu (hefu_date, hefu_time, hefu_info, hefu_name)VALUES (%(hefu_date)s, %(hefu_time)s, %(hefu_info)s, %(hefu_name)s)",
        {
            "hefu_date": hefu_date,
            "hefu_time": hefu_time,
            "hefu_info": hefu_info,
            "hefu_name": hefuName
        })
    conn.commit()
    return 'ok'


@hefuJL.route('/hefu_zs', endpoint='hefu_zs', methods=['GET', 'POST'])
@session_zsq
# @execute_time_decorator
def hefu_zs():
    conn.ping(reconnect=True)
    cursor.execute("select * from hefu order by hefu_id desc limit 200")
    results = cursor.fetchall()
    return render_template('hefu_zs.html', data=results)

@hefuJL.route('/hefu_sx', endpoint='hefu_sx', methods=['POST'])
@session_zsq
def hefu_sx():
        start_num = request.form.get('start_num')
        stop_num = request.form.get('stop_num')
        if start_num == '' or stop_num == '':
            return render_template('hefu_zs.html')
        sql = """
            select * from hefu limit {s},{e}
        """.format(s=start_num, e=stop_num)
        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template('hefu_zs.html', data=results)


@hefuJL.route('/hefu_search', endpoint='hefu_search', methods=['GET', 'POST'])
@session_zsq
def hefu_search():
    search = request.form['search']
    if search == '':
        return render_template('hefu_zs.html')
    sql = """
            select * from hefu where hefu_info like '%{name}%'  order by hefu_id desc
        """.format(name=search)
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('hefu_zs.html', data=results)
