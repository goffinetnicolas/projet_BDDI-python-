class Dep:
    def __init__(self, dbname, table_name, lhs, rhs):
        """ Represent a functional dependency """

        self.table_name = table_name
        self.lhs = lhs
        self.rhs = rhs
        self.db = dbname

    def __str__(self):
        self.db.__str__()
        print("data_base: ", self.db.__str__(), "\n")
        print("table: ", self.table_name, " Dep: ", self.lhs, " --> ", self.rhs)
