'''
                      [LIFESCORE.PY]
                 CODE PRINCIPAL DE LIFE-SCORE
Syntaxe de nos variables : 
    - Les boutons s'écrivent btn_Nom
    - Les fenêtres s'écrivent fenetre_Nom
    - Les textes (classe interface.CTkLabel) s'écrivent msg_Nom
    - Les listes s'écrivent liste_Nom
    - Les dictionnaires s'écrivent dico_Nom
    
Pour tous les widgets du code, leurs création dépendait de notre mémoire sur Tkinter et de la documentation sur CustomTkinter 
'https://github.com/TomSchimansky/CustomTkinter/wiki/'
Les valeurs (de taille, de police, de couleur,... ont été trouvées après plusieurs essais par nous même)
De même pour les placements, nos connaissances de Tkinter nous ont permis de retrouver certaines méthodes 
avec des arguments précis (.place(relx et rely))
'''



# Bibliothèques essentielles pour la mise à jour des autres bibliothèques
import subprocess
import sys
import os





# Message de bienvenue sur le terminal
print(  "####################################################",
      "\n##                   LIFE-SCORE                   ##",
      "\n##              Terminal de débogage              ##",
      "\n####################################################\n\n",)










'''
MODULE DE MISE A JOUR DES BIBLIOTHEQUES

- Idée de Nathan
- Réalisé par Thor
- Redémarrage requis par Nathan
'''

# Message sur le terminal
print(  "################################",
      "\n##  Installation des modules  ##",
      "\n################################\n\n",)

# Verifie si tout les modules dans requirements.txt sont present, sinon ils sont installés.
nouvelle_bibliotheque = False
nom_du_repertoire = os.path.dirname(__file__) # Cherche le chemin du repertoire courant

# Liste des modules deja installé
liste_pip = subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE).stdout.decode("utf-8")

# On installe tous les modules individuellement pour pouvoir les afficher un par un
for module in open(os.path.join(nom_du_repertoire,os.pardir, "requirements.txt"), "r").readlines(): # os.pardir équivaut à ../ en linux
    moduleSeul = module.split(">")[0] # Format module>=x.x.x

    if moduleSeul + "==" in liste_pip:
        print(moduleSeul, "-> Module présent")
    else: 
        print(moduleSeul, "-> Module installé")
        output = subprocess.run([sys.executable, "-m", "pip", "install", module], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")
        nouvelle_bibliotheque = True

        if output == "": # output == "" quand il y a une erreur d'installation
            raise ConnectionError("Erreur de connection, verifiez votre connection d'internet!")


# Pour éviter de lancer le programme sans avoir bien installé les bibliothèques - Fait par Nathan
if nouvelle_bibliotheque == True :
    print("\n\n\n\n\n********************\n[ATTENTION]\nVeuillez redémarrer le programme pour appliquer l'instation des bibliothèques.\n\n********************\n\n\n\n\n")
    input("Veuillez presser entrer pour quitter.")
    sys.exit(os.system(f"{sys.executable} ./LifeSCORE.py"))
print("\n\n")



'''
BIBLIOTHEQUES

'''
# Nos autres fichiers
import update # Importe les fonctions et met à jour les modules en meme temps
from classes import * # Import de nos classes créées

# Interface graphique
from tkinter import * # On utilise certaines fonctions de Tkinter avec Customtkinter
import customtkinter as interface # On utilisera Customtkinter principalement pour le style
from tkintermapview import TkinterMapView # Pour les cartes de la ville
from PIL import Image # pour les logos et les boutons de CTK

# Lecture de données (csv)
import math

# Autre(s)
from time import sleep, strftime, localtime # Sleep met en pause le programme, strftime convertit le temps et localtime redonne le temps de l'ordinateur

'''
VARIABLES GLOBALES (utilisées à travers plusieurs fonctions)

- Idée de Raphaël (au fur et à mesure que le code avançait, plusieurs variables ont été ajoutées)
'''
global dico_Reponses        # DICT | Dictionnaire de 0 et de 1 pour thor type {Q1:1,Q2,:0,Q3:0,...}(0 sera souvent un vieu/calme/fermier,...)
global msg_Principal        # CTkLabal | Afin de le modifier nous nous devons de le poser en variable globale
global n                    # INT | Pour faire liste_Questions[n]
global btn_Ok               # CTkButton | Boutton qui continue (est utilisé plusieurs fois d'où la variable globale) 
global Donnees_ville        # Donnees | Ce que l'on va traiter grâce aux autres fichiers
global icone                # PhotoImage | Prend les données du logo en png pour l'afficher sur chaques pages

# Variables globales pour la nouvelle version de UPDATE - Idee de rendre ces variables globales de Nathan 
global progressbar          # CTkProgressbar | Montre l'avancée visuelle du téléchargement
global msg_aide             # STR | Renvoie l'avancée du téléchargement
global msg_Pourcentage  # STR | Renvoie l'avancée du téléchargement



# initialisations des images des boutons, fait par Nathan
chemin_images_boutons =nom_du_repertoire+'/systeme/icones/'

image_btn_chercher = interface.CTkImage(light_image=Image.open(chemin_images_boutons+'chercher.png'),
                                size=(50, 50))

image_btn_quitter = interface.CTkImage(light_image=Image.open(chemin_images_boutons+'fermer.png'),
                                size=(100, 100))

image_btn_parametres = interface.CTkImage(light_image=Image.open(chemin_images_boutons+'parametres.png'),
                                size=(100, 100))

image_btn_aide = interface.CTkImage(light_image=Image.open(chemin_images_boutons+'aide.png'),
                                size=(100, 100))






# Constantes (les questions sont aussi de nous)
repertoire_donnees = os.path.join(nom_du_repertoire+'/donnees') # Retourne le chemin vers le dossier 'donnees'
n = 0
liste_Questions = [("Aimez vous sortir en ville ?",'Activite'),           # Reproduire les questions dans le même style que la première
                ("Êtes vous étudiant ?",'Enseignement_Superieur'),
                ("Avez-vous des enfants?",'Scolarite'),   
                ("La culture a-t-elle une place importante pour vous ?",'Culture'),
                ("Préférez vous la ville à la campagne ?",'Citadin'),
                ("Êtes vous en recherche d'emploi ?","Cherche_Emploi"),
                ("Êtes vous dans une situation précaire ?","Precarite")]


dico_Reponses = {} # Traité dans coefficients.py




'''
Système de compatiblité Windows / Linux
pour les polices d'écritures & l'interface
fait par Nathan
'''

import platform
systeme_exploitation = platform.system()

if systeme_exploitation == 'Linux' :
    polices = ['Ubuntu',
               'Ubuntu']
    
else :
    polices = ['Arial',
               'Arial Black']







'''
FONCTIONS
'''
def fenetre_telechargement(bouton,fenetre, bouton_param, bouton_aide):
    '''
    Fonction qui lance le téléchargement à l'appui du boutton (et affiche la barre de progression)
    Puis renvoie sur le qcm ou la suite du programme

    - Page calquée sur les autres pages d'aides vues plus loin par Raphaël
    - Condition de mise à jour par Nathan
    '''
    # Si les données doivent être mises à jour, on initialise la page
    if update.mettre_a_jour() :
        change_etat_btn(bouton) # Bloque le bouton sur la page principale
        change_etat_btn(bouton_param)
        change_etat_btn(bouton_aide)
        
        # Initialisation de la page
        fenetre_Telechargement = interface.CTkToplevel() # Fenetre supplémentairz de tkinter
        fenetre_Telechargement.title('LifeScore  |  Téléchargement')
        fenetre_Telechargement.iconphoto(False, icone)
        fenetre_Telechargement.minsize(width=int(510*4/3), height=384)
        fenetre_Telechargement.focus() # Ajout de cette ligne pour éviter qur ça passe derrière la page principale
        fenetre_Telechargement.resizable(False, False)
        fenetre_Telechargement.protocol("WM_DELETE_WINDOW", lambda:retour_pages(fenetre_Telechargement,bouton)) # Qu'on clique sur le btn_ok ou qu'on ferme la page on obtient le même résultat
        

        # Création des widgets
        msg_Aide = interface.CTkLabel(fenetre_Telechargement, text="Lancement de la vérification...", width = 1000, font =(polices[0],16), justify=CENTER)
        msg_Pourcentage = interface.CTkLabel(fenetre_Telechargement, text="0%", width = 1000, font =(polices[0],12), justify=LEFT)
        progressbar = interface.CTkProgressBar(fenetre_Telechargement,mode = 'determinate')
        progressbar.set(0)

        # Placements des widget
        msg_Aide.place(relx = 0.5, rely = 0.4, anchor = CENTER)
        progressbar.place(relx=0.5,rely=0.6,anchor = CENTER)
        msg_Pourcentage.place(relx=0.5,rely=0.65,anchor = CENTER)    
        
        fenetre_Telechargement.update()
        
        # Décide ensuite quelle action faire
        erreur_maj = update.mise_a_jour(progressbar,fenetre_Telechargement,msg_Aide,msg_Pourcentage)
        change_etat_btn(bouton_param)
        change_etat_btn(bouton_aide)
        if not erreur_maj:
            retour_pages(fenetre_Telechargement,bouton)
            if len(lire_fichier_dico("REPONSE_QCM")) == len(liste_Questions): # Si les données du questionnaires ont déja été remplies
                fenetre_questionnaire(fenetre,option ="sans_qcm")
            else: # Si les données ne sont pas toutes présentes (on lance le questionnaire)
                fenetre_questionnaire(fenetre)
        else: # Fenetre d'erreur en cas d'erreur dans le téléchargement
            retour_pages(fenetre_Telechargement,bouton)
            fenetre_erreur(fenetre)
            
        fenetre_Telechargement.mainloop()
        
    # Si il n'y a pas de mise à jour à faire, on saute cette étape
    else : 
        if len(lire_fichier_dico("REPONSE_QCM")) == len(liste_Questions): # Si les données du questionnaires ont déja été remplies
            fenetre_questionnaire(fenetre,option ="sans_qcm")
        else: # Si les données ne sont pas toutes présentes (on lance le questionnaire)
            fenetre_questionnaire(fenetre)
        



'''
FONCTIONS UTILISEES PLUSIEURS FOIS

'''
def efface_fenetre(fenetre,option="Classique"): # "Classique" est une valeur de base pour garder certains widgets
    """
    Fonction qui efface tous les widgets d'une fenêtre à l'autre pour pouvoir afficher d'autres choses

    - winfo_children() a été pris dans la documentation de Tkinter, les noms ont été trouvé par print() et tests par Raphaël
    """
    if option == "Classique": # On veut garder le logo, les boutons de paramètres, d'information et de fermeture et les pages d'aides
        for widget in fenetre.winfo_children():

            if str(widget) not in ['.!ctkbutton5','.!ctkbutton4','.!ctkbutton2','.!ctkbutton3'] and "toplevel" not in str(widget):
                widget.destroy() # .destroy() supprime le widget

    else: # On veut juste garder le logo
        for widget in fenetre.winfo_children():
            if str(widget) not in ['.!ctkbutton5','.!ctkbutton2','.!ctkbutton3'] : # Ici on ne prend pas les boutons d'informations en compte
                widget.destroy()


def avancer(fenetre): 
    global n # n += 1 à chaque questions
    global msg_Principal
    """
    Passe à la question 1, ouvre le qcm et ajoute les deux boutons Non et Oui.
    
    Si le qcm est terminé, ouvre la seconde page

    - Idée d'utilisation des variables globales n et du message principal par Raphaël
    """
    if n != len(liste_Questions):
        btn_Ok.place_forget() # Le cache le temps du lancement de cette fonction
        # Création des boutons
        btn_Gauche = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10), 
                                         command=lambda: plus(btn_Gauche,btn_Droite,0), text="Non",font=(polices[0],30, 'bold'))
        btn_Droite = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10), 
                                         command=lambda: plus(btn_Gauche,btn_Droite,1), text="Oui",font=(polices[0],30, 'bold'))
        
        # Placements et Modifications
        btn_Gauche.place(relx=0.40,rely=0.5,anchor=CENTER)
        btn_Droite.place(relx=0.60,rely=0.5,anchor=CENTER)
        msg_Principal.configure(text =f'{liste_Questions[n][0]}') # Affiche la premiere question
    else:
        efface_fenetre(fenetre,"Efface_reste")    
        fenetre_question(fenetre) # Ouvre la seconde page : Fin de la première


def plus(b1,b2,arg):
    '''
    Ajoute 0 ou 1 au dico de reponses (respectivement Non et Oui) En fonction de l'argument
    et passe à la question suivante

    - Idee personnelle (On avait avant une fonction plus0 et plus1, on les a combinés pour éviter la redondance) par Raphaël
    '''
    global n
    global dico_Reponses
    global msg_Principal
    
    
    dico_Reponses[liste_Questions[n][1]] = arg
    n +=1
    if not est_termine(b1,b2):
        msg_Principal.configure(text = liste_Questions[n][0])
        


def est_termine(btn_1,btn_2):
    global btn_Ok
    global msg_Principal
    '''
    Verifie si le QCM est terminé (dernière question répondue). Si c'est le cas, On affiche un message puis retour bouton ok 

    - Idee de Raphaël et Nathan pour terminer le qcm (une simple recherche sur les longueurs suffit)
    '''
    if n >= len(liste_Questions):
        btn_1.destroy()
        btn_2.destroy()
        btn_Ok.place(relx=0.5,rely=0.5,anchor =CENTER)
        msg_Principal.configure(text = "Merci d'avoir répondu aux questions, Veuillez continuer")
        modifier_fichier_dico("REPONSE_QCM", dico_Reponses)# Rajoute les lignes au option reponses_qcm dès qu'on quitte la page de QCM
        btn_Ok.configure(text="Lancer la recherche")
        return True


def retour_pages(fenetre,btn,cle=True):
    """
    Fonction qui passe d'une page à la page w_question ou qui supprime la page d'aide si présente

    - Idee de la clé de Raphaël pour pouvoir appeler cette fonction à plusieurs reprises avec des cas différents
    """
    
    if cle==True : # Si on a juste une page d'aide
        fenetre.destroy()
        change_etat_btn(btn)
    else:
        efface_fenetre(fenetre)
        fenetre_question(fenetre)


def change_etat_btn(bouton):
    '''
    Fonction qui change l'état du bouton utilisé

    - Nécessité de se renseigner sur la documentation de CustomTkinter par Tom Schimansky 
    'https://github.com/TomSchimansky/CustomTkinter/wiki/CTkButton'
    '''
    try :
        if bouton and bouton.cget("state") == NORMAL : # Récupère l'attribut et le change
            bouton.configure(state=DISABLED)
        else:
            bouton.configure(state=NORMAL)
    except TclError: # Si le boutton n'existe plus
        return None



'''
FONCTIONS PRICIPALES
'''

# Seconde page
def fenetre_questionnaire(win,option = None):
    """
    Affiche la premiere page :
        - Si le dico REPONSE_QCM dans ./donnees/options.txt est incomplet ou vide, lance le Qcm
        - Sinon (les données sont présentes), propose de passer à la suite (fin du Qcm)

    - L'idée du Questionnaire nous est venu après une discussion entre les membres et le professeur 
    sur un moyen de rendre l'expérience unique à l'utilisateur
    Cette fenêtre était la première créée dans notre programme, cette fonction ne crée plus la fenêtre désormais
    """
    # initialisation des variables utilisées
    global btn_Ok
    global n
    global msg_Principal
    n = len(liste_Questions) 
    
    efface_fenetre(win) # efface certains widgets pour rajouter ceux qui nous intéresse
    
    # Création des widgets :
    # On doit recréer le message principal pour éviter une erreur de modification
    msg_Principal = interface.CTkLabel(fenetrePrincipale, text="Les données utilisateur sont présentes, veuillez continuer.", 
                                   width = 1000, font =(polices[0],18), justify=CENTER)
    # Boutton :
    btn_Ok = interface.CTkButton(win, height=int(win.winfo_screenheight()/10), command=lambda: avancer(win), text="Lancer la recherche",font=(polices[0],30, 'bold'),image=image_btn_chercher) # Commence le Qcm ou continue le programm

    # Placement des widgets :
    msg_Principal.place(relx= 0.5, rely=0.4, anchor = CENTER) # anchor place relativement à un point (ici le centre) et relx/rely place avec un % de x et de y de ce point
    btn_Ok.place(relx=0.5, rely=0.5,anchor=CENTER) # place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place)        


    if option == None :
        msg_Principal.configure(text = "Bienvenue !  Nous allons commencer par une étude de vos préférences.")
        btn_Ok.configure(text = "Lancer Le Questionnaire")
        n = 0

    win.mainloop() # pour fermer la fenetre


def page_info(btn):

    """
    Ouvre Une page d'informations avec un texte

    - Pour la TextBox, ce code python de Tom Schimansky nous a aidé à la reproduire
    'https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py'
    le reste vient de Raphaël
    """

    # Constante 
    texte_info=("Bonjour ! Bienvenue sur LifeScore, logiciel permettant d'attribuer une note sur 100 à chaque communes de France."
    + " Pour commencer, nous réalisons un questionnaire afin de déterminer vos préférences."
    + " Pour chaques critères (correspondant à un fichier CSV), on définit une note sur 100 ainsi qu'un coefficient propre à lui même en fonction de vos réponses. "
    + " Nous essayons de réunir un maximum d'informations afin d'avoir une meilleure précision. "
    + "\n\n Attention : Ce logiciel a seulement pour but d'informer les personnes et nous ne voulons en rien nuire à aucune commune de France.") #Pour une meilleure clarté du code j'écrit ce str ainsi

    # Initialisation de la page
    change_etat_btn(btn)
    page_Info = interface.CTkToplevel() # Toplevel de CTkinter
    page_Info.title('LifeScore  |  Informations')
    page_Info.iconphoto(False, icone)
    page_Info.minsize(width=int(510*4/3), height=500)
    page_Info.resizable(False, False)

    # Création des widgets
    msg_Titre = interface.CTkLabel(page_Info, text="INFORMATIONS", font= (polices[1], 40, 'bold'), text_color="#29A272")
    box_Infos = interface.CTkTextbox(page_Info, width = 580 , corner_radius=0,border_width=2,border_color='grey')
    box_Infos.insert("0.0", text = texte_info)
    box_Infos.configure(state = "disabled", font = (polices[0],18),
                       wrap="word") # disabled pour pas qu'on puisse écrire, "word" pour le retour a la ligne
    btn_Compris = interface.CTkButton(page_Info, height=int(page_Info.winfo_screenheight()/10), command=lambda:retour_pages(page_Info,btn), text="Compris",font=(polices[0],30, 'bold'))

    # Placement des widgets
    msg_Titre.place(relx=0.5, rely=0.1, anchor = CENTER)
    box_Infos.place(relx=0.05,rely=0.2)
    btn_Compris.place(relx = 0.5, rely = 0.8, anchor = CENTER)

    # Protocole de fermeture
    page_Info.protocol("WM_DELETE_WINDOW", lambda:retour_pages(page_Info,btn)) 

    page_Info.mainloop()


def page_parametres(bouton):
    """
    Fonction qui ouvre la page de paramètres avec dessus :
        - Option pour modifier la fréquence de mises à jour
        - Volet pour changer le style de l'application 
        - Un bouton pour fermer la page
        - Suprimmer donnes d'utilisateur

    - Idee de Nathan et Raphaël, application CTk par Raphaël et application des fréquences de MaJ par Thor & Nathan

    """
    change_etat_btn(bouton) # Bloque le bouton paramètre sur la page principale jusqu'à que la page paramètre soit fermée
    
    # Création de la fenêtre
    
    fenetre_Param = interface.CTkToplevel()
    fenetre_Param.title('LifeScore  |  Paramètres')
    fenetre_Param.iconphoto(False, icone)
    fenetre_Param.geometry("680x650") # 768
    fenetre_Param.resizable(False, False)

    # Création des widgets :

    # Tous les messages présents :
    msg_Titre = interface.CTkLabel(fenetre_Param, text="PARAMÈTRES", font= (polices[1], 40, 'bold'), text_color="#29A272")
    msg_Frequence = interface.CTkLabel(fenetre_Param, text="FRÉQUENCE DE MISE À JOUR", font= (polices[0], 25), text_color="#29A272")
    msg_Verif = interface.CTkLabel(fenetre_Param, text=f"Dernière Vérification : {date_derniere_verification()}", font= (polices[0], 16), text_color="#646464")
    msg_Apparence = interface.CTkLabel(fenetre_Param, text="APPARENCE DE L'APPLICATION", font= (polices[0], 25), text_color="#29A272")
    msg_Donnees = interface.CTkLabel(fenetre_Param, text="DONNÉES UTILISATEUR", font= (polices[0], 25), text_color="#29A272")
    msg_General = interface.CTkLabel(fenetre_Param,text="Le bouton de suppression des données fermera le programme.", width = 50, font =(polices[0],18)) # font = taille + police, justify comme sur word

    # Tous les boutons présents :
    btn_Confirm_frequence = interface.CTkButton(fenetre_Param, width = 7, 
                                            command=lambda:modifier_fichier_dico("FREQ_MAJ", round(abs(float(entree_Frequence_maj.get()))*86400),"donnees/options.txt", msg_General)
                                            if est_nombre(entree_Frequence_maj.get()) \
                                            else msg_General.configure(text = "Vous devez entrer un nombre !"), # "\" permet un retour à la ligne dans le code
                                            text="Confirmer") # modifier_fichier_dico() se trouve dans classes.py
    btn_Supprimer_donnees = interface.CTkButton(fenetre_Param, width = 134, height = 42,
                                                command=supprimer_donnees_utilisateur,
                                                text="SUPPRIMER",
                                                font=(polices[0], 18))
    
    
    '''
    Désactive le bouton SUPPRIMER des données si on a toujours rien enregistré.
    Conçu par Nathan
    '''
    if lire_fichier_dico("REPONSE_QCM") == {} :
        btn_Supprimer_donnees.configure(state='disabled')
    else :
        btn_Supprimer_donnees.configure(state='normal')
    
    
    btn_Changements = interface.CTkButton(fenetre_Param,height=60,
                                                        width=550,  
                                                        command=lambda:retour_pages(fenetre_Param,bouton), 
                                                        text="FERMER LA PAGE",
                                                        font=(polices[0],30, 'bold'))
    
    # Autres (les entrées et les volets "switch") :
    
    # Pour récuperer la fréquence des màj et le transformer en jours
    frequence_maj = int(lire_fichier_dico('FREQ_MAJ')/86400)
    
    entree_Frequence_maj = interface.CTkEntry(fenetre_Param, placeholder_text=frequence_maj, width=51, font= (polices[0], 18))
    switch_Apparence = interface.CTkOptionMenu(fenetre_Param, values=["Système", "Sombre", "Clair"],command=change_apparence_page)

    # Traduction en direct, pour voir directement quel mode on a selectioné 
    apparence = lire_fichier_dico("APPARENCE")
    if apparence == "System" : apparence = "Système"
    elif apparence == "Light" : apparence = "Clair"
    elif apparence == "Dark" : apparence = "Sombre"
    
    switch_Apparence.set(apparence) # La valeur initiale (à titre indicatif) 


    # Placement des widgets (Dans l'ordre dans lequel ils sont affichés) :
    
    msg_Titre.place(relx=0.5, rely=0.064, anchor = CENTER)

    # La fréquence de mise à jour
    msg_Frequence.place(relx = 0.02, rely = 0.15)
    entree_Frequence_maj.place(relx = 0.06, rely = 0.20)
    btn_Confirm_frequence.place(relx = 0.195, rely = 0.22, anchor = CENTER)
    msg_Verif.place(relx=0.06, rely=0.24)

    # L'apparence de l'application 
    msg_Apparence.place(relx = 0.02, rely = 0.33)
    switch_Apparence.place(relx = 0.06, rely = 0.38)

    # La suppression des données 
    msg_Donnees.place(relx=0.02, rely=0.51)
    btn_Supprimer_donnees.place(relx=0.06, rely=0.56)

    # Fin de la page
    msg_General.place(relx=0.5,rely=0.75,anchor = CENTER)
    btn_Changements.place(relx = 0.5, rely = 0.87, anchor = CENTER)

    fenetre_Param.protocol("WM_DELETE_WINDOW", lambda:retour_pages(fenetre_Param,bouton))# Si on ferme avec la croix, lance retour_pages()
    fenetre_Param.mainloop()


def date_derniere_verification() -> str:
    '''
    Retourne la date formatée de la dernière mise à jour
    
    - Idee de Thor avec la documentation du module Time 'https://docs.python.org/3/library/time.html'
    '''
    derniere_maj_sec = lire_fichier_dico("DERNIERE_MAJ") # Cette fonction provient de classes.py
    if derniere_maj_sec == 0 :
        return "aucune vérification"
    return strftime("le %d/%m/%Y", localtime(derniere_maj_sec)) # Formate la donnée en jour mois année, heure minute


def supprimer_donnees_utilisateur():
    '''
    Efface les choix de qcm dans le fichier ./donnees/options.txt et le cache de l'application
    (Si l'utilisateur souhaite refaire le questionnaire)

    - Idee de Thor
    '''
    modifier_fichier_dico("REPONSE_QCM", {}) # remet les choix du qcm a vide (donc on devra le refaire)
    os.remove(repertoire_donnees+'/cache.txt')
    sys.exit() # Ferme le programme pour éviter de potentielles erreurs


def change_apparence_page(choix):
    '''
    Change l'apparence de l'interface (Sombre ou Clair)
    (Système revient à ce que l'ordinateur a pour valeur par défault)

    - Idee de transformation du texte et de l'écriture par Raphaël
    '''

    if choix in ["Système","Sombre","Clair"] : # Si on veut changer les pages
        if choix == "Système": choix = "System"
        elif choix == "Sombre": choix = "Dark"
        else:choix = "Light"

        modifier_fichier_dico('APPARENCE', choix)
        interface.set_appearance_mode(choix)




# Troisième page
def fenetre_question(fenetre):
    '''
    Affiche la seconde page qui contient la requête de la ville

    - Léger calque sur fenetre_questionnaire()
    '''
    fenetre.title('LifeScore  |  Requête de la commune') # Changement du titre de la fenêtre
    fenetre.iconphoto(False, icone)


    # Création des widgets
    entree = interface.CTkEntry(fenetre,placeholder_text="ex : Béziers ",width=int(500/3), font = (polices[0],18))
    msg_Ville= interface.CTkLabel(fenetre, text="Veuillez saisir la ville recherchée", width = 1000, font =(polices[0],20), 
                                  justify=CENTER) # font = taille + police, justify comme sur word
    btn_Arrondissement = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10),command=lambda: page_arrondissement(btn_Arrondissement), 
                                             text="",font=(polices[0],30, 'bold'),image=image_btn_aide, fg_color='transparent',hover = False) # Boutton d'aide arrondissements
    btn_Entree = interface.CTkButton(fenetre,height=int(fenetre.winfo_screenheight()/10), 
                                     command=lambda: analyse_ville(entree,msg_Ville,fenetre,btn_Entree),text="Recherche ",font=(polices[0],30, 'bold'),image=image_btn_chercher)
    
    # Placement des widgets
    msg_Ville.place(relx= 0.5, rely=0.45, anchor = CENTER)
    entree.place(relx=0.5, rely= 0.55, anchor=CENTER)
    btn_Entree.place(relx=0.5, rely= 0.65, anchor = CENTER)
    btn_Arrondissement.place(relx=0.9, rely=0.05 ,anchor = NE)


def page_arrondissement(btn):

    '''
    Ouvre Une fenêtre d'aide avec un texte et un bouton de retour

    - Copie de la fonction page_info() remaniée pour les arrondissements par Raphaël 
    '''
    # Initialisation
    fenetre_Aide = interface.CTkToplevel()
    fenetre_Aide.title('LifeScore  |  Aide arrondissements')
    fenetre_Aide.iconphoto(False, icone)
    fenetre_Aide.resizable(False, False)
    fenetre_Aide.minsize(width=int(510*4/3), height=500)

    change_etat_btn(btn) # Bloque le bouton d'accès à cette page
    texte_aide=("""Si Votre ville possède des arrondissements (ex : Paris) :
    - Si vous ne saisissez que le nom de la ville, le premier arrondissement sera pris comme base"
    - Sinon, écrivez le nom de la ville comme cela : 
        Nom 1er Arrondissement / Nom Ne Arrondissement 
                (ex : Paris 2e Arrondissement)""")

    # Création des widgets
    msg_Titre = interface.CTkLabel(fenetre_Aide, text="AIDE", font= (polices[1], 40, 'bold'), text_color="#29A272")
    box_Aide = interface.CTkTextbox(fenetre_Aide, width = 580 , corner_radius=0)
    box_Aide.insert("0.0", text = texte_aide)
    box_Aide.configure(state = "disabled", font = (polices[0],18),wrap="word") # disabled pour pas qu'on puisse écrire, "word" pour le retour a la ligne
    btn_Compris = interface.CTkButton(fenetre_Aide, height=int(fenetre_Aide.winfo_screenheight()/10), command=lambda :retour_pages(fenetre_Aide,btn), text="Compris",font=(polices[0],30, 'bold'))
    
    
    # Placement des widgets
    msg_Titre.place(relx=0.5, rely=0.1, anchor = CENTER)
    box_Aide.place(relx=0.05,rely=0.2)
    btn_Compris.place(relx = 0.5, rely = 0.8, anchor = CENTER)


    # Protocole de fermeture de page
    fenetre_Aide.protocol("WM_DELETE_WINDOW", lambda:retour_pages(fenetre_Aide,btn))
    fenetre_Aide.mainloop()





def analyse_ville(entree,msg,fenetre,bouton = None):

    '''
    Récupère l'entrée, vérifie si la ville existe bien:
        - Si oui, continue vers la page suivante
        - Sinon, affiche un message d'erreur
    
        - L'idée de créer une classe de Donnees est détaillée dans classes.py , le reste est de Raphaël
    '''
    global Donnees_ville
    
    ville = entree.get()
    Donnees_ville = Donnees(ville)
    if Donnees_ville.est_commune_france(msg):
        if bouton != None:
            bouton.configure(state=DISABLED) # Pour empêcher de lancer plusieurs fois
        msg.configure(text ='Cacul de la note de la commune et de ses "voisins"')
        fenetre.update()
        score = Donnees_ville.note_finale()
        liste_Voisins = Donnees_ville.k_plus_proches_voisins(10,msg,fenetre)
        
        efface_fenetre(fenetre,"Efface_reste") # Enlève même le bouton paramètre et les pages d'aide pour ne pas obstruer l'écran
        
        fenetre_resultat(Donnees_ville,fenetre,liste_Voisins,score)






# Dernière page
def fenetre_resultat(ville,win,liste_Dix_villes,score):
    '''
    Affiche la dernière page qui contient le score et le bouton pour revenir

    ville est un objet de la classe Donnees précédemment créé après avoir appuyé sur "recherche"

    - Reprise de fenetre_questionnaire() et fenetre_question() remaniée par Raphaël, la carte est de Thor avec l'api 'https://mt0.google.com'
    '''
    
    # Initialisation 
    win.title(f'LifeScore  |  Commune de {str(ville).capitalize()}')
    if systeme_exploitation == 'Windows' :
        fenetrePrincipale.state('zoomed')

    # Données 

    dico_Notes = Donnees_ville.notes_finales 
    bonus,malus = avantages_inconvenients(dico_Notes) 
    box_Voisins = interface.CTkTextbox(win, width = 580 ,height = 150, corner_radius=0)
    texte = "Notes des communes voisines :\n"

    for nom,note in liste_Dix_villes:
        texte += f'\n - {str(nom)} : {str(note)}/100'
    box_Voisins.insert("0.0", text = texte)
    box_Voisins.configure(state = "disabled", font = (polices[0],24),wrap = 'word')
    

    # Transformation des données en texte
    msg_Ville = interface.CTkLabel(win,text=str(ville).capitalize(), width = 500, font=(polices[1],taille_police(str(ville)), 'bold'), justify=CENTER)
    msg_Ville.place(relx=0.5,rely=0.1,anchor=CENTER)
    plus, moins = plus_et_moins(bonus,malus) # Récupère les données et les transforme en 2 str à Afficher
    box_Voisins.place(relx = 0.5, rely = 0.85, anchor = CENTER)

    """
    CARTE DE LA COMMUNE

    - Source et documentation: https://github.com/TomSchimansky/TkinterMapView (la liste des cartes possibles est tout en bas du README)
    - Idée de Nathan, implémenté par Thor
    """
    if est_connecte("https://mt0.google.com/"): # On verifie qu'il y a un connection au serveUr o% on va recuperer la carte

        carte_Ville = TkinterMapView(win, width=0.4*win.winfo_width(), height=0.4*win.winfo_height()) # On declare l'objet de la carte avec Ses tailles respectives
        carte_Ville.set_address(f"{str(ville)[:-1] if est_nombre(str(ville)[-1]) else str(ville)}, France", marker=True,text=str(ville)) # Insère le nom comme adresse (et formate pour les arrondissements)
        carte_Ville.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=22) # On decide quel carte et zoom on va utiliser
        carte_Ville.place(relx=0.3, rely=0.18)
    else:
        win.iconphoto(False, icone_connexion) # Affiche l'icone d'erreur
    


    '''
    ANIMATION DU SCORE FINAL
    
    - Idée de Nathan détaillée dans fonction_animation_score()
    - Les avantages et inconvénients sont de Raphaël
    '''
    
    if score != 'N/A':
        
        # Transformations
        score_total_animation = int(score)
        score = str(score)
        
        # Mise en place du reste du texte, pour éviter une surcharge du nombre d'elements à rafraichir
        msg_Bonus = interface.CTkLabel(win,text=plus, width = 200, font =(polices[0],23, 'bold'), justify=LEFT)
        msg_Malus = interface.CTkLabel(win,text=moins, width = 200, font =(polices[0],23,'bold'), justify=LEFT)
        msg_Note = interface.CTkLabel(win, text=0, text_color=couleur_score(0), font=(polices[1], 80, 'bold'), justify=CENTER) # On initialise
        msg_Annonce_note = interface.CTkLabel(win, text='Note :', font=(polices[1], 50, 'bold'), justify=CENTER)

        # Placements
        msg_Annonce_note.place(relx=0.9,rely=0.1, anchor=CENTER)
        msg_Note.place(relx=0.9,rely=0.2, anchor=CENTER)# Nord Est
        msg_Bonus.place(relx = 0.15, rely = 0.45,anchor = CENTER)
        msg_Malus.place(relx=0.85,rely=0.45,anchor = CENTER)
        
        win.update()
        
        change_etat_btn(btn_Quitter) # Pour éviter des problèmes d'animations
        change_etat_btn(btn_Parametre)
        
        # Pour chaque entier naturel jusqu'à notre note
        for i in range(score_total_animation+1) :
                            
            couleur = couleur_score(i)

            msg_Note.configure(text=str(i), text_color=couleur)          
            
            # Mise à jour de la page
            win.update()
            sleep(fonction_animation_score(i, score_total_animation))
 
        change_etat_btn(btn_Quitter) # Pour réactiver les bouttons
        change_etat_btn(btn_Parametre)

        btn_Donnees = interface.CTkButton(win,height=int(win.winfo_screenheight()/10), command=lambda:page_detail(btn_Donnees,dico_Notes),
                                      text= "Détails", font=(polices[0],20, "bold"))
        btn_Donnees.place(relx = 0.38,rely = 0.65, anchor = CENTER) # Pour un détail des données

            

    # Si on a pas de note
    else:
        
        # Informations :
        msg_Note = interface.CTkLabel(win, text=f'Note : \n' +score +'  ' ,text_color ='grey', font =(polices[1],60),
                                       justify=CENTER) # Score est ici égal à 'N/A'
        msg_NonAttribue = interface.CTkLabel(win,text="Nous n'avons pas pu récuperer les informations de cette ville",
                                              width = 1000, font =(polices[0],30), justify=LEFT)
        
        msg_Note.place(relx=0.9,rely=0.1, anchor=CENTER)# Nord Est
        msg_NonAttribue.place(relx = 0.5, rely = 0.9,anchor = CENTER)

    # Bouton de Retour
    btn_Retour = interface.CTkButton(win,height=int(win.winfo_screenheight()/10), command=lambda:retour_pages(win,None,False),
                                      text= "Noter une autre ville ", font=(polices[0],20, "bold"),image=image_btn_chercher)
    btn_Retour.place(relx = 0.56,rely = 0.65, anchor = CENTER)

def taille_police(chaine):
    '''
    Fonction qui retourne une taille de police adéquate en fonction du nombre de caractères et d'une fonction 
    f(x) = (-ln(x-4) + 10) * 5
    idée : Raphaël avec les cours de Mathématiques et plusieurs tests sur la calculatrice graphique Desmos
    '''
    longueur = len(chaine)
    if longueur <= 4: # Le ln() n'est pas défini pour X < 0 donc notre fonction est définie sur ]4; +oo[
        return 60
    else:
        taille = 5 * (-math.log(longueur-4)+10)
    return taille


def couleur_score(note):
    '''
    Fonction qui renvoie la note en une couleur hexadécimale. Du Rouge au Vert

    - Idee de Raphaël complétée par Nathan l'idée est de modifier des valeurs de rouge et de vert en fonction de la note
    - Basé sur la fonction fonction_animation_score de Nathan
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
            
        return '#{:02x}{:02x}{:02x}'.format(r, g, b) # Permet de passer du décimal à l'hexadécimal 

    else :
        return '#808080' # Couleur grise pour le manque de note
    

def fonction_animation_score(x, total) :
    '''
    Calcule le temps entre deux entiers pour le score total (pour l'animation de la note)
    x,total sont des entiers et la fonction renvoie un flottant pour donner la "vitesse" de changement

    - Idée et réalisation par Nathan, aidé par nos cours de mathématiques sur les fonctions et la trigonométrie
    '''
    # la vitesse "ralenti" plus on s'approche de la valeur de la note
    
    x = (x/total)*5
    x_pour_cos = x + 1.2
    return ((math.cos(x_pour_cos))+1.2)*0.03




def avantages_inconvenients(dic):
    '''
    Prend les 5 meilleurs et pires aspects de la ville pour indiquer des avantages et inconvénients à y habiter

    - Idée de Raphaël en utilisant les algorithmes de recherche de maximum et minimum de l'année de première
    '''

    # Initialisation
    liste = [''] * 10 # On travaillera avec des tuples (nom,note)
    cle_maxi = cle_mini = "Valeur initiale"    
    i = j = 0 # i pour les avantages, j pour les inconvénients

    while (i < 5 and i < len(dic)) or (j < 5  and j < len(dic)): # Pour pouvoir parcourir et les avantages et les inconvénients même si un s'arrête
        mini = maxi = 50 # Les malus seront compris entre 0 et 50, les bonus entre 50 et 100
        
        for cle in dic.keys(): # Algorithme de maximum et de minimum mélangés
            if dic[cle] > maxi and not (cle,int(dic[cle])) in liste:
                maxi = dic[cle]
                cle_maxi = cle
                
            elif dic[cle] < mini and not (cle,int(dic[cle])) in liste:
                mini = dic[cle]
                cle_mini = cle

        if (cle_maxi,int(dic[cle_maxi])) not in liste: # Ceci permet d'éviter d'avoir plusieurs fois le meme avantage
            liste[i] = (cle_maxi,int(dic[cle_maxi]))   # ou inconvénient dans le cas où il y a moins de 5 notes 
        if (cle_mini,int(dic[cle_mini])) not in liste: # au dessus de 50 ou moins de 5 notes en dessous de 50
            liste[-j-1] = (cle_mini,int(dic[cle_mini])) 
        i += 1 # Il est interdit d'écrire i,j += 1
        j += 1
                
    return liste[:4],liste[5:] # Les 5 premiers tuples seront les avantages, les 5 derniers les inconvénients


def plus_et_moins(pl,mal):
    '''
    Transforme en Str formaté pour CTk les avantages et inconvénients

    - Idee de Raphaël 
    '''

    plus, moins = "Les Avantages sur 100: ", "Les Inconvénients sur 100:" # Texte a retourner
    for val_plus in pl:
        if val_plus != '': # Il est possible que la ville n'aie pas 5 avantages mais moins
            plus = plus + "\n - " + val_plus[0] + f' : {val_plus[1]}'

    for val_moins in mal:
        if val_moins != '':
            moins = moins + "\n - " + val_moins[0] + f' : {val_moins[1]}'
        
    return plus,moins


def page_detail(btn,dictionnaire):
    '''
    Ouvre la fenêtre qui montre le détail de la note pour chaque CSV

    - Copie de la fonction page_info() mise à jour avec les notes par Raphaël 
    '''
    # Initialisation
    page_Detail = interface.CTkToplevel()
    page_Detail.title('LifeScore  |  Détail de la note')
    page_Detail.iconphoto(False, icone)
    page_Detail.resizable(False, False)
    page_Detail.minsize(width=int(510*4/3), height=500)

    change_etat_btn(btn) # Bloque le bouton d'accès à cette page
    texte_Note = ""
    liste_Notes = sorted(dictionnaire.items(), key=lambda x: x[1], reverse = True) # Cela permet de trier un dictionnaire par ses clés
    for tpl in liste_Notes :
        texte_Note += f"{tpl[0]} : {int(tpl[1])} / 100 \n"

    # Création des widgets
    msg_Titre = interface.CTkLabel(page_Detail, text="Détail des notes", font= (polices[1], 40, 'bold'), text_color="#29A272")
    box_Detail = interface.CTkTextbox(page_Detail, width = 580 , corner_radius=0)
    box_Detail.insert("0.0", text = texte_Note)
    box_Detail.configure(state = "disabled", font = (polices[0],18),wrap="word") # disabled pour pas qu'on puisse écrire, "word" pour le retour a la ligne
    btn_Compris = interface.CTkButton(page_Detail, height=int(page_Detail.winfo_screenheight()/10), 
                                      command=lambda :retour_pages(page_Detail,btn), 
                                      text="Compris",font=(polices[0],30, 'bold'))
    
    
    # Placement des widgets
    msg_Titre.place(relx=0.5, rely=0.1, anchor = CENTER)
    box_Detail.place(relx=0.05,rely=0.2)
    btn_Compris.place(relx = 0.5, rely = 0.8, anchor = CENTER)


    # Protocole de fermeture de page
    page_Detail.protocol("WM_DELETE_WINDOW", lambda:retour_pages(page_Detail,btn))
    page_Detail.mainloop()

# Page d'erreur 
def fenetre_erreur(fenetre):
    '''
    Affiche la page d'erreur qui signale le problème

    - Calque sur fenetre_questionnaire() par Raphaël
    '''
    global msg_Principal
    
    # Initialisation
    fenetre.title('LifeScore  |  Erreur')
    fenetre.iconphoto(False, icone_connexion)
    
    # Création des widgets

    msg_Principal =  interface.CTkLabel(fenetre, text="Une erreur s'est produite, le programme n'a pas pu se lancer.\nVérifiez votre connexion et réessayer.", 
        width = 1000, font =(polices[0],18), justify=CENTER) # font = taille + police justify comme sur word
    btn_Parametre = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10),command=lambda : page_parametres(btn_Parametre), text="",font=(polices[0],30, 'bold'),image=image_btn_parametres, fg_color='transparent',hover = False)

    # Placement des widgets
    msg_Principal.place(relx= 0.5, rely=0.4, anchor = CENTER) # Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    btn_Parametre.place(relx=0.1, rely=0.9, anchor = SW)  


# crée (s'il n'est pas présent) le dossier "donnees"
if not os.path.exists(repertoire_donnees):
    os.makedirs(repertoire_donnees)


'''
RECUPERATION STYLE

- Fonction lire_fichier_dico fait par Thor dans classes.py

'''

# Cree les fichiers suivants et remplis par la valeur par default s'ils ne sont pas là
style = lire_fichier_dico('APPARENCE')
interface.set_appearance_mode(str(style))  # Modes: system (default), light, dark
interface.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green (nous avons choisis le vert)



'''
CREATION DE La FENETRE PRINCIPALE

- Idée de Raphaël récupérée d'anciens travaux Tkinter complétés par la documentation de CustomTkinter 
'''

# Initialisation
fenetrePrincipale = interface.CTk() # fenetre de tkinter
icone = PhotoImage(file = nom_du_repertoire+'/systeme/icones/logo.png') # Icone provisoire (on doit la créer après la création de la fenêtre)
icone_connexion = PhotoImage(file = nom_du_repertoire+'/systeme/icones/pas-internet.png')

fenetrePrincipale.title('LifeScore  |  Menu principal')
fenetrePrincipale.iconphoto(False, icone)
fenetrePrincipale.minsize(width=1280  , height=848) # Taille minimum de la fenetre
#fenetrePrincipale.resizable(False,False)


if systeme_exploitation == 'Windows' :
    fenetrePrincipale.state('zoomed')

else :
    fenetrePrincipale.state('normal')



credits_texte = ("""                           Réalisé par :
Nathan Bosy     : Gestion des données, calculs & compatibilté
Raphaël Farenc  : Interface graphique & interprétation des notes
Thor N          : Calcul des coefficients & API
Frédéric Marquet: Recherches pour la base de données""")


# Création des widgets
btn_Ok = interface.CTkButton(fenetrePrincipale, height=int(fenetrePrincipale.winfo_screenheight()/10), 
                             command=lambda:fenetre_telechargement(btn_Ok,fenetrePrincipale, btn_Parametre, btn_Info), text="Continuer",font=(polices[0],30, 'bold')) # appele la fonction question1
msg_Principal = interface.CTkLabel(fenetrePrincipale, text="Bienvenue dans LifeScore, nous allons procéder à\nune vérification des fichiers.", 
                                   width = 1000, font =(polices[0],18), justify=CENTER)
logo = interface.CTkImage(light_image=Image.open(nom_du_repertoire +'/systeme/icones/gros-logo.png'), size=(400, 200))
btn_Nul = interface.CTkButton(fenetrePrincipale,image = logo,fg_color="transparent",hover = False,text =  "") # Contient le logo
btn_Quitter = interface.CTkButton(fenetrePrincipale,height=int(fenetrePrincipale.winfo_screenheight()/10), command=fenetrePrincipale.destroy,
                                    text= "", font=(polices[0],30, 'bold'), image=image_btn_quitter, fg_color='transparent',hover = False)
credits = interface.CTkLabel(fenetrePrincipale, width = 600 , corner_radius=2,text = credits_texte,anchor = W,fg_color=('#D0D0CE','#141414'),
                                font = ('Courier',18), pady=1,justify=LEFT)
btn_Info = interface.CTkButton(fenetrePrincipale, height=int(fenetrePrincipale.winfo_screenheight()/10),
                                command=lambda: page_info(btn_Info),text = '',font=(polices[0],30, 'bold'),
                                image=image_btn_aide, hover = False, fg_color='transparent') # Ouvre la page d'instructions
btn_Parametre = interface.CTkButton(fenetrePrincipale, height=int(fenetrePrincipale.winfo_screenheight()/10),
                                    command=lambda : page_parametres(btn_Parametre), text="",font=(polices[0],30, 'bold'), 
                                    image=image_btn_parametres, fg_color='transparent',hover = False) # Ouvre la page de paramètres




# Placement des widgets
btn_Nul.place(relx=0.16,rely=0.16,anchor = CENTER) # Il devra rester pendant toute l'exécution du programme
btn_Quitter.place(relx=0.9, rely=0.9, anchor = SE) # Lui aussi
msg_Principal.place(relx= 0.5, rely = 0.4,anchor = CENTER)
btn_Ok.place(relx=0.5, rely=0.5,anchor=CENTER) # Place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place)        
btn_Parametre.place(relx=0.1, rely=0.9, anchor = SW) # SW = SouthWest (en bas à gauche)
credits.place(relx=0.5,rely=0.9, anchor = S)
btn_Info.place(relx=0.9, rely=0.05 ,anchor = NE) # NE = NorthEast (en haut à droite)

fenetrePrincipale.mainloop()
