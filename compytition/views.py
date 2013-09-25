import flask
import os
from datetime import datetime
from flask import g, request, session
from functools import wraps
from werkzeug import secure_filename
from compytition import app, db

# TODO move to config module
app.config['SOLUTIONS_DIR'] = 'solutions'
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
	return username and password == 'password'

def requires_login(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'username' not in session:
			flask.flash('You must be logged in to view this page')
			return flask.redirect(flask.url_for('login'))

		return func(*args, **kwargs)
	return wrapper

@app.before_request
def before_request():
	db.connect()
	if 'username' in session:
		user = db.query('select id from users where username=?', [session['username']], one=True)
		if user is None:
			db.execute('insert into users(username) values(?)', [session['username']])
			db.commit()

@app.teardown_request
def teardown_request(exception):
	temp = getattr(g, 'db', None)
	if temp is not None:
		temp.close()

@app.route('/')
@requires_login
def index():
	g.scoreboard = db.query('select id, username from users order by id asc')
	return flask.render_template('index.html')

@app.route('/submit', methods=['POST'])
@requires_login
def submit():
	ufile = request.files['solution']

	user = secure_filename(session['username'])
	question = secure_filename(request.form['question'])
	timestamp = secure_filename(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
	filename = secure_filename(ufile.filename)
	upload_path = os.path.join(
		app.config['SOLUTIONS_DIR'],
		user,
		question,
		timestamp)
	upload_file = os.path.join(upload_path, filename)

	try:
		os.makedirs(upload_path)
	except:
		flask.abort(500)

	ufile.save(upload_file)

	return flask.redirect(flask.url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'username' in session:
		flask.flash('You are already logged in')
		return flask.redirect(flask.url_for('index'))

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
