'''
                        [CLASSES.PY]
                         
         Programme qui répertorie toutes nos classes
                      et nos fonctions



LISTE DES CLASSES :
- "Donnees" : traitement des données pour le programmme


LISTE DES FONCTIONS :
- "is_connected" : vérifie si l'utilisateur a accès à internet / au site demandé

'''





'''
BIBLIOTHEQUES
 
'''

import requests
from requests.exceptions import ConnectionError, ReadTimeout
from tkinter import *
import pandas as p
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
import random #Pour un easter egg
import re # pour les splits



'''
OUVERTURE DE LA BASE DE DONNEES
 
'''
import json # Pour la lecture des données csv
nom_du_repertoire = os.path.dirname(__file__)
with open(nom_du_repertoire+"\systeme\\base_de_donnees.json", "r") as fichier_json :
    infos_csv = json.load(fichier_json)





'''
SAVOIR S'IL Y A UNE CONNEXION INTERNET
(avec qu'un seul essai)

'''

def is_connected(url) :
    temp = 0

    while temp == 0 :
        try :
            requests.get(url, timeout=10)
            temp = 1
              
                
        except ConnectionError or ReadTimeout or TimeoutError :    
            print('\n\nProblème réseau.\nTentative de reconnexion en cours...')
                
            return False 
        
            
        return True

"""
FONCTIONS UTILE DANS TOUT L'APPLICATION

"""
def changer_option(option, valeur):
    """Modifie la valeur d'un option donné dans ./donnees/options.txt"""
    path_options = os.path.join(os.path.dirname(__file__), "donnees/options.txt")

    dictionaire_options = eval(open(path_options,"r").read()) # on recupere dabord les options
    dictionaire_options[option] = valeur # on change l'option
    open(path_options, "w").write(str(dictionaire_options)) # on re-ecrit tout les options au fichier

def lire_option(option):
    """Renvoi la valeur de l'option donné dans ./donnees/options.txt"""
    path_options = os.path.join(os.path.dirname(__file__), "donnees/options.txt")

    return eval(open(path_options, "r").read()).get(option) # on ouvre et recupere l'option qu'on veut
    
def est_numerique(num: str) -> bool:
    """Renvoi si un string est numerique"""
    assert num == str, "On peut que evaluer si un string est numerique."
    try:
        float(num)
        return True
    except:
        return False


'''
CLASSE PRINCIPALE

'''  

class Donnees:
    def __init__(self,ville) :
        
        self.ville = str(ville)
        self.repertoire = os.path.dirname(__file__)
        self.liste_notes = [] #La liste dans laquelle on rempli les notes 




    '''
    METHODE QUI RECUPERE AUTOMATIQUEMENT LES DONNEES D'UN CSV

    '''
    def recup_donnees_auto(self, csv) :
        
        lien_fichier = os.path.join(os.path.dirname(__file__),'donnees')+'\csv\\'+csv+'.csv'
        
        fichier = p.read_csv(lien_fichier,
                            delimiter=infos_csv[csv][2]['delimiteur'],
                            usecols=[infos_csv[csv][2]['colonne_ville'],
                                    infos_csv[csv][2]['colonne_donnee']],
                            encoding='utf-8',
                            low_memory=False)
        
        rangee = fichier[fichier[infos_csv[csv][2]['colonne_ville']] == self.code_insee] # MARCHE SEULEMENT SI LE CSV UTILISE LE CODE INSEE
        
        try:
                return int(rangee.values[0][1])
            
        except IndexError : #Si pas de données
            return None




    """
    VERIFIE SI LA COMMUNE EST FRANCAISE ET DONNE SON CODE INSEE
    """
    def is_commune_france(self,msg):

        if str(self.ville) == '':
            msg.configure(text = "Veuillez saisir le nom d'une commune.")
            return False


        self.ville = self.ville.strip() #Enlève les espaces en trop
        

        if "-" in self.ville or ' ' in self.ville:
            liste_ville = re.split("-| ",self.ville)#sépare avec espace, - et '
            for i in range(len(liste_ville)): #
                if liste_ville[i] not in ['lès','l','d','en','de','des','les','à']:
                    if liste_ville[i][:2] in ["d'","l'"] : #si on a d'hérault
                        liste_ville[i] = liste_ville[i][:2] + liste_ville[i][2].upper() + liste_ville[i][3:]
                    else: 
                        liste_ville[i] = liste_ville[i].capitalize()
            self.ville = "-".join(liste_ville)

        fichier = open(self.repertoire + '/donnees/csv/commune_modifiee.csv',"r",encoding='utf-8')
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
    TEMPORAIRE : NE MARCHE PAS AVEC LA BASE DE DONNEES
    
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

        
        data = p.read_csv(self.repertoire + '/donnees/csv/' + csv ,delimiter=delim ,usecols=colones,low_memory=False)

        rangee = data[(data[colones[0]]== self.code_insee)] #/!\ data[colones][0] != data[colones[0]] /!\
        #/!\ Il MANQUE LA CONDITION DE "LA VILLE Y EST ?" /!\
            
        try:
            nbr_etab = rangee.values[0][1]
        
            # Calcul établiseements par habitants
            etab_par_hab = nbr_etab / self.recup_donnees_auto('population')

            # Calcul réalisé avec les données Françaises
            #16071.4*etab_sport_par_hab - 3.57143
            note = m_p[0]*etab_par_hab + m_p[1]
        
            # Pour les petites villes avec plus de 0.006 étab / habitants
            note = int(note)
            if note > 100 :
                note = 100
                
            if note < 0 :
                note = 0
        
        except IndexError : # Si pas de données
            self.liste_notes.append(None)
            return None
            
            
        # MOYENNE NATIONALE : 311000/67500000 habitants (envioron 4/1000) ->  note de 50/100
        # MAX EN FRANCE DANS LES GRANDES VILLES : environ 6/1000 habitants -> note de 100/100
        # ON TROUVE CETTE FONCTION : f(x) = 16071.4*x - 3.57143
        self.liste_notes.append(note)
        return note





    '''
    METHODE POUR DONNER LE SCORE FINALE DE LA VILLE
    
    '''
    def note_finale(self):

        note_finale = 0
        for i in range(len(self.liste_notes)) :
            if self.liste_notes[i] != None:
                note_finale += int(self.liste_notes[i])
            else:
                self.liste_notes.pop(i) #Supprime tous les None
        
        if len(self.liste_notes) == 0: #Si on n'a pas de données
            return 'N/A'
        return int(note_finale / len(self.liste_notes))




    '''
    POUR REDONNER UN STR DE LA VILLE
    
    '''
    def __str__(self) :
        if self.ville != '' :
            return str(self.ville)
    