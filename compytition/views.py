import flask
from compytition import app

@app.route('/')
def index():
	scoreboard = []
	scoreboard.append({'name': 'John', 'score': 10})
	scoreboard.append({'name': 'Phil', 'score': 0})
	scoreboard.append({'name': 'Tyler', 'score': -10})
	return flask.render_template('scoreboard.html', scoreboard=scoreboard)
