'''
                        [CLASSES.PY]
                         
         Programme qui répertorie toutes nos classes
                      et nos fonctions



LISTE DES CLASSES :
- "Donnees" : traitement ddes données pour le programmme


LISTE DES FONCTIONS :
- "is_connected" : vérifie si l'utilisateur a accès à internet / au site demandé
- "meteo_code_emoji" : convertit un code donné par un emoji
- "meteo_direction"  : permet de convertir un angle donné en orientation
- "meteo_nom_pays "  : permet de convertir un code ISO-3611 de type Alpha 2 en nom



/!\ DESACTIVATION TEMPORAIRE DES CLASSES QUI UTILISENT INTERNET
- Tout ce qui utilise l'API OpenWeather
Car on ne s'en sert pas pour l'instant et si on a pas internet ça plante le programmme


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



'''
Fonction qui permet de vérifier si on est connecté à internet.
REMPLACE PAR UNE CLASSE, je le laisse pour les messages pour tkinter - Nathan


def test_connexion(msg) :

    temp, essais = 0, 0
    
    while temp == 0 and essais < 3 :
        try :
            requests.get("https://api.openweathermap.org", timeout=5) #ça ou google.com ?
            temp = 1
            
            
        except ConnectionError :    
            #msg.configure(text = 'Problème réseau.\nTentative de reconnexion en cours...')
            sleep(10)
            essais += 1            
    #assert essais != 3, ('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')

    #msg.configure(text = 'Veuillez saisir la ville recherchée')

'''





'''
Fonction pour savoir si il y a une connexion
'''

def is_connected(url) :
    temp, essais = 0, 0

    while temp == 0 and essais < 3 :
        try :
            requests.get(url, timeout=5)
            temp = 1
              
                
        except ConnectionError :    
            print('\n\nProblème réseau.\nTentative de reconnexion en cours...')
            sleep(5)
            #essais += 1
                
            return False 
        
            '''
            if essais >= 3 :
                print('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')
                return False
            '''
            
        return True





'''
Fonction qui convertit un code donné par un emoji
'''

def meteo_code_emoji(code) :
    
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
Fonction qui permet de convertir un angle donné en orientation
'''  

def meteo_direction(degré) :
    
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

def meteo_nom_pays(code, data) :
    
    ligne = data[data[" Code alpha2"] == code]     # retient seulement la ligne du pays ("FR")
                  
    return ligne.values[0][3]                      # retourne le nom associé au code ("France")



'''
test_if_connected = is_connected('https://www.data.gouv.fr')
if test_if_connected :                                                                                
    data_pays = p.read_csv('https://www.data.gouv.fr/fr/datasets/r/4cafbbf6-9f90-4184-b7e3-d23d6509e77b') # récupère le fichier csv data.gouv.fr

'''





'''
[CLASSE PRINCIPALE]

'''  

class Donnees:
    def __init__(self,ville) :
        
        '''
        if test_if_connected :
            self.url = 'https://api.openweathermap.org/data/2.5/weather?appid=25bb72e551083279e1ba6b21ad77cc88&lang=fr&q=' + str(ville)
            self.data =  requests.get(self.url).json()
        '''
        
        
        self.ville = str(ville)
        self.repertoire = os.path.dirname(__file__) # Pour récupérer le chemin relatif vers le dossier data

        #Il reste d'autres choses a mettre pour l'instant je m'occupe que du "la ville existe ?" -Raf


    '''
    QUESTION DE RAF: On supprime ses deux fonctions Nathan ou bien tu veux encore t'en servir ? C'est ok pour suppr je pense
    def ville_existe(self):
        """
        Verifie si la ville rentrée existe puis si elle est en France
        """
        return self.data['cod'] == 200                                                # code signifiant que la ville existe


    
    
    def is_commune_france(self):
        """
        Verifie si la commune est en France
        """
        return self.data['sys']['country'] ==  'FR'
    '''





    def is_commune_france_v2(self,msg):
        """
        Verifie si la commune est en france grâce à un fichier et redonne son code insee
        """
        if str(self.ville) == '':
            msg.configure(text = "Il faut saisir une ville")
            return False

        """string_variables_fin = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKNOPQRSTUVWXYZ0123456789éèû' #Tout ce par quoi une ville pourrait finir (les chiffres sont pour les arrondissements)
        while self.ville[-1] not in string_variables_fin: #Si la ville finit par autre chose qu'une lettre 
            self.ville= self.ville[:-1]"""

        self.ville = self.ville.strip()
        #print(self.ville)
        
        liste = list(self.ville)
        dico_carac_spéciaux = {"é":"e", "è":"e", "ê":"e", "ë":"e", "û":"u", "à":"a", "â":"a", "ÿ":"y", "ï":"i", 
                                "î":"i", "ô":"o"}
        #remplacer les accents par leur lettres (pas ouf mais marche)
        for i in range(len(liste)):
            if liste[i] in dico_carac_spéciaux:
                liste[i] = dico_carac_spéciaux[liste[i]]

        self.ville = ''.join(liste) #Redonne la ville sans accents

        fichier = open(self.repertoire + '/data/commune_modifiee.csv',"r",encoding='utf-8') # fichier est à modifier pour les arrondissements FAIT
        cr = p.read_csv(fichier,delimiter=",",usecols=['NCC','NCCENR','LIBELLE','COM'],encoding='utf-8-sig',low_memory=False) #encoding pour pouvoir avoir les accents 
        #à voir pour un autre 
        fichier.close()

        #recup ligne de ville pour code insee  
        row = cr[(cr['NCC'] == str(self.ville).upper()) | (cr['NCCENR'] == str(self.ville).lower()) | (cr['LIBELLE'] == str(self.ville).lower())]
        #print(row)
        if not row.empty:
            #print(row.values)
            self.code_insee = row.values[0][0]
            self.ville = row.values[0][3]
            with open(self.repertoire + '/CSV/population.csv',"r") as fichier : #à bouger
                infos = p.read_csv(fichier,delimiter=",",usecols=['com_code','popleg_tot'],encoding='utf-8',low_memory=False)
                rangee = infos[infos['com_code'] == self.code_insee]
                #print(infos)
                #print(rangee)
            if not rangee.empty :
                self.population = int(rangee.values[0][1])
            else:
                msg.configure(text = "Nous n'avons pas de données sur cette ville ")
                return False
            return True
        else:
            msg.configure(text = "Ville incorrecte veuillez réessayer")
            if random.randint(0,100000) == 14924:
                msg.configure(text = "Gustavo Fring n'autorise pas la sortie d'information sur cette ville")
            return False
    
        
        
        
        
    """def nombre_habitants(self) :
        
        Retourne le nombre d'habitants de la commune
        
        A METTRE A JOUR AVEC VERSION PLUS RECENTE DE LA POPULATION !
        
        
        fichier = open(self.repertoire + '/CSV/villes_france.csv',"r") # fichier est à modifier pour les arrondissements
        cr = p.read_csv(fichier,delimiter=",",usecols=['Nom1','Nom2','Nom3','Pop 2012'],encoding='Utf-8') #encoding pour pouvoir avoir les accents (ne marche pas)

        fichier.close()
        #recup ligne de ville pour nombre habitants
        row = cr[(cr['Nom1'] == str(self.ville).upper()) | (cr['Nom2'] == str(self.ville).lower())]
        if not row.empty:
            #print(row.values[0][3])
            self.population = row.values[0][3]
            #print(self.population)
            return int(self.population)"""
        




    def note_sport(self):
        """
        Fonction qui récupère un certain Xlsx et sors une note de sport dessus sur 100 /!\ Experimentale /!\
        """
        
        data_sport = p.read_csv(self.repertoire + '/CSV/2020_Communes_TypEq.csv',delimiter=",",usecols=['ComInsee','Nombre_equipements'],low_memory=False)
        #print(data_sport,data_sport.values[2][1])

        rangee = data_sport[(data_sport['ComInsee'] == self.code_insee)]
        #print(rangee)
        #/!\ Il MANQUE LA CONDITION DE "LA VILLE Y EST ?" /!\
            
        try:
            nbr_etab_sportifs = rangee.values[0][1]
        
            # Calcul établiseements par habitants
            etab_sport_par_hab = nbr_etab_sportifs / self.population #déja défini 

            # Calcul réalisé avec les données Françaises
            note = 16071.4*etab_sport_par_hab - 3.57143
        
            # Pour les petites villes avec plus de 0.006 étab / habitants
            note = int(note)
            if note > 100 :
                note = 100
                
            if note < 0 :
                note = 0
        
        except IndexError : #SI pas de données
            return None
            
        
        #print(nbr_etab_sportifs)
        #print(self.nombre_habitants())
        #print(etab_sport_par_hab)
        #print(note)
        
        # MOYENNE NATIONALE : 311000/67500000 habitants (envioron 4/1000) ->  note de 50/100
        # MAX EN FRANCE DANS LES GRANDES VILLES : environ 6/1000 habitants -> note de 100/100
        # ON TROUVE CETTE FONCTION : f(x) = 16071.4*x - 3.57143
        # A REVOIR EN FONCTION DES PETITES VILLES ET PEUT ETRE ETRE PLUS SEVERE
        
        return note





    def note_finale(self):
        """
        Récupère la ville sous forme de classe et appelle toutes ses fonctions de note pour faire la note finale
        """
        #IL FAUDRAIT UN CODE POUR RECUPERER TOUS LES ATTRIBUTS (pour l'instant on fait un par un :(  )
        tableau = []
        #qqchose style for attr in self : tableau .append(attr)
        tableau.append(self.note_sport())
        ##print(tableau)
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





    def recup_donnees_auto(self, infos_csv) :
        
        lien_fichier = os.path.join(os.path.dirname(__file__),'data')+'/'+infos_csv['nom_csv']+'.csv'
        
        fichier = p.read_csv(lien_fichier,
                            delimiter=infos_csv['delimiteur'],
                            usecols=[infos_csv['colonne_ville'],
                                    infos_csv['colonne_donnee']],
                            encoding='utf-8',
                            low_memory=False)
        
        rangee = fichier[fichier[infos_csv['colonne_ville']] == self.code_insee] # MARCHE SEULEMENT SI LE CSV UTILISE LE CODE INSEE
        #print(rangee)
        
        try:
                return rangee.values[0][1]
            
        except IndexError : #SI pas de données
            return None


    '''
    EXEMPLE DE METADONNES A RAJOUTER POUR CHAQUE CSV DANS DATA (ou sur un fichier json) :
    
    potentiel_radon_avec_nom_ville = {'insee' : False,
                                  'ville_maj' : True,
                                  'colonne_ville' : 'insee_com',
                                  'colonne_donnee' : 'nom_comm',
                                  'delimiteur' : ';',
                                  'nom_csv' : 'potentiel_radon'}

    potentiel_radon = {'insee' : True,
                   'colonne_ville' : 'insee_com',
                   'colonne_donnee' : 'classe_potentiel',
                   'delimiteur' : ';',
                   'nom_csv' : 'potentiel_radon'}
    '''





    '''
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
    '''


    def __str__(self) : #Pour redonner un str de la villes
        if self.ville != '' :
            return str(self.ville)



'''
CLASSE 
PREVISIONS METEO (à fusionner avec la classe principale)
'''  

'''
class DonneesPrévisions:
    def __init__(self,ville) :
        self.url = 'https://api.openweathermap.org/data/2.5/forecast?appid=25bb72e551083279e1ba6b21ad77cc88&lang=fr&q=' + str(ville)
        self.data = requests.get(self.url).json()
        self.ville = ville
        
    def PrévisionsMéteo(self):
        x = 0
        prévisions_data = self.data["list"]
        dico = {}
        for prévisions in prévisions_data:
            liste = []
            température = prévisions['main']['temp'] - 273.15
            température_min = prévisions['main']['temp_min'] - 273.15
            température_max = prévisions['main']['temp_max'] - 273.15
            liste.append(température)
            liste.append(température_min)
            liste.append(température_max)
            dico[x] = liste
            x+=1
            
        analyse = []
        for i in range (8):
            analyse.append((dico[i][0],dico[i][1],dico[i][2]))
        température,température_min,température_max = 0,0,0
        for val in analyse :
            température += val[0]
            température_min += val[1]
            température_max += val[2]
            
                
        température /= len(analyse)
        température_min /= len(analyse)
        température_max /= max(analyse)
        
        return température,température_min,température_max
        
'''









if __name__ == "__main__":
    #Code de test de la Classe et des fonctions
    ddd = Donnees('Servian')
    ##print(ddd.is_commune_france())
    ##print(ddd.meteo())
    ##print(type(ddd.code_insee))
    ##print(ddd.note_sport())
    ddd.note_finale()