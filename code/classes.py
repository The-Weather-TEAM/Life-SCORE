"""         
            CLASSES DE LIFESCORE

- "Donnees" : traitement ddes données pour le programmme
- "Internet" : pour savoir si on est connecté à internet


"""

import requests
from requests.exceptions import ConnectionError

from tkinter import *
from datetime import datetime
from time import sleep #Optionel

import csv 
import pandas as p #pour le csv

# fix pour un erreur avec pandas.read_csv(), il n'y a pas d'explication pourquoi ça marche
# https://stackoverflow.com/questions/44629631/while-using-pandas-got-error-urlopen-error-ssl-certificate-verify-failed-cert
import ssl
ssl._create_default_https_context = ssl._create_unverified_context




'''
Fonction qui permet de vérifier si on est connecté à internet.
REMPLACE PAR UNE CLASSE


def test_connexion(msg) :

    temp, essais = 0, 0
    
    while temp == 0 and essais < 3 :
        try :
            requests.get("https://api.openweathermap.org", timeout=5) #ça ou google.com ?
            temp = 1
            
            
        except ConnectionError :    
            #msg.config(text = 'Problème réseau.\nTentative de reconnexion en cours...')
            sleep(10)
            essais += 1            
    #assert essais != 3, ('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')

    #msg.config(text = 'Veuillez saisir la ville recherchée')

'''


   
'''
Fonction qui convertit un code donné par un emoji.
'''

def code_emoji(code) :
    
    if   code == '01d' :
        return "🌞"
        
    elif code == '01n' :
        return "🌚"
    
    elif code == '02d' or code == '02n' :
        return "🌥"
        
    elif code == '03d' or code == '04d' or  code == '03n' or  code == '04n':
        return "☁️"

    elif code == '09d' or code == '09n' :
        return "🌧"

    elif code == '10d' or code == '10n' :
        return "🌦"

    elif code == '11d' or code == '11n' :
        return "⛈"

    elif code == '13d' or code == '13n' :
        return "🌨"
    
    elif code == '50d' or code == '50n' :
        return "🌫"





'''
Fonction qui permet de convertir un angle donné en orientation.
'''  

def direction(degré) :
    
    orientation = ['Nord',
                   'Nord-Est',
                   'Est',
                   'Sud-Est',
                   'Sud',
                   'Sud-Ouest',
                   'Ouest',
                   'Nord-Ouest']
    
    x = round(degré / (360 / len(orientation)))    # divise l'angle par 8
    
    return orientation[x % len(orientation)]       # retourne la bonne orientation en prenant le reste une division euclidienne (entre 0 et 7)





'''
Fonction qui permet de convertir un code ISO-3611 de type Alpha 2 en nom
'''  

def nom_pays(code, data) :
    
    ligne = data[data[" Code alpha2"] == code]     # retient seulement la ligne du pays ("FR")
                  
    return ligne.values[0][3]                      # retourne le nom associé au code ("France")









#test_connexion()                                                                                      # vérification d'accès à internet
data_pays = p.read_csv('https://www.data.gouv.fr/fr/datasets/r/4cafbbf6-9f90-4184-b7e3-d23d6509e77b') # récupère le fichier csv data.gouv.fr





'''
CLASSE 
PRINCIPALE
'''  

class Donnees:
    def __init__(self,ville) :
        self.url = 'https://api.openweathermap.org/data/2.5/weather?appid=25bb72e551083279e1ba6b21ad77cc88&lang=fr&q=' + str(ville)
        self.data =  requests.get(self.url).json()
        self.ville = str(ville)
        #Il reste d'autres choses a mettre pour l'instant je m'occupe que du "la ville existe ?" -Raf



    def ville_existe(self):
        """
        Verifie si la ville rentrée existe puis si elle est en France
        """
        if self.data['cod'] == 200 :                                                # code signifiant que la ville existe
            return True
                
        else : return False

    
    
    
    
    def is_commune_france(self):
        """
        Verifie si la commune est en France
        """
        if self.data['sys']['country'] ==  'FR' :
            return True
        
        else : return False




    def is_commune_france_v2(self):
        """
        Verifie si la commune est en france grâce à un fichier et redonne son code insee
        """
        fichier = open('code/CSV/villes_france.csv',"r")
        cr = p.read_csv(fichier,delimiter=",",usecols=['Nom1','Nom2','Nom3','Code_INSEE']) #encoding pour pouvoir avoir les accents (ne marche pas)

        fichier.close()
        """
        for ind,col in cr.iteritems():
            for nom in col:
                if self.ville.lower() == nom.lower(): """
        #recup ligne de ville pour code insee  /!\BESOIN DE CORRECTION POUR EVITER LA REDONDANCE/!\
        row = cr[(cr['Nom1'] == str(self.ville).upper()) | (cr['Nom2'] == str(self.ville).lower()) | (cr['Nom3'] == str(self.ville).lower())]
        if row.values[0][3]:
            self.code_insee = row.values[0][3]
            return True
        else: return False

        





    def note_sport(self):
        """
        Fonction qui récupère un certain Xlsx et sors une note de sport dessus sur 100 /!\ Experimentale /!\
        """
        data_sport = p.read_csv('code/CSV/2020_Communes_TypEq.csv',delimiter=",",usecols=['ComInsee','Nombre_equipements'])
        print(data_sport.values[2][1])

        rangee = data_sport[(data_sport['ComInsee'] == self.code_insee)]
        #/!\ Il MANQUE LA CONDITION DE "LA VILLE Y EST ?" /!\
        nb = rangee.values[0][1]
        note = nb*100/400
        return note














    def note_finale(self):
        """
        Récupère kla ville sous forme de classe et appelle toutes ses fonctions de note pour faire la note finale
        """
        #IL FAUDRAIT UN CODE POUR RECUPERER TOUS LES ATTRIBUTS (pour l'instant on fait un par un :(  )
        tableau = []
        #qqchose style for attr in self : tableau .append(attr)
        tableau.append(int(self.note_sport))
        print(tableau)
        note_finale = 0
        for note in tableau :
            note_finale += int(note)
        return int(note_finale / len(tableau))



            













    def meteo(self):
        
        r = {}   
        
        r['pays']             = nom_pays(self.data['sys']['country'], data_pays)               # exemple : convertion "FR" en "France"
        r['description']        = self.data['weather'][0]['description']  
        r['emoji']              = self.data['weather'][0]['icon']
        r['temperature']        = round(self.data['main']['temp'] - 273.15, 1)                   # convertion kelvin en degrés celsus
        r['temps']              = datetime.utcfromtimestamp(self.data['dt'] + self.data['timezone']).strftime('%Hh%M')
        
        
        
        r['UTC']                = round(self.data['timezone']/3600)                              # diviser par le nombre de sec dans une heure
        
        if r['UTC'] >= 0 :
            r['UTC_texte'] = '+'+str(r['UTC'])                                                   # rajouter "+" si l'UTC est positif
        else :
            r['UTC_texte'] = str(r['UTC'])
        
        

        r['temperature_min']    = round(self.data['main']['temp_min'] - 273.15, 1)        
        r['temperature_max']    = round(self.data['main']['temp_max'] - 273.15, 1)     
        r['ressenti']           = round(self.data['main']['feels_like'] - 273.15, 1)
        
        r['humidite']           = self.data['main']['humidity']                                  # en pourcent
        r['pression']           = round(self.data['main']['pressure']/1013.25, 3)                # convertion hP en ATM
        

        r['nuages']             = self.data['clouds']['all']
        r['visibilite']         = round(self.data['visibility']/1000, 1)                         # convertion m en degrés km
        
        r['vent']               = round(self.data['wind']['speed'] * 3.6, 1)
        r['orientation_vent']   = direction(self.data['wind']['deg'])                            # pour calculer la direction du vent

        r['lever_soleil']       = datetime.utcfromtimestamp(self.data['sys']['sunrise'] + self.data['timezone']).strftime('%Hh%M') 
        r['coucher_soleil']     = datetime.utcfromtimestamp(self.data['sys']['sunset']  + self.data['timezone']).strftime('%Hh%M')
        
        if ('rain' in self.data) :
            r['pluie'] = self.data['rain']['1h']

        if ('snow' in self.data) :
            r['neige'] = self.data['snow']['1h']

        if ('gust' in self.data['wind']) :
            r['rafales']  = round(self.data['wind']['gust'] * 3.6, 1)

        return r


if __name__ == "__main__":
    #Code de test de la Classe et des fonctions
    ddd = Donnees('Servian')
    #print(ddd.is_commune_france())
    #print(ddd.meteo())
    ddd.is_commune_france_v2()
    print(type(ddd.code_insee))
    print(ddd.note_sport())
    ddd.note_finale()










'''
Classe pourr savoir si il y a une connexion
'''




class Internet :
    def __init__(self, url) :
        self.url = url
    
    def is_connected(self) :
        temp, essais = 0, 0
    
        while temp == 0 and essais < 3 :
            try :
                requests.get(self.url, timeout=5)
                temp = 1
                
                
            except ConnectionError :    
                print('\n\nProblème réseau.\nTentative de reconnexion en cours...')
                sleep(10)
                essais += 1
                
                if essais >= 3 :
                    print('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')
                    return False
        
        return True



    
