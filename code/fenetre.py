# -*- coding: utf-8 -*-
"""
Code Tkinter ne pas oublier quand on crée des variable de les commenter (bon nom + fonction)
réferences : 
    - Les boutons s'écrivent btn_NOM
    - Les fenêtres s'écrivent windowNOM
    - Les textes (classe Message) s'écrivent msg_NOM
    - Les listes s'écrivent list_NOM
    - Les dictionnaires s'écrivent dico_NOM
    - Les url de csv ou d'API s'écrivent url_csv_NOM ou url_api_NOM

modif précédente : 11/12/2022 19:31
dernière modif : 12/12/2022 19:28  #Est-ce qu'on le garde ça ? meme moi j'oublie de le changer mdr - Raf
"""
from tkinter import *
from urllib.request import urlopen #pour les photos (peut etre enlever)
from recup_meteo_classe import *

import requests
from requests.exceptions import ConnectionError #Pas sûr de l'utilité là


import csv

'''
FICHIERS CSV (importés d'internet à chaque appel du fichier) 
'''

url_csv_Communes = 'https://sql.sh/ressources/sql-villes-france/villes_france.csv'
""" CODE DE TEST AUSSI POUR IMPMENTATION DU TECHARGEMENT (je sais pas quoi faire avec mdrr) - Raf
with requests.get(url_csv_Communes, stream=True) as r:
    lines = (line.decode('utf-8') for line in r.iter_lines())
    for a in csv.reader(lines):

        if 'Puissalicon' in a :
            print('oui',type(a))
"""

""" CODE TEST SUJET A MODIFICATION
with requests.Session() as s: #Importe les fichiers csv 
    s.post(url, data=payload)
    download = s.get('url that directly download a csv report')
"""

#from PIL import ImageTk, Image

global msg_principal #on pose les questions a travers lui
global list_Questions #Les valeurs de ce tableau sont les questions 
global list_alternative #Les valeurs de ce tableau sont les questions alternatives (ex pour ne pas demander à un sextagénère s'il est étudiant)
global dico_Reponses #dictionnaire de 0 et de 1 pour thor type {Q1:1,Q2,:0,Q3:0,...}(0 sera souvent un vieu/calme/fermier,...)
global n #pour faire list_Questions[n]
global btn_ok

n = 0
list_Questions = [('Vous êtes plutôt ?\nCalme                    Actif','Activite'),           #Reproduire les questions dans le même style que la première
                ('Quel âge avez vous ?\nMoins de 30 ans               Plus de 30 ans','Age'),
                ('Etes vous etudiant ?\nNon                    Oui','Scolarite'), #Change pour  X si personne = vieille                
                ('Avez vous\Vivez vous avec des enfants ?\nNon                   Oui','Famille'),
                ('La culture a-t-elle une place importante pour vous ?\nNon                    Oui','Culture'),
                ('Que préférez vous ?\nLa campagne                   La ville','citadin'),                               #s 4 dernières questions sont a revoir ducoup
                ('Avez vous un travail ?\nNon                    Oui','Travail'),
                ("Etes vous en recherche d'emploi ?\nNon                    Oui","Cherche_Emploi"),
                ('Q9','Theme9'),                              #!!! Est-ce qu'on fait des questions adaptative ? (jeune?: oui > étudiant ?, non > retraité ?)
                ('Q10','Theme10')]

list_alternative = [('Q_remplace_1','theme_remplace_1'),#Sers comme questions mais en remplacement
                    ('Bénéficiez vous du système de télétravail ?\nNon                    Oui','reseau'),#Pour les travailleurs
                    ('Q_remplace_3','theme_remplace_3'),
                    ('Q_remplace_4','theme_remplace_4'),
                    ('Q_remplace_5','theme_remplace_5'),
]


dico_Reponses = {}


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
    windowQCM.minsize(width=768, height=500) #768
    windowQCM.state('zoomed')

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

def change_questions(arg):
    """
    Fonction qui modifie notre liste de questions en fonction des réponses (bonne chance pour gérer les résultats)
    """
    global list_Questions
    global list_alternative
    global dico_Reponses
    if arg in dico_Reponses:
        if arg == 'Age': 
            if dico_Reponses[arg] == 1: #Si plus de 30 ans
                list_Questions[2] = list_alternative[0] #Pas encore décidé

        elif arg == "Travail":
            if dico_Reponses[arg] == 1:
                list_Questions[7] = list_alternative[1]





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
        change_questions(list_Questions[n-1][1])
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
        dico_Reponses[list_Questions[n-1][1]] = 1
        msg_principal.config(text = list_Questions[n][0])
        change_questions(list_Questions[n-1][1])
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
    windowQuestion.minsize(width=768, height=500)
    windowQuestion.state('zoomed') #Plein écran

    #windowQuestion.resizable(False,False) #Taille non modifiable
    #input
    entree = Entry(windowQuestion,cursor = 'Pencil', font = ('Bold',18))
    entree.place(relx=0.5, rely= 0.55, anchor=CENTER)
    
    #message
    msg_ville= Message(text="Veuillez saisir la ville recherchée", width = 1000, font =('Bold',18), justify=CENTER) #font = taille + police justify comme sur word
    msg_ville.place(relx= 0.5, rely=0.45, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    test_connexion(msg_ville) #Petit problème si ya pas de connection ça empêche le démarrage de l'application

    #Boutton
    btn_entree = Button(windowQuestion,width=20, height=3, command=lambda: ville(entree,msg_ville,windowQuestion), bg='#B9F7D0', text="Recherche")
    btn_entree.place(relx=0.5, rely= 0.65, anchor = CENTER)

    #windowQuestion.bind('KP_Return',ville(entree,msg_ville,windowQuestion)) #Appuyer sur entrée revient à appuyer sur le Bouton NE MARCHE PAS!


    windowQuestion.mainloop()


def ville(entree,msg,fenetre):
    """
    Récupère l'entrée, vérifie si la ville existe bien:
        -Si oui, continue vers la page 3
        -Si non, affiche un message d'erreur
    """
    ville = entree.get()
    print(ville)
    Donnees_ville = Donnees(ville)
    if Donnees_ville.is_commune_france('code/CSV/villes_france.csv'): #Je dois ajouter Code/ au début car vscode lance mal le fichier sinon ça va
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

    #Donnees PROVISOIRES
    dico = {'ville fleurie':9,'polution':10,'Animation':5,'th4':7,'th5':-2,'th6':4,'Culture':-1,'th8':-2,'Education':-1,'th10':-1} #Exemple
    score = 50 #Provisoire
    bonus,malus = trouve_bonus(dico), trouve_malus(dico) #Fonction non terminée (besoin du fichier qui fait les données)






    #Transfo des données en texte
    msg_ville = Message(windowScore,text=ville, width = 1000, font =('Bold',30), justify=CENTER)
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
    btn_Retour = Button(windowScore, width=20, height=3, command=lambda:retour_p2(windowScore), bg='#B9F7D0', text= "Noter une autre ville", font=('Bold',20))
    btn_Retour.place(relx = 0.5,rely = 0.7, anchor = CENTER)




    windowScore.mainloop()

def retour_p2(fenetre):
    """
    Retourne à la page n2 (pour redemander une ville)
    """
    fenetre.destroy()
    w_question()

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
    #A RETRAVAILLER PEUT ETRE METTRE UN PEU DE BLEU
    couleur = (255,0,127)
    rouge = 255 - int(n*255/100)
    vert = 0 + int(n*255/100)
    print(rouge,vert)
    couleur = (rouge,vert,100)

    rgb = '#' + ''.join(f'{i:02X}' for i in couleur)




    return rgb


#couleur_score(0)
#couleur_score(50)
#couleur_score(100)


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
w_qcm() #ligne  à lancer a la fin
#w_question()
#w_score('Beziers')
#print(n,dico_Reponses,msg_principal)
