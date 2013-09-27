import flask
import os
import sys
from datetime import datetime
from flask import g, request, session
from functools import wraps
from werkzeug import secure_filename
from compytition import app
from compytition.db import Database

try:
	import ldap
except:
	print 'LDAP module not available'
	sys.exit(1)

def validate_login(username, password):
	if not password:
		password = ' '
	con = ldap.initialize(app.config['LDAP_SERVER'])
	dn = app.config['LDAP_DN'](username)
	rv = con.simple_bind(dn, password)

	try:
		r = con.result(rv)
		return (r[0] == 97)
	except:
		pass

	return False

def requires_login(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'username' not in session:
			flask.flash('You must be logged in to view this page')
			return flask.redirect(flask.url_for('login'))

		return func(*args, **kwargs)
	return wrapper

def requires_auth(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		auth = request.authorization
		if not auth or not validate_login(auth.username, auth.password):
			return flask.Response(
				'Could not verify your access level for that URL.\n'
				'You have to login with proper credentials.\n', 401,
				{'WWW-Authenticate': 'Basic realm="Login Required"'})
		session['username'] = auth.username
		return func(*args, **kwargs)
	return wrapper

@app.before_request
def before_request():
	if 'contest' in request.view_args:
		g.contest = request.view_args['contest']
		g.contest_path = os.path.join('contests', request.view_args['contest'])

		g.db = Database(os.path.join(g.contest_path, 'data.db'))
		g.scoreboard = g.db.query('select * from users order by id asc')
		g.questions = []
		for f in sorted(os.listdir(os.path.join(g.contest_path, 'questions'))):
			path = os.path.join(g.contest_path, 'questions', f)
			question = {
				'base': f,
				'src': path,
				'content': open(path).read(),
				}
			g.questions.append(question)

		if 'username' in session:
			uargs = [session['username']]
			user = g.db.query('select id from users where username=?', uargs, True)
			if user is None:
				g.db.query('insert into users(username) values(?)', uargs)
				g.db.commit()

			g.user = g.db.query('select * from users where username=?', uargs, True)
			g.status = g.db.query('select * from status where username=? order by id desc limit 5', uargs)

@app.teardown_request
def teardown_request(exception):
	temp = getattr(g, 'db', None)
	if temp is not None:
		temp.close()

@app.route('/<contest>')
def index(contest):
	return flask.render_template('index.html')

@app.route('/favicon.ico')
def favicon():
	return flask.abort(404)

@app.route('/<contest>/scoreboard')
def scoreboard(contest):
	return flask.render_template('scoreboard.html')

@app.route('/<contest>/status')
@requires_login
def status(contest):
	return flask.render_template('status.html')

@app.route('/<contest>/submit', methods=['POST'])
@requires_login
def submit(contest):
	ufile = request.files['solution']

	username = secure_filename(session['username'])
	question = secure_filename(request.form['question'])
	timestamp = secure_filename(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
	filename = secure_filename(ufile.filename)
	upload_path = os.path.join(
		app.config['SOLUTIONS_DIR'],
		username,
		question,
		timestamp)
	upload_file = os.path.join(upload_path, filename)

	try:
		os.makedirs(upload_path)
	except:
		flask.abort(500)

	ufile.save(upload_file)

	db.query('insert into status(username,status,message) values(?,?,?)',
		[session['username'], 0, 'Your submission for {} was uploaded'.format(question)])
	db.commit()
	return flask.redirect(flask.url_for('index', contest=g.contest))

@app.route('/<contest>/term', methods=['POST'])
@requires_auth
def term_submit(contest):
	submit(contest)
	return 'Success.\n'

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'username' in session:
		flask.flash('You are already logged in')
		return flask.redirect(flask.url_for('index', contest=g.contest))

	if request.method == 'GET':
		return flask.render_template('login.html')

	if validate_login(request.form['username'], request.form['password']):
		session['username'] = request.form['username']
		flask.flash('Logged in')
		return flask.redirect(flask.url_for('index', contest=g.contest))

	flask.flash('Invalid login')
	return flask.redirect(flask.url_for('login'))

@app.route('/logout')
def logout():
	session.pop('username', None)
	flask.flash('Logged out')
	return flask.redirect(flask.url_for('login'))
