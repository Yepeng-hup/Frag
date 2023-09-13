# 系统多线程池模块
import time
import json
import flask
from concurrent.futures import ThreadPoolExecutor

# app = flask.Flask(__name__)
sys_thread_pool = ThreadPoolExecutor()


# test mode

# def read_file():
#     time.sleep(1)
#     return "file"
#
#
# def read_db():
#     time.sleep(2)
#     return "database"
#
#
# def read_net():
#     time.sleep(3)
#     return "network"
#
#
# @app.route("/")
# def not_sys_pool_index():
#     filetext = read_file()
#     dbtext = read_db()
#     nettext = read_net()
#     return json.dumps({
#         "text1": filetext,
#         "text2": dbtext,
#         "text3": nettext,
#     })

# def sys_pool_index():
#     filetext = sys_thread_pool.submit(read_file)
#     dbtext = sys_thread_pool.submit(read_db)
#     nettext = sys_thread_pool.submit(read_net)
#     return json.dumps({
#         "text1": filetext.result(),
#         "text2": dbtext.result(),
#         "text3": nettext.result(),
#     })


# if __name__ == "__main__":
#     app.run()
