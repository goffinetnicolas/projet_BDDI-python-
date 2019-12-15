import sqlite3

con = sqlite3.connect('putDataBaseHere/test.db')

c = con.cursor()

c.execute("""SELECT Title,ArtistId FROM albums""")

print(c.fetchall())

con.commit()

con.close()

def test():
    dico={"a":1}
    t=[]
    z="a"
    b=2
    if (z in dico and dico[z]!=b ):
        t.append(z)
    print(dico)    
    return t    


def remplire(d,t,v):
    for i in range(len(t)):
        x=t[i]
        d[x]=v[i]
    return d

t2=["un","deux","trois"]
t1=["deux","trois"]
'''d={}
remplire(d,t1,t2)
print(t1)
t1=[]
print(t1) 
print(d)
d={}
print(len(t1)==0)  ''' 
def findIndice(lp,eli):
    i=0
    while(i<len(lp)):
        print(i)
        if (lp[i] in eli):
            lp.pop(i)
            i=i-1
        i=i+1
    return lp

  
print(findIndice(t1,t2))



'''
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
            if(len(lhs)==1):
                res.append(lhs[0])
            else:
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

a="table_name  {lhs1}   rhs"
b="table_name  {lhs1,   lhs2, lhs3  ,    lhs4}   rhs"

print(sep(a), sep(b))

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

def compare_list(a,b):
    c1=[]
    c2=[]
    a.sort()
    b.sort()
    for i in a:
        c1.append(i.lower())
    for e in b:
        c2.append(e.lower())
    return c1 == c2

def insert(s): # s = "lol lal lil lul"
    res=""
    a=s.split()
    for i in a:
        res=res + i +" "
    return res[:len(res)-1]'''


