
Level Design

1. Level
La création d'un niveau correspond à un fichier txt, chaque ligne de ce fichier correspond a une ligne de ma grille de jeu et chaque élement de la liste à une colonne.
Ce qui me permet de définir ma grille de jeu .

Code de correspondance pour chaque celulle:

-1: Way out
0 : Free path
1 : Wall
2 : Hero start position
3 : Boss

5 : Item 1
6 : Item 2
7 : Item 3
8 : Key door
9 : Locked door

Exemple de grille :
1,1,1,1,1,1,1,1,1,1,1,1,1,-1,1
1,0,0,0,1,0,0,0,0,1,0,0,0,3,1
1,0,0,0,1,0,0,0,1,1,0,1,1,1,1
1,0,1,1,1,0,1,1,1,0,0,0,0,0,1
1,0,0,8,1,0,0,0,0,0,0,1,1,1,1
1,0,0,0,1,0,0,0,1,1,1,1,0,0,1
1,1,0,1,1,1,1,0,1,0,0,0,0,0,1
1,0,0,0,0,0,1,0,1,1,1,1,1,0,1
1,1,1,1,1,0,1,0,0,1,0,0,0,0,1
1,0,0,0,1,0,1,1,0,1,1,0,1,1,1
1,0,1,1,1,0,1,1,0,0,1,0,0,1,1
1,0,0,0,1,0,0,1,0,0,1,0,0,0,1
1,1,0,1,1,1,0,1,1,0,1,1,0,1,1
1,0,0,0,0,0,0,9,0,0,0,0,0,0,1
1,2,1,1,1,1,1,1,1,1,1,1,1,1,1

Créer un espace d'environement
Dans le dossier du projet créer un nouveau dossier 
Dans ce dossier ouvrir la console
cmd : virtualenv .
lancer l'environement virtuel 
cmd : ./Scripts/activate
Si message d'erreur windows ne permet pas d'exécuter les scripts 
cmd : Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser -Force
*Activer l'utilisation de script pour l'utilisateur courrant
Installer les modules
Pour vérifier que les modules installer 
cmd : pip freeze

Fichier de dépendances
cmd : pip list > requirements.txt
