'''-----------------------------------------------------------------------------
                               Utilisation                                     |
	python3 labyrinthe.py                                                      |
-----------------------------------------------------------------------------'''

import random

'''-----------------------------------------------------------------------------
                             Génération de la matrice                          |
 Nous créeons une matrice de dimensions (h*2)+1 et (l*2)+1. De plus nous diff- |
 érencions une cellule avec un mur en fonction de sa colonne et sa ligne, à    |
 l'aide de modulo                                                              |
 Hauteur : h ; Largeur : l                                                     |
-----------------------------------------------------------------------------'''
def geneMatrice (h,l):
	k=0
	li = []
	for i in range((h*2)+1): #i : Ligne
		ki = [] #initialisaton avec une colonne vide
		for j in range ((l*2)+1): #j : colonne
			if (i%2 == 0) or (j%2 == 0):
				ki.append(-1) #S'il s'agit d'un mur on ajoute à l'indice aproprié un -1
			else:
				ki.append(k) #sinon on ajoute un chiffre k qui augmente au fur et à mesure
				k += 1
		li.append(ki) #ajout de la ligne dans la matrice
	return li

'''-----------------------------------------------------------------------------
                             Génération du Labyrinthe                          |
 Pour commencer la génération du labyrinthe, nous choississons aléatoirement   |
 une cellue. Pour cela, on créer une liste avec toutes les cellules à l'aide de|
 listeDeCells(matr). Ensuite, nous la choissionsson aléatoirement à l'aide de  |
 cellDepart(matr). La fonction creationPassageDe est la fonction qui nous      |
 permet de créer nos passages dans la matrice donc faire le labyrinthe. Nous   |
 utilisons une fonction appellée possible, qui nous permet de savoir si une    |
 certaine case est bien dans les limites du labyrinthe. Cette fonction nous    |
 renvoie un booleen. Nous utiliserons donc cee résultat dans la fonction       |
 voisinPossible qui vérifie pour une case donnée toutes les possibilité        |
 de cassage de mur. Nous récupérons alors ces possibilités sous une liste et   |
 choississons aléatoirement parmis cette liste une case. Nous avons également  |
 instauré une liste sous forme de pile qui nous permet donc de revenir en      |
 arrière si jamais nous rencontrons un cul de sac et ainsi repartir par un     |
 autre chemin. Nous arretons le parcours de la matrice à parcouru h*l cases.   |
 De plus, nous instaurons une liste avec toutes les cases parcouru pour être   |
 sur de ne pas comptabliser 2 fois une case.                                   |
-----------------------------------------------------------------------------'''

def listeDeCells (matr):
	li = [] #Création d'une liste vide où nous allons ajouter au fur et à mesure les cases
	for i in range(1,len(matr)-1):
		for j in range (1,len(matr[i])-1):
			if matr[i][j] != -1: #si la case parcouru n'est pas égale à -1 alors on ajoute ces coordonnées dans la liste
				li.append((i,j))
	return li

def cellDepart (matr):
	return random.choice(listeDeCells(matr)) #Nous choississons une case aléatoirement pris de la liste précédente pour point de départ à la création du labyrinthe

def possible (matr,depart):
	(dx,dy) = depart #Extraction des coordonnées du point
	if (dx < 0) or (dx > len(matr)-2): #Nous vérifions si ce point est bien dans les bornes des dimensions de la matrice. Si non, nous renvoyons faux, sinon vrai
		return False
	elif (dy < 0) or (dy > len(matr[dx])-2):
		return False
	else :
		return True

def voisinPossible(deja, matr,depart): #nous prennons un paramètre deja qui est la liste des cases déjà visité pour éviter tout calcul et test fait plusieurs fois.
	(dx,dy) = depart #extraction des coordonnées du point
	vPossible  = [] #liste vide où nous allons ajouter chaque voisin possible à ce point là
	if ((dx-2,dy) not in deja) and (possible(matr,(dx-2,dy))) and (matr[dx-1][dy] == -1) and (matr[dx-2][dy] != -1):
		vPossible.append((dx-2,dy)) #vérification de la possibilité de ce voisin en fonction de la direction. Si oui l'ajouter dans la liste des voisins possible. Si non, rien faire
	if ((dx+2,dy) not in deja) and (possible(matr,(dx+2,dy))) and (matr[dx+1][dy] == -1) and (matr[dx+2][dy] != -1):
		vPossible.append((dx+2,dy))
	if ((dx,dy-2) not in deja) and (possible(matr,(dx,dy-2))) and (matr[dx][dy-1] == -1) and (matr[dx][dy-2] != -1):
		vPossible.append((dx,dy-2))
	if ((dx,dy+2) not in deja) and (possible(matr,(dx,dy+2))) and (matr[dx][dy+1] == -1) and (matr[dx][dy+2] != -1):
		vPossible.append((dx,dy+2))
	return vPossible #sortie de la liste des voisins possible

def creationPassageDe(depart,matr,deja_visit,cell_lifo,compt,total): #Fonction de création du labyrinthe
	(dx,dy) = depart #exctraction du point en question
	if compt < total: #vérification que nous ne tournons pas en rond. Sinon récursivité infini
		voisinPosi = voisinPossible(deja_visit, matr,(dx,dy)) #sortie de la liste de voisin possible pour le point donnée
		if ((dx,dy) not in deja_visit): #Si ce point n'est pas dans la liste des deja visite, nous l'ajoutons
			deja_visit.append((dx,dy))

		if (not voisinPosi): #si la liste des voisins possible est vide nous retournons sur nos pas grace à cell_lifo qui est une pile contenant le chamin pris.
			return creationPassageDe(cell_lifo.pop(),matr,deja_visit,cell_lifo,compt,total) #appel récursif pour retour en arrière
		else:
			(nv_x,nv_y) = random.choice(voisinPosi) #choix aléatoire d'un des voisins possible de la liste
			(var_x,var_y) = (nv_x-dx,nv_y-dy) #cette opération nous permet de trouver la variation dans la direction, donc de trouver l'orientation du déplacement
			if (var_x == -2):
				matr[dx-1][dy] = min(matr[nv_x][nv_y],matr[dx][dy]) #on donne la valeur minimum à la case créée entre deux cases
			elif (var_x == 2):
				matr[dx+1][dy] = min(matr[nv_x][nv_y],matr[dx][dy])
			elif (var_y == -2):
				matr[dx][dy-1] = min(matr[nv_x][nv_y],matr[dx][dy])
			else:
				matr[dx][dy+1] = min(matr[nv_x][nv_y],matr[dx][dy])
			cell_lifo.append((nv_x,nv_y)) #ajout de la case en question dans la liste des case visité
			return creationPassageDe((nv_x,nv_y),matr,deja_visit,cell_lifo,compt+1,total) #appel récursif avec la nouvelle case, qui nous permet d'avancer et ajout de 1 au compteur pour nous permettre de bien garder le compte
	else:
		return matr #si le compteur deviens supèrieur au nombre de cases total, alors, nous sortons de la récursion et ressortons le labyrinthe créé

'''-----------------------------------------------------------------------------
                             Affichage du labyrinthe                           |
-----------------------------------------------------------------------------'''
def afficheLabyrinthe (lab): #fonction nous permettant d'afficher à l'écran le labyrinthe
	for ligne in lab : #boucles for pour nous permettre de parcourir la totalité de la matrice
		for case in ligne :
			if case == -1: #Cas où nous recontrons un mur, alors on print un #
				print('\033[1;37m#\033[1;m', sep='', end='', flush=True)
			elif str(case).isalpha(): #Cas où nous rencontrons un point de départ ou d'arrivé et nous affichons la lettre
				print('\033[1;35m'+case + '\033[1;m', sep='', end='', flush=True)
			elif str(case) == '.': #cas où nous rencontrons une case faisant partis du chemin final, nous affichons alors un point
				print('\033[1;36m'+case+ '\033[1;m', sep='', end='', flush=True)
			else: #pour tout autre cas, il s'agit d'une case vide alors nous n'affichons qu'un espace
				print(' ', sep='', end='', flush=True)
		print ('') #cette ligne nous permet de rien imprimer mais d'effecteur un retour à la ligne
#On peut remarquer que nous avons des codes avant et après chaque case. Celà correspond à une couleur d'impression. C'est donc ce qui nous permet d'avoir des couleurs différentes dans le labyrinthe et donc de mieux différencier les différents éléments.

'''-----------------------------------------------------------------------------
                             Entrées Utilisateur                               |
-----------------------------------------------------------------------------'''
def demande_param (): #Fonction de demande de dimension
	print('\033[1;32mVeuillez entrer la taille souhaite de votre labyrinthe :')
	l = input('Largeur : ')
	h = input('Hauteur : ')
	print('Voici le labyrinthe aleatoire genere :\033[1;m')
	return (int(l),int(h)) #Quand l'utilisateur entre ses dimensions voulu, cela nous rend un string, or nous ne travaillons qu'avec des entier, donc nous renvoyons directement les strings tranformé en entier.

'''-----------------------------------------------------------------------------
                                 Ouvertures                                    |
	La fonction demande_ouverture va demander à l'utilisateur d'entrer les     |
	coordonnées du point de départ et d'arrivé. À l'aide de la fonction        |
	test_ouvertures, nous vérifions si les coordonnées entrées sont correcte   |
	ou non. Si elles sont correctes nous appellons finalement la fonction      |
	ouverture qui va elle, remplacer les murs choisis par A ou par B.          |
-----------------------------------------------------------------------------'''

def test_ouvertures (laby,x,y): # Fonction permettant de vérifier si les coordonées entrer pour former des ouvertures sont correct où non.
	if (y==0) and (x>0) and (x < (len(laby[y])-1)) and (laby[y+1][x] != -1): #Nous vérifions si les coordonnées font bien partis des murs exterieurs et si, en fonction du mur choisis la première case à l'intèrieur n'est pas un mur, ce qui rendrait l'ouverture impossible
		return True
	elif (y==(len(laby)-1)) and (x>0) and (x < (len(laby[y])-1)) and (laby[y-1][x] != -1):
		return True
	elif (x==0) and (y>0) and (y < (len(laby)-1)) and (laby[y][x+1] != -1):
		return True
	elif (x==(len(laby[y])-1)) and (y>0) and (y < (len(laby)-1)) and (laby[y][x-1] != -1):
		return True
	else:
		return False # Si l'ouverture est impossible alors nous renvoyons faux. Sinon vrai

def demande_ouverture (laby) : #Cette fonction appelle 2 fois la fonction précédentes, permettant de vérifier l'ouverture du départ et l'ouverture de l'arrivée.
	print('\033[1;32mEntrer les coordonnees du point de depart :')
	entree_x = int(input('X : '))
	entree_y = int(input('Y : '))
	print("Entrer les coordonnees du point d'arrivé :")
	sortie_x = int(input('X : '))
	sortie_y = int(input('Y : '))
	while (not test_ouvertures(laby,entree_x,entree_y)) or (not test_ouvertures(laby,sortie_x,sortie_y)) : # Si l'utilisateur entre des coordonnées non valide alors à l'aide de la boucle while nous lui redemandons jusqu'à ce qu'il entre des ouvertures valide.
		print('Erreur : Les coordonnes entrees ne sont pas valides. Veuillez reessayer.\033[1;m')
		return demande_ouverture(laby)
	return (entree_x,entree_y,sortie_x,sortie_y)

def ouverture(e_x,e_y,s_x,s_y,laby): #Fonction faisant l'ouverture
	laby[e_y][e_x] = 'A' #Après avoir fais touts les test, nous modifions alors la matrice avec les ouvertures voulu
	laby[s_y][s_x] = 'B'
	return laby


'''-----------------------------------------------------------------------------
                                 Solution                                      |
 Pour trouver la solution, nous crééons une file et une liste vide. Cette liste|
 nous permets de stocké les chemins déjà visité pour éviter de tourner en rond.|
 Nous commençons tout d'abord par ajouter le point de départ dans la file. En  |
 réalité, voici le fonctionnement de la file : toute possibilité de cases      |
 adjacentes est mis à la fin de la file et chacun leur tour nous les étudions. |
 À chaque cases, nous appellons la fonction neighborhood qui nous ressort une  |
 liste composé de touts les voisins adjacents. Et à chaque voisin nous créons  |
 un chemin. Quand nous visitons pour la première fois une case nous la mettons |
 dans la liste visited. À chaque itération nous vérifions si la case est dans  |
 la liste visited ou non. Si oui, nous passons à la case d'après dans la file. |
 Sinon, nous l'étudions. Et ainsi de suite jusqu'a que l'on trouve la case     |
 d'arrivé. Comme on ajoute chaque chemin sous forme de liste à la fin de la    |
 de la file, nous étudions alors que le dernier élément de cette liste qui nous|
 donne la position actuelle. Une fois que nous sommes à la bonne case cela veux|
 dire qu'on a trouvé un chemin nous ammenant à l'arrivée. Et donc il s'agit du |
 plus court car nous arretons tous dès que nous trouvons cette case. Le chemin |
 ressort sous forme de liste, donc pour chaque élément de cette liste, nous    |
 récupérrons les coordonnées et ajoutons un '.' aux coordonnées voulu qui nous |
 fera donc le chemin.                                                          |
-----------------------------------------------------------------------------'''

def neighborhood (laby,coords): #Fonction nous permettant de sortir toutes les cases disponible adjacentes à celle sur la quelle on est actuellement
	[x,y] = coords #extraction des coordonnées
	neighbors = [] #création d'une liste vide qui sera rempli au fur et à mesure
	if (laby[y-1][x] != -1):
		neighbors.append((x,y-1))

	if (laby[y+1][x] != -1):
		neighbors.append((x,y+1))

	if (laby[y][x-1] != -1):
		neighbors.append((x-1,y))

	if (laby[y][x+1] != -1):
		neighbors.append((x+1,y))
	return neighbors #sortis de la liste remplis


def solver(laby,start,end): #fonction Princiaple utilisée pour la résolution du labyrinthe
	queue = [] #création de la file vide
	visited = [] #création de la liste vide qui va ensuite comporter les cellules étudié et donc baissé le temps de résolution car aucune répétition d'opérations inutile
	queue.append([start]) #nous ajoutons dès le début le point de départ dans la file
	while queue: #tant que file n'est pas vide
		path = queue.pop(0) #nous ressortons le premier élément de la file
		node = path[-1]  #nous utilisons alors la dernière valeur de l'élément sortie de la file, qui est égale à la position actuelle de l'algorithme dans le labyrinthe
		if node == end: #Si cette position actuelle est égale aux coordonnées d'arrivées alors nous avons trouvé le chemin le plus court
			return path #sortie du chemin le plus court
		if node in visited: #si la position acutelle est déjà présente dans la liste comportant les cases visité, alors nous passons à la boucle d'après, c'est à dire à l'élément suivant dans la file
			continue
		visited.append(node) # sinon nous ajoutons cette case dans la liste des cases visités
		neighborhoodList = neighborhood(laby,node) #nous ressortons la liste des voisins adjacents possible
		for neighbor in neighborhoodList: # pour chaque élément de la liste ressortis :
			new_path = list(path) #nous créons une liste avec le chemin emprunté
			new_path.append(neighbor) #nous ajoutons à cette liste le voisin en question
			queue.append(new_path)	#et nous ajoutons à la fin de la file ce chemin pour être ensuite étudié

def tracePath (laby,chemin): #fonction permettant d'ajouter le chemin le plus court dans le labyrinthe
	del chemin[0] #nous supprimons le premier élément de cette liste car il s'agit du point de départ qui à déjà une valeur
	del chemin[-1] #nous supprimon également le dernier élément de cette liste qui s'agit de l'arrivé
	for case in chemin: #pour chaque élément dans le chemin
		(x,y) = case #extraction des coordonnées
		laby[y][x] = '.' #ajout d'un point aux coordonnées corespondante
	return laby #sortis du labyrinthe résolu

'''-----------------------------------------------------------------------------
                        Fonction Princiaple                                    |
 La fonction main est la fonction princpiale qui est appellée directement au   |
 lancement du programme. En effet, nous commençons alors par demander les      |
 dimensions du labyrinthe voulu. Cela nous génère alors une matrice toute      |
 avec les cases et 4 murs pour chaque cases. Ensuit nous envoyons cette matrice|
 dans la fonction de création de labyrinthe, qui nous renvoie alors la matrice |
 modifiée. Nous affichons à ce moment là  le labyrinthe à l'utilisateur. Il va |
 ensuite être demandé d'entrer les coordonnées des ouvertures pour le départ et|
 l'arrivée. Après avoir récupéré ces coordonnées en question, nous formons les |
 ouvertures dans les murs du labyrinthe. Et finalement nous lançons la         |
 recherche du chemin de solution le plus court. Cette fonction nous ressort une|
 liste avec les coordonnées de chaque case à emprunter. Donc nous appellons la |
 fonction tracePath qui va ajouter dans la matrice un '.' dans les cases       |
 corespondante. Puis nous finissons par afficher le labyrinthe résolu.         |
-----------------------------------------------------------------------------'''

def main(): #fonction Princiaple
	(l,h) = demande_param() #sortie des dimension
	matrGene = geneMatrice(h,l) #génération de la matrice de dimensions h*l
	labyGene = creationPassageDe(cellDepart(matrGene),matrGene,[],[],1,h*l) #génération du labyrinthe à partir de la matrice
	afficheLabyrinthe(labyGene) #Affichage du labyrinthe
	[e_x,e_y,s_x,s_y] = demande_ouverture (labyGene) #sortie des coordonnées d'ouverture
	labyGene2 = ouverture(e_x,e_y,s_x,s_y,labyGene) #ouverture des murs du labyrinthe
	pointsSolution = solver(labyGene2,(e_x,e_y),(s_x,s_y)) #sortie du chemin le plus court sous forme de liste
	print('\033[1;32mVoici le plus court chemin :\033[1;m')
	afficheLabyrinthe(tracePath(labyGene,pointsSolution)) #affichage du labyrinthe avec le chemin le plus court affiché dedans

main() #appel de la fonction Principale
