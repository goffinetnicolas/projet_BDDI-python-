import sqlite3


con = sqlite3.connect('putDataBaseHere/test.db')

c = con.cursor()

c.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)",
                                    ("albums", "ArtistId Title", "AlbumId"))

print(c.fetchall())

con.commit()

con.close()





