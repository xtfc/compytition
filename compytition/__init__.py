import flask
from werkzeug.contrib.fixers import ProxyFix

app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

import compytition.filters, compytition.views
