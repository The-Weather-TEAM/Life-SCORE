import requests
from datetime import datetime
from requests.exceptions import ConnectionError
from time import sleep


def data() :


    '''
    Ici on a un programme qui demande ET vérifie si la ville qui est entrée existe,
    puis après on récupère toutes ses données
    '''
    temp = 0
    while temp == 0 :
        
            ville = input('Votre ville : ')
            #ville = ville.replace(' ','') -> pas possible (contre-exemple : New York)
            #ville = 'Béziers'                         # test plus rapide
            
            test_connexion()                           # test de connexion à internet
            url = 'https://api.openweathermap.org/data/2.5/weather?appid=25bb72e551083279e1ba6b21ad77cc88&lang=fr&q=' + ville
            data =  requests.get(url).json()
            
            if data['cod'] == 200 :
                temp = 1
                
            else : print('\n Cette ville n\'existe pas. Veuillez réessayer.\n')
            

    #print(data)     # test pour avoir toutes les données



    '''
    Récupération de toutes les données puis conversion avec les bonnes unités
    '''  
    t     = round(data['main']['temp'] - 273.15, 1)            # convertion kelvin en degrés celsus
    t_min = round(data['main']['temp_min'] - 273.15, 1)        
    t_max = round(data['main']['temp_max'] - 273.15, 1)     
    
    res   = round(data['main']['feels_like'] - 273.15, 1)
    hum   = data['main']['humidity']
    desc  = data['weather'][0]['description']  
    pres  = round(data['main']['pressure']/1013.25, 3)         # convertion hP en ATM
    vis   = round(data['visibility']/1000, 1)                  # convertion m en degrés km
    
    logo  = data['weather'][0]['icon']
    
    lever = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime('%Hh%Mm%Ss') 
    coucher=datetime.utcfromtimestamp(data['sys']['sunset']  + data['timezone']).strftime('%Hh%Mm%Ss')
    
    wind  = round(data['wind']['speed'] * 3.6, 1)
    cloud = data['clouds']['all']
    

    
    
    UTC =   round(data['timezone']/3600)      # diviser par le nombre de sec dans une heure
    
    if UTC >= 0 :
        UTC = '+'+str(UTC)                    # rajouter "+" si l'UTC est positif
    
    
    
    '''
    Affichage (pour l'instant que dans la console) des données extraites avec la convertion
    '''   
    print('\n\n',f"DONNÉES DE LA VILLE DE {ville.upper()} -", image(logo, data))    # fonction upper pour mettre la var en majuscules
    
    print('\n',f" - Température :          {t}°C",
          '\n',f" - Température min :      {t_min}°C",
          '\n',f" - Température max :      {t_max}°C",
          '\n',f" - Ressenti :             {res}°C",
          '\n',f" - Humidité :             {hum}%",
          '\n',f" - Description :          {desc.capitalize()}",                    # capitalize pour rajouter une majuscule
          '\n',f" - Pression :             {pres} ATM",
          '\n',f" - Visibilité :           {vis}km",
          '\n',f" - Lever du soleil :      {lever} (UTC{UTC})",
          '\n',f" - Coucher :              {coucher} (UTC{UTC})",
          '\n',f" - Vent :                 {wind}hm/h",
          '\n',f" - Nuages :               {cloud}%",)



    if ('rain' in data) :
        rain = data['rain']['1h']
        print(f"  - Précipitations :       {rain}mm/h")
        
    if ('snow' in data) :
        snow = data['snow']['1h']
        print(f"  - Neige :                {snow}mm/h")
    



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
          'deg': 325,
          'gust': 3.71},

 'clouds': {'all': 100},                          -> à améliorer avec les emojis
 
 'dt': 1664730576,
 
 'sys': {'type': 1,
         'id': 6519,
         'country': 'FR',
         'sunrise': 1664689553,                    FAIT
         'sunset': 1664731685},                    FAIT

 'timezone': 7200,                                 FAIT
 
 'id': 3032832,
 
 'name': 'Béziers',                                FAIT

 'cod': 200}                                       FAIT
'''






def image(code, data) : #data pour calculer ensuite les % des nuages
    
    '''
    Convertion du code de la météo en émoji
    
    A AMELIORER EN FONCTION DES PRECIPITATIONS / NUAGES
    '''
    
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
PROGRAMME DE TEST
'''
while True :
    data()
    
    
