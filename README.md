# projet_BDDI-python-

Bienvenue dans le fichier README

Voici les explications concernant ce programme. Ce programme est codé en Python par Nicolas GOFFINET et Maxime Renversez. Il gère les dépendances fonctionnelles des bases de données introduites dans le répertoire "putDataBaseHere".
Lien du github: https://github.com/goffinetnicolas/projet_BDDI-python-

Voici un récapitulatif des commandes que l'on peut executer dans l'interpréteur de ligne de commande (les commandes doivent être executées sans les crochets):

 1. [help] ou [?] 

-Affiche les commandes programmées sur la console. "help" permet aussi de donner la documentation d'une commande si vous introduisez la commande ainsi: [help commande_name]


 2. [exit]

-Quitte le programme


 3. [connect database_name.db] 

-Cette commande permet de se connecter à la base de donnée indiquée afin de pouvoir effectuer des  opérations sur celle-ci. Si aucune base de donnée n'est connectée, il est impossible d'effectuer des opérations


 4. [disconnect database_name.db]

-Cette commande permet de se déconnecter à la base de donnée indiquée.


 5. [showDep]

-Permet d'afficher toutes les dépendances fonctionnelles de la base de donnée connectée.


 6. [addDep table_name lhs rhs]

-Permet d'ajouter une dépendance fonctionnelle avec un 'lhs' singulier dans la table indiquée. Il est à noter que la formulation est importante, chaque argument doit être séparer d'un espace comme montré ci-dessus afin d'éviter d'afficher une erreur.


 7. [addDep table_name {lhs1, lhs2, lhs3, ...} rhs]

-Permet d'ajouter une dépendance fonctionnelle avec plusieurs 'lhs' dans la table indiqué. L'utilisateur doit indiquer les 'lhs' entre accolade et séparé par des virgules comme montré ci-dessus.


 8. [removeDep table_name lhs rhs] et [removeDep table_name {lhs1, lhs2, lhs3, ...} rhs]

-Permet d'enlever la dépendance fonctionnelle indiquée en paramètre.


 9. [removeTableDep table_name]

-Enlève toutes les dépendances fonctionnelles liées à la table.


 10. [removeAllDep]

-Enlève toutes les dépendances fonctionnelles de la base de donnée.


 11. [showNSD table_name] 

-Montre les dépendances fonctionnelles non-satisfaites dans la table indiquée (showNSD = show Not Satisfied Dependencies).


 12. [showLCD table_name]

-Montre les dépendances fonctionnelles logiques déterminées par les dépendances fonctionnelles initiales de la table (showLCD = show Logical Consequence Dependencies).


 13. [showCOAS table_name attribute] ou [showCOAS table_name attribute1 attribute2 ...]

-Permet de calculer et montrer la fermeture d'un ou plusieurs attributs.


 14. [deleteUID table_name]

-Permet de montrer les dépendances fonctionnelles redondantes et inutiles si elles existent et de proposer à l'utilisateur de les enlever (deleteUID = delete Unnecessary or Inconsistent Dependencies).


 15. [showKey table_name]

-Permet de calculer toutes les clés de la table indiquée


 16. [showSuperKey]

-Permet de calculer toutes les super-clés présentes dans les clés


 17. [checkBCNF table_name]

-Permet de savoir si la table est en BCNF


 18. [showBCNF table_name]

-Permet de montrer les dépendances fonctionnelles qui empêche la table d'être en BCNF. 


 19. [show3NF table_name]

-Permet de savoir si la table est en 3NF, si ce n'est pas le cas et si toutes les dépendances fonctionnelles sont respectées par la table, l'utilisateur peut décider de recréer une nouvelle base de donnée avec des décompositions en 3NF. il est à noter que la décomposition en 3NF n'a pas été beaucoup testée et peut mener à des erreurs.
