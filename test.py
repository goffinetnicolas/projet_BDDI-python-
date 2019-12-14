import sqlite3

con = sqlite3.connect('putDataBaseHere/test.db')

c = con.cursor()

c.execute("""SELECT Title,ArtistId FROM albums""")

#print(c.fetchall())

con.commit()

con.close()


def sep(arg): # "table {lhs1  ,lhs2, lhs3,lhs4, lhs5} rhs"
    res = [] # [table,]
    lhs=[] #
    a="" #
    b="" #
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

a="test test test"
a=sep(a)
print(a)
print(a[1])