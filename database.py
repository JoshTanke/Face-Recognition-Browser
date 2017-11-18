import sqlite3

conn = sqlite3.connect("my-database.db")

cursor = conn.cursor()



def addUser(name):
	cursor.execute("INSERT INTO users VALUES ( '" + name + "', 'google https://www.google.com/', '', '', '', '', '2')")
	conn.commit()



def getUserData(name):
	sql = "SELECT * FROM users WHERE name=?"
	cursor.execute(sql, [(name)])
	return cursor.fetchall()


def deleteUser(name):
	sql = "DELETE FROM users WHERE name = '" + name + "'"
	cursor.execute(sql)
	conn.commit()


def updateUser(name, siteInfo):
	sql = "SELECT count FROM users WHERE name=?"
	cursor.execute(sql, [(name)])
	count = cursor.fetchall()[0][0]
	sql = "UPDATE users SET site" + count + " = " +"'" + siteInfo + "'" + "WHERE name = '" + name + "'"
	cursor.execute(sql)
	count = int(count) + 1
	sql = "UPDATE users SET count = " + str(count) + " WHERE name = '" + name + "'"
	cursor.execute(sql)
	conn.commit()



