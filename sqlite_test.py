import sqlite3


con = sqlite3.connect('putDataBaseHere/test.db')

c = con.cursor()

c.execute("""CREATE TABLE test ()""")
c.execute("""ALTER TABLE test ADD c1 VARCHAR""")
c.execute("""ALTER TABLE test ADD c2 VARCHAR""")
c.execute("""ALTER TABLE test ADD c3 VARCHAR""")
print(c.fetchall())

con.commit()

con.close()





