###################################################################
# Nom du programme: Tetreecs                        # # # #       #
#                                               #         #   #   #
# Auteurs: Jouault Jilian, Subsol Thomas        # #           #   #
#                                               #         #   #   #
# Licence:                                          # # # #       #
###################################################################

###################################################################
# Importation des fonctions externes:

import os
import winsound
import time
from tkinter import *
from random import choice, randint
import figures
import tkinter.font as tkFont

###################################################################
# Corps du programme principal:

root = Tk()
L = 11 # Largeur (en cases)
H = 23 # Hauteur (en cases)
SIZE = 28 # Taille d'une case
results = 0
position = 0
En_Pause = False

police1 = tkFont.Font(family='Impact', size=60)
police2 = tkFont.Font(family='Impact', size=40)

# Chargement des images du jeu

son1=PhotoImage(file="images/son_off.gif")
son2=PhotoImage(file="images/son_on.gif")
play=PhotoImage(file="images/jouer.gif")
playagain=PhotoImage(file="images/rejouer.gif")
stop=PhotoImage(file="images/quitter.gif")
logo=PhotoImage(file="images/logo.gif")
commands=PhotoImage(file="images/commandes.gif")
R=PhotoImage(file="images/cuberouge.gif")
J=PhotoImage(file="images/cubejaune.gif")
B=PhotoImage(file="images/cubebleu.gif")
V=PhotoImage(file="images/cubevert.gif")
Vi=PhotoImage(file="images/cubeviolet.gif")
C=PhotoImage(file="images/cubecristal.gif")
M=PhotoImage(file="images/cubemechant.gif")
A=PhotoImage(file="images/cubeamour.gif")
IMAGES = R, J, B, V, Vi, C, M, A

# Création de l'interface graphique
root.attributes("-fullscreen", 1)
root.title("Tetreecs 10.0")
root.configure(bg="white")
canvas1 = Canvas(root, width=375, height=750, bg="white", highlightthickness=0)
canvas1.grid(row=0, column=0)
canvas1.create_image(183, 375, image=logo)

largeur = L * SIZE
hauteur = H * SIZE
canvas = Canvas(root, width=largeur, height=hauteur, bg="#000040")
canvas.grid(row=0, column=1)

canvas2 = Canvas(root, width=700, height=750, bg="white", highlightthickness=0)
canvas2.grid(row=0, column=2)
canvas2.create_image(350, 225, image=commands)
activer_son = canvas2.create_image(350, 480, image=son1)

# Tableau des scores
results = IntVar()
widget1 = Label(canvas2, text='Score :',font=police1, bg="white")
widget2 = Label(canvas2, textvariable=results, font=police1, bg="white")
canvas2.create_window(250, 650, window=widget1)
canvas2.create_window(550, 650, window=widget2)

# Initialisation de variables métier
nbFormes=len(figures.piece)-1
Forme=randint(0,nbFormes)
coord_x=6*SIZE
coord_y=-(figures.piece[Forme][position][2][0][1]+0.5)*SIZE

###################################################################
# Définition des fonctions locales:

# Création du carré 
def create_square(image, x, y, types):
    canvas.create_image(x, y, image = image, tag = types) # Création du carré
    

# Création d'une figure
def create_figure(figure, image, types):
    for i in figure:
        create_square(image, coord_x+i[0]*SIZE, coord_y+i[1]*SIZE, types)

def test_deplacement(figure):
    global coord_x, coord_y
    superposition=0
    debordement=False
    for i in figure:
        superposition+=len(canvas.find_overlapping(coord_x+i[0]*SIZE,coord_y+i[1]*SIZE,coord_x+i[0]*SIZE,coord_y+i[1]*SIZE))
        debordement=debordement or (coord_x+i[0]*SIZE<SIZE or coord_x+i[0]*SIZE>largeur-SIZE or coord_y+i[1]*SIZE>hauteur)
    return superposition==0 and not(debordement)

# Suppression des lignes complètes
def suppr_ligne():
    Ligne=1
    Coef=1

    # Tant que l'on n'a pas atteint une ligne vide en remontant à partir du bas:
    while len(canvas.find_overlapping(SIZE, hauteur-Ligne*SIZE+1, largeur-SIZE, hauteur-(Ligne-1)*SIZE-1))!=0:
        # Si la ligne est complète
        if len(canvas.find_overlapping(SIZE, hauteur-Ligne*SIZE+1, largeur-SIZE, hauteur-(Ligne-1)*SIZE-1))==10:
            # Suppression de la ligne
            canvas.addtag_overlapping('ligne', SIZE, hauteur-Ligne*SIZE+1, largeur-SIZE, hauteur-(Ligne-1)*SIZE-1) 
            canvas.delete('ligne')
            # Descendre les lignes du dessus d'une ligne
            canvas.addtag_overlapping('bloc2', SIZE, 0, largeur-SIZE, hauteur-Ligne*SIZE-1)
            canvas.move('bloc2', 0, SIZE)
            canvas.dtag('bloc2')
            canvas.addtag_overlapping('bloc', SIZE, 0, largeur-SIZE, hauteur)
            # Incrémente le score du nombre de lignes supprimées
            results.set(results.get() + 1*Coef)
            Coef+=1
        else:
            Ligne+=1
    
# Déplacement de la figure
def do_move():
    global encore_do_move
    global coord_x
    global coord_y
    global position
    global nbFormes, Forme
    global image
    global En_Pause

    delay=1000-results.get()*50
    if delay<100:
        delay=100
    encore_do_move = True

    # Si le jeu n'est pas en pause
    if not(En_Pause):
        image=canvas.itemcget('figure','image')
        # Si arrivée en bas ou figure en dessous alors:
        if test_deplacement(figures.piece[Forme][position][2])==False: 
            # Fige la figure active
            create_figure(figures.piece[Forme][position][1], image, 'bloc')
            canvas.delete('figure') # Fait disparaitre la figure qui descendait
            if coord_y<SIZE/2: # Si la figure se trouve tout en haut
               # Fin de la partie
                encore_do_move = False # Arrêt du programme
                menu2()
            else:
                suppr_ligne()
        
            # Créer une nouvelle figure mobile
            position=0
            Forme=randint(0,nbFormes)
            coord_x=6*SIZE
            coord_y=-(figures.piece[Forme][position][2][0][1]+0.5)*SIZE
            image = choice(IMAGES)
            create_figure(figures.piece[Forme][position][1], image, 'figure')
        # Sinon
        else:
            canvas.move('figure', 0, SIZE)
            coord_y+=SIZE

    # Si relance possible alors
    if encore_do_move:
        # Répète l'action do_move après un délai en ms
        root.after(delay, do_move)


def gauche(event):
    global coord_x
    global position
    global encore_do_move
    global En_Pause
    # Forme globale
    if test_deplacement(figures.piece[Forme][position][3]) and encore_do_move==True and not(En_Pause):
        canvas.move('figure', -SIZE, 0) # Déplacement à gauche
        coord_x-=SIZE
        

def droite(event):
    global coord_x
    global position
    global Forme
    global En_Pause
    if test_deplacement(figures.piece[Forme][position][4]) and encore_do_move==True and not(En_Pause):
        canvas.move('figure', SIZE, 0) # Déplacement à droite
        coord_x+=SIZE

def bas(event):
    global coord_y
    global position
    global Forme
    global En_Pause
    if test_deplacement(figures.piece[Forme][position][2]) and encore_do_move==True and not(En_Pause):
        canvas.move('figure', 0, SIZE) # Déplacement vers le bas
        coord_y+=SIZE

def rotation(event):
    global position
    global image
    global Forme
    global En_Pause
    if test_deplacement(figures.piece[Forme][position][0]) and encore_do_move==True and not(En_Pause):
        canvas.delete('figure')
        position = (position+1)%4
        create_figure(figures.piece[Forme][position][1], image, 'figure')

def sortie(event):
    winsound.PlaySound(None,0)
    root.destroy()

def music_on(event):
    global desactiver_son
    canvas2.delete(activer_son)
    desactiver_son = canvas2.create_image(350, 480, image=son2)
    canvas2.tag_bind(desactiver_son,'<1>',music_off)
    winsound.PlaySound("images/tetris_origin.wav",winsound.SND_ASYNC | winsound.SND_LOOP)

def music_off(event):
    global activer_son
    canvas2.delete(desactiver_son)
    activer_son = canvas2.create_image(350, 480, image=son1)
    canvas2.tag_bind(activer_son,'<1>',music_on)
    winsound.PlaySound(None,0)

def lancement():
    image = choice(IMAGES)
    create_figure(figures.piece[Forme][position][1], image, 'figure')
    canvas.create_rectangle(0, 0, 13, 644, fill="black")
    canvas.create_rectangle(294, 0, 308, 644, fill="black")
    do_move()

def demarrer(event):
    canvas.delete(jouer)
    canvas.delete(quitter)
    lancement()

def redemarrer(event):
    jeu = 'tetreecs_v10.0.py'
    os.system(jeu)
    winsound.PlaySound(None,0)
    root.destroy()

def menu():
    global jouer
    global quitter
    jouer = canvas.create_image(154, 154, image=play)
    canvas.tag_bind(jouer,'<1>',demarrer)
    quitter = (canvas).create_image(154, 466, image=stop)
    canvas.tag_bind(quitter,'<1>',sortie)

def menu2():
    global rejouer
    global quitter
    global finPartie
    finPartie = canvas.create_text(154, 150, text="GAME OVER", fill="white", font=police2)
    rejouer = canvas.create_image(154, 275, image=playagain)
    canvas.tag_bind(rejouer,'<1>',redemarrer)
    quitter = (canvas).create_image(154, 450, image=stop)
    canvas.tag_bind(quitter,'<1>',sortie)

def menu_pause(event):
    global En_Pause
    # Passer du mode Jeu au mode Pause et réciproquement
    En_Pause = not(En_Pause)

# Association des touches aux commandes
root.bind("<Left>", gauche)
root.bind("<Right>", droite)
root.bind('<Down>', bas)
root.bind("<Up>", rotation)
root.bind('<Escape>', sortie)
root.bind("<space>", menu_pause)
canvas2.tag_bind(activer_son,'<1>',music_on)

# Affichage du menu
menu()
root.mainloop()
