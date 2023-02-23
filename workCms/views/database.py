import pymysql
import yaml, os, traceback
from dbutils.pooled_db import PooledDB

from workCms import config

yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config.YAML_DIR)


def project_config():
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data
x = project_config()
configs = []
for k, v in x.items():
    for s, j in v.items():
        configs.append(j)

pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True,
    ping=0,
    db=configs[0],
    user=configs[1],
    host=configs[2],
    port=configs[3],
    passwd=configs[4],
    charset='utf8mb4'

)
conn = pool.connection()

def database_conn():
    try:
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cursor
    except Exception:
        traceback.format_exc()

cursor = database_conn()

data_save = configs[5]
flask_port = configs[6]
flask_addr = configs[7]
debug = configs[8]
ssh_port = configs[9]
