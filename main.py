import cmd, sys

from db import DataBase
from dep import Dep

class Shell(cmd.Cmd):
    intro = 'Welcome to the data base I project shell.   Type help or ? to list commands.\n'
    prompt = 'Type a command >>> '
    dbObject = None

    def do_bye(self, arg):
        print('Thank you for using this project, Goodbye')
        self.close()
        return True

    def do_load(self, arg):
        print(arg, " has been successfully loaded")
        newDB = DataBase(arg)
        self.dbObject = newDB

    def do_remove(self, arg):
        if (self.dbObject == None):
            print("Error, no data base file loaded")
        else:
            text = " has been successfully removed"
            print(self.dbObject.db + text)
            db = None

    def do_addDep(self, arg): # first argument is table name, second is lhs and third is rhs
        argTab=arg.split()
        if (self.dbObject == None):
            print("Error, No loaded data base")
        else:
            newDep = Dep(self.dbObject.dbName, argTab[0], argTab[1], argTab[2])
            self.dbObject.addDep(newDep)
            newDep.__str__()

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == '__main__':
    Shell().cmdloop()
