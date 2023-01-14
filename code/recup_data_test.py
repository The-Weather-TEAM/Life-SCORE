
'''
csv            = csv qu'on utilise
ville          = nom de la ville
colonne_ville  = c'est dans le nom mdr
colonne_donnee = c'est dans le nom mdr
insee_ou_nom   = pour savoir si on cherche la ville par son nom ou son code insee


'''



import requests
from requests.exceptions import ConnectionError

from tkinter import *
from datetime import datetime
from time import sleep
import customtkinter

import csv 
import pandas as p # Pour la lecture des CSV

# fix pour un erreur avec pandas.read_csv(), il n'y a pas d'explication pourquoi ça marche
# https://stackoverflow.com/questions/44629631/while-using-pandas-got-error-urlopen-error-ssl-certificate-verify-failed-cert
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os #Pour les paths
import random #Pour un easter egg







def recup_donnees(infos_csv) :
    
    lien_fichier = os.path.join(os.path.dirname(__file__), 'data')+'/'+infos_csv['nom_csv']+'.csv'
    fichier = p.read_csv(lien_fichier, delimiter=infos_csv['delimiteur'],usecols=[infos_csv['colonne_ville'],infos_csv['colonne_donnee']],encoding='utf-8',low_memory=False)
    rangee = fichier[fichier[infos_csv['colonne_ville']] == infos_csv['nom_csv']]
    
    try:
            return rangee.values[0][1]
        
    except IndexError : #SI pas de données
        return None
    
    
    








potentiel_radon = {'insee' : True,
                   'colonne_ville' : 'insee_com',
                   'colonne_donnee' : 'classe_potentiel',
                   'delimiteur' : ';',
                   'nom_csv' : 'potentiel_radon'}


potentiel_radon_avec_nom_ville = {'insee' : False,
                                  'ville_maj' : True,
                                  'colonne_ville' : 'insee_com',
                                  'colonne_donnee' : 'nom_comm',
                                  'delimiteur' : ';',
                                  'nom_csv' : 'potentiel_radon'}


print(recup_donnees(potentiel_radon))
