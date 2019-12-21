t=[1,2,3,4,3,1]
print(set(t))

def argAttribute(a):
        x=len(a)
        res=""
        if(not isinstance(a,list)):
            res=""+str(a) 
        else:  
            res=""+str(a) 
            for i in range(1,x):
                res=res+', '+str(a[i])     
        return res         


x=[["3ABCDE", "un}"],"hel"]
y=["hllo"]
print(", ".join(x))
print(argAttribute(x))
#print(argAttribute(x[1:len(x)-1]))
      