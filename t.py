t=[1,2,3,4,3,1]
print(set(t))

def argAttribute(a):
        x=len(a)
        res=""+str(a[0])
        if(x>1):
            for i in range(1,x):
                res=res+', '+str(a[i])
        return res     


x=["3ABCDE", "un}"]
y=["hllo"]
print(", ".join(x))
print(argAttribute(y))
#print(argAttribute(x[1:len(x)-1]))
      