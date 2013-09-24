import os
import flask
from flask import g, request
from compytition import app, db

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

@app.before_request
def before_request():
	g.db = db.connect()

@app.teardown_request
def teardown_request(exception):
	temp = getattr(g, 'db', None)
	if temp is not None:
		temp.close()

@app.route('/')
def index():
	cur = g.db.execute('select id, username from users order by id asc')
	g.scoreboard = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]

	return flask.render_template('index.html')
