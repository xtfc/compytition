import os
import flask
from compytition import app

# TODO move to config module
app.config['QUESTION_DIR'] = 'questions'
app.config['QUESTIONS'] = []
for f in sorted(os.listdir(app.config['QUESTION_DIR'])):
	path = os.path.join(app.config['QUESTION_DIR'], f)
	question = {
		'base': f,
		'src': path,
		'content': open(path).read()
		}
	app.config['QUESTIONS'].append(question)
app.config['DATABASE'] = '/tmp/compytition.db'

@app.route('/')
def index():
	flask.g.scoreboard = []
	flask.g.scoreboard.append({'name': 'John', 'score': 10})
	flask.g.scoreboard.append({'name': 'Phil', 'score': 0})
	flask.g.scoreboard.append({'name': 'Tyler', 'score': -10})

	return flask.render_template('index.html')
