class Dep:
    def __init__(self, dbName, table_name, lhs, rhs):
        self.table_name=table_name
        self.lhs=lhs
        self.rhs=rhs
        self.db=dbName

    def __str__(self):
        self.db.__str__()
        print("data_base: ",self.db.__str__(),"\n")
        print("table: ",self.table_name," Dep: ",self.lhs," --> ", self.rhs)