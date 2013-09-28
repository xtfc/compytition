import bumpy
import os, sys, shutil

# won't be able to find compytition package without this
if '.' not in sys.path:
	sys.path.append('.')

# if compytition/config.py doesn't exist, this explodes
try:
	from compytition.db import Database
	from compytition import app
except:
	pass

bumpy.config(cli=True)

@bumpy.task
def setup():
	'''Run standard setup tasks'''
	bumpy.shell('git submodule init')
	bumpy.shell('git submodule update')

@bumpy.task
def config():
	'''Create the default config file and open it with $EDITOR'''
	config_ex = os.path.join('compytition', 'config.py.example')
	config = os.path.join('compytition', 'config.py')
	if not os.path.exists(config):
		print "Copying example config..."
		shutil.copyfile(config_ex, config)

	os.system('{} "{}"'.format(os.getenv('EDITOR', 'nano'), config))

@bumpy.task
def new(name):
	'''Create a skeleton contest'''
	path = os.path.join('contests', name)

	print "Making skeleton contest directory..."
	os.makedirs(os.path.join(path, 'questions'))
	os.makedirs(os.path.join(path, 'solutions'))

	print "Making test question..."
	test = open(os.path.join(path, 'questions', 'test'), 'w+')
	test.write('This is a sample question file. You can use [Markdown](http://daringfireball.net/projects/markdown/) here.\n')
	test.close()

@bumpy.task
def init(name):
	'''Initialize/reset a contest database'''
	print "Reading question files..."
	question_path = os.path.join('contests', name, 'questions')
	questions = []
	for f in sorted(os.listdir(question_path)):
		path = os.path.join(question_path, f)
		questions.append([f, path, open(path).read()])

	db = Database(os.path.join('contests', name, 'data.db'))

	print "Creating users table..."
	db.query('drop table if exists users')
	db.query('''create table users (
		id integer primary key autoincrement,
		username text not null,
		nickname text not null,'''
		+ ', '.join(x[0] + ' integer default 0' for x in questions) + ')')

	print "Creating status table..."
	db.query('drop table if exists status')
	db.query('''create table status (
		id integer primary key autoincrement,
		username text not null,
		status integer not null,
		message text not null)''')

	print "Creating questions table..."
	db.query('drop table if exists questions')
	db.query('''create table questions (
		id integer primary key autoincrement,
		name text not null,
		path text not null,
		content text not null)''')

	print "Populating questions table..."
	db.querymany('insert into questions(name, path, content) values(?, ?, ?)', questions)

	db.commit()
	db.close()

@bumpy.private
def check_databases():
	contests = os.listdir('contests')
	for contest in contests:
		if not os.path.exists(os.path.join('contests', contest, 'data.db')):
			bumpy.abort('Contest "{0}" does not have a database. Please initialize it first:\n\tbumpy init {0}'.format(contest))

@bumpy.requires(check_databases)
def run():
	'''Run the production server'''
	app.run(host='0.0.0.0')

@bumpy.requires(check_databases)
def debug():
	'''Run the debug server'''
	app.run(host='0.0.0.0', debug=True)
