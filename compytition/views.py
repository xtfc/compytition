import flask
from compytition import app

@app.route('/')
def index():
	scoreboard = []
	scoreboard.append({'name': 'John', 'score': 10})
	scoreboard.append({'name': 'Phil', 'score': 0})
	scoreboard.append({'name': 'Tyler', 'score': -10})

	questions = []
	questions.append({'content': 'Do some *emphasis*.'})
	questions.append({'content': 'Do some **strong**.'})
	questions.append({'content': 'Do some ***emphasized strong***.'})
	questions.append({'content': 'Do some `code`.'})

	return flask.render_template('index.html', scoreboard=scoreboard, questions=questions)
