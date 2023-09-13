from flask import Flask
from flask_cors import *
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from workCms.views.user import user
from workCms.views.deploy import deployJL
from workCms.views.shut import hefuJL
from workCms.views.event import eventJL
from workCms.views.serverCheck import server_check
from workCms.views.serviceone import serviceone
from workCms.views.file import file
from workCms.views.codePush import codepush
from workCms.views.deleteApi import delete
from workCms.databases.redis_db import redisx
from workCms.views.webhook import webhooks
from workCms.views.documents import documents
from workCms.views.system import system
from workCms.views.secure import secure
from workCms.views.serverAdm import serveradm
from workCms.views.metrics import metrics

# app = Flask(__name__, template_folder='workCms/templates', static_folder="workCms/static")
app = Flask(__name__)
app.secret_key = 'ddfkowfwfmfddddcccvvvrtRTYssa345oplyt'

#flask配置
app.config['JSON_AS_ASCII'] = False
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Shanghai'

# 支持跨域
# CORS(app, resources=r'/*')

# 定时任务配置
scheduler = APScheduler()
scheduler.init_app(app)

app.register_blueprint(user)
app.register_blueprint(deployJL)
app.register_blueprint(hefuJL)
app.register_blueprint(eventJL)
app.register_blueprint(server_check)
app.register_blueprint(serviceone)
app.register_blueprint(file)
app.register_blueprint(codepush)
app.register_blueprint(delete)
app.register_blueprint(redisx)
app.register_blueprint(webhooks)
app.register_blueprint(documents)
app.register_blueprint(system)
app.register_blueprint(secure)
app.register_blueprint(serveradm)
app.register_blueprint(metrics)
