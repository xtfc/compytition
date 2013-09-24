import sqlite3
from contextlib import closing
from compytition import app

def init():
	with closing(connect()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def connect():
	return sqlite3.connect(app.config['DATABASE'])
