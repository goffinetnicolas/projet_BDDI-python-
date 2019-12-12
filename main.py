import cmd, sys

from db import DataBase
from dep import Dep


class Shell(cmd.Cmd):
    intro = 'Welcome to the data base I project shell.   Type help or ? to list commands.\n'
    prompt = 'Type a command >>> '
    db = None
    
    def do_bye(self, arg):  
        print('Thank you for using this project, Goodbye')
        self.close()
        return True

    def do_load(self,arg):
        print(arg," has been successfully loaded")
        newDB=DataBase(arg)
        self.db=newDB

    def do_remove(self, arg):
        if(self.db==None):
            print("Error, no data base file loaded")
        else:
            print(self.db," has been successfully removed")
            db=None

    def do_addDep(self,table_name, lhs, rhs):
        if(self.db==None):
            print("Error, No loaded data base")
        else:
            dep=Dep(self.db,table_name,lhs,rhs)

    
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

if __name__ == '__main__':
    Shell().cmdloop()





