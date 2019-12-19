import copy
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
                s = i[1] # s may be "att1 att2 att3" or "att"
                ins = insert(s)
                new_dep_object = Dep(self.db_name, i[0], ins, i[2])
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
        lhs_arg = dep_object.lhs  # could be a string or a list
        rhs_arg = dep_object.rhs # always a string

        if(isinstance(lhs_arg, list)):
            lhs_arg_tab=lhs_arg
            try:
                for i in self.depTab:
                    if(dep_object.__eq__(i)):
                        print("Error, the functional dependency already exists")
                        print("")  # space
                        return 0  # we don't want to execute the rest of the function


                for i in lhs_arg_tab:
                    self.command.execute("SELECT "+i+", "+rhs_arg+" FROM "+table_name_arg)
                    # make an error if the attributes or the table is not in the data base

                lhs_string = extract(lhs_arg_tab)

                self.command.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)",
                                    (table_name_arg, lhs_string, rhs_arg))
                self.connection.commit()
                self.depTab.append(dep_object)
                print("New functional dependency added:")
                dep_object.__str__()

            except:
                print("Error, the attribute(s) or the table indicated do not exist")
                print("")  # space


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
                print("")
                print("New functional dependency added:")
                dep_object.__str__()


            except Exception as e:
                print(e)
                print("Error, the attribute(s) or the table indicated do not exist")
                print("")  # space


    def removeDep(self, dep_object):

        """ Triggered when the addDep command is typed,
        it removes the functional dependency in the FuncDep table and the Dep object is removed in the depTab"""

        table_name_arg = dep_object.table_name
        lhs_arg = dep_object.lhs  # could be a string or a list
        rhs_arg = dep_object.rhs  # always a string
        print("removeDep executed")

        if(isinstance(lhs_arg, list)):
            lhs_string = extract(lhs_arg)
            current_dep_tab = self.depTab

            if (not_member_of(dep_object, current_dep_tab)):

                print("Error, The arguments indicated are not in the functional dependencies")
                print("")  # space
            else:
                for i in current_dep_tab:
                    if (i.__eq__(dep_object)):
                        self.depTab.remove(i)

                self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                     {'table_name': table_name_arg, 'lhs': lhs_string, 'rhs': rhs_arg})
                self.connection.commit()


                print("[" + table_name_arg + ": {" + lhs_string + "} --> " + rhs_arg
                    + "] has been successfully removed from the functional dependencies")
                print("")  # space
        else:
            current_dep_tab = self.depTab
            if (not_member_of(dep_object, current_dep_tab)):
                print("")  # space
                print("Error, The arguments indicated are not in the functional dependencies")
                print("")  # space
            else:
                for i in current_dep_tab:
                    if (i.__eq__(dep_object)):
                        self.depTab.remove(i)

                self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                     {'table_name': table_name_arg, 'lhs': lhs_arg, 'rhs': rhs_arg})
                self.connection.commit()
                print("")  # space
                print("[" + table_name_arg + ": " + lhs_arg + " --> " + rhs_arg
                      + "] has been successfully removed from the functional dependencies")

    def showNSD2(self, table):  # Nicolas version
        not_satisfied = []
        dep_list = self.depTab
        table_dep_list = []  # total list of dependencies of the indicated table

        for dep in dep_list:
            if (dep.table_name == table):
                table_dep_list.append(dep)

        for dep in table_dep_list:
            lhs = dep.lhs
            rhs = dep.rhs

            if (isinstance(lhs, list)):
                lhs_list = lhs
                lhs_number = len(lhs_list)
                pos_tab = []

                for lhs in lhs_list:
                    position = self.find_attribute_position(lhs, table)
                    pos_tab.append(position)
                self.command.execute("""SELECT * FROM """ + table)
                result = self.command.fetchall()

                for line1 in result:
                    for line2 in result:
                        cnt = 0  # cnt count if all the lhs are the same
                        for i in range(lhs_number):
                            if (line1[pos_tab[i]] == line2[pos_tab[i]] and line1 != line2):
                                cnt = cnt + 1
                        if (cnt == lhs_number):
                            rhs_pos = self.find_attribute_position(rhs, table)
                            print(line1)
                            print(rhs_pos)
                            if ((line1[rhs_pos] != line2[rhs_pos])
                                    and (not_member_of(dep, not_satisfied))
                                    and line1 != line2):
                                not_satisfied.append(dep)

            else:
                lhs_pos = self.find_attribute_position(lhs, table)
                rhs_pos = self.find_attribute_position(rhs, table)
                self.command.execute("""SELECT * FROM """ + table)
                result = self.command.fetchall()
                for line1 in result:
                    for line2 in result:
                        if (line1[lhs_pos] == line2[lhs_pos]):
                            if ((line1[rhs_pos] != line2[rhs_pos]) and (not_member_of(dep, not_satisfied))):
                                not_satisfied.append(dep)

        if (not_satisfied == []):
            print("All the functional dependencies are satisfied")
            print("")  # space
        else:
            for dep in not_satisfied:
                print("The functional dependency: [" + dep.table_name + ": " + dep.lhs_rep + " ---> " + dep.rhs +
                      "] is not satisfied")

    def find_attribute_position(self, lhs, table):
        self.command.execute("""SELECT """ + lhs + """ FROM """ + table) # ("title of a music")
        result = self.command.fetchone()
        print(result)
        self.command.execute("""SELECT * FROM """ + table)
        result2 = self.command.fetchall()
        print(result2)
        for res in result2:
            if(result in res):
                pass




    def checkBCNF(self, table):
        l = self.depTab
        table_dep_list = []  # = [dep1, dep2, dep3]

        for dep in l:  # extract the functional dependencies linked to the table
            if (dep.table_name == table):
                table_dep_list.append(dep)

        if (len(table_dep_list) == 0):
            print("")  # space
            print("There is not functional dependencies linked to the indicated table")
            print("")  # space
            return 0

        att_list = self.find_table_attribute(table)  # total attribute list of the table
        # att_list = title, artistid, albumid
        if(len(table_dep_list) == 1):

            att_obtained = []  # attributes that we will obtain thanks to functional dependencies
            lhs = table_dep_list[0].lhs
            rhs = table_dep_list[0].rhs

            if (isinstance(lhs, list)):
                for lhs_string in lhs:
                    att_obtained.append(lhs_string)
            else:
                att_obtained.append(lhs)

            att_obtained.append(rhs)

            if(not compareList(att_list,att_obtained)):
                print("")  # space
                print(table + " is not in BCNF :(")
                print("")  # space
                return False
            print("")  # space
            print(table + " is in BCNF :)")
            print("")  # space
            return True
        else:
            for dep1 in table_dep_list:
                att_obtained = []  # attributes that we will obtain thanks to functional dependencies
                # att_obtained = title,artistid,albumid
                att_obtained.append(dep1.rhs)

                if (isinstance(dep1.lhs, list)):
                    for lhs in dep1.lhs:
                        att_obtained.append(lhs)
                else:
                    att_obtained.append(dep1.lhs)

                while (not compareList(att_list,att_obtained)):
                    print("beginning of the loop with att_list=",att_list," and att_obtained=",att_obtained)
                    check_list = copy.deepcopy(att_obtained) # title,artistid
                    print("check_list=",check_list)
                    for dep2 in table_dep_list:
                        if (detect(dep2.lhs, att_obtained) and dep2.rhs not in att_obtained):
                            att_obtained.append(dep2.rhs)
                            print(dep2.rhs+" has been added to att_obtained")
                    print("att_obtained is now =",att_obtained)
                    print("check_list is now =",check_list)
                    if (compareList(check_list, att_obtained)):
                        print("")  # space
                        print(table + " is not in BCNF :(")
                        print("")  # space
                        return False

            print("")  # space
            print(table+" is in BCNF :)")
            print("")  # space
            return True

    def showKey(self, table):
        pass

    def find_table_attribute(self, table):
        self.command.execute("""SELECT * from """+table)
        att_list = [description[0] for description in self.command.description]
        return att_list

    def close(self):
        pass

    def __str__(self):
        print(self.db_name)

def insert(s):
    a=s.split()
    if(len(a)==1):
        return a[0]
    return a

def extract(s):
    res=""
    for i in s:
        res=res+i+" "
    l=len(res)-1
    return res[:l]

def not_member_of(depObject, depList): # not working correctly
    for i in depList:
        if(depObject.__eq__(i)):
            return False
    return True

def detect(string_or_list_lhs, string_list):
    if(isinstance(string_or_list_lhs, list)):
        lhs_list=string_or_list_lhs
        for lhs in lhs_list:
            if(lhs not in string_list):
                return False
        return True
    else:
        lhs_string=string_or_list_lhs
        if(lhs_string in string_list):
            return True
        else:
            return False

def compareList(list1, list2):
    a=[]
    b=[]
    for i in list1:
        a.append(i.lower())
    for i in list2:
        b.append(i.lower())
    for i in a:
        if(i not in b):
            return False
    for i in b:
        if(i not in a):
            return False
    return True

