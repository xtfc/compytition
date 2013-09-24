import flask
import os
from flask import g, request, session
from functools import wraps
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
app.config['SECRET_KEY'] = 'thiskeyneedstobesecret'

def validate_login(username, password):
	return username == 'testlogin'

def requires_login(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'username' not in session:
			flask.flash('You must be logged in to view this page.')
			return flask.redirect(flask.url_for('login'))

		return func(*args, **kwargs)
	return wrapper

@app.before_request
def before_request():
	g.db = db.connect()

@app.teardown_request
def teardown_request(exception):
	temp = getattr(g, 'db', None)
	if temp is not None:
		temp.close()

@app.route('/')
@requires_login
def index():
	cur = g.db.execute('select id, username from users order by id asc')
	g.scoreboard = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]

	return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return flask.render_template('login.html')

	if validate_login(request.form['username'], request.form['password']):
		session['username'] = request.form['username']
		flask.flash('Logged in')
		return flask.redirect(flask.url_for('index'))

	flask.flash('Invalid login')
	return flask.redirect(flask.url_for('login'))

@app.route('/logout')
def logout():
	session.pop('username', None)
	flask.flash('Logged out')
	return flask.redirect(flask.url_for('login'))
