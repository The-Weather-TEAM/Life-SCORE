# -*- coding: utf-8 -*-
"""
Code Tkinter ne pas oublier quand on crée des variable de les commenter (bon nom + fonction)

modif précédente : 07/12/2022 10:58
dernière modif : 08/12/2022 15:48
"""
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image

#fonctions
"""fonction pour ouvrir la fenetre d'accueil"""







#Image en url bitmap ?
URL = "https://avatars.githubusercontent.com/u/119951824?s=200&v=4"
u = urlopen(URL)
raw_data = u.read()
u.close()








#fenêtre
windowQCM = Tk() #fenetre de tkinter
windowQCM.title('Accueil - QCU')
#window.tk.call('tk::PlaceWindow', window)
windowQCM.minsize(width=1020, height=768)
windowQCM.resizable(False,False) #Taille non modifiable

# Create an object of tkinter ImageTk
photo = ImageTk.PhotoImage(data=raw_data) # <-----



"""appel de la fonction pour la première"""

#Plusieurs Bouttons 
#affiche la photo
label = Label(windowQCM, image = photo)
label.place(x=10,y=0)

windowQCM.mainloop() #pour fermer la fenetre
