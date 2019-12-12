import sqlite3

con = sqlite3.connect('putDataBaseHere/chinook.db')

c = con.cursor()

c.execute("""SELECT * FROM albums""")

print(c.fetchone()) #print the first line of 'album' relation

con.commit()

con.close()

