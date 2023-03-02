'''
                      [LIFESCORE.PY]
                 CODE PRINCIPAL DE LIFE-SCORE
Code Tkinter ne pas oublier quand on crée des variable de les commenter (bon nom + fonction)
réferences : 
    - Les boutons s'écrivent btn_NOM
    - Les fenêtres s'écrivent windowNOM
    - Les textes (classe interface.CTkLabel) s'écrivent msg_NOM
    - Les listes s'écrivent list_NOM
    - Les dictionnaires s'écrivent dico_NOM
    - Les url de csv ou d'API s'écrivent url_csv_NOM ou url_api_NOM
'''
import subprocess
import sys
import os



'''
MODULE DE MISE A JOUR DES BIBLIOTHEQUES
 
'''
def maj_modules_requirements():
    """
    Verifie si tout les modules dans requirements.txt sont present, sinon ils sont installés.
    """

    nom_du_repertoire = os.path.dirname(__file__) # Cherche path du repertoir courant

    #list des modules deja installé
    pipList = subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE).stdout.decode("utf-8")

    # on installe tous les modules individuellement pour pouvoir les afficher un par un
    for module in open(os.path.join(nom_du_repertoire,os.pardir, "requirements.txt"), "r").readlines():
        moduleSeul = module.split(">")[0] # car c'est en format module>=x.x.x

        if moduleSeul + "==" in pipList:
            print(moduleSeul, "-> Module présent")
        else: 
            print(moduleSeul, "-> Module installé")
            output = subprocess.run([sys.executable, "-m", "pip", "install", module], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")

            if output == "": # output == "" quand il y a un erreur d'installation
                raise ConnectionError("Erreur de connection, verifiez votre connection d'internet!")



maj_modules_requirements() # A AMELIORER









'''
BIBLIOTHEQUES
 
'''
import update # import les fonctions et met a jours le modules en meme temps
from tkinter import *
import tkinter.font
from classes import * #Import de nos classes créées

from requests.exceptions import ConnectionError #Pas sûr de l'utilité là
from PIL import Image #pour les logos et les boutons de CTK


import pandas
from time import sleep, strftime, localtime
import csv
import customtkinter as interface
from tkintermapview import TkinterMapView



'''
RECUPERATION REPERTOIRE COURANT
'''

nom_du_repertoire = os.path.dirname(__file__)  #Explicite

'''
A REMPLACER PAR LES CSV
'''
repertoire_courant = os.path.dirname(__file__)
repertoire_donnees = os.path.join(repertoire_courant+'/donnees')
if not os.path.exists(repertoire_donnees):
    os.makedirs(repertoire_donnees)
    os.makedirs(repertoire_donnees+'/csv')
    os.makedirs(repertoire_donnees+'/utilisateur')



#Cree les fichiers suivants et remplis par la valeur par default s'ils ne sont pas là
if not os.path.isfile(nom_du_repertoire+'/donnees/utilisateur/style.txt'):
    nom_fichier = nom_du_repertoire+'/donnees/utilisateur/style.txt'
    with open(nom_fichier,"w") as fichier:
        fichier.write("System")

if not os.path.isfile(nom_du_repertoire+'/donnees/utilisateur/couleur_boutons.txt'):
    nom_fichier = nom_du_repertoire+'/donnees/utilisateur/couleur_boutons.txt'
    with open(nom_fichier,"w") as fichier:
        fichier.write("green")

with open(nom_du_repertoire +'/donnees/utilisateur/style.txt') as txt:
    style = txt.read()

with open(nom_du_repertoire +'/donnees/utilisateur/couleur_boutons.txt') as txt:
    style_bouton = txt.read()





'''
RECUPERATION POLICES ET STYLE
'''
interface.set_appearance_mode(str(style))  # Modes: system (default), light, dark
interface.set_default_color_theme(str(style_bouton))  # Themes: blue (default), dark-blue, green





'''
VARIABLES GLOBALES
'''
global msg_principal # On pose les questions a travers lui
global list_Questions # Les valeurs de ce tableau sont les questions 
# global list_alternative # Les valeurs de ce tableau sont les questions alternatives (ex pour ne pas demander à un sextagénère s'il est étudiant)
global dico_Reponses # Dictionnaire de 0 et de 1 pour thor type {Q1:1,Q2,:0,Q3:0,...}(0 sera souvent un vieu/calme/fermier,...)
global n # Pour faire list_Questions[n]
global btn_ok # Boutton qui continue (est utilisé plusieurs fois d'où la variable globale 
global Donnees_ville # Ce que l'on va traiter grâce aux autres fichiers
global erreur_maj
#global Fenetre_CTk #Globale pour la fenêtre principale


# Global pour la nouvelle version de UPDATE
global progressbar,windowDownload,msg_aide,message_pourcentage




'''
FONCTIONS DU CODE PRINCIPAL
'''


# Fonction qui calcule le temps entre deux entiers pour le score total
def fonction_animation_score(x, total) :
    
    # Remet le total sur 100 pour avoir un ralenti à la fin de la note
    x = (x/total)*100
    
    # A REFAIRE car c'est pas fluide comme annimation !
    if x < 50:
        return 0.20 - (x/250)
    elif x < 85:
        return 0.10
    else:
        return 0.50 + ((x-85)/15)


#pour remplacer le lancement de update et afficher la barre de progression
def telechargement(bouton,fenetre):
    '''
    Fonction qui lance le téléchargement à l'appui du boutton (et affiche la barre de progression)
    '''
    global erreur_maj
    change_etat_btn(bouton)
    
    
    windowDownload = interface.CTkToplevel() #fenetre de tkinter
    windowDownload.title('LifeScore  |  Téléchargement')
    #window.tk.call('tk::PlaceWindow', window) A VOIR PEUT ETRE (PLACEMENT AU CENTRE ?)
    windowDownload.minsize(width=int(510*4/3), height=384) #768
    windowDownload.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowDownload,bouton)) #Qu'on clique sur le btn ok ou qu'on ferme la page on obtient le meme resultat

    msg_aide = interface.CTkLabel(windowDownload, text="Lancement de la vérification...", width = 1000, font =('Bold',16), justify=LEFT)
    msg_aide.place(relx = 0.5, rely = 0.4, anchor = CENTER)

    message_pourcentage = interface.CTkLabel(windowDownload, text="0%", width = 1000, font =('Bold',12), justify=LEFT)
    message_pourcentage.place(relx=0.5,rely=0.65,anchor = CENTER)

    progressbar = interface.CTkProgressBar(windowDownload,mode = 'determinate')
    progressbar.place(relx=0.5,rely=0.6,anchor = CENTER)
    progressbar.set(0)
    windowDownload.update()
    
    
    erreur_maj = update.executer(progressbar,windowDownload,msg_aide,message_pourcentage)
    if not erreur_maj:
        valeur_bol = creation_fichiers()
        retour_pages(windowDownload,bouton)
        if valeur_bol == (True,True):
            w_qcm(fenetre,option ="sans_qcm")
        else: #Qcm non terminé
            w_qcm(fenetre)
    else:
        retour_pages(windowDownload,bouton)
        w_erreur(fenetre)

    windowDownload.mainloop()

    #lancement de update.py
    
def creation_fichiers(arg = None):
    '''
    fonction qui cree ou complete le fichier csv_dico.csv
    '''
    if arg == None:
        # Création le fichier du dico s'il existe pas :
        if not os.path.isfile(nom_du_repertoire+'/donnees/csv/csv_dico.csv') : 
            file = open(nom_du_repertoire+'/donnees/csv/csv_dico.csv','w')
            ecriture = csv.writer(file)
            ecriture.writerow(['CLE','VALEUR'])
            file.close()
            return False, False
        else:
            #si qcm terminé
            try :
                if len(pandas.read_csv(nom_du_repertoire+'/donnees/csv/csv_dico.csv')) +1 == len(list_Questions):
                    return True,True
                else:
                    #Si on a pas un fichier complet
                    
                    return True,False #fichier = true, complété = False
            except pandas.errors.EmptyDataError:
                return False,False
        
    tab_Reponses = [[tpl[0],tpl[1]] for tpl in dico_Reponses.items()] #valeurs du dico
    if not len(pandas.read_csv(nom_du_repertoire+'/donnees/csv/csv_dico.csv')) +1 == len(list_Questions):
        with open(nom_du_repertoire+'/donnees/csv/csv_dico.csv','w', encoding='UTF8', newline='') as f:
            ecriture = csv.writer(f)
            ecriture.writerow(['CLE','VALEUR'])
            ecriture.writerows(tab_Reponses)





# Premiere page
def w_qcm(win,option = None): # w pour window
    global msg_principal
    global btn_ok
    global list_Questions
    global n

    efface_fenetre(win) #efface tout ce qui était déja présennt pour y rajouter les choses



    """
    Affiche la premiere page qui contient donc le qcm
    """
    n = len(list_Questions)
    

    msg_principal = interface.CTkLabel(win, text="Les données utilisateur sont présentes, veuillez continuer.", width = 1000, font =('Bold',18), justify=CENTER)
    msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    #boutons 
    #bouton_explication/aide
    btn_aide = interface.CTkButton(win, height=int(win.winfo_screenheight()/10),command=lambda: aide(btn_aide), text="AIDE" ,font=('Arial Black',30)) #Bouton d'aide
    btn_aide.place(relx=0.9, rely=0.9 ,anchor = SE)
    #bouton de paramètres qui ouvre une page pour les mises à jour et leur fréquence
    btn_parametre = interface.CTkButton(win, height=int(win.winfo_screenheight()/10),command=lambda : parametres(btn_parametre), text="Paramètres",font=('Arial Black',30))
    btn_parametre.place(relx=0.1, rely=0.9, anchor = SW)

    #bouton ok Qui continue après le premier message
    btn_ok = interface.CTkButton(win, height=int(win.winfo_screenheight()/10), command=lambda: avancer(win), text="Lancer la recherche",font=('Arial Black',30)) #appele la fonction question1
    btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) #place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place)        




    if option == None :
        msg_principal.configure(text = "Bienvenue !  Nous allons commencer par une étude de vos préférences.")
        n = 0

    win.mainloop() #pour fermer la fenetre





def avancer(fenetre): 
    global msg_principal
    #global btn_ok
    global n #n prend +1 a chaque questions
    """
    Passe à la question 1 et ouvre le qcm ajoute les deux boutons Non et Oui
    
    Si le qcm est terminé, ouvre la seconde page
    """
    if n < len(list_Questions):
        btn_ok.place_forget() #Cache ce bouton
        btn_gauche = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10), command=lambda: plus0(btn_gauche,btn_droite), text="Non",font=('Arial Black',30))
        btn_droite = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10), command=lambda: plus1(btn_gauche,btn_droite), text="Oui",font=('Arial Black',30))
        btn_gauche.place(relx=0.40,rely=0.5,anchor=CENTER)
        btn_droite.place(relx=0.60,rely=0.5,anchor=CENTER)
        msg_principal.configure(text =f'{list_Questions[n][0]}') #change le texte du msg principal pour la question suivante

    else:
        efface_fenetre(fenetre)    
        w_question(fenetre) #Ouvre la seconde fenêtre : Fin de la première





def efface_fenetre(fenetre,option="Classique"): #option = "Classique" est une valeur de base pour garder lee btn parametres si on met une autre option il efface quand meme ce bouton
    """
    Fonction qui efface tout d'une fenêtre à l'autre pour pouvoir afficher d'autres choses
    """
    if option == "Classique":
        for widget in fenetre.winfo_children():

            if str(widget) not in ['.!ctkbutton4','.!ctkbutton2'] and "toplevel" not in str(widget): #Pour garder le btn parametres et le logo et les pages d'aides

                widget.destroy()
    else:
        for widget in fenetre.winfo_children():

            if str(widget) != '.!ctkbutton2' : #Pour garder le logo

                widget.destroy()

        





def plus0(b1,b2):
    """ajoute 0 au dico de reponses (Non)"""
    global list_Questions
    global n
    global dico_Reponses
    global msg_principal

    
    n += 1
    if not est_termine(b1,b2):
        dico_Reponses[list_Questions[n-1][1]] = 0
        msg_principal.configure(text = list_Questions[n][0])





def plus1(b1,b2):
    """ajoute 1 au dico de reponses (Oui)"""
    global list_Questions
    global n
    global dico_Reponses
    global msg_principal
    
    n += 1
    if not est_termine(b1,b2):
        dico_Reponses[list_Questions[n-1][1]] = 1
        msg_principal.configure(text = list_Questions[n][0])





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
        msg_principal.configure(text = "Merci d'avoir répondu aux questions, Veuillez continuer")
        return True


def aide(btn):

    """
    Ouvre Une fenêtre d'aide avec un texte et peut être des graphismes
    """
    texte_aide=("Bonjour ! Voilà notre protoype de LifeScore où vous pourrez visualiser la note de villes."
    + " Pour commencer, nous réalisons un QCM de 8 questions afin de déterminer vos préférences."
    + " Pour chaques critères, on définit une note sur 100 ainsi qu'un coefficient propre à lui même. "
    + " Le plus de critères sont réunis afin d'avoir le plus de précision possible. "
    + "\n\nIls sont répartis en 4 catégories :"
    + "\n   - Le climat (pluie par an / pollution de l'air / température / vent / ...)"
    + "\n   - La qualité de vie (activités / patrimoine / ville fleurie / ...)"
    + "\n   - Le coût (essence / gaz / loyer / prix de la vie / salaire moyen / ...)"
    + "\n   - La sécurité (taux d'accidents / vols / risques / ...)")
    change_etat_btn(btn)
    windowAide = interface.CTkToplevel() #fenetre de tkinter
    windowAide.title('LifeScore  |  Aide')
    #window.tk.call('tk::PlaceWindow', window) A VOIR PEUT ETRE (PLACEMENT AU CENTRE ?)
    windowAide.minsize(width=int(510*4/3), height=384) #768
    txt_aide = interface.CTkTextbox(windowAide, width = 580 , corner_radius=0)
    txt_aide.insert("0.0", text = texte_aide)
    txt_aide.place(relx=0.05,rely=0.05)
    txt_aide.configure(state = "disabled", font = ("Arial",18),wrap="word") #disabled pour pas qu'on puisse écrire, "word" pour le retour a la ligne
    btn_compris = interface.CTkButton(windowAide, height=int(windowAide.winfo_screenheight()/10), command=lambda:retour_pages(windowAide,btn), text="Compris !",font=('Arial Black',30))
    btn_compris.place(relx = 0.5, rely = 0.7, anchor = CENTER)
    windowAide.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowAide,btn)) #Qu'on clique sur le btn ok ou qu'on ferme la page on obtient le meme resultat

    windowAide.mainloop()
    return windowAide


def date_dernier_verification() -> str:
    """Renvoi date formaté du dernier mis a jour des donnees"""
    dernier_maj_sec = lire_option("DERNIERE_MAJ")
    return strftime("%d/%m/%Y à %Hh%M", localtime(dernier_maj_sec))

def supprimer_donnees_utilisateur():
    """Suprime le fichier csv_dico.csv de ./donnees/csv/"""
    repertoire_cible = nom_du_repertoire + "/donnees/csv/"
    if "csv_dico.csv" in os.listdir(repertoire_cible): # on verifie que le fichier existe
        os.remove(repertoire_cible + "csv_dico.csv") # on suprime le fichier
        sys.exit() #ferme le programme pour éviter de potentielles erreurs


def parametres(bouton):
    """
    Fonction qui ouvre la page de paramètres avec dessus : (X  = pas fait, A = à Améliorer, V = fait)
        -Crédits #!On les garde ?                                       X
        -Option pour modifier la fréquence de mises à jour              V
        -Volet pour changer le style de l'application                   V 
        -Un bouton pour fermer la page                                  V
        -Suprimmer donnes d'utilisateur                                 V

    """
    change_etat_btn(bouton) #Bloque le bouton paramètre sur la page principale jusqu'à que cell-ci soit fermée
    
    # Création de la fenêtre
    
    windowParam = interface.CTkToplevel()
    windowParam.title('LifeScore  |  Paramètres')
    windowParam.geometry("680x650") #768
    windowParam.resizable(False, False)

    #Création des widgets :

    #Tous les messages présents :
    msg_titre = interface.CTkLabel(windowParam, text="PARAMÈTRES", font= ('Arial Black', 40), text_color="#29A272")
    msg_frequence = interface.CTkLabel(windowParam, text="FRÉQUENCE DE MISE À JOUR :", font= ('Yu Gothic Light', 25), text_color="#29A272")
    msg_verif = interface.CTkLabel(windowParam, text=f"Dernière Vérification: {date_dernier_verification()}", font= ("Yu Gothic Light", 16), text_color="#646464")
    msg_apparence = interface.CTkLabel(windowParam, text="APPARENCE DE L'APPLICATION :", font= ('Yu Gothic Light', 25), text_color="#29A272")
    msg_donnees = interface.CTkLabel(windowParam, text="DONNÉES UTILISATEUR :", font= ('Yu Gothic Light', 25), text_color="#29A272")
    message = interface.CTkLabel(windowParam,text="Le bouton de suppression des données fermera le programme ", width = 50, font =('Bold',18)) #font = taille + police, justify comme sur word

    #Tous les boutons présents :
    btn_confirm_frequence = interface.CTkButton(windowParam, width = 7, 
                                                            command=lambda:changer_option("FREQ_MAJ", round(abs(float(entree_frequence_maj.get()))*86400),message) if est_nombre(entree_frequence_maj.get()) else message.configure(text = "Vous devez entrer un nombre !"), # jours * nb sec dans jour 
                                                            text="Confirmer")
    btn_supprimer_donnees = interface.CTkButton(windowParam, width = 134, height = 42,
                                                command=supprimer_donnees_utilisateur,
                                                text="SUPPRIMER",
                                                font=("Bold", 18))
    btn_changements = interface.CTkButton(windowParam,height=60,
                                                        width=550,  
                                                        command=lambda:retour_pages(windowParam,bouton), 
                                                        text="FERMER LA PAGE",
                                                        font=('Arial Black',30))
    
    #Autres (les entrées et les volets "switch") :
    entree_frequence_maj = interface.CTkEntry(windowParam, placeholder_text="30", width=51, font= ('Bold', 18))
    switch_apparence = interface.CTkOptionMenu(windowParam, values=["Système", "Sombre", "Clair"],command=change_apparence_page)
    switch_apparence.set('Styles') #La valeur initiale (à titre indicatif) 


    #Placement des widgets (Dans l'ordre dans lequel ils sont affichés) :
    
    msg_titre.place(relx=0.5, rely=0.064, anchor = CENTER)

    #La fréquence de mise à jour
    msg_frequence.place(relx = 0.02, rely = 0.15)
    entree_frequence_maj.place(relx = 0.06, rely = 0.20)
    btn_confirm_frequence.place(relx = 0.195, rely = 0.22, anchor = CENTER)
    msg_verif.place(relx=0.06, rely=0.24)

    #L'apparence de l'application 
    msg_apparence.place(relx = 0.02, rely = 0.33)
    switch_apparence.place(relx = 0.06, rely = 0.38)

    #La suppression des données 
    msg_donnees.place(relx=0.02, rely=0.51)
    btn_supprimer_donnees.place(relx=0.06, rely=0.56)

    #Fin de la page
    message.place(relx=0.5,rely=0.75,anchor = CENTER)
    btn_changements.place(relx = 0.5, rely = 0.87, anchor = CENTER)

    # TODO: Boutton credit et rapporter bug
    # TODO: Boutton conditions Utilisateur -Raf : Non c'est bon ya pas de conditions a accepter ?
    windowParam.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowParam,bouton))#Meme effet que le bouton sauf que c'est si on ferme la page manuellement
    windowParam.mainloop()




def change_apparence_page(choix):

    if choix in ["Système","Sombre","Clair"] : #Si on veut changer les pages
        if choix == "Système": choix = "System"
        elif choix == "Sombre": choix = "Dark"
        else:choix = "Light"

        with open(nom_du_repertoire + '/donnees/utilisateur/style.txt', 'w') as txt:
            txt.write(choix)

        interface.set_appearance_mode(choix)
    else: #Si on veut changer les boutons
        if choix == "Bleu": choix = "blue"
        elif choix == "Bleu Foncé": choix = "dark-blue"
        else:choix = "green"

        with open(nom_du_repertoire + '/donnees/utilisateur/couleur_boutons.txt', 'w') as txt:
            txt.write(choix)
    
        



def retour_pages(window,btn,cle=True):
    """
    Fonction qui passe de la page actuelle à la page N°x
    """
    
    if cle==True : #Si on a juste une page d'aide
        window.destroy()
        change_etat_btn(btn)
    else:
        
        efface_fenetre(window)
        w_question(window)





def change_etat_btn(bouton):
    """
    Fonction qui change l'état du bouton utilisé
    
    Ca marche désormais :) 
    """
    try :
        if bouton  and bouton.cget("state") == NORMAL : #Récupère l'attribut et le change
            bouton.configure(state=DISABLED)
        else:
            bouton.configure(state=NORMAL)
    except TclError:
        return None





# Seconde page
def w_question(fenetre):
    """
    affiche la seconde page qui contient la requête de la ville
    """
    creation_fichiers("Rajout des lignes") #rajoute les lignes au dico csv dès qu'on quitte la page de QCM
    fenetre.title('LifeScore  |  Requête de la commune')
    
    icone = tkinter.PhotoImage(file = nom_du_repertoire+'\systeme\icones\\1.png')
    fenetre.iconphoto(False, icone)

    #input
    entree = interface.CTkEntry(fenetre,placeholder_text="ex : Puissalicon ",width=int(500/3), font = ('Bold',18))
    entree.place(relx=0.5, rely= 0.55, anchor=CENTER)
    
    #message
    msg_ville= interface.CTkLabel(fenetre, text="Veuillez saisir la ville recherchée", width = 1000, font =('Bold',20), justify=CENTER) #font = taille + police, justify comme sur word
    msg_ville.place(relx= 0.5, rely=0.45, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 

    btn_arrondissement = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10),command=lambda: arrondissement(btn_arrondissement), text="Aide\narrondissements",font=('Arial Black',30)) #Boutton d'aide arrondissements
    btn_arrondissement.place(relx=0.9, rely=0.9 ,anchor = SE)
    
    #test_connexion(msg_ville) #Petit problème si ya pas de connection ça empêche le démarrage de l'application


    # Boutton
    btn_entree = interface.CTkButton(fenetre,height=int(fenetre.winfo_screenheight()/10), command=lambda: ville(entree,msg_ville,fenetre),text="Recherche",font=('Arial Black',30))
    btn_entree.place(relx=0.5, rely= 0.65, anchor = CENTER)

    fenetre.bind('KP_Return',ville(entree,msg_ville,fenetre)) #Appuyer sur entrée revient à appuyer sur le Bouton NE MARCHE PAS!







def arrondissement(btn):

    """
    Ouvre Une fenêtre d'aide avec un texte et peut être des graphismes
    """
    change_etat_btn(btn) # bouton devient inactif grâce à l'autre fonction pour ne pas qu'on appuye dessus plusieurs fois
    texte_aide=("Si Votre ville possède plusieurs arrondissemnts (ex : Paris) :"
    + "\n     - Si vous saisissez uniquement le nom de la ville, le premier            arrondissement sera pris comme base"
    + "\n     - Sinon, écrivez le nom de la ville comme cela : \n\n           Nom_X avec X le numéro de l'arrondissement (ex : Paris_7)")

    windowAide = interface.CTkToplevel() #fenetre de tkinter
    windowAide.title('LifeScore  |  Aide')
    icone = tkinter.PhotoImage(file = nom_du_repertoire+'\systeme\icones\\1.png')
    windowAide.iconphoto(False, icone)
    #window.tk.call('tk::PlaceWindow', window) A VOIR PEUT ETRE (PLACEMENT AU CENTRE ?)
    windowAide.minsize(width=int(510*4/3), height=384) 
    txt_aide = interface.CTkTextbox(windowAide, width = 580 , corner_radius=0)
    txt_aide.insert("0.0", text = texte_aide)
    txt_aide.place(relx=0.05,rely=0.05)
    txt_aide.configure(state = "disabled", font = ("Arial",18),wrap="word") #disabled pour pas qu'on puisse écrire, "word" pour le retour a la ligne
    btn_compris = interface.CTkButton(windowAide, height=int(windowAide.winfo_screenheight()/10), command=lambda :retour_pages(windowAide,btn), text="Compris !",font=('Arial Black',30))
    btn_compris.place(relx = 0.5, rely = 0.7, anchor = CENTER)
    windowAide.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowAide,btn))

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
    Donnees_ville = Donnees(ville)
    if Donnees_ville.is_commune_france(msg): #Je dois ajouter Code/ au début car vscode lance mal le fichier sinon ça va
        msg.configure(text = "Veuillez patienter ...")
        #FAIRE TOUS LES CALCULS ICI :
        Donnees_ville.note_par_habitants('sport_test.csv',['ComInsee','Nombre_equipements'],[16071.4,-3.57143],',')
        #ON OUVRE LA TROISIEME PAGE QU'APRES AVOIR FAIT TOUS LES CALCULS
        efface_fenetre(fenetre,"Efface_reste")
        w_score(Donnees_ville,fenetre)





#troisieme page
def w_score(ville,win):
    """
    affiche la dernière page qui contient le score et le bouton pour revenir
    -    ville est un objet de la classe Donnees précédemment créé après avoirs appuyé sur recherche
    """
    
    
    icone = tkinter.PhotoImage(file = nom_du_repertoire+'\systeme\icones\\1.png')
    win.iconphoto(False, icone)
    win.title(f'LifeScore  |  Commune de {str(ville).capitalize()}')
        

    #Donnees PROVISOIRES !!!
    dico = {'Atout 1':9,'Atout 2':10,'Atout 3':5,'Atout 4':7,'Inconvéniant 1':-2,'Atout 5':4,'Inconvéniant 2':-1,'Inconvéniant 3':-2,'Inconvéniant 4':-1,'Inconvéniant 5':-1} #Exemple
    score = Donnees_ville.note_finale() #Provisoire
    bonus,malus = trouve_bonus(dico), trouve_malus(dico) #Fonction non terminée (besoin du fichier qui fait les données)


    #Transfo des données en texte
    msg_ville = interface.CTkLabel(win,text=str(ville).capitalize(), width = 500, font=('Arial Black',70), justify=CENTER)#fix temporaire qui aggrandit de 2.5 pour les grosses ville à rajouter, une fonction inverse pour la taille
    msg_ville.place(relx=0.5,rely=0.1,anchor=CENTER)
    plus, moins = plus_et_moins(bonus,malus) # Récupère les données et les transforme en 2 str à Afficher
    
    # Carte du ville
    if is_connected("https://mt0.google.com/"):
        carte_ville = TkinterMapView(win, width=0.4*win.winfo_width(), height=0.4*win.winfo_height())
        carte_ville.set_address(f"{str(ville)[:-1] if est_nombre(str(ville)[-1]) else str(ville)}, France") # insert la ville pour l'adress (et format pour les arrondissements) 
        carte_ville.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        carte_ville.place(relx=0.3, rely=0.18)
    


    '''
    ANIMATION DU SCORE FINAL
    
    '''
    
    if score != 'N/A':
        
        # Transformations
        score_total_animation = int(score)
        score = str(score)
        
        # Mise en place du reste du texte, pour éviter une surcharge du nmbr d'elem à rafraichir
        msg_bonus = interface.CTkLabel(win,text=plus, width = 1000, font =('Bold',30), justify=LEFT)
        msg_malus = interface.CTkLabel(win,text=moins, width = 1000, font =('Bold',30), justify=LEFT)
        msg_bonus.place(relx = 0.15, rely = 0.7,anchor = CENTER)
        msg_malus.place(relx=0.8,rely=0.7,anchor = CENTER)
        msg_note = interface.CTkLabel(win, text=0, text_color=couleur_score(0), font=('Arial Black', 80), justify=CENTER) #On initialise
        msg_note.place(relx=0.9,rely=0.2, anchor=CENTER)#Nord Est
        win.update()
        
        
        # Pour chaque entier naturel jusqu'à notre note
        for i in range(score_total_animation+1) :
            
            """if i > 0 :
                msg_note.destroy() # pour pas laisser de traces après ou sinon il y a superposition"""
                
            couleur= couleur_score(i)
            #Textes :
            msg_annonce_note = interface.CTkLabel(win, text='Note :', font=('Arial Black', 50), justify=CENTER)
            msg_note.configure(text=str(i), text_color=couleur)
            
            msg_annonce_note.place(relx=0.9,rely=0.1, anchor=CENTER)#Nord Est
            
            

            # Mise à jour de la page
            win.update()
            sleep(fonction_animation_score(i, score_total_animation)*0.1)
            
            

    # Si on a pas de note
    else:
        
        #Textes :
        msg_note = interface.CTkLabel(win, text=f'Note : \n' +score +'  ' ,text_color ='grey', font =('Arial Black',60), justify=CENTER)
        msg_note.place(relx=0.9,rely=0.1, anchor=CENTER)#Nord Est
        msg_NonAttribue = interface.CTkLabel(win,text="Nous n'avons pas pu récuperer les informations de cette ville", width = 1000, font =('Bold',30), justify=LEFT)
        msg_NonAttribue.place(relx = 0.5, rely = 0.9,anchor = CENTER)



    #Bouton retour
    btn_Retour = interface.CTkButton(win,height=int(win.winfo_screenheight()/10), command=lambda:retour_pages(win,None,False), text= "Noter une autre ville", font=('Arial Black',20))
    btn_Retour.place(relx = 0.5,rely = 0.7, anchor = CENTER)
    




def trouve_bonus(dic):
    """
    Prend les 5 meilleurs aspects de la ville pour mettre des plus à y habiter
    """
    
    bonus_list= []
    for i in range(5):
        maxi = 0
        cle_maxi = "Valeur initiale"
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
    cle_mini = "Valeur initiale"
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





def couleur_score(note):
    '''
    Fonction qui renvoie la note en une couleur hexadécmal. Rouge -> Vert
    '''
    if note != 'N/A' :
        
        if note == 0 :
            r,g,b = 100,0,0
            
        elif note <= 20:
            r = int(110 * (note/20) + 100)
            g, b = 0, 0
            
        elif note <= 60 :
            r = 210
            g = int(210 * (note-20)/40)
            b = 0
            
        else :
            r = int(210*(100-note)/40)
            g = 210
            b = 0
            
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    else :
        return '#808080'





#Page d'erreur 
def w_erreur(fenetre): # w pour window
    """
    Affiche la page d'erreur qui signale le problème
    """
    
    #fenêtre
    fenetre.title('LifeScore  |  Erreur')
    icone = tkinter.PhotoImage(file = nom_du_repertoire+'\systeme\icones\\1.png')
    fenetre.iconphoto(False, icone)
    
    msg_principal =  interface.CTkLabel(fenetre, text="Une erreur s'est produite, le programme n'a pas pu se lancer\nEssayez de vous reconnecter à internet", 
        width = 1000, font =('Bold',18), justify=CENTER) #font = taille + police justify comme sur word
    msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    #boutons 
    #bouton_explication/aide
    btn_aide  = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10),command=lambda: aide(btn_aide), text="Aide",font=('Arial Black',30)) #Bouton d'aide
    btn_aide.place(relx=0.9, rely=0.9 ,anchor = SE)
    #bouton de paramètres qui ouvre une page pour les mises à jour et leur fréquence
    btn_parametre = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10),command=lambda : parametres(btn_parametre), text="Paramètres",font=('Arial Black',30))
    btn_parametre.place(relx=0.1, rely=0.9, anchor = SW)

    #bouton ok Qui continue après le premier message
    btn_ok = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10), command=fenetre.destroy, text="OK",font=('Arial Black',30)) #Ferme la page
    btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) #place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place)

def taille_police(chaine):
    '''
    Fonction qui retourne une taille de police adéquate en fonction du nombre de caractères et d'une fonction f(x) = -mx+p
    idée : Raf
    '''
    longueur = len(chaine)
    taille = -1.5*longueur + 70 #a modifier peut etre faire une fonction inverse ?
    return taille



'''
VARIABLE GLOBALES
'''


n = 0
list_Questions = [('Aimez vous sortir en ville ?','Activite'),           # Reproduire les questions dans le même style que la première
                ('Avez vous moins de 30 ans ?','Age'),
                ('Etes vous etudiant ?','Scolarite'), # Change pour  X si personne = vieille                
                ('Avez vous\Vivez vous avec des enfants ?','Famille'),
                ('La culture a-t-elle une place importante pour vous ?','Culture'),
                ('préférez vous la campagne à la ville ?','citadin'),
                ('Avez vous un travail ?','Travail'),
                ("Etes vous en recherche d'emploi ?","Cherche_Emploi")]

dico_Reponses = {} # Traité dans coefficients.py

'''
CREATION DE La FENETRE PRINCIPALE
'''
#fenêtre
fenetrePrincipale = interface.CTk() #fenetre de tkinter
fenetrePrincipale.title('LifeScore  |  Menu principal')
icone = tkinter.PhotoImage(file = nom_du_repertoire+'\systeme\icones\\1.png')
fenetrePrincipale.iconphoto(False, icone)
fenetrePrincipale.minsize(width=768, height=500) #768 = taille minimum de la fenetre
fenetrePrincipale.state('zoomed')
#boutton de lancement
btn_ok = interface.CTkButton(fenetrePrincipale, height=int(fenetrePrincipale.winfo_screenheight()/10), command=lambda:telechargement(btn_ok,fenetrePrincipale), text="Continuer",font=('Arial Black',30)) #appele la fonction question1
btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) #place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place)        

#message de lancement
msg_principal = interface.CTkLabel(fenetrePrincipale, text="Bienvenue dans LifeScore, nous allons procéder à\nune vérification des fichiers.", width = 1000, font =('Bold',18), justify=CENTER)
msg_principal.place(relx= 0.5, rely = 0.4,anchor = CENTER)

#logo qui doit rester tt le long
logo = interface.CTkImage(light_image=Image.open(nom_du_repertoire +'/systeme/icones/logo.png'), size=(180, 180))
btn_nul = interface.CTkButton(fenetrePrincipale,image = logo,fg_color="transparent",hover = False,text =  "")
btn_nul.place(relx=0.1,rely=0.15,anchor = CENTER)

fenetrePrincipale.mainloop()
