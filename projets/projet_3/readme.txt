
Level Design

1. Level
La cr�ation d'un niveau correspond � un fichier json, chaque ligne de ce fichier correspond a une ligne de ma grille de jeu et chaque element � une colonne.
Ce qui me permet de d�finir ma grille de jeu .

Code de correspondance pour chaque celulle:

-1: Way out
0 : Free path
1 : Wall
2 : Hero
3 : Boss

5 : Item 1
6 : Item 2
7 : Item 3
8 : Key door
9 : Locked door

Exemple de grille :
[
{1,1,1,1,1,1,1,1,1,1,1,1,1,-1,1},
{1,0,0,0,1,0,0,0,0,0,0,0,0,3,1},
{1,0,0,0,1,0,0,0,0,0,0,0,0,0,1},	
{1,0,1,1,1,0,0,0,0,0,0,0,0,0,1},	
{1,0,0,0,1,0,0,0,0,0,0,0,0,0,1},	
{1,0,0,0,1,0,0,0,0,0,0,0,0,0,1},	
{1,1,0,1,1,1,1,0,0,0,0,0,0,0,1},	
{1,0,0,0,0,0,1,0,0,0,0,0,0,0,1},	
{1,1,1,1,1,0,1,0,0,0,0,0,0,0,1},	
{1,0,0,0,1,0,1,0,0,0,0,0,0,0,1},
{1,0,1,1,1,0,1,1,0,0,0,0,0,0,1},	
{1,0,0,0,1,0,0,1,0,0,0,0,0,0,1},	
{1,1,0,1,1,1,0,1,0,0,0,0,0,0,1},	
{1,0,0,0,0,0,0,9,0,0,0,0,0,0,1},	
{1,2,1,1,1,1,1,1,1,1,1,1,1,1,1},				
]
