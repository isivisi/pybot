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
		self.conn = False
		try:
			self.conn = _mysql.connect(host, user, password, database)
			pybotPrint("connected to database")
		except:
			pybotPrint("Could not connect to database")
			self.conn = False
	def query_r(self, q):
		try:
			self.conn.query(q)
			result = self.conn.store_result()
			return result.fetch_row(maxrows=0)
		except:
			pybotPrint("Failed sql query", "filter")
			return False
		return False
	
	def query(self, q):
		try:
			self.conn.query(q)
		except:
			pybotPrint("Failed sql query", "filter")
			return False
	
	