import cmd

from db import DataBase
from dep import Dep


class Shell(cmd.Cmd):
    """ Displayed shell when the program starts, The user can type different commands described below """

    intro = 'Welcome to the functional dependencies shell.   Type help or ? to list commands.\n'
    prompt = 'Type a command >>> '
    db_object = None
    tabNSD=[] #table ou il y a les df qui ne sont pas satisafite 
    dejafaitNSD=0 #pour savoir si on a déja fait une methode 
    #Il faudrait que tabNSD soit propre a chauqe table ou que les tables n'aient pas les mêmes attributs sino il y a un risque d'erreurs 

    def do_exit(self, arg):

        """ The user type 'exit' and leave the application """

        print('Thank you for using this program, Goodbye')
        self.close()
        return True

    def close(self):
        if self.db_object:
            self.db_object.close()
            self.db_object = None

    def do_connect(self, arg):

        """ The user type 'connect data_base.db' to create a DataBase object connected with the file indicated """

        if (arg == ""):
            print("")  # space
            print("please, enter a data base file")
            print("")  # space
            return False
        print("")  # space
        print("connected to " + arg)
        print("")  # space
        newDB = DataBase(arg)
        self.db_object = newDB

    def do_disconnect(self, arg):

        """The user type 'disconnect' to remove the data base file connected"""
        tabNSD=None
        if (self.db_object == None):
            print("")  # space
            print("Error, no data base file connected")
            print("")  # space
        else:
            print("")  # space
            print("Disconnected to " + self.db_object.db_name)
            print("")  # space
            self.db_object = None

    def do_addDep(self, arg):  # first argument is table name, second is lhs and third is rhs

        """ The user type 'addDep table_name lhs rhs' or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs'
         to create a new functional dependency.
         It creates a new Dep object with the arguments indicated,
         the Dep object is added to the depTab list in the current DataBase object"""

        if(arg==""):
            print("Error, you must type 'addDep table_name lhs rhs' "
                  "or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs' ")
            return 0
        arg_tab=sep(arg)  # transform the argument string with this pattern list : [table_name [lhs, lhs2,...] rhs]

        if (self.db_object == None):
            print("")  # space
            print("Error, you must connect a data base file")
            print("")  # space
            return 0

        if (len(arg_tab) < 3):
            print("")  # space
            print("Error, you must type 'addDep table_name lhs rhs' or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs'")
            print("")  # space
            return 0

        if(isinstance(arg_tab[1], list)): # doesn't work ?
            if(not_recurrent_lhs(arg_tab[1])):  # verify if there are identical lhs
                print("")  # space
                print("Error, you have types 2 identical attributes in lhs")
                print("")  # space

        else:
            new_dep_object = Dep(self.db_object.db_name, arg_tab[0], arg_tab[1], arg_tab[2])
            self.db_object.addDep(new_dep_object)

    def do_removeDep(self, arg):  # first argument is table name, second is lhs and third is rhs

        """ The user type 'removeDep table_name lhs rhs' or 'removeDep table_name {lhs1, lhs2, lhs3, ...} rhs'
         to remove the functional dependency indicated,
         the Dep object is removed from the depTab list in the current DataBase object"""

        arg_tab=sep(arg)
        if (self.db_object == None):
            print("")  # space
            print("Error, you must connect a data base file")
            print("")  # space
        if (len(arg_tab) < 3):
            print("")  # space
            print("Error, you must type 'addDep table_name lhs rhs' or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs'")
            print("")  # space
        else:
            compare_dep = Dep(self.db_object, arg_tab[0], arg_tab[1], arg_tab[2])
            self.db_object.removeDep(compare_dep)

    def do_removeAllDep(self, arg):
        if (self.db_object == None):
            print("")  # space
            print("Error, you must connect a data base file")
            print("")  # space
        else:
            for i in self.db_object.depTab:
                self.db_object.removeDep(i)

    def do_showDep(self, arg):

        """Show the current functional dependency in the data base file"""

        if (self.db_object == None):
            print("Error, you must connect a data base file")
        else:
            print("")  # space
            l = self.db_object.depTab
            if (l == []):
                print("There is no functional dependencies yet, "
                      "you can add them with the command 'addDep table_name lhs rhs' "
                      "or 'addDep table_name {lhs1, lhs2, lhs3, ...} rhs'")
            for i in l:
                print(i.table_name + ": " + i.lhs_rep + " --> " + i.rhs)
            print("")  # space

    def do_showNSD(self, arg):  # NSD = Not Satisfied Dependencies

        """ Compute and show the not satisfied functional dependencies
        The user type 'showNSD table_name' """

        #Ok ça detecte quand il n'y a pas de NSD, il faut juste tester si ça les détecte mtn 

        l = self.db_object.depTab
        arg_tab=sep(arg)
        self.dejafaitNSD=1
        tabD=[]
        tabG=[]
        self.tabNSD=[]
        self.tabNSD.append(str(arg_tab[0]))
        tabDf={} # c'est un dico ou les clefs sont les attributs de gauche et les valeurs sont les attributs de droite
        #On considere qu'on ne selectionne que un attribut à gauche !!!
        r=0 #pour ne toucher que les df qui concerne la table
        for i in l:
            if i.table_name==arg_tab[0]:
                attribute1=argAttribute(self.db_object.depTab[r].lhs) #le nom de l'attribut à gauche de la fléche
                attribute2=str(self.db_object.depTab[r].rhs) #le nom de l'attribut à droite de la flèche
                print(attribute1)
                print(attribute2)
                self.db_object.command.execute("""SELECT """+attribute2 +""" FROM  """ +arg_tab[0]) #on considere qu'il n'y a que un attribut pour le moment
                tabD=self.db_object.command.fetchall() #affiche les resultas sous forme de tableaux
                self.db_object.command.execute("""SELECT """+attribute1 +""" FROM  """ +arg_tab[0])
                tabG=self.db_object.command.fetchall()
                # Cette boucle va nous permettre de comparer les valeurs pour voir si les df sont respecte
                z=0
                print(len(tabD[z]))
                while (z<len(tabG)):
                    k=tabG[z]
                    if (k not in tabDf): #Si il n'est pas dans le dico on l'ajoute
                        tabDf[k]=tabD[z]
                    if (k in tabDf and tabDf[k]!=tabD[z]): #pb on rentre pas dans cette boucle
                        self.tabNSD.append(i)
                        print("ok")
                        z=len(tabG) #pour sortir de la boucle et passer à la Df suivante
                    z=z+1
            r=r+1
            tabD=[]
            tabG=[]
            tabDf={}
            #pas oublier de vider les tableaux et le dico
        if (len(self.tabNSD)>1):    
            print("It's the not satisfied functional dependencies")
            length=len(self.tabNSD)
            for m in range(1,length):
                print(self.tabNSD[m])
        else:
            print("There is no functional dependencies")        

    #recopier le code de mon gsm pour LCD 
    def do_showLCD(self, arg):  # LCD = Logical Consequence Dependencies

        """ Compute and show the functional dependencies that are a logical consequence
        The user type 'showLCD table_name' """

        #Il faut que showNSD ait ete effectue avant de faire ça 
        ''' arg_tab=sep(arg) #c'est le nom de la table dans la base de données
        if (arg_tab[0]==self.tabNSD[0]):
        if(self.dejafaitNSD==1):
            l=self.db_object.depTab
            supelem(l,self.tabNSD) 
            print("The logical consequence dependencies are : \n")
            for m in l:
                print(m)
            else:
                print("You must do 'showNSD' before")
        else:
             print("Please use the same table that you have used 'showNSD'")     '''
        l=self.db_object.depTab
        other=self.db_object.depTab
        nameT=str(arg[0])
        lLCD=[]
        lDF=[]
        for i in l:
        	lDF.append(str(i.lhs)+" --> "+str(i.rhs)) #liste pour supprimer les doublons 
        	for j in other:
        		if i.table_name==nameT and j.table_name==nameT and i.rhs==j.lhs:
        			lLCD.append(str(i.lhs)+" --> "+str(j.rhs))
        			i.rhs=j.rhs
        noDoublons(lLCD,lDF) #permet de supprimer les doublons 
        print("The logical dependencies are : \n") #Il faut qu'elles ne soient pas déja dans les df de base 
        for x in lLCD:
        	print(x)
        			               


    def do_showCOAS(self,arg): # CSOA = Closure Of an Attribute Set

        """ Compute and show the closure of the attribute of the table indicated  
        The user type 'showCOAS table_name attribute_name' """

        #Precondition, il faut que les Df soit deja toutes correctes donc que les mauvaises Df pour la table aient ete supprime 
        lCSOA=[] #liste pour ajouter la fermeture 
        l=self.db_object.depTab
        other=self.db_object.depTab #pour la transitivité 
        nameT=str(arg[0]) #c'est le nom de la table dans la quelle on travaille 
        nameAttribute=str(arg[1])
        lCSOA.append(nameAttribute) #c'est toujours vrai ça 
        for i in l:
            if i.table_name==name and i.lhs==nameAttribute: #pour traiter que les DF qui sont propre à la table et donc lhs est l'attribut donc on veut la fermeture  
                lCSOA.append(str(i.rhs))
                for j in other: #C'est pour traiter la transitivité 
                    if j.table_name==name and i.rhs==j.lhs:
                        lCSOA.append(str(j.rhs))  
                        i.rhs=j.rhs #pour traiter les cas 1->2 2->3 3->4 et du coup que 4 soit dans la liste
        print("The closure of "+nameAttribute+" is : \n")                    
        for nom in lCSOA:
            print(nom)                



        
#a faire pui simplifier le code 
    def do_deleteUID(self, arg):  # UID = Unnecessary or Inconsistent Dependencies

        """ Compute and show functional dependencies that are unnecessary or inconsistent,
        the user can delete them if he wishes """

    def do_checkBCNF(self, arg):

        """ Check if the data base file in in BCNF,
        user has to type the command 'checkBCNF table_name' """

        if(arg==""):
            print("you have to enter a table")
            return 0
        self.db_object.checkBCNF(arg)

    def do_check3NF(self, arg):

        """ Check if the data base file in in 3NF """

    def do_showKey(self, arg):

        """ Compute and show the key(s) of the functional dependencies """

    def do_showSuperKey(self, arg):

        """ Compute and show the super-key(s) of the functional dependencies """


def sep(arg):
    res = []
    lhs=[]
    a=""
    b=""
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
            if (len(lhs) == 1):
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

def not_recurrent_lhs(tab):
    c=0
    for i in tab:
        for e in tab:
            if i == e:
                c=c+1
        if(c>1):
            return False
        c=0
    return True

def argAttribute(a):
        e=a.split()
        x=len(e)
        res=""+str(e[0])
        if(x>1):
            for i in range(1,x):
                res=res+', '+str(e[i])
        return res       

'''def remplire(d,t,v) # le t c'est les clef et v les valeurs 
    for i in range(len(t)):
        x=t[i]
        d[x]=v[i]
    return d   '''    

def supelem(lp,eli):
    i=0
    while(i<len(lp)):
        if (lp[i] in eli):
            lp.pop(i)
            i=i-1
        i=i+1
    return lp
#pour supprimer les elements de eli dans lp    

def noDoublons(a,b):
	for x in a:
		if x in b:
			a.remove(x)
	return a		        


if __name__ == '__main__':
    Shell().cmdloop()
