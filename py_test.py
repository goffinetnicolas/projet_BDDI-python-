import itertools

from dep import Dep

# This file tests if the implemented functions work correctly

def test():
    dico = {"a": 1}
    t = []
    z = "a"
    b = 2
    if (z in dico and dico[z] != b):
        t.append(z)
    print(dico)
    return t


def remplire(d, t, v):
    for i in range(len(t)):
        x = t[i]
        d[x] = v[i]
    return d


def findIndice(lp, eli):
    i = 0
    while (i < len(lp)):
        print(i)
        if (lp[i] in eli):
            lp.pop(i)
            i = i - 1
        i = i + 1
    return lp


def compareList(list1, list2):
    a = []
    b = []
    for i in list1:
        a.append(i.lower())
    for i in list2:
        b.append(i.lower())
    for i in a:
        if (i not in b):
            return False
    for i in b:
        if (i not in a):
            return False
    return True



a='A'
a=a.lower()
print(a)
