import sqlite3


con = sqlite3.connect('putDataBaseHere/test.db')

c = con.cursor()

c.execute("SELECT * FROM albums")

print(c.fetchall())

con.commit()

con.close()





