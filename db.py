import sqlite3

class DataBase:
    def __init__(self, db):
        dep=[]
        con = sqlite3.connect('putDataBaseHere/chinook.db')
        c = con.cursor()

        try:
            c.execute("""SELECT * FROM FuncDep""")
            a=c.fetchall()
            print(a)
        except:
            c.execute("""CREATE TABLE FuncDep ()""")

        self.db=db

    def __str__(self):
        print(self.db)



