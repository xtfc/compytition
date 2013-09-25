import flask
import sqlite3
from contextlib import closing
from compytition import app

def init():
	with closing(sqlite3.connect(app.config['DATABASE'])) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def connect():
	db = getattr(flask.g, 'db', None)
	if db is None:
		db = sqlite3.connect(app.config['DATABASE'])
		db.row_factory = sqlite3.Row
		flask.g.db = db
	return db

def query(query, args=(), one=False):
	cur = connect().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

def execute(query, args=()):
	flask.g.db.execute(query, args)

def commit():
	flask.g.db.commit()

