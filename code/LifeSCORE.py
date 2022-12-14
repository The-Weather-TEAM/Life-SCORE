'''

                      [LIFESCORE.PY]
                 CODE PRINCIPAL DE LIFE-SCORE



Code Tkinter ne pas oublier quand on crée des variable de les commenter (bon nom + fonction)
réferences : 
    - Les boutons s'écrivent btn_NOM
    - Les fenêtres s'écrivent windowNOM
    - Les textes (classe customtk.CTkLabel) s'écrivent msg_NOM
    - Les listes s'écrivent list_NOM
    - Les dictionnaires s'écrivent dico_NOM
    - Les url de csv ou d'API s'écrivent url_csv_NOM ou url_api_NOM


'''



from tkinter import *
import tkinter.font
#from urllib.request import urlopen #pour les photos (peut etre enlever)
from classes import * #Import de nos classes créées

import requests
from requests.exceptions import ConnectionError #Pas sûr de l'utilité là

#from PIL import ImageTk, Image #Pour l'esthétique
import customtkinter as customtk
import os

with open(os.path.dirname(__file__) +'/data/style.txt') as txt:
    style = txt.read()
customtk.set_appearance_mode(str(style))  # Modes: system (default), light, dark
customtk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


'''
LANCEMENT DU PROGRAMME 
     [UPDATE.PY]
      (Nathan)

'''
import update

#erreur_maj = True si et seulement si il n'y a pas de données sur l'ordinateur et
#                   si il n'y a pas d'accès à internet
erreur_maj = update.executer()
#erreur_maj = False
# Si erreur_maj = False, on lance le programme
# Nathan : il foudrait après faire un else avec tkinter pour informer que le code ne se lance pas
if not erreur_maj :





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
        windowQCM = customtk.CTk() #fenetre de tkinter
        windowQCM.title('Accueil - QCU')
        windowQCM.minsize(width=768, height=500) #768 = taille minimum de la fenetre
        windowQCM.state('zoomed')

        #widgets
        msg_principal =  customtk.CTkLabel(windowQCM, text="Bienvenue, nous allons commencer avec un petit test", width = 1000, font =('Bold',18), justify=CENTER) #font = taille + police justify comme sur word
        msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
        
        #boutons 
        
        #bouton_explication/aide
        btn_aide  = customtkinter.CTkButton(windowQCM, height=int(windowQCM.winfo_screenheight()/15),command=lambda: aide(btn_aide), text="AIDE") #Bouton d'aide
        btn_aide.place(relx=0.9, rely=0.9 ,anchor = SE)
        #bouton ok Qui continue après le premier message
        btn_ok = customtkinter.CTkButton(windowQCM, height=int(windowQCM.winfo_screenheight()/15), command=lambda: avancer(windowQCM,btn_aide), text="OK") #appele la fonction question1
        btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) #place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place
        #bouton de paramètres qui ouvre une page pour les mises à jour et leur fréquence
        btn_parametre = customtkinter.CTkButton(windowQCM, height=int(windowQCM.winfo_screenheight()/15),command=lambda : parametres(btn_parametre,windowQCM), text="PARAMETRES")
        btn_parametre.place(relx=0.1, rely=0.9, anchor = SW)

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
        if n < len(list_Questions):
            btn_ok.place_forget() #Cache ce bouton
            btn_gauche = customtkinter.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/15), command=lambda: plus0(btn_gauche,btn_droite), text="Non")
            btn_droite = customtkinter.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/15), command=lambda: plus1(btn_gauche,btn_droite), text="Oui")
            btn_gauche.place(relx=0.40,rely=0.5,anchor=CENTER)
            btn_droite.place(relx=0.60,rely=0.5,anchor=CENTER)
            msg_principal.configure(text =f'{list_Questions[n][0]}') #change le texte du msg principal pour la question suivante

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
            msg_principal.configure(text = list_Questions[n][0])
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
            msg_principal.configure(text = list_Questions[n][0])
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
            msg_principal.configure(text = "Merci d'avoir répondu aux questions, Veuillez continuer")
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
        change_etat_btn(btn)
        windowAide = customtk.CTkToplevel() #fenetre de tkinter
        windowAide.title('Page 1bis - Aide')
        #window.tk.call('tk::PlaceWindow', window) A VOIR PEUT ETRE (PLACEMENT AU CENTRE ?)
        windowAide.minsize(width=int(510*4/3), height=384) #768
        windowAide.resizable(False,False) #Taille non modifiable !!! ON NE LE MET PAS !!!
        msg_aide = customtk.CTkLabel(windowAide, text=texte_aide, width = 1000, font =('Bold',10), justify=CENTER)
        msg_aide.place(relx = 0.5, rely = 0.3, anchor = CENTER)
        btn_compris = customtkinter.CTkButton(windowAide, height=int(windowAide.winfo_screenheight()/15), command=lambda:retour_pages(windowAide,btn), text="Compris !")
        btn_compris.place(relx = 0.5, rely = 0.7, anchor = CENTER)
        windowAide.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowAide,btn)) #Qu'on clique sur le btn ok ou qu'on ferme la page on obtient le meme resultat

        windowAide.mainloop()
        return windowAide


    def parametres(bouton,fenetre):
        """
        Fonction qui ouvre la page de paramètres avec dessus : (X  = pas fait, A = à Améliorer, V = fait)
            -Crédits                                                        X
            -Option pour modifier la fréquence de mises à jour              X
            -Volet pour changer le style de l'application                   V (placements à regarder)
            -Un bouton pour fermer la page et appliquer les changements     A
        """
        #fenetre.wait_window()     # block until window is destroyed
        change_etat_btn(bouton)
        windowParam = customtk.CTkToplevel()
        windowParam.title('Page 1ter - Parametres')
        windowParam.minsize(width=int(510*4/3), height=384) #768
        #windowParam.resizable(False,False) #Taille non modifiable !!! ON NE LE MET PAS !!!
        frame_tk =customtk.CTkFrame(windowParam) #On va y mettre les crédits

        message = customtk.CTkLabel(windowParam,text="Vous devrez relancer l'application pour actualiser les changements", width = 100, font =('Bold',18), justify=CENTER) #font = taille + police, justify comme sur word
        message.place(relx=0.1,rely=0.5,anchor = CENTER)

        """variable = customtk.StringVar()
        variable.set("System")"""
        switch_apparence = customtk.CTkOptionMenu(windowParam, values=["Système", "Sombre", "Clair"],command=change_apparence_page)
        switch_apparence.place(relx = 0.1, rely = 0.8, anchor = CENTER)
        btn_changements = customtk.CTkButton(windowParam,height=int(windowParam.winfo_screenheight()/15),  
                                                                    command=lambda:retour_pages(windowParam,bouton), 
                                                                    text="Appliquer les Changements")

        btn_changements.place(relx = 0.5, rely = 0.7, anchor = CENTER)

        windowParam.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowParam,bouton))#Meme effet que le bouton sauf que c'est si on ferme la page manuellement


        windowParam.mainloop()


    """def change_etat_page(*arg): #*arg nous laisse le choix de mettre n arguments 
        
        Fonction qui bloque tous les widgets d'une page tant qu'on est sur une autre (on ne peut pas bloquer une page entiere)
        
        for argument in arg:
            if argument.cget("state") == NORMAL : #Récupère l'attribut et le change
                argument.configure(state=DISABLED)
            else:
                argument.configure(state=NORMAL)"""



    def change_apparence_page(choix):
        if choix == "Système": choix = "System"
        elif choix == "Sombre": choix = "Dark"
        else:choix = "Light"

        #print("Option choisie (en anglais):", choix)
        with open(os.path.dirname(__file__) + '/data/style.txt', 'w') as txt:
            txt.write(choix)
        
            

    def retour_pages(window,btn,cle=0):
        """
        Fonction qui passe de la page actuelle à la page N°x
        """
        
        if cle==0 : #Si on a juste une page d'aide
            window.destroy()
            change_etat_btn(btn)
        else:
            window.destroy()
            w_question()


    def change_etat_btn(bouton):
        """
        Fonction qui change l'état du bouton utilisé
        
        Ca marche désormais :) 
        """
        if bouton.cget("state") == NORMAL : #Récupère l'attribut et le change
            bouton.configure(state=DISABLED)
        else:
            bouton.configure(state=NORMAL)


    #seconde page
    def w_question():
        """
        affiche la seconde page qui contient la requête de la ville
        """
        windowQuestion = customtk.CTk() #fenetre de tkinter
        windowQuestion.title('Seconde page - requête de la ville')
        windowQuestion.minsize(width=768, height=500)
        windowQuestion.state('zoomed') #Plein écran

        #input
        entree = customtk.CTkEntry(windowQuestion,placeholder_text="ex : Puissalicon ",width=int(500/3), font = ('Bold',18))
        entree.place(relx=0.5, rely= 0.55, anchor=CENTER)
        
        #message
        msg_ville= customtk.CTkLabel(windowQuestion, text="Veuillez saisir la ville recherchée", width = 1000, font =('Bold',18), justify=CENTER) #font = taille + police, justify comme sur word
        msg_ville.place(relx= 0.5, rely=0.45, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 

        btn_arrondissement = customtkinter.CTkButton(windowQuestion, height=int(windowQuestion.winfo_screenheight()/15),command=lambda: arrondissement(windowQuestion,btn_arrondissement), text="AIDE\nARRONDISSEMENTS") #Boutton d'aide arrondissements
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
        btn_entree = customtkinter.CTkButton(windowQuestion,height=int(windowQuestion.winfo_screenheight()/15), command=lambda: ville(entree,msg_ville,windowQuestion),text="Recherche")
        btn_entree.place(relx=0.5, rely= 0.65, anchor = CENTER)

        #windowQuestion.bind('KP_Return',ville(entree,msg_ville,windowQuestion)) #Appuyer sur entrée revient à appuyer sur le Bouton NE MARCHE PAS!


        windowQuestion.mainloop()


    def arrondissement(window,btn):

        """
        Ouvre Une fenêtre d'aide avec un texte et peut être des graphismes
        """
        change_etat_btn(btn) # bouton devient inactif grâce à l'autre fonction pour ne pas qu'on appuye dessus plusieurs fois
        texte_aide="""
        Si Votre ville possède plusieurs arrondissemnts (ex : Paris) :
        - Si vous saisissez uniquement le nom de la ville, le premier arrondissement sera pris comme base
        - Sinon, écrivez le nom de la ville comme cela : Nom_X avec X le numéro de l'arrondissement (ex : Paris_7)"""

        windowAide = customtk.CTkToplevel() #fenetre de tkinter
        windowAide.title('Page 2bis - Aide')
        #window.tk.call('tk::PlaceWindow', window) A VOIR PEUT ETRE (PLACEMENT AU CENTRE ?)
        windowAide.minsize(width=int(690*4/3), height=384) #768
        #windowAide.resizable(False,False) #Taille non modifiable !!! ON NE LE MET PAS !!!
        msg_aide = customtk.CTkLabel(windowAide, text=texte_aide, width = 1000, font =('Bold',14))
        msg_aide.place(relx = 0.5, rely = 0.3, anchor = CENTER)
        btn_compris = customtkinter.CTkButton(windowAide, height=int(windowAide.winfo_screenheight()/15), command=lambda :retour_pages(windowAide,btn), text="Compris !")
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
        print(ville)
        Donnees_ville = Donnees(ville)
        if Donnees_ville.is_commune_france_v2(msg): #Je dois ajouter Code/ au début car vscode lance mal le fichier sinon ça va
            msg.configure(text = "Veuillez patienter ...")
            #FAIRE TOUS LES CALCULS ICI :
            #ON OUVRE LA TROISIEME PAGE QU'APRES AVOIR FAIT TOUS LES CALCULS
            fenetre.destroy()
            w_score(Donnees_ville)






    #troisieme page
    def w_score(ville):
        """
        affiche la dernière page qui contient le score et le bouton pour revenir

        -    ville est un objet de la classe Donnees précédemment créé après avoirs appuyé sur recherche
        """
        windowScore = customtk.CTk() #fenetre de tkinter
        windowScore.title('Dernière page - Note de la ville')
        windowScore.minsize(width=1000, height=600)
        windowScore.state('zoomed') #Plein écran

        #Donnees PROVISOIRES !!!
        dico = {'Atout 1':9,'Atout 2':10,'Atout 3':5,'Atout 4':7,'Inconvéniant 1':-2,'Atout 5':4,'Inconvéniant 2':-1,'Inconvéniant 3':-2,'Inconvéniant 4':-1,'Inconvéniant 5':-1} #Exemple
        score = int(Donnees_ville.note_finale()) #Provisoire
        bonus,malus = trouve_bonus(dico), trouve_malus(dico) #Fonction non terminée (besoin du fichier qui fait les données)



        #Transfo des données en texte
        msg_ville = customtk.CTkLabel(windowScore,text=str(ville).capitalize(), width = 1000, font =('Bold',50), justify=CENTER)
        msg_ville.place(relx=0.5,rely=0.1,anchor=CENTER)
        plus, moins = plus_et_moins(bonus,malus) # Récupère les données et les transforme en 2 str à Afficher
        #print(plus,moins)


        couleur= couleur_score(score)
        score = str(score)

        #Textes :
        msg_note = customtk.CTkLabel(windowScore, text=f'Note : \n' +score +'  ' ,text_color =couleur, font =('Franklin gothic medium',40), justify=CENTER)
        msg_note.place(relx=0.9,rely=0.1, anchor=CENTER)#Nord Est
        msg_bonus = customtk.CTkLabel(windowScore,text=plus, width = 1000, font =('Bold',30), justify=LEFT)
        msg_malus = customtk.CTkLabel(windowScore,text=moins, width = 1000, font =('Bold',30), justify=LEFT)
        msg_bonus.place(relx = 0.15, rely = 0.7,anchor = CENTER)
        msg_malus.place(relx=0.8,rely=0.7,anchor = CENTER)


        #Bouton retour
        btn_Retour = customtkinter.CTkButton(windowScore,height=int(windowScore.winfo_screenheight()/15), command=lambda:retour_pages(windowScore,None,"page2"), text= "Noter une autre ", font=('Bold',20))
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
        #print(rouge,vert)
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





    # Objet image de tkinter 
    # photo = ImageTk.PhotoImage(data=raw_data)



    # appel de la fonction de la première page
    w_qcm() #ligne  à lancer a la fin

    #Lignes pour accéder à différentes page directement
    #w_question() 
    #w_score('Paris')
    #print(n,dico_Reponses,msg_principal)

else: #Il est impossible de traiter les fichiers qui sont inexistants puisqu'on a pas internet
    #fenêtre
    windowError = customtk.CTkToplevel() #fenetre de tkinter
    windowError.title('Erreur - ')
    windowError.minsize(width=768, height=500) #768 = taille minimum de la fenetre


    #Variables
    str_erreur = "Vous n'êtes pas connecté à internet et nous n'avons pas pu récupérer les fichiers (endommagés ou inexistants)\n programme ne peut pas se lancer dans ces conditions"

    #widgets
    msg_principal =  customtk.CTkLabel(windowError, text=str_erreur, width = 500, font =('Bold',16), justify=CENTER) #font = taille + police justify comme sur word
    msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) #Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    
    #boutons 

    #bouton ok Qui Ferme la page et termine le programme
    #btn_ok = customtk.CTkButton(windowError,height =int(windowError.winfo_screenheight()/15), command=windowError.destroy(),text="OK") 
    #btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) #place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place

    windowError.mainloop()
    
