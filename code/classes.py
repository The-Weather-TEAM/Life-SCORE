'''
                        [CLASSES.PY]
                         
         Programme qui répertorie toutes nos classes
                      et nos fonctions



LISTE DES CLASSES :
- "Donnees" : traitement des données pour le programmme :
     . Traitement des données (transformer les infos d'uun csv en note) par Nathan
     . Savoir si la commune est française par Raphaël
     . Note finale par Raphaël et Nathan


LISTE DES FONCTIONS :
- "is_connected" : vérifie si l'utilisateur a accès à internet / au site demandé, fait par Nathan
- Fonctions pour lire/écrire/initialiser les paramètres, fait par Thor
- Fonction pour calculer une fonction affine, fait par Nathan

'''





'''
BIBLIOTHEQUES
 
'''
# Bibliothèques souvent utilisées :
import requests                        # Demandes de connexion
from tkinter import *                  # Interface utilisateur
import os                              # Interaction avec le système
import random                          # Pour un petit easter egg
import re                              # pour les splits

# Bibliothèque pour l'utilisation des CSV :
import pandas as p    # Lecture des csv

#* Fix pour une erreur avec pandas.read_csv(), il n'y a pas d'explication pourquoi ça marche
#* Source : https://stackoverflow.com/questions/44629631/while-using-pandas-got-error-urlopen-error-ssl-certificate-verify-failed-cert
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Bibliothèques pour éviter erreurs de coupure réseau :
from requests.exceptions import ConnectionError, ReadTimeout


# Multithreading, géré par Nathan (permet de faire plusieurs actions en même temps)
import threading


'''
OUVERTURE DE LA BASE DE DONNEES

'''
import json # Pour la lecture des données csv
nom_du_repertoire = os.path.dirname(__file__)
with open(nom_du_repertoire+"\systeme\\base_de_donnees.json", "r") as fichier_json :
    infos_csv = json.load(fichier_json)





'''
SAVOIR S'IL Y A UNE CONNEXION INTERNET
(avec qu'un seul essai pour éviter les bugs)

Fait par Nathan d'après un ancien projet (v.4 de l'application)
'''
def is_connected(url) :
    temp = 0

    while temp == 0 :
        try :
            requests.get(url, timeout=10)
            temp = 1
              
                
        except ConnectionError or ReadTimeout or TimeoutError :    
            print('\n\nProblème réseau.\nVeuillez vous reconnecter et relancer le programme')
                
            return False 
        
            
        return True





"""
FONCTIONS UTILE DANS TOUTE L'APPLICATION

Fait par Thor

"""

# Vérifier si le fichier options est présent
def is_options() :
    """
    Fonction qui verifie si le fichier options.txt existe pour eviter des erreurs avec les autres fontions options
    - Idée + Implémentation par Nathan
    """
    path_options = os.path.join(os.path.dirname(__file__),"donnees/options.txt") # localise le fichier cible
    if not os.path.isfile(path_options) : # on verifie si cette fichie existe pas
        dic_def = {'APPARENCE': 'System',
                   'FREQ_MAJ': 0,
                   'DERNIERE_MAJ': 0,
                   "REPONSE_QCM": {}}
        open(path_options, "w").write(str(dic_def)) # on cree et ecrit les options default a cette fichier


# Changer une option
def changer_option(option: str, valeur: any,msg=None):
    """Modifie la valeur d'une option donnée dans ./donnees/options.txt
    - Idée et Implémentation par Thor
    """
    is_options()
    if msg != None:
        msg.configure(text = "Modification effectuée !")      # Si un message est renseigné

    path_options = os.path.join(os.path.dirname(__file__), "donnees/options.txt")
    dictionaire_options = eval(open(path_options,"r").read()) # on recupere dabord les options
    dictionaire_options[option] = valeur                      # on change l'option
    open(path_options, "w").write(str(dictionaire_options))   # on re-ecrit tout les options au fichier


# Récupérer une option du fichier
def lire_option(option: str):
    """Renvoie la valeur de l'option donnée dans ./donnees/options.txt
    - Idée et Implémentation par Thor
    """
    is_options()
    path_options = os.path.join(os.path.dirname(__file__), "donnees/options.txt")

    return eval(open(path_options, "r").read()).get(option)   # on ouvre et recupere l'option qu'on veut
    
    
# Renvoie uniquement les nombres
def est_nombre(num: str) -> bool:
    """Verifie si l'entrée est un nombre (plus précisément un float)
    - Code de Thor
    """

    #assert num == str, "Seul un nombre est accepté comme réponse" #Je le commente car num sera forcément un str (précisé au dessus)
    try:
        float(num)
        return True
    except:
        return False





'''
Pour calculer une fonction à l'aide de deux points

Idée et réalisation de Nathan

'''
def calculer_fonction_affine(moyenne, max, x) : # Deux points correspondant à la moyenne (50) et le maximum (100)
   
    m = (max - moyenne) / 50                    # On calcule le coef directeur
    p = moyenne - (m*50)                        # On calcule l'ordonnée à l'oginine
   
    return (x-p)/m                              # On renvoie la note





'''
CLASSE PRINCIPALE

'''  
class Donnees:
    def __init__(self,ville) :
        
        self.ville = str(ville)
        self.repertoire = os.path.dirname(__file__)
        self.liste_notes = [] #La liste dans laquelle on rempli les notes 
        self.habitants = None
        
        #! Dictionnaire des notes (valeurs) avec les csv en clé. Pour Thor
        self.notes_finales = {}










    '''
    METHODE QUI RECUPERE AUTOMATIQUEMENT LES DONNEES D'UN CSV (simple)
    
    Pensé et réalisé par Nathan
    
    '''
    def recup_donnees_simple(self, csv) :
        
        # On récupère le répertoire pour accéder au csv
        lien_fichier = os.path.join(os.path.dirname(__file__),'donnees')+'\csv\\'+csv+'.csv'
        
        # On récupère les infos des données qu'on voudrait récupérer
        colonnes = [infos_csv[csv][2]['colonne_ville']]
        for i in range(len(infos_csv[csv][2]['colonne_donnee'])) :
            colonnes.append(infos_csv[csv][2]['colonne_donnee'][i])
        
        # On va lire le fichier
        fichier = p.read_csv(lien_fichier,
                            delimiter=infos_csv[csv][2]['delimiteur'],
                            usecols=colonnes,
                            encoding='utf-8',
                            low_memory=False)
        
        # On trouve la rangée qui valide le code insee
        rangee = fichier[fichier[infos_csv[csv][2]['colonne_ville']] == self.code_insee] # MARCHE SEULEMENT SI LE CSV UTILISE LE CODE INSEE
            
            
        try:
                resultat = []
                for i in range(len(infos_csv[csv][2]['colonne_donnee'])) :
                    resultat.append(rangee.values[0][i+1])
                return resultat
            
        # Au cas où il n'y a pas de données
        except IndexError : #Si pas de données
            
            return 0
        
        
            
            
            
    '''
    METHODE QUI RECUPERE AUTOMATIQUEMENT LES DONNEES D'UN CSV (en comptant le nombre d'éléments)
    
    Pensé et réalisé par Nathan, basé par la fonction recup_donnees_simple
    
    '''
    def recup_donnees_compter_par_habitant(self, csv, liste_csv):
        
        try:
            
            # Ici c'est tout comme la fonction au dessus
            lien_fichier = os.path.join(os.path.dirname(__file__),'donnees')+'\csv\\'+csv+'.csv'
            
            colonnes = [infos_csv[csv][2]['colonne_ville']]
            for i in range(len(infos_csv[csv][2]['colonne_donnee'])) :
                colonnes.append(infos_csv[csv][2]['colonne_donnee'][i])
            
            fichier = p.read_csv(lien_fichier,
                                delimiter=infos_csv[csv][2]['delimiteur'],
                                usecols=colonnes,
                                encoding='utf-8',
                                low_memory=False)
            
            res = fichier[fichier[infos_csv[csv][2]['colonne_ville']] == self.code_insee] # MARCHE SEULEMENT SI LE CSV UTILISE LE CODE INSEE
            
            # Là on récupère seulement le nombre de lignes qui restent pour compter les éléments
            df = p.DataFrame(res)
            rep = len(df)
            
            
            # Extention pour les CSV de type oui_non
            if infos_csv[csv][2]['type'] == 'oui_non':
                if rep != 0 :
                    return 100
                else:
                    return 0
            
            
            
            # On récupère les habitants si c'est pas déjà fait, basé sur mon autre fonction recup_donnees_par_population
            if self.habitants is None :
                self.habitant = int(self.recuperation_donnees('population')[0])
            
            # On divise si un CSV repertorie plusieurs années
            diviseur = infos_csv[csv][2].get('diviseur')
            if diviseur != None :
                rep = rep / diviseur
                
            print(" - Total dans la ville :", rep)
            
            note = rep / self.habitant
            print(" - Par habitant :", note)
            
            #On récupère directement la note en utilisant la fonction affine
            a = liste_csv[csv][2]['moyenne']
            b = liste_csv[csv][2]['max']   
            return calculer_fonction_affine(a, b, note)
            
        except : #Si pas de données
            return 0





    '''
    METHODE QUI RECUPERE AUTOMATIQUEMENT LES DONNEES D'UN CSV (par habaitant)
    
    Pensé et réalisé par Nathan
    
    '''
    def recup_donnees_par_population(self, csv, liste_csv) :
        
        if self.habitants is None :
            self.habitant = int(self.recuperation_donnees('population')[0])
        
        # On utilise recup_donnees_simple pour éviter de faire la même chose dans un autre endroit
        nombre = Donnees.recup_donnees_simple(self, csv)
        
        try :
            nombre = int(nombre[0])
            if nombre is None :
                nombre = 0
        except :
            return 0
        
        # On divise par le nombre d'habitants et on utilise la fonction affine
        note = nombre / self.habitant
        print(" - Par habitant :", note)
        # On récupère directement la note
        a = liste_csv[csv][2]['moyenne']
        b = liste_csv[csv][2]['max']
        
        return calculer_fonction_affine(a, b, note)
        
        
        


    '''
    METHODE QUI RECUPERE AUTOMATIQUEMENT LES DONNEES D'UN CSV (simple juste en utilisant l'affine)
    
    Pensé et réalisé par Nathan, basé par la fonction recup_donnees_simple et recup_donnees_population
    
    '''
    def recup_donnees_simple_affine(self, csv, liste_csv) :
    
        try :
            nombre = Donnees.recup_donnees_simple(self, csv)
            print(" - Donnée :", nombre)
            a = liste_csv[csv][2]['moyenne']
            b = liste_csv[csv][2]['max']
            
            nombre = int(((str(nombre[0])).split(','))[0])
    
            return calculer_fonction_affine(a, b, nombre)
        
        except :
            return 0





    '''
    METHODE QUI RECUPERE AUTOMATIQUEMENT LES DONNEES D'UN CSV
    
    HUB où on fait le pont entre les autres fonctions par rapport au type de CSV 
    Pensé et réalisé par Nathan
    
    '''
    def recuperation_donnees(self, csv, liste_csv=None) :
        type_recuperation = infos_csv[csv][2]['type']
        
        if type_recuperation == 'simple' :
            return Donnees.recup_donnees_simple(self, csv)
        
        elif type_recuperation  == 'par_population' :
            return Donnees.recup_donnees_par_population(self, csv, liste_csv)
        
        elif type_recuperation == 'compter_par_population' or type_recuperation == 'oui_non':
            return Donnees.recup_donnees_compter_par_habitant(self, csv, liste_csv)
        
        elif type_recuperation == 'simple_affine' :
            return Donnees.recup_donnees_simple_affine(self, csv, liste_csv)
        
        else :
            print("Fonction pas encore implémentée")
        
        


        
        
        
    """
    VERIFIE SI LA COMMUNE EST FRANCAISE ET DONNE SON CODE INSEE
    
    Fait par Raphaël
    
    """
    def is_commune_france(self,msg):

        if str(self.ville) == '':
            msg.configure(text = "Veuillez saisir le nom d'une commune.")
            return False


        self.ville = self.ville.strip() # Enlève les espaces en trop
        

        if "-" in self.ville or ' ' in self.ville:
            liste_ville = re.split("-| ",self.ville)# Sépare avec espace, - et '
            for i in range(len(liste_ville)):
                if liste_ville[i] not in ['lès','l','d','en','de','des','les','à']:
                    if liste_ville[i][:2] in ["d'","l'"] : # Si on a d'hérault
                        liste_ville[i] = liste_ville[i][:2] + liste_ville[i][2].upper() + liste_ville[i][3:]
                    else: 
                        liste_ville[i] = liste_ville[i].capitalize()
            self.ville = "-".join(liste_ville)

        fichier = open(self.repertoire + '/commune_modifiee.csv',"r",encoding='utf-8')
        cr = p.read_csv(fichier,delimiter=",",usecols=['NCC','NCCENR','LIBELLE','COM'],encoding='utf-8-sig',low_memory=False) # Encoding pour pouvoir avoir les accents 

        fichier.close()

        # Recup ligne de ville pour code insee  
        row = cr[(cr['NCCENR'] == str(self.ville)) | (cr['LIBELLE'] == str(self.ville))]
        if not row.empty:
            self.code_insee = row.values[0][0]
            self.ville = row.values[0][3]
            
            with open(self.repertoire + '/donnees/csv/population.csv',"r") as fichier : 
                infos = p.read_csv(fichier,delimiter=",",usecols=['com_code','popleg_tot'],encoding='utf-8',low_memory=False)
                rangee = infos[infos['com_code'] == self.code_insee]

            if not rangee.empty :
                self.population = int(rangee.values[0][1])
                
            else:
                msg.configure(text = "Nous n'avons pas de données sur cette ville ")
                return False
            
            return True
        
        else:
            self.ville = self.ville.strip('-')        
            liste = list(self.ville)
            dico_carac_spéciaux = {"é":"e", "è":"e", "ê":"e", "ë":"e", "û":"u", "à":"a", "â":"a", "ÿ":"y", "ï":"i", 
                                    "î":"i", "ô":"o","-":" ","'":" "}
            # Remplacer les accents par leur lettres (pas ouf mais marche)
            for i in range(len(liste)):
                if liste[i] in dico_carac_spéciaux:
                    liste[i] = dico_carac_spéciaux[liste[i]]
            self.ville = ''.join(liste) #Redonne la ville sans accents
            row = cr[(cr['NCC'] == str(self.ville).upper())] 

            if not row.empty:
                self.code_insee = row.values[0][0]
                self.ville = row.values[0][3]
                
                with open(self.repertoire + '/donnees/csv/population.csv',"r") as fichier : 
                    infos = p.read_csv(fichier,delimiter=",",usecols=['com_code','popleg_tot'],encoding='utf-8',low_memory=False)
                    rangee = infos[infos['com_code'] == self.code_insee]

                if not rangee.empty :
                    self.population = int(rangee.values[0][1])
                    
                else:
                    msg.configure(text = "Nous n'avons pas de données sur cette ville ")
                    return False
                return True
            else :
                if self.ville == "Hello There" :
                    msg.configure(text = "General Kenobi !")
                else :
                    msg.configure(text = "Ville incorrecte. Veuillez réessayer")
                
                # EASTER EGG
                if random.randint(0,100000) == 14924:
                    msg.configure(text = "Gustavo Fring n'autorise pas la sortie d'information sur cette ville")
                    
                return False
        
        
        
        
        
    '''
    METHODE POUR NOTER LES ETABLISSEMENTS SPORTIFS
    
    Fait par Raphaël et Nathan
    
    #! VERSION QU'AVEC LE CSV TEST SPORT
    '''
    def note_par_habitants(self,csv,colones,m_p,delim = ','):
        """
        Methode qui renvoie une note en fonction des habitants
        ajoute la valeur de la note a self.liste_notes et la retourne (si on veut l'afficher)
        
        csv : str qui donne le nom du csv en question
        colones : list les colones utilisées a voir si on peut pas l'automatiser ['ComInsee','Nombre_equipements']
        m_p : list de int (mx+p) pour la fonction affine
        delim : str le delimiteur, une virgule par défaut
        """
        data = p.read_csv(self.repertoire + '/' + csv ,delimiter=delim ,usecols=colones,low_memory=False) 
        #data = p.read_csv(self.repertoire + '/donnees/csv/' + csv ,delimiter=delim ,usecols=colones,low_memory=False) 

        rangee = data[(data[colones[0]]== self.code_insee)] #/!\ data[colones][0] != data[colones[0]] /!\
        #/!\ Il MANQUE LA CONDITION DE "LA VILLE Y EST ?" /!\
        try:
            nbr_etab = rangee.values[0][1]
        
            # Calcul établiseements par habitants
            habitant = self.recuperation_donnees('population')[0]
            etab_par_hab = nbr_etab / int(habitant)
            print("Le csv sport (test)\n - Par habitant :", etab_par_hab)

            # Calcul réalisé avec les données Françaises
            #16071.4*etab_sport_par_hab - 3.57143
            note = m_p[0]*etab_par_hab + m_p[1]
        
            # Pour les petites villes avec plus de 0.006 étab / habitants
            note = int(note)
            if note > 100 :
                note = 100
                
            if note < 0 :
                note = 0
            print(" - Note /100 :", note)
        except IndexError : # Si pas de données
            return None
            
            
        # MOYENNE NATIONALE : 311000/67500000 habitants (envioron 4/1000) ->  note de 50/100
        # MAX EN FRANCE DANS LES GRANDES VILLES : environ 6/1000 habitants -> note de 100/100
        # ON TROUVE CETTE FONCTION : f(x) = 16071.4*x - 3.57143
        self.liste_notes.append(note)
        self.notes_finales["sport"]=note
        return note



    """
    ITER LES NOTES ET APPLIQUE LES REPONSES AUX DIFFERENTS CRITERES PAR RAPPORT AU QCM
    
    Idée par le group, fait par Thor
    """
    def applique_coefs_QCM(self, qcm_reponses: dict, notes: dict) -> dict:
        """
        Applique les choix du QCM aux notes pour que les notes en question
        sont pris en compte ou pas
        
        """
        #! La fonction n'est pas du tout dans sont etat terminé

        qcm_to_criteres = { # Chaque reponse du QCM et ses notes qui sont en relation
            #! Besoin d'aide pour choisir quoi va avec quoi
            "Activite": ["monuments_historiques"],
            "Age": [],
            "Scolarite": ["sport"],
            "Enfants": ["ecoles", "colleges", "lycees", "sport"],
            "Culture": ["monuments_historique"],
            "Citadin": [],
            "Travail": [],
            "Cherche_Emploi": []
        }

        for qcm_coefs in qcm_to_criteres.keys(): # pour chaque choix de question
            
            if not qcm_reponses[qcm_coefs]: # si la reponse est 0 (ou non)

                for critere in qcm_to_criteres[qcm_coefs]: # pour chaque critere en relation avec la question
                    critere_note = notes.get(critere)
                    if critere_note: # on verifie que la note de ce critere existe
                        del notes[critere] # on suprimme cette note du dict car elle n'a plus d'importance
        
        return notes # renvoi nouveau dictionaire de notes
            



    '''
    METHODE POUR DONNER LE SCORE FINALE DE LA VILLE
    
    Fait par Raphaëm et Nathan
    
    '''
    def note_finale(self):


        '''
        Ici on  récupère chaque données pour chaque CSV, si elle sont utilisables on rajoute ça dans la note finale
        Pensé et réalisé par Nathan, à l'aide des fonctions au dessus
        '''
        # On ouvre le fichier json de la base de données
        with open(os.path.dirname(__file__)+"/systeme/base_de_donnees.json", "r") as fichier_json :
            liste_csv = json.load(fichier_json)
        
        # Pour chaque CSV
        for id in liste_csv :
            self.prepa_recup_donnees(liste_csv, id) #Ancienne méthode, pas très rapide avec bcp de CSV
            
        """ Bip boup ça marche mais ça créer des bugs au niveau des notes dcp pas ouf         
            a = threading.Thread(target=self.prepa_recup_donnees, args=(liste_csv, id,))
            a.start()
        a.join()
        """
        
        # Pour tester avant de tout envoyer
        print("\nLES NOTES :",self.liste_notes)
        print(self.notes_finales)
        print("\n\n\n\n\n")
        




        '''
        Création de la note finale
        Fait par Raphaël #?(je crois)
        '''
        note_finale = 0
        for i in range(len(self.liste_notes)) :
            if self.liste_notes[i] != None:
                note_finale += int(self.liste_notes[i])
            else:
                self.liste_notes.pop(i) # Supprime tous les None
        
        if len(self.liste_notes) == 0: # Si on n'a pas de données
            return 'N/A'
        return int(note_finale / len(self.liste_notes))



    '''
    Gérér les notes avant de faire la note finale
    
    Fait par Raphaël et Nathan
    
    '''
    def prepa_recup_donnees(self, liste_csv, id):
        print ("\nLe csv", id)
        if liste_csv[id][2]['insee'] == 1 : # Pour l'instant on regarde seulement les CSV avec un insee dedans
            resultat = self.recuperation_donnees(id, liste_csv)
                    
            print(" - Note /100 :", resultat)
                # Le code marche, mais la base de données renseigne seulement la moyenne pour les types de CSV par habitant
            if resultat is not None :
                if type(resultat) is not list :
                        # Si le résultat est trop faible ou trop élevée (ce qui arrive), on met en place un max et un min
                    if resultat < 0 :
                        resultat = 0
                    elif resultat > 100 :
                        resultat = 100
                    self.liste_notes.append(resultat)
                    self.notes_finales[id] = resultat
        else :
            print("Fonction pas encore implémentée")




    '''
    POUR REDONNER UN STR DE LA VILLE
    
    Fait par Raphaël
    '''
    def __str__(self) :
        if self.ville != '' :
            return str(self.ville)
    


# Fin du code !
