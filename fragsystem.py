from flask import render_template
import logging
from datetime import datetime

from workCms import app
from workCms.views.auxiliay import session_zsq
from workCms.views.database import (
    cursor,
    flask_port,
    flask_addr,
    debug)

logging.basicConfig(filename="./works.log", format='%(levelname)s - %(message)s')


@app.route('/home', endpoint='home')
@session_zsq
def home():
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("select COUNT(user_name) from users")
    rel = cursor.fetchall()
    rel = rel[0]
    rel = rel['COUNT(user_name)']
    return render_template('index_l.html', rel=rel, date=now_time)


if __name__ == "__main__":
    app.run(debug=debug, host=flask_addr, port=flask_port)
