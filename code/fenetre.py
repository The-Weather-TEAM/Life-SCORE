# -*- coding: utf-8 -*-
"""
Code Tkinter ne pas oublier quand on crée des variable de les commenter (bon nom + fonction)
réferences : 
    - Les boutons s'écrivent btn_NOM
    - Les fenêtres s'écrivent windowNOM
    - Les textes (classe Message) s'écrivent msg_NOM
    - Les listes s'écrivent list_NOM
    - Les dictionnaires s'écrivent dico_NOM
    - d'autres à venir
modif précédente : 11/12/2022 19:31
dernière modif : 12/12/2022 19:28 AAAAAAAAAA test
"""
from tkinter import *
from urllib.request import urlopen #pour les photos (peut etre enlever)
#from PIL import ImageTk, Image

global msg_principal #on pose les questions a travers lui
global list_Questions #Les valeurs de ce tableau sont les questions 
global dico_Reponses #dictionnaire de 0 et de 1 pour thor type {Q1:1,Q2,:0,Q3:0,...}(0 sera souvent un vieu/calme/fermier,...)
global n #pour faire list_Questions[n]
global btn_ok
n = 0
list_Questions = [('Vous êtes plutôt ?\nCalme                    Actif','Activité'),           #Reproduire les questions dans le même style que la première
                ('Q2','Theme2'),
                ('Q3','Theme3'),
                ('Q4','Theme4'),
                ('Q5','Theme5'),
                ('Q6','Theme6'),
                ('Q7','Theme7'),
                ('Q8','Theme8'),
                ('Q9','Theme9'),
                ('Q10','Theme10')]
dico_Reponses = {}
print(list_Questions[0])

#fonctions
#premiere page
def w_qcm(): #w pour window
    global msg_principal
    global btn_ok
    """
    affiche la premiere page qui contient donc le qcm
    """
    x = 0 #pour le boutton ok qu'on va reutiliser
    #fenêtre
    windowQCM = Tk() #fenetre de tkinter
    windowQCM.title('Accueil - QCU')
    #window.tk.call('tk::PlaceWindow', window)
    windowQCM.minsize(width=1020, height=768) #768
    #windowQCM.resizable(False,False) #Taille non modifiable !!! ON NE LE MET PAS !!!
    #widgets
    msg_principal =  Message(text="Bienvenue, nous allons commencer avec un petit test", width = 1000, font =('Bold',18), justify=CENTER) #font = taille + police justify comme sur word
    msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    #entree a utiliser peut etre ailleurs
    """entree = Entry(windowQCM,width=30, font=('Bold',18))
    entree.place(relx=0.5, rely= 0.45, anchor=CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y """
    #bouton ok
    btn_ok = Button(width=20, height=3, command=lambda: avancer(windowQCM), bg='#70add7', text="OK") #appele la fonction question1
    btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER)
    #bouton_explication
    btn_aide  = Button(width=20, height=3,command=lambda: aide(btn_aide), bg = '#f44336', text="AIDE") #Boutton d'aide
    btn_aide.place(relx=0.9, rely=0.9 ,anchor = SE)
    #affiche la photo
    #label = Label(windowQCM, image = photo)
    #label.place(x=10,y=0)



    windowQCM.mainloop() #pour fermer la fenetre

def avancer(fenetre):
    global msg_principal
    global btn_ok
    global n
    """
    Passe à la question 1 et ouvre le qcm ajoute les deux boutons <-- et -->
    
    Sinon, ouvre la seconde page
    """
    if n < len(list_Questions):
        btn_ok.place_forget() #Cache ce bouton
        btn_gauche = Button(width=20, height=3, command=lambda: plus0(btn_gauche,btn_droite), bg='#70add7', text="<---")
        btn_droite = Button(width=20, height=3, command=lambda: plus1(btn_gauche,btn_droite), bg='#70add7', text="--->")
        btn_gauche.place(relx=0.40,rely=0.5,anchor=CENTER)
        btn_droite.place(relx=0.60,rely=0.5,anchor=CENTER)
        msg_principal.config(text =f'{list_Questions[n][0]}') #change le texte du msg principal
    else:
        fenetre.destroy()
        w_question() #Ouvre la seconde fenêtre : Fin de la première

def plus0(b1,b2):
    """ajoute 0 au tableau de reponses (<---)"""
    global list_Questions
    global n
    global dico_Reponses
    global msg_principal

    n += 1
    if not est_termine(b1,b2):
        dico_Reponses[list_Questions[n-1][1]] = 0
        msg_principal.config(text = list_Questions[n][0])
    else:
        b1.destroy()
        b2.destroy()


def plus1(b1,b2):
    """ajoute 1 au tableau de reponses (--->)"""
    global list_Questions
    global n
    global dico_Reponses
    global msg_principal
    
    n += 1
    if not est_termine(b1,b2):
        dico_Reponses[list_Questions[n-1][1]] = 0
        msg_principal.config(text = list_Questions[n][0])
    else:
        b1.destroy()
        b2.destroy()

def est_termine(btn_1,btn_2):
    global msg_principal
    global btn_ok
    """
    Verifie si le QCM est terminé (dernière question répondue). Si c'est le cas, On affiche un message puis retour bouton ok 
    """
    if n >= len(list_Questions):
        btn_1.destroy()
        btn_2.destroy()
        btn_ok.place(relx=0.5,rely=0.5,anchor =CENTER)
        msg_principal.config(text = "Merci d'avoir répondu aux questions, Veuillez continuer")
        return True

def aide(btn):

    """
    Ouvre Une fenêtre d'aide avec un texte et peut être des graphismes
    """
    texte_aide="""
    Bonjour ! Voilà notre protoype de CityScore où vous pourrez regarder le score de villes.

Pour commencer, nous réalisons un QCM de 10 questions pour voir vos préférences.


Pour chaque critère, on définit une note sur 100 ainsi qu'un coefficient qui est de base 1. 
Le plus de critères sont réunis afin d'avoir le plus de précision possible. Ils sont répartis en 4 catégories :

Le climat (pluie en un an / pollution de l'air / températures / vent / ...)
La qualité de vie (activités / patrimoine / ville fleurie / ...)
Le prix (essence / gaz / loyer / prix de la vie / salaire moyen / ...)
La sécurité (taux d'accidents / vols / risques / ...)
"""
    btn.destroy() #TROUVER UNE MEILLEURE SOLUTION
    windowAide = Tk() #fenetre de tkinter
    windowAide.title('Page 1bis - Aide')
    #window.tk.call('tk::PlaceWindow', window) A VOIR PEUT ETRE (PLACEMENT AU CENTRE ?)
    windowAide.minsize(width=int(510*4/3), height=384) #768
    windowAide.resizable(False,False) #Taille non modifiable !!! ON NE LE MET PAS !!!
    print(texte_aide)
    msg_aide = Message(windowAide, text=texte_aide, width = 1000, font =('Bold',10), justify=CENTER)
    msg_aide.place(relx = 0.5, rely = 0.3, anchor = CENTER)
    btn_compris = Button(windowAide, width=20, height=3, command=windowAide.destroy, bg='#B9F7D0', text="Compris !")
    btn_compris.place(relx = 0.5, rely = 0.7, anchor = CENTER)

    windowAide.mainloop()
    return windowAide

#seconde page
def w_question():
    """
    affiche la seconde page qui contient la requête de la ville
    """
    windowQuestion = Tk() #fenetre de tkinter
    windowQuestion.title('Seconde page - requête de la ville')
    #window.tk.call('tk::PlaceWindow', window)
    windowQuestion.minsize(width=1020, height=768)
    windowQuestion.resizable(False,False) #Taille non modifiable


    windowQuestion.mainloop()



#troisieme page
def w_score():
    """
    affiche la dernière page qui contient le score et le bouton pour revenir
    """
    pass


"""
#Image en url bitmap ?
URL = "https://avatars.githubusercontent.com/u/119951824?s=200&v=4"
u = urlopen(URL)
raw_data = u.read()
u.close()
"""









# Create an object of tkinter ImageTk
# photo = ImageTk.PhotoImage(data=raw_data) # <-----



# appel de la fonction de la première page
w_qcm()

print(n,dico_Reponses,msg_principal)
