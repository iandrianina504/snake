from fltk import *
from time import sleep
from random import randint

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases

obstacle = True

def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la
	forme d'un couple d'entiers (id_colonne, id_ligne) et renvoyant les
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul
	prend en compte la taille de chaque case, donnée par la variable
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case

def affiche_pommes(pommes):
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen')

def affiche_serpent(serpent):
    for case_serpent in serpent:
        x, y = case_vers_pixel(case_serpent)
        cercle(x, y, taille_case/2 + 1,
           couleur='darkgreen', remplissage='green')



def ajout_pommes(pommes, largeur_plateau, hauteur_plateau):
    """
	Fonction recevant les coordonnées aléatoire d'une pomme sous la
	forme d'un couple d'entiers (id_colonne, id_ligne) et renvoyant
	ces coordonnées.
    """
    pomme = (0,0)
    x = randint(0, largeur_plateau-1)
    y = randint(0, hauteur_plateau-1)
    pomme= (x, y)
    pommes.append(pomme)
    return (pommes)


def change_direction(direction, touche):
    """
	Fonction recevant les directions sous la forme d'un couple d'entiers
	(id_colonne, id_ligne) possibles du serpent.
    """
    if touche == 'Up':
            # flèche haut pressée
        return (0, -1)
    elif touche == 'Down':
        return (0, 1)
    elif touche == 'Left':
        return(-1, 0)
    elif touche == 'Right':
        return(1, 0)
    else:
        # pas de changement !
        return direction


def bouge_serpent(serpent, direction):
    """
	Fonction recevant les coordonnées de l'élement à l'indice 0
	de la liste serpent, qui permettra d'ajouter aux coordonnées
	du serpent les coordonnées de sa direction.

    """
    nouveau_serpent = [(0,0)]*(len(serpent))
    x, y = serpent[0]
    x_direction, y_direction = direction
    nouveau_serpent[0] = (x + x_direction, y + y_direction)
    for i in range(1, len(serpent)):
        nouveau_serpent[i]=serpent[i-1]
    return(nouveau_serpent)



def serpent_touche_pas_bords(serpent, direction,
    largeur_plateau, hauteur_plateau):
    x, y = serpent[0]
    x_direction, y_direction = direction
    x1, y1 = (x + x_direction, y + y_direction)

    return (0 <= x1 < largeur_plateau and 0 <= y1 < hauteur_plateau)


def serpent_se_mange(serpent):
    reponse = False
    for i in range(len(serpent)-1):
        for j in range(i+1, len(serpent)):
            if serpent[i]==serpent[j]:
                reponse = True
    return(reponse)


# programme principal
if __name__ == "__main__":
        Bouton_JOUER = [(150,50),(450,150)]
        Bouton_QUITTER = [(150,200),(450,300)]
        cree_fenetre(taille_case * largeur_plateau,
                     taille_case * hauteur_plateau)
         #le bouton jouer
        rectangle(Bouton_JOUER[0][0], Bouton_JOUER[0][1], Bouton_JOUER[1][0], Bouton_JOUER[1][1],\
                  couleur='black', remplissage='pink', epaisseur=1, tag='menu')
        texte((Bouton_JOUER[0][0]+Bouton_JOUER[1][0])/2,(Bouton_JOUER[0][1]+Bouton_JOUER[1][1])/2,\
              "Jouer",tag='menu')
        rectangle(Bouton_QUITTER[0][0], Bouton_QUITTER[0][1], Bouton_QUITTER[1][0], Bouton_QUITTER[1][1],\
                  couleur='black', remplissage='green', epaisseur=1, tag='menu')
        texte((Bouton_QUITTER[0][0]+Bouton_QUITTER[1][0])/2,(Bouton_QUITTER[0][1]+Bouton_QUITTER[1][1])/2,\
              "Quitter",tag='menu')
while True: #TANT QU'UN BOUTON N'A PAS ÉTÉ PRESSÉ
            clic = attend_clic_gauche()
            if Bouton_JOUER[0][0] <= clic[0] and clic[0] <= Bouton_JOUER[1][0] and \
               Bouton_JOUER[0][1] <= clic[1] and clic[1] <= Bouton_JOUER[1][1]:
                efface_tout()
                break

            elif Bouton_QUITTER[0][0] <= clic[0] and clic[0] <= Bouton_QUITTER[1][0] and \
               Bouton_QUITTER[0][1] <= clic[1] and clic[1] <= Bouton_QUITTER[1][1]:
                ferme_fenetre()
                break

    # initialisation du jeu
framerate = 10    # taux de rafraîchissement du jeu en images/s
direction = (0, 0)  # direction initiale du serpent
pommes = [] # liste des coordonnées des cases contenant des pommes
nb_pommes_max = 5 # le nombre de pommes maximal qui doit être affiché à l'écran
serpent = [(0, 0)]# liste des coordonnées de cases adjacentes décrivant le serpent

texte(130, 200, "Press 2 Start", taille = 35, couleur = 'black', tag = "début")
mise_a_jour()
attend_ev()
    # boucle principale
jouer = True
cmpt=0
SPEEDY = True
while jouer:
        # affichage des objets
        efface_tout()
        if randint(1,1000)<50 and len(pommes)<nb_pommes_max:
            pommes = ajout_pommes(pommes, largeur_plateau, hauteur_plateau)

        affiche_pommes(pommes)
        affiche_serpent(serpent)


        texte(500, 5, f"Score: {len(serpent)-1}", taille = 15, couleur = 'black', tag = "score")
        mise_a_jour()

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':
            direction = change_direction(direction, touche(ev))
            
        else:
            if serpent_touche_pas_bords(serpent, direction,
                largeur_plateau, hauteur_plateau)== True :
                serpent = bouge_serpent(serpent, direction)
                if serpent_se_mange(serpent) == True :
                    jouer = False
            else :
                jouer = False

            for pomme in pommes:
                if pomme == serpent[0]:
                    # ajouter les coordonnées de la pomme à la liste serpent à la dernière position
                    serpent.append(pomme)
                    # la pomme mangée disparait
                    pommes.remove(pomme)
        
        # attente avant rafraîchissement
        sleep(1/framerate)

    #fermeture et sortie
ferme_fenetre()

