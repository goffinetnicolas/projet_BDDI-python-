import copy
import itertools
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
                print(dep_object.__str__())

            except:
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
                print(dep_object.__str__())

            except Exception as e:
                print(e)
                print("Error, the attribute(s) or the table indicated do not exist")
    


    def removeDep(self, dep_object):

        """ Triggered when the addDep command is typed,
        it removes the functional dependency in the FuncDep table and the Dep object is removed in the depTab"""

        table_name_arg = dep_object.table_name
        lhs_arg = dep_object.lhs  # could be a string or a list
        rhs_arg = dep_object.rhs  # always a string
        current_dep_tab = self.depTab

        if(isinstance(lhs_arg, list)):
            lhs_string = extract(lhs_arg)

            if (not_member_of(dep_object, current_dep_tab)):
                print("Error, The arguments indicated are not in the functional dependencies")

            else:
                for i in current_dep_tab:
                    if (i.__eq__(dep_object)):
                        self.depTab.remove(dep_object)

                self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                     {'table_name': table_name_arg, 'lhs': lhs_string, 'rhs': rhs_arg})
                self.connection.commit()


                print("[" + table_name_arg + ": {" + lhs_string + "} --> " + rhs_arg
                    + "] has been successfully removed from the functional dependencies")

        else:
            if (not_member_of(dep_object, current_dep_tab)):
                print("Error, The arguments indicated are not in the functional dependencies")

            else:
                for i in current_dep_tab:
                    if (i.__eq__(dep_object)):
                        self.depTab.remove(dep_object)

                self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                     {'table_name': table_name_arg, 'lhs': lhs_arg, 'rhs': rhs_arg})
                self.connection.commit()

                print("[" + table_name_arg + ": " + lhs_arg + " --> " + rhs_arg
                      + "] has been successfully removed from the functional dependencies")

    def showNSD2(self, table):
        not_satisfied = []
        table_dep_list = self.extract_dep(table)  # total list of dependencies of the indicated table

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
                        if (line1[lhs_pos] == line2[lhs_pos] and line1 != line2):
                            if ((line1[rhs_pos] != line2[rhs_pos])
                                    and (not_member_of(dep, not_satisfied)
                                    and line1 != line2)):
                                not_satisfied.append(dep)

        return not_satisfied

    def find_attribute_position(self, lhs, table):

        self.command.execute("""SELECT """ + lhs + """ FROM """ + table) # ("title of a music")
        tup_result = self.command.fetchone()

        self.command.execute("""SELECT * FROM """ + table)
        tup_list_result = self.command.fetchall()

        for tup in tup_list_result:
            a=0
            for string in tup:
                if(string == tup_result[0]):
                    return a
                else:
                    a=a+1


    def checkBCNF(self, table):

        """ Triggered with the command 'checkBCNF',
         this algorithm check if all the functional dependencies can gives t
         he entire attribute list of the indicated table """

        table_dep_list = self.extract_dep(table)  # the dep list of the indicated table

        if (len(table_dep_list) == 0):
            print("There is not functional dependencies linked to the indicated table")
            return False

        att_list = self.find_table_attribute(table)  # total attribute list of the table

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

            if(not compareList(att_list,att_obtained)):  # compareList returns True if the lists are the same
                return False

            return True

        else:
            for dep1 in table_dep_list:
                att_obtained = []  # attributes that we will obtain thanks to functional dependencies
                att_obtained.append(dep1.rhs)

                if (isinstance(dep1.lhs, list)):
                    for lhs in dep1.lhs:
                        att_obtained.append(lhs)
                else:
                    att_obtained.append(dep1.lhs)

                while (not compareList(att_list,att_obtained)):  # compareList returns True if the lists are the same
                    check_list = copy.deepcopy(att_obtained)

                    for dep2 in table_dep_list:
                        if (detect(dep2.lhs, att_obtained) and dep2.rhs not in att_obtained):
                            # detect() returns true if the first argument is in the second
                            att_obtained.append(dep2.rhs)

                    if (compareList(check_list, att_obtained)):  # compareList returns True if the lists are the same
                        return False

            return True

    def checkWrongDepBCNF(self, table):
        att_list = self.find_table_attribute(table)  # total attribute list of the table
        table_dep_list = self.extract_dep(table)
        wrong_dep = []

        for dep in table_dep_list:
            tab = []
            tab.append(table)
            if(isinstance(dep.lhs, list)):
                for lhs in dep.lhs:
                    tab.append(lhs)
            else:
                tab.append(dep.lhs)
            COAS=self.showCOAS2(tab)
            if(compareList(COAS, att_list) == False):
                wrong_dep.append(dep)

        return wrong_dep

    def showKey(self, table):
        table_dep_list = self.extract_dep(table)
        att_list = self.find_table_attribute(table)  # total attribute list of the table

        if (len(table_dep_list) == 0):
            print("There is not functional dependencies linked to the indicated table")
            return []

        key_list = []

        for L in range(0, len(att_list) + 1):  # test all possible attribute combinations
            for potential_key in itertools.combinations(att_list, L):
                if(self.check_all_attributes_obtained(table_dep_list, att_list, list(potential_key))):
                    #  this function check if with the current attribute combination,
                    #  we can reach all attributes of the table
                    key_list.append(list(potential_key))

        return key_list


    def check_all_attributes_obtained(self, dep_list, total_attribute_list, potential_key):
        #  this function check if with the current attribute combination,
        #  we can reach all attributes of the table
        while(not compareList(potential_key,total_attribute_list)):
            compare_key = copy.deepcopy(potential_key)
            for dep in dep_list:
                if(detect(dep.lhs,potential_key) and dep.rhs not in potential_key):
                    potential_key.append(dep.rhs)
            if(compare_key == potential_key):
                return False
        return True

    def check_all_attributes_obtained(self, dep_list, total_attribute_list, potential_key):
        l=[]
        l.append(dep_list[0].table_name)
        for att in potential_key:
            l.append(att)
        COAS=self.showCOAS2(l)
        if(compareList(COAS, total_attribute_list)):
            return True
        return False

    def find_table_attribute(self, table):
        try:
            self.command.execute("""SELECT * from """+table)
            att_list = [description[0] for description in self.command.description]
            return att_list

        except:
            print(table+" does not exist in the database")


    def showSuperKey(self, key_list):
        not_super_key=[]
        for key1 in key_list:
            for key2 in key_list:
                if(not compareList(key1,key2)):
                    cnt=0
                    for att in key1:
                        if(att in key2):
                            cnt=cnt+1
                    if(cnt == len(key1) and key2 not in not_super_key):
                        not_super_key.append(key2)

        for key in not_super_key:
            key_list.remove(key)

        return key_list

    def check3NF(self, table):
        table_dep_list=self.extract_dep(table)
        total_key=self.showKey(table)
        sup_key=self.showSuperKey(total_key)
        if(self.checkBCNF(table) == True):
            return True
        else:
            print(sup_key)
            for dep in table_dep_list:
                cnt=0
                for key in sup_key:
                    if(dep.rhs not in key):
                        cnt=cnt+1
                if(cnt==len(sup_key)):
                    return False
            return True



    def showLCD2(self, table):
        table_dep_list = self.extract_dep(table)
        LCD=[]
        for dep in table_dep_list:
            tab=[]
            tab.append(table)
            if(isinstance(dep.lhs,list)):
                for lhs in dep.lhs:
                    tab.append(lhs)
                COAS = self.showCOAS2(tab)
                for att in COAS:
                    if(att != dep.rhs and att not in dep.lhs):
                        newDep = Dep(self.db_name, table, dep.lhs, att)
                        if (not_member_of(newDep, table_dep_list) and not_member_of(newDep, LCD)):
                            cnt=0
                            for lhs in dep.lhs:
                                comp=Dep(self.db_name, table, lhs, att)
                                if(not_member_of(comp, table_dep_list)):
                                    cnt=cnt+1
                            print(cnt, len(dep.lhs))
                            if(cnt == len(dep.lhs)):
                                LCD.append(newDep)
            else:
                tab.append(dep.lhs)
                COAS = self.showCOAS2(tab)
                for att in COAS:
                    if (att != dep.rhs and att != dep.lhs):
                        newDep = Dep(self.db_name, table, dep.lhs, att)
                        if(not_member_of(newDep, table_dep_list) and not_member_of(newDep,LCD)):
                            LCD.append(newDep)
        return LCD


    def showCOAS2(self, arg_tab):
        # arg_tab is a list with minimum 2 objects,
        # the first one is the table and rest of the list are the attributes set
        table=arg_tab[0]
        lhs_tab=arg_tab[1:]
        table_dep_list=self.extract_dep(table)
        att_obtained=copy.deepcopy(lhs_tab)
        att_comp=[]

        while(att_obtained != att_comp):
            att_comp=copy.deepcopy(att_obtained)
            for dep in table_dep_list:
                if(detect(dep.lhs, att_obtained) and dep.rhs not in att_obtained):
                    att_obtained.append(dep.rhs)

        return att_obtained


    def check_redundant_dep(self, table):
        table_dep_list = self.extract_dep(table)
        redundant=[]
        for dep1 in table_dep_list:
            rmv=copy.deepcopy(table_dep_list)
            rmv.remove(dep1)
            T=list(dep1.lhs)
            for dep2 in rmv:
                if(detect(dep2.lhs, T)):
                    T.append(dep2.rhs)
                if(detect(dep1.rhs, T)):
                    redundant.append(dep1)
        return redundant

    def extract_dep(self, table):
        l = self.depTab
        table_dep_list = []
        for dep in l:  # extract the functional dependencies linked to the table
            if (dep.table_name == table):
                table_dep_list.append(dep)

        return table_dep_list

    def create3NF_dec(self, table, db_name):

        new_db = DataBase(db_name + ".db")
        redundant = self.check_redundant_dep(table)
        for dep in redundant:
            self.removeDep(dep)
        table_dep_list = self.extract_dep(table)
        a=0
        for dep in table_dep_list:
            b = str(a)
            l=[]
            if(isinstance(dep.lhs, list)):
                for lhs in dep.lhs:
                    l.append(lhs)
            else:
                l.append(dep.lhs)
            l.append(dep.rhs)
            print(l)

            new_db.command.execute("""CREATE TABLE dep"""+b+""" ("""+l[0]+""")""")
            d=1
            while(d != len(l)):
                new_db.command.execute("""ALTER TABLE dep"""+b+""" ADD """+l[d]+""" VARCHAR""")
                d=d+1
            a=a+1
            new_db.connection.commit()

        for dep in table_dep_list:
            new_db.depTab.append(dep)
            if(isinstance(dep.lhs, list)):
                lhs_string=extract(dep.lhs)
                new_db.command.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)",
                                    (dep.table_name, lhs_string, dep.rhs))
                new_db.connection.commit()
            else:
                new_db.command.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)",
                                       (dep.table_name, dep.lhs, dep.rhs))
                new_db.connection.commit()


    def close(self):
        pass

    def __str__(self):
        return self.db_name

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

def not_member_of(depObject, depList):  # returns True if the dep is not in the dep list
    for i in depList:
        if(depObject.__eq__(i)):
            return False
    return True

def detect(string_or_list_lhs, string_list):  # returns True if the lhs is in the string list
    low_string_list=[]
    for u in string_list:
        low_string_list.append(u.lower())
    if(isinstance(string_or_list_lhs, list)):
        lhs_list=[]
        for s in string_or_list_lhs:
            lhs_list.append(s.lower())
        for lhs in lhs_list:
            if(lhs not in low_string_list):
                return False
        return True
    else:
        lhs_string=string_or_list_lhs.lower()
        if (lhs_string in low_string_list):
            return True
        else:
            return False

def compareList(list1, list2):  # returns True is the list are the same
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






