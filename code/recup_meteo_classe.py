"""         Tentative de reproduction de 'recup_meteo.py'
                Mais avec des classes

            Sers aussi pour regarder les fichiers csv
                
                        V 0.1
"""

import requests
from requests.exceptions import ConnectionError

from tkinter import *
from datetime import datetime
from time import sleep #Optionel

import csv 
import pandas as p #Pour les csv ?







'''
Fonction qui permet de vérifier si on est connecté à internet.
'''

def test_connexion(msg) :

    temp, essais = 0, 0
    
    while temp == 0 and essais < 3 :
        try :
            requests.get("https://api.openweathermap.org", timeout=5) #ça ou google.com ?
            temp = 1
            
            
        except ConnectionError :    
            msg.config(text = 'Problème réseau.\nTentative de reconnexion en cours...')
            sleep(10)
            essais += 1            
    #assert essais != 3, ('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')

    msg.config(text = 'Veuillez saisir la ville recherchée')

class Donnees:
    def __init__(self,ville) :
        self.url = 'https://api.openweathermap.org/data/2.5/weather?appid=25bb72e551083279e1ba6b21ad77cc88&lang=fr&q=' + str(ville)
        self.data =  requests.get(self.url).json()
        self.ville = ville
        #Il reste d'autres choses a mettre pour l'instant je m'occupe que du "la ville existe ?" -Raf





    def ville_existe(self):
        """
        Verifie si la ville rentrée existe puis si elle est en France
        """
        if self.data['cod'] == 200 :                                                # code signifiant que la ville existe
            return True
                
        else : return False

    
    def is_commune_france(self,fichier_csv):
        """
        Verifie si la commune est en france grâce à un fichier qui lui est donne
        """
        fichier = open(fichier_csv,"r")
        cr = p.read_csv( fichier,delimiter=",",encoding ='iso-8859-1',usecols=['Nom1','Nom2','Nom3']) #encoding pour pouvoir avoir les accents (ne marche pas)
        fichier.close()
        for ind,col in cr.items():
            for nom in col:
                if self.ville.lower() == nom.lower(): return True
        return False

#Code de test de la Classe et des fonctions

ddd = Donnees('Beziers')
print(ddd.is_commune_france('code/CSV/villes_france.csv'))
