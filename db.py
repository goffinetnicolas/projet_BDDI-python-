import sqlite3

class DataBase:
    def __init__(self, dbName):
        self.dbName = dbName
        self.depTab=[]
        self.connection = sqlite3.connect('putDataBaseHere/' + dbName)
        self.command = self.connection.cursor()

        try:
            self.command.execute("""SELECT * FROM FuncDep""")
        except:
            self.command.execute("""CREATE TABLE FuncDep (table_name VARCHAR, lhs VARCHAR, rhs VARCHAR)""")


    def addDep(self, depObject):
        table_name = depObject.table_name
        lhs = depObject.lhs
        rhs = depObject.rhs
        self.depTab.append(depObject)
        self.command.execute("""INSERT INTO FuncDep VALUES ("""+table_name+""","""+lhs+""","""+rhs+""")""")

    def __str__(self):
        print(self.dbName)



