import yaml
import os
import traceback
from workCms import config

yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config.YAML_DIR)


def read_yaml():
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except:
        print(traceback.format_exc())


y = read_yaml()
_mysql = y.get("mysql")
mysql_dbname = _mysql.get("dbName")
mysql_dbhost = _mysql.get("dbHost")
mysql_port = _mysql.get("dbPort")
mysql_dbuser = _mysql.get("dbUser")
mysql_dbpasswd = _mysql.get("dbPasswd")

_flasks = y.get("flasks")
flask_host = _flasks.get("addr")
flask_port = _flasks.get("port")
flask_debug = _flasks.get("debug")

_redis = y.get("redis")
redis_host = _redis.get("host")
redis_port = _redis.get("port")
redis_dbName_num = _redis.get("dbName_num")
redis_passwd = _redis.get("passwd")

_data = y.get("data")
data_save = _data.get("PushData_save_dir")
ssh_port = _data.get("ssh_port")
cron = _data.get("crontab")
log_dir = _data.get("logs_dir")
sys_log_dir = _data.get("sys_log_dir")
system_secure = _data.get("system_secure")
ip_count_num = _data.get("ip_count_num")


