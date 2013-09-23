import flask
from compytition import app

@app.route('/')
def index():
	return 'Hello, world!'
