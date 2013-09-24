import os
import flask
from compytition import app

# TODO move to config module
app.config['QUESTION_DIR'] = 'questions'

@app.route('/')
def index():
	scoreboard = []
	scoreboard.append({'name': 'John', 'score': 10})
	scoreboard.append({'name': 'Phil', 'score': 0})
	scoreboard.append({'name': 'Tyler', 'score': -10})

	questions = []
	for f in sorted(os.listdir(app.config['QUESTION_DIR'])):
		path = os.path.join(app.config['QUESTION_DIR'], f)
		questions.append({'base': f, 'src': path, 'content': open(path).read()})

	return flask.render_template('index.html', scoreboard=scoreboard, questions=questions)
