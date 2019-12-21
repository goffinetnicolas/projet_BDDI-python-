import itertools

from dep import Dep


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



dep1=Dep("t", "a", "b", "c")
dep2=Dep("t", "a", "b", "a")
dep3=Dep("t", "a", ["z","x"], "c")
dep4=Dep("t", "a", ["x","z","a"], "c")


print(dep1.__eq__(dep2))
print(dep1.__eq__(dep3))
print(dep3.__eq__(dep4))