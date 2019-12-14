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
                s = i[1] # s = "att1 att2 att3"
                s.split()
                new_dep_object = Dep(self.db_name, i[0], s, i[2])
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

        table_name_arg = dep_object.table_name
        lhs_arg = dep_object.lhs
        rhs_arg = dep_object.rhs

        if(isinstance(lhs_arg, list)):
            try:
                for i in self.depTab:
                    if(dep_object.__eq__(i)):
                        print("Error, the functional dependency already exists")
                        return 0 # we don't want to execute the rest of the function

                lhs_string = ""
                for i in lhs_arg:
                    self.command.execute("SELECT "+i+", "+rhs_arg+" FROM "+table_name_arg)
                    # make an error if the attributes or the table is not in the data base
                    # N.B : I have tried to do this with dictionary
                    # and variables filling during 2 hours but it didn't work
                    lhs_string = lhs_arg + i + " "
                lhs_string = lhs_arg[:len(lhs_string)-1] # we don't want the last space

                self.command.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)",
                                    (table_name_arg, lhs_string, rhs_arg))
                self.connection.commit()
                self.depTab.append(dep_object)
                print("New functional dependency added:")
                dep_object.__str__()

            except Exception as e:
                print(e)
                print("Error, the attribute(s) or the table indicated do not exist")

        else:
            try:
                for i in self.depTab:
                    if(dep_object.__eq__(i)):
                        print("Error, the functional dependency already exists")
                        return 0 # we don't want to execute the rest of the function

                self.command.execute("SELECT "+lhs_arg+", "+rhs_arg+" FROM "+table_name_arg)
                # make an error if the attributes or the table is not in the data base

                self.command.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)",
                                    (table_name_arg, lhs_arg, rhs_arg))
                self.connection.commit()
                self.depTab.append(dep_object)
                print("New functional dependency added:")
                dep_object.__str__()


            except Exception as e:
                print(e)
                print("Error, the attribute(s) or the table indicated do not exist")

    def removeDep(self, dep_object):

        """ Triggered when the addDep command is typed,
        it removes the functional dependency in the FuncDep table and the Dep object is removed in the depTab"""

        table_name_arg = dep_object.table_name
        lhs_arg = dep_object.lhs
        rhs_arg = dep_object.rhs

        if(isinstance(lhs_arg, list)):
            lhs_string = ""
            for i in lhs_arg:
                lhs_string =  i + " "
            lhs_string = lhs_arg[:len(lhs_string) - 1]

            current_dep_tab = self.depTab
            if (dep_object not in current_dep_tab):
                print("Error, The arguments indicated are not in the functional dependencies")
            else:
                for i in current_dep_tab:
                    if (i.__eq__(dep_object)):
                        self.depTab.remove(i)

                self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                     {'table_name': table_name_arg, 'lhs': lhs_string, 'rhs': rhs_arg})
                self.connection.commit()

                print("[" + table_name_arg + ": " + lhs_string + " --> " + rhs_arg
                    + "] has been successfully removed from the functional dependencies")
        else:
            current_dep_tab = self.depTab
            if (dep_object not in current_dep_tab):
                print("Error, The arguments indicated are not in the functional dependencies")
            else:
                for i in current_dep_tab:
                    if (i.__eq__(dep_object)):
                        self.depTab.remove(i)

                self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                     {'table_name': table_name_arg, 'lhs': lhs_arg, 'rhs': rhs_arg})
                self.connection.commit()

                print("[" + table_name_arg + ": " + lhs_arg + " --> " + rhs_arg
                      + "] has been successfully removed from the functional dependencies")

    def close(self):
        pass

    def __str__(self):
        print(self.db_name)
