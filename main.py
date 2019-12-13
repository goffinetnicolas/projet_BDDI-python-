import cmd, sys

from db import DataBase
from dep import Dep


class Shell(cmd.Cmd):
    """ Displayed shell when the program starts, The user can type different commands described below """

    intro = 'Welcome to the data base I project shell.   Type help or ? to list commands.\n'
    prompt = 'Type a command >>> '
    db_object = None

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
            print("please, enter a data base file")
            return False
        print("connected to " + arg)
        newDB = DataBase(arg)
        self.db_object = newDB

    def do_disconnect(self, arg):

        """The user type 'disconnect' to remove the data base file connected"""

        if (self.db_object == None):
            print("Error, no data base file connected")
        else:
            print("Disconnected to " + self.db_object.db_name)
            self.db_object = None

    def do_addDep(self, arg):  # first argument is table name, second is lhs and third is rhs

        """ The user type 'addDep [table_name] [lhs] [rhs]' to create a new functional dependency.
         It creates a new Dep object with the arguments indicated,
         the Dep object is added to the depTab list in the current DataBase object"""

        argTab = arg.split()
        if (self.db_object == None):
            print("Error, you must connect a data base file")
        else:
            new_dep_object = Dep(self.db_object.db_name, argTab[0], argTab[1], argTab[2])
            self.db_object.addDep(new_dep_object)
            print("New functional dependency added")
            new_dep_object.__str__()

    def do_removeDep(self, arg):

        """ Remove the functional dependency indicated from the data base file"""

        arg_tab = arg.split()
        if (self.db_object == None):
            print("Error, you must connect a data base file")
        if (arg_tab == []):
            print("Error, you must type 3 arguments (table_name, lhs, rhs)")
        else:
            table_name_arg = arg_tab[0]
            lhs_arg = arg_tab[1]
            rhs_arg = arg_tab[2]

            compare_dep = Dep(self.db_object, table_name_arg, lhs_arg, rhs_arg)
            self.db_object.removeDep(compare_dep)

    def do_showDep(self, arg):

        """Show the current functional dependency in the data base file"""

        list = self.db_object.depTab
        if (list == []):
            print("There is no functional dependencies yet")
        for i in list:
            i.__str__()

    def do_showNSD(self, arg):  # NSD = Not Satisfied Dependencies

        """ Compute and show the not satisfied functional dependencies """

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



if __name__ == '__main__':
    Shell().cmdloop()
