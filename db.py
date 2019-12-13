import sqlite3

from dep import Dep


class DataBase:
    def __init__(self, db_name):

        """ Represent a data base """

        self.db_name = db_name
        self.depTab = []  # list of Dep object

        self.connection = sqlite3.connect('putDataBaseHere/' + db_name)
        self.command = self.connection.cursor()


        try:
            self.command.execute("""SELECT * FROM FuncDep""")
            # check if the FuncDep table is created
            selected = self.command.fetchall()
            for i in selected:
                new_dep_object = Dep(self.db_name, i[0], i[1], i[2])
                self.depTab.append(new_dep_object)
                # adding functional dependency already created in the table FuncDep

        except:
            self.command.execute(
                """CREATE TABLE FuncDep (table_name VARCHAR, lhs VARCHAR, rhs VARCHAR)""")
            # create the FuncDep table if an error is detected
            self.connection.commit()

    def addDep(self, dep_object):

        """ Triggered when the addDep command is typed,
        it inserts the functional dependency in the FuncDep table and the Dep object is added in the depTab """

        table_name = dep_object.table_name
        lhs = dep_object.lhs
        rhs = dep_object.rhs

        self.depTab.append(dep_object)
        self.command.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)", (table_name, lhs, rhs))
        self.connection.commit()

    def removeDep(self,dep_object):

        """ Triggered when the addDep command is typed,
        it removes the functional dependency in the FuncDep table and the Dep object is removed in the depTab"""

        current_dep_tab = self.depTab
        if(dep_object not in current_dep_tab):
            print("Error, The arguments indicated are not in the functional dependencies")
        else:
            for i in current_dep_tab:
                if(i.__eq__(dep_object)):
                    self.depTab.remove(i)

            self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                 {'table_name':dep_object.table_name, 'lhs':dep_object.lhs, 'rhs':dep_object.rhs})
            self.connection.commit()
            print("["+dep_object.table_name+": "+dep_object.lhs+" --> "+ dep_object.rhs
                     +"] has been successfully removed from the functional dependencies")

    def close(self):
        pass

    def __str__(self):
        print(self.db_name)
