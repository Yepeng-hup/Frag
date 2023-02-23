from flask import Flask
from .views.user import user
from .views.deploy import deployJL
from .views.shut import hefuJL
from .views.event import eventJL
from .views.serverCheck import server_check
from .views.serviceone import serviceone
from .views.file import file
from .views.codePush import codepush
from .views.deleteApi import delete

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