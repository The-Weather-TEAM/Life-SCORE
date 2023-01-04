"""
Code Tkinter ne pas oublier quand on crée des variable de les commenter (bon nom + fonction)
réferences : 
    - Les boutons s'écrivent btn_NOM
    - Les fenêtres s'écrivent windowNOM
    - Les textes (classe Message) s'écrivent msg_NOM
    - Les listes s'écrivent list_NOM
    - Les dictionnaires s'écrivent dico_NOM
    - Les url de csv ou d'API s'écrivent url_csv_NOM ou url_api_NOM


"""



from tkinter import *
#from urllib.request import urlopen #pour les photos (peut etre enlever)
from classes import * #Import de nos classes créées

import requests
from requests.exceptions import ConnectionError #Pas sûr de l'utilité là

#from PIL import ImageTk, Image #Pour l'esthétique

global msg_principal #on pose les questions a travers lui
global list_Questions #Les valeurs de ce tableau sont les questions 
#global list_alternative #Les valeurs de ce tableau sont les questions alternatives (ex pour ne pas demander à un sextagénère s'il est étudiant)
global dico_Reponses #dictionnaire de 0 et de 1 pour thor type {Q1:1,Q2,:0,Q3:0,...}(0 sera souvent un vieu/calme/fermier,...)
global n #pour faire list_Questions[n]
global btn_ok #Boutton qui continue (est utilisé plusieurs fois d'où la variable globale 
global Donnees_ville #Ce que l'on va traiter grâce aux autres fichiers

n = 0
list_Questions = [('Aimez vous sortir en ville ?','Activite'),           #Reproduire les questions dans le même style que la première
                ('Avez vous moins de 30 ans ?','Age'),
                ('Etes vous etudiant ?','Scolarite'), #Change pour  X si personne = vieille                
                ('Avez vous\Vivez vous avec des enfants ?','Famille'),
                ('La culture a-t-elle une place importante pour vous ?','Culture'),
                ('préférez vous la campagne à la ville ?','citadin'),                               # 4 dernières questions sont a revoir ducoup
                ('Avez vous un travail ?','Travail'),
                ("Etes vous en recherche d'emploi ?","Cherche_Emploi")]

dico_Reponses = {} #Traité dans coefficients.py


'''
fonctions
'''

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
    windowQCM.minsize(width=768, height=500) #768 = taille minimum de la fenetre
    windowQCM.state('zoomed')

    #widgets
    msg_principal =  Message(text="Bienvenue, nous allons commencer avec un petit test", width = 1000, font =('Bold',18), justify=CENTER) #font = taille + police justify comme sur word
    msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    
    #boutons 
    
    #bouton_explication
    btn_aide  = Button(width=20, height=3,command=lambda: aide(btn_aide,windowQCM), bg = '#f44336', text="AIDE") #Bouton d'aide
    btn_aide.place(relx=0.9, rely=0.9 ,anchor = SE)
    #bouton ok Qui continue après le premier message
    btn_ok = Button(width=20, height=3, command=lambda: avancer(windowQCM,btn_aide), bg='#70add7', text="OK") #appele la fonction question1
    btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) #place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place
    
    #affiche la photo
    #label = Label(windowQCM, image = photo)
    #label.place(x=10,y=0)

    windowQCM.mainloop() #pour fermer la fenetre



def avancer(fenetre,bouton): # bouton est le bouton d'aide qui disparait après le premier passage
    global msg_principal
    global btn_ok
    global n #n prend +1 a chaque questions
    """
    Passe à la question 1 et ouvre le qcm ajoute les deux boutons Non et Oui
    
    Si le qcm est terminé, ouvre la seconde page
    """
    if n == 0:
        bouton.destroy()
    if n < len(list_Questions):
        btn_ok.place_forget() #Cache ce bouton
        btn_gauche = Button(width=20, height=3, command=lambda: plus0(btn_gauche,btn_droite), bg='#70add7', text="Non")
        btn_droite = Button(width=20, height=3, command=lambda: plus1(btn_gauche,btn_droite), bg='#70add7', text="Oui")
        btn_gauche.place(relx=0.40,rely=0.5,anchor=CENTER)
        btn_droite.place(relx=0.60,rely=0.5,anchor=CENTER)
        msg_principal.config(text =f'{list_Questions[n][0]}') #change le texte du msg principal pour la question suivante

    else:
        fenetre.destroy() #ferme la fenetre
        w_question() #Ouvre la seconde fenêtre : Fin de la première

def plus0(b1,b2):
    """ajoute 0 au dico de reponses (Non)"""
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
    """ajoute 1 au dico de reponses (Oui)"""
    global list_Questions
    global n
    global dico_Reponses
    global msg_principal
    
    n += 1
    if not est_termine(b1,b2):
        dico_Reponses[list_Questions[n-1][1]] = 1
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

def aide(btn,fenetre):

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
    fenetre.destroy()
    windowAide = Tk() #fenetre de tkinter
    windowAide.title('Page 1bis - Aide')
    #window.tk.call('tk::PlaceWindow', window) A VOIR PEUT ETRE (PLACEMENT AU CENTRE ?)
    windowAide.minsize(width=int(510*4/3), height=384) #768
    windowAide.resizable(False,False) #Taille non modifiable !!! ON NE LE MET PAS !!!
    msg_aide = Message(windowAide, text=texte_aide, width = 1000, font =('Bold',10), justify=CENTER)
    msg_aide.place(relx = 0.5, rely = 0.3, anchor = CENTER)
    btn_compris = Button(windowAide, width=20, height=3, command=lambda:retour_pages(windowAide,"page1"), bg='#B9F7D0', text="Compris !")
    btn_compris.place(relx = 0.5, rely = 0.7, anchor = CENTER)

    windowAide.mainloop()
    return windowAide


def retour_pages(window,string):
    """
    Fonction qui passe de la page actielle à la page N°x
    """
    global dico_Reponses #Au cas où que quelquechose soit dedans on va le reset
    window.destroy()
    if string == "page1" : #si on veut accéder à la page 1
        dico_Reponses = {}
        w_qcm()
    elif string == "page2" :
        w_question()




#seconde page
def w_question():
    """
    affiche la seconde page qui contient la requête de la ville
    """
    windowQuestion = Tk() #fenetre de tkinter
    windowQuestion.title('Seconde page - requête de la ville')
    windowQuestion.minsize(width=768, height=500)
    windowQuestion.state('zoomed') #Plein écran

    #input
    entree = Entry(windowQuestion,cursor = 'Pencil', font = ('Bold',18))
    entree.place(relx=0.5, rely= 0.55, anchor=CENTER)
    
    #message
    msg_ville= Message(text="Veuillez saisir la ville recherchée", width = 1000, font =('Bold',18), justify=CENTER) #font = taille + police, justify comme sur word
    msg_ville.place(relx= 0.5, rely=0.45, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 

    btn_arrondissement = Button(width=20, height=3,command=lambda: arrondissement(windowQuestion), bg = '#f44336', text="AIDE\nARRONDISSEMENTS") #Boutton d'aide arrondissements
    btn_arrondissement.place(relx=0.94, rely=0.9 ,anchor = SE)
    
    #test_connexion(msg_ville) #Petit problème si ya pas de connection ça empêche le démarrage de l'application


    '''
    #Nathan : le test_connexion c'est la fonction pour tester si il y a internet ? Si oui tu peux utiliser :

    import classes as i
    connexion = i.Internet('https://www.data.gouv.fr') #ou un autre site
    if connexion.is_connected() :
        #blabla
        
    #ça retourne une valeur booléenne ducoup ça bloque plus le programme si t'es pas co c'est à toi de décider

    '''






    #Boutton
    btn_entree = Button(windowQuestion,width=20, height=3, command=lambda: ville(entree,msg_ville,windowQuestion), bg='#B9F7D0', text="Recherche")
    btn_entree.place(relx=0.5, rely= 0.65, anchor = CENTER)

    #windowQuestion.bind('KP_Return',ville(entree,msg_ville,windowQuestion)) #Appuyer sur entrée revient à appuyer sur le Bouton NE MARCHE PAS!


    windowQuestion.mainloop()


def arrondissement(window):

    """
    Ouvre Une fenêtre d'aide avec un texte et peut être des graphismes
    """
    texte_aide="""
    Si Votre ville possède plusieurs arrondissemnts (ex : Paris) :
    - Si vous saisissez uniquement le nom de la ville, le premier arrondissement sera pris comme base
    - Sinon, écrivez le nom de la ville comme cela : Nom_X avec X le numéro de l'arrondissement (ex : Paris_7)"""
    window.destroy()
    windowAide = Tk() #fenetre de tkinter
    windowAide.title('Page 2bis - Aide')
    #window.tk.call('tk::PlaceWindow', window) A VOIR PEUT ETRE (PLACEMENT AU CENTRE ?)
    windowAide.minsize(width=int(690*4/3), height=384) #768
    #windowAide.resizable(False,False) #Taille non modifiable !!! ON NE LE MET PAS !!!
    msg_aide = Message(windowAide, text=texte_aide, width = 1000, font =('Bold',14))
    msg_aide.place(relx = 0.5, rely = 0.3, anchor = CENTER)
    btn_compris = Button(windowAide, width=20, height=3, command=lambda :retour_pages(windowAide,"page2"), bg='#B9F7D0', text="Compris !")
    btn_compris.place(relx = 0.5, rely = 0.7, anchor = CENTER)

    windowAide.mainloop()
    return windowAide


def ville(entree,msg,fenetre):
    """
    Récupère l'entrée, vérifie si la ville existe bien:
        -Si oui, continue vers la page 3
        -Si non, affiche un message d'erreur
    """
    global Donnees_ville
    ville = entree.get()
    print(ville)
    Donnees_ville = Donnees(ville)
    if Donnees_ville.is_commune_france_v2(msg): #Je dois ajouter Code/ au début car vscode lance mal le fichier sinon ça va
        msg.config(text = "Veuillez patienter ...")
        #FAIRE TOUS LES CALCULS ICI :
        #ON OUVRE LA TROISIEME PAGE QU'APRES AVOIR FAIT TOUS LES CALCULS
        fenetre.destroy()
        w_score(ville)
    else:
        msg.config(text = "Erreur : La ville choisie n'est pas dans notre base de donnée")





#troisieme page
def w_score(ville):
    """
    affiche la dernière page qui contient le score et le bouton pour revenir
    """
    windowScore = Tk() #fenetre de tkinter
    windowScore.title('Dernière page - Note de la ville')
    windowScore.minsize(width=1000, height=600)
    windowScore.state('zoomed') #Plein écran

    #Donnees PROVISOIRES !!!
    dico = {'Atout 1':9,'Atout 2':10,'Atout 3':5,'Atout 4':7,'Inconvéniant 1':-2,'Atout 5':4,'Inconvéniant 2':-1,'Inconvéniant 3':-2,'Inconvéniant 4':-1,'Inconvéniant (':-1} #Exemple
    score = int(Donnees_ville.note_finale()) #Provisoire
    bonus,malus = trouve_bonus(dico), trouve_malus(dico) #Fonction non terminée (besoin du fichier qui fait les données)



    #Transfo des données en texte
    msg_ville = Message(windowScore,text=ville.capitalize(), width = 1000, font =('Bold',30), justify=CENTER)
    msg_ville.place(relx=0.5,rely=0.1,anchor=N)
    plus, moins = plus_et_moins(bonus,malus) # Récupère les données et les transforme en 2 str à Afficher
    print(plus,moins)


    couleur= couleur_score(score)
    score = str(score)

    #Textes :
    msg_note = Message(windowScore, text=f'Note : \n' +score +'  ' , width = 1000,fg =couleur, font =('Franklin gothic medium',40), justify=CENTER)
    msg_note.place(relx=0.95,rely=0.05, anchor=NE)#Nord Est
    msg_bonus = Message(windowScore,text=plus, width = 1000, font =('Bold',30), justify=LEFT)
    msg_malus = Message(windowScore,text=moins, width = 1000, font =('Bold',30), justify=LEFT)
    msg_bonus.place(relx = 0, rely = 0.5)
    msg_malus.place(relx=0.7,rely=0.5)


    #Bouton retour
    btn_Retour = Button(windowScore, width=20, height=3, command=lambda:retour_pages(windowScore,"page2"), bg='#B9F7D0', text= "Noter une autre ville", font=('Bold',20))
    btn_Retour.place(relx = 0.5,rely = 0.7, anchor = CENTER)




    windowScore.mainloop()


def trouve_bonus(dic):
    """
    Prend les 5 meilleurs aspects de la ville pour mettre des plus à y habiter
    """
    
    bonus_list= []
    for i in range(5):
        maxi = 0
        for cle in dic.keys():
            if dic[cle] > maxi:
                maxi = dic[cle]
                cle_maxi = cle
        bonus_list.append(cle_maxi)
        dic.pop(cle_maxi,None)

    return bonus_list


def trouve_malus(dic):
    """
    Prend les 5 pires aspects de la ville pour mettre des inconvénients à y habiter
    """
 
    malus_list= []
    for i in range(5):
        mini = 0 # REQUIERT QUE LES MALUS SOIENT EN NEGATIF !!!
        for cle in dic.keys():
            if dic[cle] < mini:
                mini = dic[cle]
                cle_mini = cle
        malus_list.append(cle_mini)
        dic.pop(cle_mini,None)

    return malus_list

def plus_et_moins(pl,mal):
    """
    Fonction qui transforme en Str formaté les plus et les moins
    """
    plus, moins = "Les Avantages : ", "Les Inconvénients :" #texte a retourner
    for val_plus in pl:
        plus += f"\n - {val_plus} "
    for val_moins in mal:
        moins += f"\n - {val_moins} "

    return plus,moins

def couleur_score(n):
    """
    Choisit une couleur en fonction du chiffre obtenu (de 0 à 100) et la retourne en RGB
    """
    #A RETRAVAILLER PEUT ETRE METTRE UN PEU PLUS DE BLEU
    couleur = (255,0,127)
    rouge = 255 - int(n*255/100)
    vert = 0 + int(n*255/100)
    print(rouge,vert)
    couleur = (rouge,vert,100)

    rgb = '#' + ''.join(f'{i:02X}' for i in couleur)




    return rgb


"""
#Image en url bitmap ? TEST D'IMAGE 
URL = "https://avatars.githubusercontent.com/u/119951824?s=200&v=4"
u = urlopen(URL)
raw_data = u.read()
u.close()
"""





# Create an object of tkinter ImageTk
# photo = ImageTk.PhotoImage(data=raw_data) # <-----



# appel de la fonction de la première page
#w_qcm() #ligne  à lancer a la fin

#Lignes pour accéder à différentes page directement
w_question() 
#w_score('Paris')
#print(n,dico_Reponses,msg_principal)
