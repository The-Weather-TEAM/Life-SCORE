'''
              LOGICIEL MÉTÉO (sans interface)
affiche les données météorologiques de la ville souhaitée.

                       créé par 
                   Frédéric MARQUET 
                          & 
                     Nathan BOSY


                       v0.4.0
'''


import requests
from requests.exceptions import ConnectionError

from datetime import datetime
from time import sleep

import pandas as p





'''
Fonction qui permet de vérifier si on est connecté à internet.
'''

def test_connexion() :

    temp, essais = 0, 0
    
    while temp == 0 and essais < 3 :
        try :
            requests.get("https://google.com", timeout=5)
            temp = 1
            
            
        except ConnectionError :    
            print('\n\nProblème réseau.\nTentative de reconnexion en cours...')
            sleep(10)
            essais += 1
            
    assert essais != 3, ('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')





nbr_recherches = 0 

test_connexion()                                                                                      # vérification d'accès à internet
data_pays = p.read_csv('https://www.data.gouv.fr/fr/datasets/r/4cafbbf6-9f90-4184-b7e3-d23d6509e77b') # récupère le fichier csv data.gouv.fr




def data(nbr_recherches) :

    

    '''
    Programme qui demande et vérifie si la ville qui est entrée existe,
    puis après on récupère toutes ses données dans un variable.
    '''

    nouvelle_recherche = ''
    
    if nbr_recherches == 0 :
        print('\n                    LOGICIEL MÉTÉO',
              '\nAffiche les données météorologiques de la ville souhaitée.'       # message de bienvenue (:
              '\n              (entrer \"q\" pour quitter)')   
    
    temp = 0
    while temp == 0 :
        
            if nbr_recherches >= 1 :
                nouvelle_recherche = 'nouvelle '                                   # pour changer le texte en recherchant
            
            ville = input(f'\nVeuillez entrer le nom de la {nouvelle_recherche}ville : ')
             
            assert ville != 'q', ('\nMerci d\'avoir utilisé nos services !')       # pour quitter le programme
            
            
            #ville = 'Béziers'                                                     # test plus rapide
            #ville = ville.replace(' ','')                                         -> pas possible (contre-exemple : New York)
            
            
            test_connexion()                                                       # vérification d'accès à internet
        
            url = 'https://api.openweathermap.org/data/2.5/weather?appid=25bb72e551083279e1ba6b21ad77cc88&lang=fr&q=' + ville
            data =  requests.get(url).json()
            

            if data['cod'] == 200 :                                                # code signifiant que la ville existe
                temp = 1
                
            else : print('\nCette ville n\'existe pas ! Veuillez réessayer.\n\n')
            

    #print(data)                                                                   # test pour avoir toutes les données





    '''
    Récupération de toutes les données puis conversion avec les bonnes unités.
    '''  
    
    
    pays               = nom_pays(data['sys']['country'], data_pays)               # exemple : convertion "FR" en "France"
    description        = data['weather'][0]['description']  
    emoji              = data['weather'][0]['icon']
    temperature        = round(data['main']['temp'] - 273.15, 1)                   # convertion kelvin en degrés celsus
    temps              = datetime.utcfromtimestamp(data['dt'] + data['timezone']).strftime('%Hh%M')
    
    
    
    UTC                = round(data['timezone']/3600)                              # diviser par le nombre de sec dans une heure
    
    if UTC >= 0 :
        UTC_texte = '+'+str(UTC)                                                   # rajouter "+" si l'UTC est positif
    else :
        UTC_texte = str(UTC)
    
    
    
    temperature_min    = round(data['main']['temp_min'] - 273.15, 1)        
    temperature_max    = round(data['main']['temp_max'] - 273.15, 1)     
    ressenti           = round(data['main']['feels_like'] - 273.15, 1)
    
    humidite           = data['main']['humidity']
    pression           = round(data['main']['pressure']/1013.25, 3)                # convertion hP en ATM
    

    nuages             = data['clouds']['all']
    visibilite         = round(data['visibility']/1000, 1)                         # convertion m en degrés km
    
    vent               = round(data['wind']['speed'] * 3.6, 1)
    orientation_vent   = direction(data['wind']['deg'])                            # pour calculer la direction du vent

    lever_soleil       = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime('%Hh%M') 
    coucher_soleil     = datetime.utcfromtimestamp(data['sys']['sunset']  + data['timezone']).strftime('%Hh%M')


    

 
    '''
    Affichage dans la console des données extraites avec les convertions.
    '''   
    
    
    print(f'\n\n\n\nDONNÉES DE LA VILLE DE {ville.upper()}, {pays.upper()}',
          
        f'\n\n{description.capitalize()}  - ', code_emoji(emoji), f' -  {temperature}°C',
        f'\ndonnées de {temps} (UTC{UTC_texte})',
           
         '\n\n\nTEMPÉRATURES',
        f'\n  • Minimum :       {temperature_min}°C',
        f'\n  • Maximum :       {temperature_max}°C',
        f'\n  • Ressenti :      {ressenti}°C',


         '\n\nPRÉCIPITATIONS')



    if ('rain' in data) :
        pluie = data['rain']['1h']
        print(f'  • Pluie :         {pluie}mm/h')
        
    if ('snow' in data) :
        neige = data['snow']['1h']
        print(f'  • Neige :         {neige}mm/h')
    
    
    
    print(f'  • Humidité :      {humidite}%',
        f'\n  • Pression :      {pression} ATM'   
          
          
         '\n\nTEMPS',
        f'\n  • Nuages :        {nuages}%',
        f'\n  • Visibilité :    {visibilite}km' 
          
          
         '\n\nVENT',
        f'\n  • Moyenne :       {vent}km/h')
    
    

    if ('gust' in data['wind']) :
        rafales  = round(data['wind']['gust'] * 3.6, 1)
        print(f'  • Rafales :       {rafales}km/h')
    
              

    print(f'  • Orientation :   {orientation_vent}', 
    
    
         '\n\nSOLEIL',
        f'\n  • Lever :         {lever_soleil}',
        f'\n  • Coucher :       {coucher_soleil}\n\n\n')
    
    
    
    
    
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





'''
Boucle pour lancer le programme en boucle jusqu'à ce que l'utilisateur quitte.
'''

while True :
    data(nbr_recherches)
    nbr_recherches += 1 
    
    



'''
Exemple de données qui arrvient après la demande :
    
    //////////
    
    {'coord': {'lon': 3.0833,
               'lat': 43.5},
     
     'weather': [{'id': 804,                          
                  'main': 'Clouds', 
                  'description': 'couvert',            FAIT
                  'icon': '04d'}],                     FAIT
    
     'base': 'stations',
     
     'main': {'temp': 295.33,                          FAIT
              'feels_like': 295.12,                    FAIT
              'temp_min': 291.47,                      FAIT
              'temp_max': 296.61,                      FAIT
              'pressure': 1023,                        FAIT
              'humidity': 58,                          FAIT
              'sea_level': 1023,
              'grnd_level': 984},
     
     'visibility': 10000,                              FAIT
     
     'wind': {'speed': 2.54,                           FAIT
              'deg': 325,                              FAIT
              'gust': 3.71},                           FAIT
    
     'clouds': {'all': 100},                           FAIT
     
     'dt': 1664730576,                                 FAIT
     
     'sys': {'type': 1,
             'id': 6519,
             'country': 'FR',                          FAIT
             'sunrise': 1664689553,                    FAIT
             'sunset': 1664731685},                    FAIT
    
     'timezone': 7200,                                 FAIT
     
     'id': 3032832,
     
     'name': 'Béziers',                                FAIT
    
     'cod': 200}                                       FAIT
    
    //////////
    
    + 'snow' et 'rain'                                 FAIT
    
    '''
