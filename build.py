import bumpy
import os, sys, shutil

if '.' not in sys.path:
	sys.path.append('.')
from compytition.db import Database
from compytition import app

bumpy.config(cli=True)

@bumpy.task
def new(name):
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
		username text not null,'''
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

@bumpy.task
def run():
	app.run(host='0.0.0.0')

@bumpy.task
def debug():
	app.run(host='0.0.0.0', debug=True)

@bumpy.task
def config():
	config_ex = os.path.join('compytition', 'config.py.example')
	config = os.path.join('compytition', 'config.py')
	if not os.path.exists(config):
		print "Copying example config..."
		shutil.copyfile(config_ex, config)

	os.system('{} "{}"'.format(os.getenv('EDITOR', 'nano'), config))
