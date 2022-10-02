import requests




def data() :

    '''
    Ici on a un programme qui demande ET vérifie si la ville qui est entrée existe,
    puis après on récupère toutes ses données
    '''
    temp = 0
    while temp == 0 :
        
            ville = input('Votre ville : ')
            #ville = 'Béziers'                         #test plus rapide
            
            url = 'https://api.openweathermap.org/data/2.5/weather?appid=25bb72e551083279e1ba6b21ad77cc88&lang=fr&q=' + ville
            data =  requests.get(url).json()
            
            if data['cod'] == 200 :
                temp = 1
                
            else : print('\n Cette ville n\'existe pas. Veuillez réessayer.\n')
            

    print(data)     #test pour avoir toutes les données



    '''
    Récupération de toutes les données puis conversion avec les bonnes unités
    '''  
    t     = round(data['main']['temp'] - 273.15, 1)            # convertion kelvin en degrés celsus
    t_min = round(data['main']['temp_min'] - 273.15, 1)        
    t_max = round(data['main']['temp_max'] - 273.15, 1)        
    res   = round(data['main']['feels_like'] - 273.15, 1)
    hum   = data['main']['humidity']
    desc  = data['weather'][0]['description']  
    pres  = round(data['main']['pressure']/1013.25, 2)         # convertion hP en ATM
    vis   = round(data['visibility']/1000, 1)                  # convertion m en degrés km
    
    

    
    
    
    '''
    Affichage (pour l'instant que dans la console) des données extraites avec la convertion
    '''   
    print('\n\n',f"DONNÉES DE LA VILLE DE {ville.upper()}")    #Fonction upper pour mettre la var en majuscules
    print('\n',f" - Température :          {t}°C",
          '\n',f" - Température min :      {t_min}°C",
          '\n',f" - Température max :      {t_max}°C",
          '\n',f" - Ressenti :             {res}°C",
          '\n',f" - Humidité :             {hum}%",
          '\n',f" - Description :          {desc}",
          '\n',f" - Pression :             {pres} ATM",
          '\n',f" - Visibilité :           {vis}km")


    logo = data['weather'][0]['icon']
    print(logo)
    print(image(logo))
    



'''
EXEMPLE DE DONNEES RECUPEREES


{'coord': {'lon': 3.0833,
           'lat': 43.5},
 
 'weather': [{'id': 804,
              'main': 'Clouds',
              'description': 'couvert',           FAIT
              'icon': '04d'}],                    -> à faire avec les emojis

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
 
 'wind': {'speed': 2.54,
          'deg': 325,
          'gust': 3.71},

 'clouds': {'all': 100},
 
 'dt': 1664730576,
 
 'sys': {'type': 1,
         'id': 6519,
         'country': 'FR',
         'sunrise': 1664689553,
         'sunset': 1664731685},

 'timezone': 7200,
 
 'id': 3032832,
 
 'name': 'Béziers',

 'cod': 200}
'''






def image(code) :
    
    '''
    Convertion du code de la météo en émoji
    
    A AMELIORER EN FONCTION DES PRECIPITATIONS
    '''
    
    if   code == '01d' :
        return "🌞"
        
    elif code == '02d' :
        return "🌤"
        
    elif code == '03d' or code == '04d' :
        return "☁️"

    elif code == '09d' :
        return "🌧"

    elif code == '10d' :
        return "🌦"

    elif code == '11d' :
        return "⛈"

    elif code == '13d' :
        return "🌨"
    
    elif code == '50d' :
        return "🌫"





#🌚






data()
