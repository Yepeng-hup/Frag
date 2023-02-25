from flask import Flask
from workCms.views.user import user
from workCms.views.deploy import deployJL
from workCms.views.shut import hefuJL
from workCms.views.event import eventJL
from workCms.views.serverCheck import server_check
from workCms.views.serviceone import serviceone
from workCms.views.file import file
from workCms.views.codePush import codepush
from workCms.views.deleteApi import delete

app = Flask(__name__)
app.secret_key = 'ddfkowfwfmfddddcccvvvrtRTYssa345oplyt'
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(user)
app.register_blueprint(deployJL)
app.register_blueprint(hefuJL)
app.register_blueprint(eventJL)
app.register_blueprint(server_check)
app.register_blueprint(serviceone)
app.register_blueprint(file)
app.register_blueprint(codepush)
app.register_blueprint(delete)