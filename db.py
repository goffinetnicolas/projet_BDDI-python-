import sqlite3


class DataBase:
    def __init__(self, db_name):

        """ Represent a data base """

        self.dbName = db_name
        self.depTab = []  # list of Dep object

        self.connection = sqlite3.connect('putDataBaseHere/' + db_name)
        self.command = self.connection.cursor()

        try:
            self.command.execute("""SELECT * FROM FuncDep""")
            # check if the FuncDep table is created
        except:
            self.command.execute(
                """CREATE TABLE FuncDep (table_name VARCHAR, lhs VARCHAR, rhs VARCHAR)""")
            # create the FuncDep table if an error is detected

    def addDep(self, dep_object):

        """ Triggered when the addDep command is typed,
        it inserts new values in the FuncDep table and the Dep object is added in the depTab """

        table_name = dep_object.table_name
        lhs = dep_object.lhs
        rhs = dep_object.rhs

        self.depTab.append(dep_object)
        self.command.execute("""INSERT INTO FuncDep VALUES (""" + table_name + """,""" + lhs + """,""" + rhs + """)""")

    def __str__(self):
        print(self.dbName)
