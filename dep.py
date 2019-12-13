class Dep:
    def __init__(self, dbname, table_name, lhs, rhs):
        """ Represent a functional dependency """

        self.table_name = table_name
        self.lhs = lhs
        self.rhs = rhs
        self.db = dbname

    def __eq__(self, other):
        if not isinstance(other, Dep):
            return NotImplemented

        return self.table_name == other.table_name and self.lhs == other.lhs and self.rhs == other.rhs

    def __str__(self):
        self.db.__str__()
        print("data_base: "+self.db.__str__())
        print("table: ", self.table_name)
        print("Dep: ", self.lhs, " --> ", self.rhs + "\n")
