import flask
import os
import sys
from datetime import datetime
from flask import g, request, session
from functools import wraps
from werkzeug import secure_filename
from compytition import app, db

try:
	import ldap
except:
	print "LDAP module not available"
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

def authenticate():
	return flask.Response(
		'Could not verify your access level for that URL.\n'
		'You have to login with proper credentials', 401,
		{'WWW-Authenticate': 'Basic realm="Login Required"'})

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
			return authenticate()
		session['username'] = auth.username
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

		g.user = db.query('select * from users where username=?', [session['username']], one=True)
		g.scoreboard = db.query('select * from users order by id asc')
		g.status = db.query('select * from status where username=? order by id desc limit 5', [session['username']])


@app.teardown_request
def teardown_request(exception):
	temp = getattr(g, 'db', None)
	if temp is not None:
		temp.close()

@app.route('/')
@requires_login
def index():
	return flask.render_template('index.html')

@app.route('/scoreboard')
@requires_login
def scoreboard():
	return flask.render_template('scoreboard.html')

@app.route('/status')
@requires_login
def status():
	return flask.render_template('status.html')

@app.route('/submit', methods=['POST'])
@requires_login
def submit():
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

	db.execute('insert into status(username,status,message) values(?,?,?)',
		[session['username'], 0, 'Your submission for {} was uploaded'.format(question)])
	db.commit()
	return flask.redirect(flask.url_for('index'))

@app.route('/term', methods=['POST'])
@requires_auth
def term_submit():
	submit()
	return "Success."

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
