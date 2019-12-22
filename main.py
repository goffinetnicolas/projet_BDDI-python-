import cmd

from db import DataBase
from dep import Dep


class Shell(cmd.Cmd):
    """ Displayed shell when the program starts, The user can type different commands described below """

    intro = 'Welcome to the functional dependencies shell.   Type help or ? to list commands.\n'
    prompt = 'Type a command >>> '
    db_object = None
    #tabNSD=[] #table ou il y a les df qui ne sont pas satisafite 
    #dejafaitNSD=0 #pour savoir si on a déja fait une methode 
    #Il faudrait que tabNSD soit propre a chauqe table ou que les tables n'aient pas les mêmes attributs sino il y a un risque d'erreurs 

    def do_exit(self, arg):

        """ The user type 'exit' and leave the application """

        print("")  # space
        print('Thank you for using this program, Goodbye')
        self.close()
        return True
        print("")  # space

    def close(self):
        if self.db_object:
            self.db_object.close()
            self.db_object = None

    def do_connect(self, arg):

        """ The user type 'connect data_base.db' to create a DataBase object connected with the file indicated """

        print("")  # space
        if (arg == ""):
            print("please, enter a data base file")
            return False
        print("connected to " + arg)
        newDB = DataBase(arg)
        self.db_object = newDB
        print("")  # space

    def do_disconnect(self, arg):

        """The user type 'disconnect' to remove the data base file connected"""

        print("")  # space
        if (self.db_object == None):
            print("Error, no data base file connected")
        else:
            print("Disconnected to " + self.db_object.db_name)
            self.db_object = None
        print("")  # space

    def do_addDep(self, arg):  # first argument is table name, second is lhs and third is rhs

        """ The user type 'addDep table_name lhs rhs' or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs'
         to create a new functional dependency.
         It creates a new Dep object with the arguments indicated,
         the Dep object is added to the depTab list in the current DataBase object"""

        print("")  # space
        if(arg==""):
            print("Error, you must type 'addDep table_name lhs rhs' "
                  "or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs' ")
            return 0
        arg_tab=sep(arg)  # transform the argument string with this pattern list : [table_name [lhs, lhs2,...] rhs]

        if (self.db_object == None):
            print("Error, you must connect a data base file")
            return 0

        if (len(arg_tab) < 3):
            print("Error, you must type 'addDep table_name lhs rhs' or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs'")
            return 0

        if(isinstance(arg_tab[1], list)):
            if(verify_recurrent_lhs(arg_tab[1])):
                print("Error, you have types 2 identical attributes in lhs")
                return 0

        new_dep_object = Dep(self.db_object.db_name, arg_tab[0], arg_tab[1], arg_tab[2])
        self.db_object.addDep(new_dep_object)
        print("")  # space

    def do_removeDep(self, arg):  # first argument is table name, second is lhs and third is rhs

        """ The user type 'removeDep table_name lhs rhs' or 'removeDep table_name {lhs1, lhs2, lhs3, ...} rhs'
         to remove the functional dependency indicated,
         the Dep object is removed from the depTab list in the current DataBase object"""

        print("")  # space
        arg_tab=sep(arg)
        if (self.db_object == None):
            print("Error, you must connect a data base file")
        if (len(arg_tab) < 3):
            print("Error, you must type 'addDep table_name lhs rhs' or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs'")
        else:
            compare_dep = Dep(self.db_object, arg_tab[0], arg_tab[1], arg_tab[2])
            self.db_object.removeDep(compare_dep)
        print("")  # space

    def do_showDep(self, arg):

        """Show the current functional dependency in the data base file"""

        print("")  # space
        if (self.db_object == None):
            print("Error, you must connect a data base file")
        else:
            l = self.db_object.depTab
            if (l == []):
                print("There is no functional dependencies yet, "
                      "you can add them with the command 'addDep table_name lhs rhs' "
                      "or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs'")
            for i in l:
                print(i.table_name + ": " + i.lhs_rep + " --> " + i.rhs)
        print("")  # space

    def do_showNSD(self, arg):  # Maxime's version

        """ Compute and show the not satisfied functional dependencies
        The user type 'showNSD table_name' """

        print("")  # space
        if (self.db_object == None):
            print("Error, you must connect a data base file")

        if(arg==""):
            print("Error, you must enter a table name")

        else:
            self.db_object.showNSD(arg)
        print("")  # space
       

    def do_showNSD2(self, arg): # Nicolas's version

        """ Compute and show the not satisfied functional dependencies
            The user type 'showNSD table_name' """

        print("")  # space
        if (self.db_object == None):
            print("Error, you must connect a data base file")

        if(arg==""):
            print("Error, you must enter a table name")

        else:
            self.db_object.showNSD2(arg)
        print("")  # space

    #recopier le code de mon gsm pour LCD 
    def do_showLCD(self, arg):  # LCD = Logical Consequence Dependencies

        """ Compute and show the functional dependencies that are a logical consequence
        The user type 'showLCD table_name' """

        print("")  # space
        if (self.db_object == None):
            print("Error, you must connect a data base file")

        if(arg==""):
            print("Error, you must enter a table name")

        else:
            self.db_object.showLCD(arg)
        print("")  # space

    def do_showCOAS2(self, arg):
        print("")  # space

        if (self.db_object == None):
            print("Error, you must connect a data base file")
            return 0

        arg_tab=sep(arg)
        if(len(arg_tab) < 2):
            #print("Error, you must enter a table name and an attribute name")
            return 0

        else:
            COAS=self.db_object.showCOAS2(arg_tab[0], arg_tab[1])
            if(len(COAS) == 0):
                print("No functional dependencies found")
            else:
                print("Closure of the attribute set: ")
                for att in COAS:
                    print(att)

    def do_showCOAS(self,arg): # CSOA = Closure Of an Attribute Set

        """ Compute and show the closure of the attribute of the table indicated  
        The user type 'showCOAS table_name attribute_name' """

        print("")  # space
        if (self.db_object == None):
            print("Error, you must connect a data base file")
            return 0

        print(arg)
        if(arg==""):
            print("Error, you must enter a table name and an attribute")
        arg_tab=sep(arg)  # transform the argument string with this pattern list : [table_name [lhs, lhs2,...] rhs]
        if (len(arg_tab)<2):
            print("Error you must enter a table name and an attribute")
        else:
            self.db_object.showCOAS(arg_tab[0],arg_tab[1])
        print("")  # space
        
        
    #a faire pui simplifier le code
    def do_deleteUID(self, arg):  # UID = Unnecessary or Inconsistent Dependencies

        """ Compute and show functional dependencies that are unnecessary or inconsistent,
        the user can delete them if he wishes 
        The user type 'deleteUID table_name' """

        print("")  # space
        if (self.db_object == None):
            print("Error, you must connect a data base file")

        if(arg==""):
            print("Error, you must enter a table name and an attribute")

        else:
            self.db_object.deleteUID(arg)
        print("")  # space


    def do_checkBCNF(self, arg):

        """ Check if the data base file in in BCNF,
        user has to type the command 'checkBCNF table_name' """

        print("")  # space
        table=arg
        if(table==""):
            print("Error, you have to type a table as argument")
            return 0
        if(self.db_object.checkBCNF(table) == True):
            print(table," is in BCNF")
        else:

            print(table," is not in BCNF")
        print("")  # space

    def do_check3NF(self, arg):
        """ Check if the data base file in in 3NF """

        table = arg
        if (table == ""):
            print("Error, you have to type a table as argument")
            return 0
        else:
            if (self.db_object.check3NF(table) == True):
                print(table + " is in 3NF")
            else:
                if (len(self.db_object.showNSD2(table)) == 0):
                    print(table + " is not in 3NF but satisfies the current functional dependencies")
                    print("Do you want to create a new data base with 3NF decompositions ? (y/n)")
                    user_res = input()
                    if (user_res == "y"):
                        print("Please, enter the data base file name that you want to create")
                        user_db_name = input()
                        self.db_object.create3NF_dec(table, user_db_name)
                else:
                    print(table + " is not in 3NF and does not satisfy the current functional dependencies")

    def do_showKey(self, arg):

        """ Compute and show the key(s) of the functional dependencies """

        print("")  # space
        table=arg
        if(table==""):
            print("Error, you have to type a table as argument")
            return 0
        else:
            key_list = self.db_object.showKey(table)
            if(key_list == []):
                print("No key found")
            else:
                print("key list:")
                for key in key_list:
                    print(key)
        print("")  # space

    def do_showSuperKey(self, arg):

        """ Compute and show the super-key(s) of the functional dependencies """

        print("")  # space
        table = arg
        if (table == ""):
            print("Error, you have to type a table as argument")
            return 0
        else:
            key_list = self.db_object.showKey(table)
            super_key_list = self.db_object.showSuperKey(key_list)
            if (super_key_list == []):
                print("No super key found")
            else:
                print("super-key list:")
                for key in super_key_list:
                    print(key)
        print("")  # space

    def do_removeTableDep(self, arg):
        print("")  # space
        table = arg
        if (table == ""):
            print("Error, you have to type a table as argument")
            return 0
        else:
            removed=[]
            for dep in self.db_object.depTab:
                if(dep.table_name == table):
                    removed.append(dep)

            for dep in removed:
                self.db_object.removeDep(dep)
        print("")  # space

    def do_removeAllDep(self, arg):
        print("")  # space
        remove=[]
        for dep in self.db_object.depTab:
            remove.append(dep)
        for dep in remove:
            self.db_object.depTab.remove(dep)
        print("")  # space

def sep(arg):
    res = []
    lhs=[]
    a=""
    b=""
    c=0
    lhs_mode=False
    for i in arg:
        c=c+1
        if (i == ' ' and lhs_mode==False and a != ""):
            res.append(a)
            a=""

        if(i == '{'):
            lhs_mode=True

        if(i== '}'):
            lhs.append(b)
            lhs_mode=False
            if (len(lhs) == 1):
                res.append(lhs[0])
            else:
                res.append(lhs)

        if(lhs_mode==True):
            if(i==','):
                lhs.append(b)
                b=""
            if(i==' ' or i=='{'):
                pass
            else:
                if(i != ','):
                    b=b+i
        else:
            if(i != '}' and i != ' '):
                a=a+i
            if(c==len(arg)):
                res.append(a)
                a = ""

    return res

def verify_recurrent_lhs(tab):
    # return True if something in the list is recurrent
    comp = [tab[0]]
    a=1
    while(a != len(tab)):
        if(tab[a] in comp):
            return True
        comp.append(tab[a])
        a=a+1
    return False



if __name__ == '__main__':
    Shell().cmdloop()
