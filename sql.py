import _mysql
import MySQLdb
import re
from pybotextra import * 

# TODO: Get this info from config
host = 'localhost'
user = 'root'
password = ""
database = 'pybot'

class sql:
	def __init__(self):
		self.conn = _mysql.connect(host, user, password, database)
		printHTML("connected to database")
		
	def query_r(self, q):
		try:
			self.conn.query(q)
			result = self.conn.store_result()
			return result.fetch_row(maxrows=0)
		except:
			printHTML("Failed sql query", "filter")
			return False
		return False
	
	def query(self, q):
		self.conn.query(q)
	
	