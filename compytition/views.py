import flask
from compytition import app

@app.route('/')
def index():
	scoreboard = []
	scoreboard.append({'name': 'John', 'score': 10})
	scoreboard.append({'name': 'Phil', 'score': 0})
	scoreboard.append({'name': 'Tyler', 'score': -10})

	questions = []
	questions.append({'content': '*Question 1* is hard.'})
	questions.append({'content': '**Question 2** is `weird`.'})

	return flask.render_template('index.html', scoreboard=scoreboard, questions=questions)
