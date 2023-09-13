from prometheus_client import make_wsgi_app
from flask import Blueprint


metrics = Blueprint('metrics', __name__)


@metrics.route('/metrics', endpoint='/metrics')
def frag_metrics():
    return make_wsgi_app()
