from flask import render_template, request, Blueprint

from .database import cursor, conn
from .auxiliay import session_zsq

eventJL = Blueprint('event', __name__)


@eventJL.route('/event_w', endpoint='event_w', methods=['GET'])
@session_zsq
def event_w():
    return render_template('event_w.html')


@eventJL.route('/event_w_database', endpoint='event_w_database', methods=['POST'])
@session_zsq
def event_w_database():
    event_date = request.form.get('date')
    event_info = request.form.get('info')
    event_name = request.form.get('eventName')

    cursor.execute(
        "INSERT INTO event (event_date, event_info, event_name) VALUES (%(event_date)s, %(event_info)s, %(event_name)s)",
        {
            "event_date": event_date,
            "event_info": event_info,
            "event_name": event_name
        })
    conn.commit()
    return ''


@eventJL.route('/event_zs', endpoint='event_zs', methods=['GET', 'POST'])
@session_zsq
def event_zs():
    cursor.execute("select * from event order by event_id desc")
    results = cursor.fetchall()
    return render_template('event_zs.html', data=results)


@eventJL.route('/event_search', endpoint='event_search', methods=['GET', 'POST'])
@session_zsq
def event_search():
    search = request.form['search']
    sql = """
                select * from event where event_info like '%{name}%'  order by event_id desc
        """.format(name=search)
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('event_zs.html', data=results)
