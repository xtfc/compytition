import flask
from compytition import app

@app.route('/')
def index():
	return flask.render_template('index.html', content='<p>Hello, world!</p>')
