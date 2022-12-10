# -*- coding: utf-8 -*-
"""
Code Tkinter ne pas oublier quand on crée des variable de les commenter (bon nom + fonction)
réferences : 
    - Les boutons s'écrivent btn_NOM
    - Les fenêtres s'écrivent windowNOM
    - Les textes (classe Message) s'écrivent msg_NOM
    - d'autres à venir

modif précédente : 08/12/2022 15:48
dernière modif : 10/12/2022 19:11
"""
from tkinter import *
from urllib.request import urlopen
#from PIL import ImageTk, Image

global msg_principal #on pose les questions a travers lui



#fonctions
#premiere page
def w_qcm(): #w pour window
    global msg_principal
    """
    affiche la premiere page qui contient donc le qcm
    """
    #fenêtre
    windowQCM = Tk() #fenetre de tkinter
    windowQCM.title('Accueil - QCU')
    #window.tk.call('tk::PlaceWindow', window)
    windowQCM.minsize(width=1020, height=768)
    windowQCM.resizable(False,False) #Taille non modifiable
    #widgets
    msg_principal =  Message(text="Bienvenue, nous allons commencer avec un petit test", width = 1000, font =('Bold',18), justify=CENTER) #font = taille + police justify comme sur word
    msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    #entree a utiliser peut etre ailleurs
    """entree = Entry(windowQCM,width=30, font=('Bold',18))
    entree.place(relx=0.5, rely= 0.45, anchor=CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y """
    #bouton ok
    btn_ok = Button(width=20, height=3, command=lambda: question1(windowQCM,btn_ok), bg='#70add7', text="OK") #appele la fonction question1
    btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER)
    
    #affiche la photo
    #label = Label(windowQCM, image = photo)
    #label.place(x=10,y=0)



    windowQCM.mainloop() #pour fermer la fenetre

def question1(fenetre,boutton):
    global msg_principal
    """
    Passe à la question 1 et ouvre le qcm ajoute les deux boutons <-- et -->
    """
    boutton.destroy() #supprime ce bouton
    btn_gauche = Button(width=20, height=3, command=lambda: print(), bg='#70add7', text="<---")
    btn_droite = Button(width=20, height=3, command=lambda: print(), bg='#70add7', text="--->")
    btn_gauche.place(relx=0.40,rely=0.5,anchor=CENTER)
    btn_droite.place(relx=0.60,rely=0.5,anchor=CENTER)
    msg_principal.config(text ="Vous êtes plutôt ?\nCalme                    Actif") #change le texte du msg principal



#seconde page
def w_question():
    """
    affiche la seconde page qui contient la requête de la ville
    """
    pass


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


