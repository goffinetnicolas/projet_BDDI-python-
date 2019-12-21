import copy
import itertools
import sqlite3

from dep import Dep
class DataBase:
    def __init__(self, db_name):

        """ Represent a data base """

        self.db_name = db_name
        self.depTab = []  # list of Dep object

        self.connection = sqlite3.connect('putDataBaseHere/' + db_name)
        self.command = self.connection.cursor()

        try:
            self.command.execute("""SELECT * FROM FuncDep""")
            # check if the FuncDep table is created
            selected = self.command.fetchall()
            for i in selected:
                s = i[1] # s may be "att1 att2 att3" or "att"
                ins = insert(s)
                new_dep_object = Dep(self.db_name, i[0], ins, i[2])
                self.depTab.append(new_dep_object)
                # adding functional dependency already created in the table FuncDep

        except:
            self.command.execute(
                """CREATE TABLE FuncDep (table_name VARCHAR, lhs VARCHAR, rhs VARCHAR)""")
            # create the FuncDep table if an error is detected
            self.connection.commit()

    def addDep(self, dep_object):

        """ Triggered when the addDep command is typed,
        it inserts the functional dependency in the FuncDep table and the Dep object is added in the depTab """

        table_name_arg = dep_object.table_name
        lhs_arg = dep_object.lhs  # could be a string or a list
        rhs_arg = dep_object.rhs # always a string

        if(isinstance(lhs_arg, list)):
            lhs_arg_tab=lhs_arg
            try:
                for i in self.depTab:
                    if(dep_object.__eq__(i)):
                        print("Error, the functional dependency already exists")
                        print("")  # space
                        return 0  # we don't want to execute the rest of the function


                for i in lhs_arg_tab:
                    self.command.execute("SELECT "+i+", "+rhs_arg+" FROM "+table_name_arg)
                    # make an error if the attributes or the table is not in the data base

                lhs_string = extract(lhs_arg_tab)

                self.command.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)",
                                    (table_name_arg, lhs_string, rhs_arg))
                self.connection.commit()
                self.depTab.append(dep_object)
                print("New functional dependency added:")
                print(dep_object.__str__())

            except:
                print("Error, the attribute(s) or the table indicated do not exist")
                print("")  # space


        else:
            try:
                for i in self.depTab:
                    if(dep_object.__eq__(i)):
                        print("Error, the functional dependency already exists")
                        return 0 # we don't want to execute the rest of the function

                self.command.execute("SELECT "+lhs_arg+", "+rhs_arg+" FROM "+table_name_arg)
                # make an error if the attributes or the table is not in the data base

                self.command.execute("INSERT INTO FuncDep VALUES (:table_name, :lhs, :rhs)",
                                    (table_name_arg, lhs_arg, rhs_arg))
                self.connection.commit()
                self.depTab.append(dep_object)
                print("New functional dependency added:")
                print(dep_object.__str__())
                print("")  # space

            except Exception as e:
                print(e)
                print("Error, the attribute(s) or the table indicated do not exist")
                print("")  # space


    def removeDep(self, dep_object):

        """ Triggered when the addDep command is typed,
        it removes the functional dependency in the FuncDep table and the Dep object is removed in the depTab"""

        table_name_arg = dep_object.table_name
        lhs_arg = dep_object.lhs  # could be a string or a list
        rhs_arg = dep_object.rhs  # always a string
        current_dep_tab = self.depTab

        if(isinstance(lhs_arg, list)):
            lhs_string = extract(lhs_arg)

            if (not_member_of(dep_object, current_dep_tab)):
                print("Error, The arguments indicated are not in the functional dependencies")
                print("")  # space

            else:
                for i in current_dep_tab:
                    if (i.__eq__(dep_object)):
                        self.depTab.remove(i)

                self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                     {'table_name': table_name_arg, 'lhs': lhs_string, 'rhs': rhs_arg})
                self.connection.commit()


                print("[" + table_name_arg + ": {" + lhs_string + "} --> " + rhs_arg
                    + "] has been successfully removed from the functional dependencies")
                print("")  # space

        else:
            if (not_member_of(dep_object, current_dep_tab)):
                print("Error, The arguments indicated are not in the functional dependencies")
                print("")  # space

            else:
                for i in current_dep_tab:
                    if (i.__eq__(dep_object)):
                        self.depTab.remove(i)

                self.command.execute("DELETE FROM FuncDep WHERE table_name = :table_name AND lhs = :lhs AND rhs = :rhs",
                                     {'table_name': table_name_arg, 'lhs': lhs_arg, 'rhs': rhs_arg})
                self.connection.commit()
                print("")  # space
                print("[" + table_name_arg + ": " + lhs_arg + " --> " + rhs_arg
                      + "] has been successfully removed from the functional dependencies")

    def showNSD2(self, table):  # Nicolas version
        not_satisfied = []
        dep_list = self.depTab
        table_dep_list = []  # total list of dependencies of the indicated table

        for dep in dep_list:
            if (dep.table_name == table):
                table_dep_list.append(dep)

        for dep in table_dep_list:
            lhs = dep.lhs
            rhs = dep.rhs

            if (isinstance(lhs, list)):
                lhs_list = lhs
                lhs_number = len(lhs_list)
                pos_tab = []

                for lhs in lhs_list:
                    position = self.find_attribute_position(lhs, table)
                    pos_tab.append(position)
                self.command.execute("""SELECT * FROM """ + table)
                result = self.command.fetchall()

                for line1 in result:
                    for line2 in result:
                        cnt = 0  # cnt count if all the lhs are the same
                        for i in range(lhs_number):
                            if (line1[pos_tab[i]] == line2[pos_tab[i]] and line1 != line2):
                                cnt = cnt + 1
                        if (cnt == lhs_number):
                            rhs_pos = self.find_attribute_position(rhs, table)
                            if ((line1[rhs_pos] != line2[rhs_pos])
                                    and (not_member_of(dep, not_satisfied))
                                    and line1 != line2):
                                not_satisfied.append(dep)

            else:
                lhs_pos = self.find_attribute_position(lhs, table)
                rhs_pos = self.find_attribute_position(rhs, table)
                self.command.execute("""SELECT * FROM """ + table)
                result = self.command.fetchall()
                for line1 in result:
                    for line2 in result:
                        if (line1[lhs_pos] == line2[lhs_pos] and line1 != line2):
                            if ((line1[rhs_pos] != line2[rhs_pos])
                                    and (not_member_of(dep, not_satisfied)
                                    and line1 != line2)):
                                not_satisfied.append(dep)

        if (not_satisfied == []):
            print("All the functional dependencies are satisfied")
            print("")  # space
        else:
            for dep in not_satisfied:
                print("The functional dependency: [" + dep.table_name + ": " + dep.lhs_rep + " ---> " + dep.rhs +
                      "] is not satisfied")

    def find_attribute_position(self, lhs, table):

        self.command.execute("""SELECT """ + lhs + """ FROM """ + table) # ("title of a music")
        tup_result = self.command.fetchone()

        self.command.execute("""SELECT * FROM """ + table)
        tup_list_result = self.command.fetchall()

        for tup in tup_list_result:
            a=0
            for string in tup:
                if(string == tup_result[0]):
                    return a
                else:
                    a=a+1


    def checkBCNF(self, table):

        """ Triggered with the command 'checkBCNF',
         this algorithm check if all the functional dependencies can gives t
         he entire attribute list of the indicated table """

        l = self.depTab
        table_dep_list = []  # the dep list of the indicated table

        for dep in l:  # extract the functional dependencies linked to the table
            if (dep.table_name == table):
                table_dep_list.append(dep)

        if (len(table_dep_list) == 0):
            print("There is not functional dependencies linked to the indicated table")
            print("")  # space
            return False

        att_list = self.find_table_attribute(table)  # total attribute list of the table

        if(len(table_dep_list) == 1):

            att_obtained = []  # attributes that we will obtain thanks to functional dependencies
            lhs = table_dep_list[0].lhs
            rhs = table_dep_list[0].rhs

            if (isinstance(lhs, list)):
                for lhs_string in lhs:
                    att_obtained.append(lhs_string)

            else:
                att_obtained.append(lhs)

            att_obtained.append(rhs)

            if(not compareList(att_list,att_obtained)):  # compareList returns True if the lists are the same
                return False

            return True

        else:
            for dep1 in table_dep_list:
                att_obtained = []  # attributes that we will obtain thanks to functional dependencies
                att_obtained.append(dep1.rhs)

                if (isinstance(dep1.lhs, list)):
                    for lhs in dep1.lhs:
                        att_obtained.append(lhs)
                else:
                    att_obtained.append(dep1.lhs)

                while (not compareList(att_list,att_obtained)):  # compareList returns True if the lists are the same
                    check_list = copy.deepcopy(att_obtained)

                    for dep2 in table_dep_list:
                        if (detect(dep2.lhs, att_obtained) and dep2.rhs not in att_obtained):  # must verify
                            att_obtained.append(dep2.rhs)

                    if (compareList(check_list, att_obtained)):  # compareList returns True if the lists are the same
                        return False

            return True

    def showKey(self, table):
        l = self.depTab
        table_dep_list = []
        att_list = self.find_table_attribute(table)  # total attribute list of the table

        for dep in l:  # extract the functional dependencies linked to the table
            if (dep.table_name == table):
                table_dep_list.append(dep)

        if (len(table_dep_list) == 0):
            print("")  # space
            print("There is not functional dependencies linked to the indicated table")
            print("")  # space
            return []

        key_list = []

        for L in range(0, len(att_list) + 1):  # test all possible attribute combinations
            for potential_key in itertools.combinations(att_list, L):
                if(self.check_all_attributes_obtained(table_dep_list, att_list, list(potential_key))):
                    #  this function check if with the current attribute combination,
                    #  we can reach all attributes of the table
                    key_list.append(list(potential_key))

        return key_list


    def check_all_attributes_obtained(self, dep_list, total_attribute_list, potential_key):
        #  this function check if with the current attribute combination,
        #  we can reach all attributes of the table
        while(not compareList(potential_key,total_attribute_list)):
            compare_key = copy.deepcopy(potential_key)
            for dep in dep_list:
                if(detect(dep.lhs,potential_key) and dep.rhs not in potential_key):  # verify this condition
                    potential_key.append(dep.rhs)
            if(compare_key == potential_key):
                return False
        return True

    def find_table_attribute(self, table):
        try:
            self.command.execute("""SELECT * from """+table)
            att_list = [description[0] for description in self.command.description]
            return att_list

        except:
            print(table+" does not exist in the database")


    def showSuperKey(self, key_list):
        not_super_key=[]
        for key1 in key_list:
            for key2 in key_list:
                if(not compareList(key1,key2)):
                    cnt=0
                    for att in key1:
                        if(att in key2):
                            cnt=cnt+1
                    if(cnt == len(key1) and key2 not in not_super_key):
                        not_super_key.append(key2)

        for key in not_super_key:
            key_list.remove(key)

        return key_list

    def check3NF(self, table):
        if(self.checkBCNF(table) == True):
            return True
        else:
            super_key_list=self.showSuperKey(table)
            att_list = self.find_table_attribute(table)
            for att in att_list:
                if(att not in super_key_list):
                    return False

            return True

    def showNSD(self,table):
        l=self.depTab
        #arg_tab=sep(arg)
        tabNSD=[]
        tabNSD.append(str(table))
        tabDf={} # c'est un dico ou les clefs sont les attributs de gauche et les valeurs sont les attributs de droite
        #On considere qu'on ne selectionne que un attribut à gauche !!!
        r=0 #pour ne toucher que les df qui concerne la table
        for i in l:
            if i.table_name==table:
                attribute1=argAttribute(l[r].lhs) #le nom de l'attribut à gauche de la fléche
                attribute2=str(l[r].rhs) #le nom de l'attribut à droite de la flèche
                self.command.execute("""SELECT """+attribute2 +""" FROM  """ + table) #on considere qu'il n'y a que un attribut pour le moment
                tabD=self.command.fetchall() #affiche les resultas sous forme de tableaux
                self.command.execute("""SELECT """+attribute1 +""" FROM  """ + table)
                tabG=self.command.fetchall()
                # Cette boucle va nous permettre de comparer les valeurs pour voir si les df sont respecte
                z=0
                while (z<len(tabG)):
                    k=tabG[z]
                    if (k not in tabDf): #Si il n'est pas dans le dico on l'ajoute
                        tabDf[k]=tabD[z]
                    if (k in tabDf and tabDf[k]!=tabD[z]): #pb on rentre pas dans cette boucle
                        tabNSD.append(i)
                        z=len(tabG) #pour sortir de la boucle et passer à la Df suivante
                    z=z+1
            r=r+1

        if (len(tabNSD)>1):    
            print("It's the not satisfied functional dependencies")
            length=len(tabNSD)
            for m in range(1,length):
                print(tabNSD[m])
        else:
            print("There is no functional dependencies")    

    def showLCD(self,table):
        l=self.depTab
        other=self.depTab
        lLCD=[]
        lDF=[]
        for i in l:
            lDF.append(str(i.lhs)+" --> "+str(i.rhs)) #liste pour supprimer les doublons
            a_irhs=i.rhs #pour sauvegarder la prmiere valeur 
            for j in other:
                if i.lhs==j.rhs and i.table_name==table and j.table_name==table:
                    i.rhs=a_irhs
                    lLCD.append(str(j.lhs)+" --> "+str(i.rhs))
                if i.table_name==table and j.table_name==table and i.rhs==j.lhs:
                    lLCD.append(str(i.lhs)+" --> "+str(j.rhs))
                    i.rhs=j.rhs
                    #voir cas sur papier avec des chiffres 
                    #i.rhs=j.rhs
                            # si on inerse pas et qu'on recoit 1->2 2->3
        noDoublons(lLCD,lDF) #permet de supprimer les doublons 
        print("The logical dependencies are : \n") #Il faut qu'elles ne soient pas déja dans les df de base 
        for x in set(lLCD):
            print(x)
        lLCD=[]
        lDF=[]    

    def showCOAS(self,table,attribut):
        #Precondition, il faut que les Df soit deja toutes correctes donc que les mauvaises Df pour la table aient ete supprime 
        lCSOA=[] #liste pour ajouter la fermeture 
        l=self.depTab
        other=self.depTab #pour la transitivité 
        x=attribut
        if isinstance(attribut,list):
            x=", ".join(attribut)
        print(x)   
        lCSOA.append(x) #c'est toujours vrai ça 
        for i in l:
            if i.lhs==attribut:
                lCSOA.append(str(i.rhs))  
            if i.table_name==table : #and i.rhs not in lCSOA:#and i.lhs==nameAttribute and i.rhs not in lCSOA: #pour traiter que les DF qui sont propre à la table et donc lhs est l'attribut donc on veut la fermeture  
                for j in other[1:]: #C'est pour traiter la transitivité
                    if j.table_name==table and (i.rhs==j.lhs or i.lhs==j.rhs):
                        if i.rhs==j.lhs and j.rhs not in lCSOA:
                            lCSOA.append(str(j.rhs))
                            lCSOA.append(str(i.rhs)) 
                        if i.lhs==j.rhs and j.lhs not in lCSOA:
                            if isinstance(j.lhs,list):
                                y=", ".join(j.lhs)
                                lCSOA.append(y)
                            else:
                                lCSOA.append(str(j.lhs))        
                                           
        print("The closure of "+x+" is : \n")                    
        for nom in set(lCSOA):
            print(nom) 

    def deleteUID(self,table):
        l=self.depTab
        other=self.depTab
        lUID=[] #pour avoir ceux qui ne sont pas correcte 
        lNameDep=[] #pour avoir juste le nom des dep 
        for h in l:
            if (isinstance(h.lhs,list)):
                h.lhs=", ".join(h.lhs)
            lNameDep.append(str(h.lhs)+" --> "+str(h.rhs))
        for i in l:  
            a_irhs=i.rhs  
            for j in other: 
                if j.table_name==table and i.table_name==table and (i.rhs==j.lhs or i.lhs==j.rhs):
                    lUID.append(str(i.lhs)+" --> "+str(i.rhs))
                    if (i.rhs==j.lhs):
                        x=str(i.lhs)+" --> "+str(j.rhs) #C'est pour le tester si il est dans l'ensemble des df 
                        i.rhs=j.rhs
                    if (i.lhs==j.rhs):
                        x=str(j.lhs)+" --> "+str(i.rhs) #C'est pour le tester si il est dans l'ensemble des df 
                        i.rhs=a_irhs
                    if x not in lUID: 
                        lUID.append(x)   
        for z in lUID:
            print(z)    
        print("If you want to delete them, please press 1 but if you don't want press 2")
        y=input()
        doublons=[]
        if y=="1":
            for v in l:
                if (isinstance(v.lhs,list)):
                    v.lhs=", ".join(v.lhs)
                if v.table_name==table and (str(v.lhs)+" --> "+str(v.rhs)) in lUID:
                    doublons.append(v)
                    self.removeDep(v)                             

    def close(self):
        pass

    def __str__(self):
        return self.db_name

def insert(s):
    a=s.split()
    if(len(a)==1):
        return a[0]
    return a

def extract(s):
    res=""
    for i in s:
        res=res+i+" "
    l=len(res)-1
    return res[:l]

def not_member_of(depObject, depList):  # returns True if the dep is not in the dep list
    for i in depList:
        if(depObject.__eq__(i)):
            return False
    return True

def detect(string_or_list_lhs, string_list):  # returns True if the lhs is in the string list
    if(isinstance(string_or_list_lhs, list)):
        lhs_list=string_or_list_lhs
        for lhs in lhs_list:
            if(lhs not in string_list):
                return False
        return True
    else:
        lhs_string=string_or_list_lhs
        if(lhs_string in string_list):
            return True
        else:
            return False

def compareList(list1, list2):  # returns True is the list are the same
    a=[]
    b=[]
    for i in list1:
        a.append(i.lower())
    for i in list2:
        b.append(i.lower())
    for i in a:
        if(i not in b):
            return False
    for i in b:
        if(i not in a):
            return False
    return True

def argAttribute(a):
        x=len(a)
        res=""+str(a[0])
        if(x>1):
            for i in range(1,x):
                res=res+', '+str(a[i])
        return res       

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


