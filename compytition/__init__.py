import flask
from werkzeug.contrib.fixers import ProxyFix
from flaskext.markdown import Markdown

app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
Markdown(app)

import compytition.config
import compytition.filters
import compytition.views
