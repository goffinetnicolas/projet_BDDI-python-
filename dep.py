class Dep:
    def __init__(self, dbname, table_name, lhs, rhs):
        """ Represent a functional dependency """

        self.table_name = table_name
        self.lhs = lhs  # lhs is a list of attribute or a string attribute depending on what the user has typed
        self.lhs_rep = rep(lhs)  # String representation of the lhs part
        self.rhs = rhs
        self.dbname = dbname

    def __eq__(self, other):
        if not isinstance(other, Dep):
            return NotImplemented

        stn = self.table_name.lower()  # all the dependencies name are in lowercase to avoid multiple identical objects
        otn = other.table_name.lower()
        srhs = self.rhs.lower()
        orhs = other.rhs.lower()

        if(isinstance(self.lhs, list) and isinstance(other.lhs, list)): # list of lhs comparing to list of lhs
            sl = self.lhs
            ol = other.lhs
            return stn == otn and compare_list(sl, ol) and srhs == orhs
        if(isinstance(self.lhs, str) and isinstance(other.lhs, list)): # single lhs comparing to list of lhs
            return False

        if(isinstance(self.lhs, list) and isinstance(other.lhs, str)): # list of lhs comparing to single lhs
            return False

        else: # single lhs comparing to single lhs
            sl = self.lhs.lower()
            ol = other.lhs.lower()
            return stn == otn and sl == ol and srhs == orhs

    def __str__(self):
        return ("data_base: "+ str(self.dbname)+"\n"+"table: "+ str(self.table_name) +"\n"+"Dep: "+ str(self.lhs_rep) +" --> "+str(self.rhs)+"\n")
        '''print("data_base: ", self.dbname)
        print("table: ", self.table_name)
        print("Dep: ", self.lhs_rep, " --> ", self.rhs , "\n")'''

def compare_list(a,b):
    c1=[]
    c2=[]
    for i in a:
        c1.append(i.lower())
    for e in b:
        c2.append(e.lower())
    c1.sort()
    c2.sort()
    return c1 == c2

def rep(lhs):
    if(isinstance(lhs, str)):
        return lhs
    s="{"
    c=0
    for i in lhs:
        if(c != len(lhs)-1):
            s = s+i
            s=s+", "
            c = c+1
        else:
            s=s+i
            s=s+"}"
    return s





