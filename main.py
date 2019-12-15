import cmd

from db import DataBase
from dep import Dep


class Shell(cmd.Cmd):
    """ Displayed shell when the program starts, The user can type different commands described below """

    intro = 'Welcome to the functional dependencies shell.   Type help or ? to list commands.\n'
    prompt = 'Type a command >>> '
    db_object = None
    tabNSD=[]

    def do_exit(self, arg):

        """ The user type 'exit' and leave the application """

        print('Thank you for using this program, Goodbye')
        self.close()
        return True

    def close(self):
        if self.db_object:
            self.db_object.close()
            self.db_object = None

    def do_connect(self, arg):

        """ The user type 'connect [data base file]' to create a DataBase object connected with the file indicated """

        if (arg == ""):
            print("")  # space
            print("please, enter a data base file")
            print("")  # space
            return False
        print("")  # space
        print("connected to " + arg)
        print("")  # space
        newDB = DataBase(arg)
        self.db_object = newDB

    def do_disconnect(self, arg):

        """The user type 'disconnect' to remove the data base file connected"""
        tabNSD=None
        if (self.db_object == None):
            print("")  # space
            print("Error, no data base file connected")
            print("")  # space
        else:
            print("")  # space
            print("Disconnected to " + self.db_object.db_name)
            print("")  # space
            self.db_object = None

    def do_addDep(self, arg):  # first argument is table name, second is lhs and third is rhs

        """ The user type 'addDep [table_name] [lhs] [rhs]' to create a new functional dependency.
         It creates a new Dep object with the arguments indicated,
         the Dep object is added to the depTab list in the current DataBase object"""

        arg_tab=sep(arg)  # transform the argument string with this pattern list : [table_name [lhs, lhs2,...] rhs]

        if (self.db_object == None):
            print("")  # space
            print("Error, you must connect a data base file")
            print("")  # space
        if (len(arg_tab[1]) < 2):
            print("")  # space
            print("Error, you must type 3 arguments (table_name, lhs, rhs)")
            print("")  # space
        else:
            new_dep_object = Dep(self.db_object.db_name, arg_tab[0], arg_tab[1], arg_tab[2])
            self.db_object.addDep(new_dep_object)

    def do_removeDep(self, arg):  # first argument is table name, second is lhs and third is rhs

        """ The user type 'removeDep [table_name] [lhs] [rhs]' to remove the functional dependency indicated,
         the Dep object is removed from the depTab list in the current DataBase object"""

        arg_tab=sep(arg)
        if (self.db_object == None):
            print("")  # space
            print("Error, you must connect a data base file")
            print("")  # space
        if (len(arg_tab) < 3):
            print("")  # space
            print("Error, you must type 3 arguments (table_name, lhs, rhs)")
            print("")  # space
        else:
            compare_dep = Dep(self.db_object, arg_tab[0], arg_tab[1], arg_tab[2])
            self.db_object.removeDep(compare_dep)

    def do_removeAllDep(self, arg):
        if (self.db_object == None):
            print("")  # space
            print("Error, you must connect a data base file")
            print("")  # space
        for i in self.db_object.depTab:
            self.db_object.removeDep(i)

    def do_showDep(self, arg):

        """Show the current functional dependency in the data base file"""

        if (self.db_object == None):
            print("Error, you must connect a data base file")
        else:
            print("")  # space
            l = self.db_object.depTab
            if (l == []):
                print("There is no functional dependencies yet, "
                      "you can add them with the command 'addDep [table_name] [lhs] [rhs]'")
            for i in l:
                print(i.table_name + ": " + i.lhs_rep + " --> " + i.rhs)
            print("")  # space

    def do_showNSD(self, arg):  # NSD = Not Satisfied Dependencies

        """ Compute and show the not satisfied functional dependencies """
        list = self.db_object.depTab
        tabD=[]
        tabG=[]
        #On considere qu'on ne selectionne que un attribut à gauche !!!
        for i in list:
            i.__str__()
            attribute1=str(self.db_object.depTab.lhs) #le nom de l'attribut à gauche de la fléche 
            attribute2=str(self.db_object.depTab.rhs) #le nom de l'attribut à droite de la flèche 
            name=str(self.db_object.db_name)
            self.db_object.command.execute("""SELECT """+attribute1 +""" FROM  """ +name) #on considere qu'il n'y a que un attribut pour le moment
            tabD=self.db_object.command.fetchall() #affiche les resultas sous forme de tableaux 
            self.db_object.command.execute("""SELECT """+attribute1 +""" FROM  """ +name)
            tabG=self.db_object.command.fetchall() 
            # Cette boucle va nous permettre de comparer les valeurs pour voir si les df sont respecte  
            l=0
            while (l<len(tabG)):
                if (tabG[l]!=tabD[l]):
                    tabNSD.append(i)
                    l=len(tabG) #pour sortir de cette boucle et passer à la DF suivante 
                l=l+1   
       self.showNSD()         
                
    def showNSD(self,arg):
        print("It's the not satisfied functional dependencies")
        for m in tabNSD:
            print(m)     

    def do_showLCD(self, arg):  # LCD = Logical Consequence Dependencies

        """ Compute and show the functional dependencies that are a logical consequence """

    def do_deleteUID(self, arg):  # UID = Unnecessary or Inconsistent Dependencies

        """ Compute and show functional dependencies that are unnecessary or inconsistent,
        the user can delete them if he wishes """

    def do_checkBCNF(self, arg):

        """ Check if the data base file in in BCNF """

    def do_check3NF(self, arg):

        """ Check if the data base file in in 3NF """

    def do_showKey(self, arg):

        """ Compute and show the key(s) of the functional dependencies """

    def do_showSuperKey(self, arg):

        """ Compute and show the super-key(s) of the functional dependencies """


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

if __name__ == '__main__':
    Shell().cmdloop()
