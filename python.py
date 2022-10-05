'''
                    LOGICIEL MÉTÉO
affiche les données météorologiques de la ville souhaitée.

                       créé par 
                   Frédéric MARQUET 
                          & 
                     Nathan BOSY


                       v0.3.1
'''


import requests
from requests.exceptions import ConnectionError

from datetime import datetime
from time import sleep


researches = 0


def data(researches) :

    

    '''
    Ici on a un programme qui demande ET vérifie si la ville qui est entrée existe,
    puis après on récupère toutes ses données
    '''

    new = ''
    
    if researches == 0 :
        print('\n                    LOGICIEL MÉTÉO',
              '\nAffiche les données météorologiques de la ville souhaitée.'       # message de bienvenue (:
              '\n              (entrer \"q\" pour quitter)')   
    
    temp = 0
    while temp == 0 :
        
            if researches >= 1 :
                new = 'nouvelle '                                                  # pour changer le texte en recherchant
            
            ville = input(f'Veuillez entrer le nom de la {new}ville : ')
             
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
    Récupération de toutes les données puis conversion avec les bonnes unités
    '''  
    
    
    
    pays        = data['sys']['country']                             # -> à améliorer avec un fichier CSV des pays
    desc        = data['weather'][0]['description']  
    logo        = data['weather'][0]['icon']
    t           = round(data['main']['temp'] - 273.15, 1)            # convertion kelvin en degrés celsus
    time        = datetime.utcfromtimestamp(data['dt'] + data['timezone']).strftime('%Hh%M')
    
    
    
    UTC =   round(data['timezone']/3600)                             # diviser par le nombre de sec dans une heure
    
    if UTC >= 0 :
        str_UTC = '+'+str(UTC)                                       # rajouter "+" si l'UTC est positif
    else :
        str_UTC = str(UTC)
    
    
    
    t_min       = round(data['main']['temp_min'] - 273.15, 1)        
    t_max       = round(data['main']['temp_max'] - 273.15, 1)     
    res         = round(data['main']['feels_like'] - 273.15, 1)
    
    hum         = data['main']['humidity']
    pres        = round(data['main']['pressure']/1013.25, 3)         # convertion hP en ATM
    

    cloud       = data['clouds']['all']
    vis         = round(data['visibility']/1000, 1)                  # convertion m en degrés km
    
    wind        = round(data['wind']['speed'] * 3.6, 1)
    orientation = direction(data['wind']['deg'])                     # pour calculer la direction du vent

    lever = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime('%Hh%M') 
    coucher=datetime.utcfromtimestamp(data['sys']['sunset']  + data['timezone']).strftime('%Hh%M')


    

 
    '''
    Affichage (pour l'instant que dans la console) des données extraites avec la convertion
    '''   
    
    
    
    print(f'\n\n\n\nDONNÉES DE LA VILLE DE {ville.upper()}, {pays.upper()}',
          
        f'\n\n{desc.capitalize()}  - ', image(logo, data), f' -  {t}°C',
        f'\nil est {time} (UTC{str_UTC})',
           
         '\n\n\nTEMPÉRATURES',
        f'\n  • Minimum :       {t_min}°C',
        f'\n  • Maximum :       {t_max}°C',
        f'\n  • Ressenti :      {res}°C',


         '\n\nPRÉCIPITATIONS')



    if ('rain' in data) :
        rain = data['rain']['1h']
        print(f'  • Pluie :         {rain}mm/h')
        
    if ('snow' in data) :
        snow = data['snow']['1h']
        print(f'  • Neige :         {snow}mm/h')
    
    
    
    print(f'  • Humidité :      {hum}%',
        f'\n  • Pression :      {pres} ATM'   
          
          
         '\n\nTEMPS',
        f'\n  • Nuages :        {cloud}%',
        f'\n  • Visibilité :    {vis}km' 
          
          
         '\n\nVENT',
        f'\n  • Moyenne :       {wind}km/h')
    
    

    if ('gust' in data['wind']) :
        wind_max  = round(data['wind']['gust'] * 3.6, 1)
        print(f'  • Rafales :       {wind_max}km/h')
    
              

    print(f'  • Orientation :   {orientation}', 
    
    
         '\n\nSOLEIL',
        f'\n  • Lever :         {lever}',
        f'\n  • Coucher :       {coucher}\n\n\n')
    
    
    
    
    
'''
    Convertion du code de la météo en émoji
    
    A AMELIORER EN FONCTION DES PRECIPITATIONS / NUAGES (ou le code de la météo c'est sympa aussi)
    à voir si on préfère les images
'''
def image(code, data) : # data pour calculer ensuite les % des nuages (non utilis pour l'instant)
    
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
Fonction qui permet de vérifier si on est connecté à internet
'''
def test_connexion() :

    temp, trys = 0, 0
    while temp == 0 and trys < 3 :
        try :
            requests.get("https://google.com", timeout=5)
            temp = 1
        except ConnectionError :    
            print('\n\nProblème réseau.\nTentative de reconnexion en cours...')
            sleep(10)
            trys += 1
    assert trys != 3, ('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')
        
    
    
    
    
'''
Fonction qui permet de convertir un angle en orientation
'''  
def direction(degré) :
    dirs = ['Nord', 'Nord-Est', 'Est', 'Sud-Est', 'Sud', 'Sud-Ouest', 'Ouest', 'Nord-Ouest']
    ix = round(degré / (360 / len(dirs)))
    return dirs[ix % len(dirs)]






'''
PROGRAMME DE TEST
'''
while True :
    data(researches)
    researches += 1 
    
    



'''
    EXEMPLE DE DONNEES RECUPEREES
    
    
    {'coord': {'lon': 3.0833,
               'lat': 43.5},
     
     'weather': [{'id': 804,                          -> à améliorer avec les emojis
                  'main': 'Clouds',
                  'description': 'couvert',           FAIT
                  'icon': '04d'}],                    -> à améliorer avec les emojis
    
     'base': 'stations',
     
     'main': {'temp': 295.33,                         FAIT
              'feels_like': 295.12,                   FAIT
              'temp_min': 291.47,                     FAIT
              'temp_max': 296.61,                     FAIT
              'pressure': 1023,                       FAIT
              'humidity': 58,                         FAIT
              'sea_level': 1023,
              'grnd_level': 984},
     
     'visibility': 10000,                             FAIT
     
     'wind': {'speed': 2.54,                          -> à améliorer avec les emojis
              'deg': 325,                             -> à faire en donnant E, O, N, S
              'gust': 3.71},                          FAIT
    
     'clouds': {'all': 100},                          -> à améliorer avec les emojis
     
     'dt': 1664730576,                                 FAIT
     
     'sys': {'type': 1,
             'id': 6519,
             'country': 'FR',                          -> à améliorer (avec emoji ou data.gouv.fr)
             'sunrise': 1664689553,                    FAIT
             'sunset': 1664731685},                    FAIT
    
     'timezone': 7200,                                 FAIT
     
     'id': 3032832,
     
     'name': 'Béziers',                                FAIT
    
     'cod': 200}                                       FAIT
    
    
    + SNOW ET RAIN BIEN SÛR !!!                        FAIT
    
    '''
