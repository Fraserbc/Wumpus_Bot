#Import sqlite3 because database
import sqlite3

#Create the connection to the db
conn = sqlite3.connect("database.db")
cur = conn.cursor()

#Get the server prefixs
def get_prefixs():
	#sql statement
	cur.execute("SELECT * FROM prefixs")

	#Turn it into json
	prefixs = {}
	for row in cur.fetchall():
		prefixs[row[0]] = row[1]

	return prefixs