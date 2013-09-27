import flask
import sqlite3
from contextlib import closing
from compytition import app

class Database:
	def __init__(self, path):
		self.path = path
		self._connection = None

	def create(self):
		with closing(self.connect()) as db:
			with app.open_resource('schema.sql', mode='r') as f:
				db.cursor().executescript(f.read())
			db.commit()

	def connect(self):
		if not self._connection:
			self._connection = sqlite3.connect(self.path)
			self._connection.row_factory = sqlite3.Row

		return self._connection

	def close(self):
		if self._connection:
			self._connection.close()

	def query(self, query, args=(), one=False):
		cur = self.connect().execute(query, args)
		rv = cur.fetchall()
		cur.close()
		return (rv[0] if rv else None) if one else rv

	def querymany(self, query, args):
		cur = self.connect().executemany(query, args)

	def commit(self):
		self.connect().commit()
