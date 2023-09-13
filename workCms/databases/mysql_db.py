import pymysql
import traceback
from dbutils.pooled_db import PooledDB

from workCms.core.conf import (
    mysql_dbname, mysql_dbhost, mysql_port, mysql_dbuser, mysql_dbpasswd
)

pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True,
    ping=0,
    db=mysql_dbname,
    user=mysql_dbuser,
    host=mysql_dbhost,
    port=mysql_port,
    passwd=mysql_dbpasswd,
    charset='utf8mb4'

)
conn = pool.connection()


def database_conn():
    try:
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cursor
    except Exception:
        print(traceback.format_exc())


cursor = database_conn()

