import cmd, sys

class Shell(cmd.Cmd):
    intro = 'Welcome to the data base I project shell.   Type help or ? to list commands.\n'
    prompt = 'Type a command >>> '
    file = None
    
    def do_bye(self, arg):
        ' BYE '
        print('Thank you for using this project, Goodbye')
        self.close()
        bye()
        return True

    # ----- record and playback -----
    
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
    Shell().cmdloop()





