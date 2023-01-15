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
from datetime import datetime
from time import sleep
import customtkinter
import csv 
import pandas as p
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
import random #Pour un easter egg




'''
OUVERTURE DE LA BASE DE DONNEES
 
'''
import json # Pour la lecture des données csv
nom_du_repertoire = os.path.dirname(__file__)
with open(nom_du_repertoire+"\database.json", "r") as fichier_json :
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





'''
CLASSE PRINCIPALE

'''  

class Donnees:
    def __init__(self,ville) :
        
        self.ville = str(ville)
        self.repertoire = os.path.dirname(__file__)




    '''
    METHODE QUI RECUPERE AUTOMATIQUEMENT LES DONNEES D'UN CSV

    '''
    def recup_donnees_auto(self, csv) :
        
        lien_fichier = os.path.join(os.path.dirname(__file__),'data')+'/'+csv+'.csv'
        
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
            msg.configure(text = "Il faut saisir une ville")
            return False


        self.ville = self.ville.strip()
        
        
        liste = list(self.ville)
        dico_carac_spéciaux = {"é":"e", "è":"e", "ê":"e", "ë":"e", "û":"u", "à":"a", "â":"a", "ÿ":"y", "ï":"i", 
                                "î":"i", "ô":"o"}
        
        # Remplacer les accents par leur lettres (pas ouf mais marche)
        for i in range(len(liste)):
            if liste[i] in dico_carac_spéciaux:
                liste[i] = dico_carac_spéciaux[liste[i]]

        self.ville = ''.join(liste) #Redonne la ville sans accents

        fichier = open(self.repertoire + '/data/commune_modifiee.csv',"r",encoding='utf-8')
        cr = p.read_csv(fichier,delimiter=",",usecols=['NCC','NCCENR','LIBELLE','COM'],encoding='utf-8-sig',low_memory=False) # Encoding pour pouvoir avoir les accents 

        fichier.close()

        # Recup ligne de ville pour code insee  
        row = cr[(cr['NCC'] == str(self.ville).upper()) | (cr['NCCENR'] == str(self.ville).lower().capitalize()) | (cr['LIBELLE'] == str(self.ville).lower().capitalize())]
        #print(row)
        if not row.empty:
            print(row.values)
            print(self.ville)
            self.code_insee = row.values[0][0]
            self.ville = row.values[0][3]
            
            with open(self.repertoire + '/data/population.csv',"r") as fichier : 
                infos = p.read_csv(fichier,delimiter=",",usecols=['com_code','popleg_tot'],encoding='utf-8',low_memory=False)
                rangee = infos[infos['com_code'] == self.code_insee]

            if not rangee.empty :
                self.population = int(rangee.values[0][1])
                
            else:
                msg.configure(text = "Nous n'avons pas de données sur cette ville ")
                return False
            
            return True
        
        else:
            if self.ville == "hello there" :
                msg.configure(text = "GENERAL KENOBI !")
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
    def note_sport(self):

        
        data_sport = p.read_csv(self.repertoire + '/data/sport.csv',delimiter=",",usecols=['ComInsee','Nombre_equipements'],low_memory=False)

        rangee = data_sport[(data_sport['ComInsee'] == self.code_insee)]
        #/!\ Il MANQUE LA CONDITION DE "LA VILLE Y EST ?" /!\
            
        try:
            nbr_etab_sportifs = rangee.values[0][1]
        
            # Calcul établiseements par habitants
            etab_sport_par_hab = nbr_etab_sportifs / self.recup_donnees_auto('population')

            # Calcul réalisé avec les données Françaises
            note = 16071.4*etab_sport_par_hab - 3.57143
        
            # Pour les petites villes avec plus de 0.006 étab / habitants
            note = int(note)
            if note > 100 :
                note = 100
                
            if note < 0 :
                note = 0
        
        except IndexError : # Si pas de données
            return None
            
            
        # MOYENNE NATIONALE : 311000/67500000 habitants (envioron 4/1000) ->  note de 50/100
        # MAX EN FRANCE DANS LES GRANDES VILLES : environ 6/1000 habitants -> note de 100/100
        # ON TROUVE CETTE FONCTION : f(x) = 16071.4*x - 3.57143
        
        return note





    '''
    METHODE POUR DONNER LE SCORE FINALE DE LA VILLE
    
    '''
    def note_finale(self):

        #IL FAUDRAIT UN CODE POUR RECUPERER TOUS LES ATTRIBUTS (pour l'instant on fait un par un :(  )
        tableau = []
        
        #qqchose style for attr in self : tableau .append(attr)
        tableau.append(self.note_sport())

        note_finale = 0
        for i in range(len(tableau)) :
            if tableau[i] != None:
                note_finale += int(tableau[i])
            else:
                tableau.pop(i) #Supprime tous les None
        #print(tableau,'adidjeidjzofjroef')
        
        if len(tableau) == 0: #Si on n'a pas de données
            return 'N/A'
        return int(note_finale / len(tableau))




    '''
    POUR REDONNER UN STR DE LA VILLE
    
    '''
    def __str__(self) :
        if self.ville != '' :
            return str(self.ville)