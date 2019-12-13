import cmd, sys

from db import DataBase
from dep import Dep


class Shell(cmd.Cmd):

    """ Displayed shell when the program starts, The user can type different commands described below """

    intro = 'Welcome to the data base I project shell.   Type help or ? to list commands.\n'
    prompt = 'Type a command >>> '
    db_object = None

    def do_bye(self, arg):

        """ The user type 'bye' and leave the application """

        print('Thank you for using this project, Goodbye')
        self.close()
        return True

    def do_connect(self, arg):

        """ The user type 'connect [data base file]' to create a DataBase object connected with the file indicated """

        print(arg, " has been successfully loaded")
        newDB = DataBase(arg)
        self.db_object = newDB

    def do_remove(self, arg):

        """The user type 'remove' to remove the data base file connected"""

        if (self.db_object == None):
            print("Error, no data base file loaded")
        else:
            text = " has been successfully removed"
            print(self.db_object.db + text)
            db = None

    def do_addDep(self, arg):  # first argument is table name, second is lhs and third is rhs

        """ The user type 'addDep [table_name] [lhs] [rhs]' to create a new functional dependency.
         It creates a new Dep object with the arguments indicated,
         the Dep object is added to the depTab list in the current DataBase object"""

        argTab = arg.split()
        if (self.db_object == None):
            print("Error, No loaded data base")
        else:
            new_dep = Dep(self.db_object.dbName, argTab[0], argTab[1], argTab[2])
            self.db_object.addDep(new_dep)
            new_dep.__str__()

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == '__main__':
    Shell().cmdloop()
