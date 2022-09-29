import requests


def température() :
    
    #ville = input('Votre ville : ')
    url = 'https://api.openweathermap.org/data/2.5/weather?appid=25bb72e551083279e1ba6b21ad77cc88&lang=fr&q='+'Rennes'
    
    
    data =  requests.get(url).json()
    print(data)
    
    temp = round(data['main']['temp'] - 273.15, 1)             # convertion kelvin en degrés celsus
    
    print('\n\n\n\n\n\n', temp, '°C ⛈')






'''
data_test = {'coord': {'lon': 3.2642,
           'lat': 43.4412},

 'weather': [{'id': 800,
               'main': 'Clear',
               'description': 'clear sky'
               , 'icon': '01d'}],

 'base': 'stations',
 'main': {'temp': 200.57,
          'feels_like': 292.13,
          'temp_min': 292.1,
          'temp_max': 292.71,
          'pressure': 1002,
          'humidity': 60},
 
 'visibility': 10000,
 
 'wind': {'speed': 5.14,
           'deg': 270},
 
 'clouds': {'all': 0},
 
 'dt': 1664455575,

 'sys': {'type': 1,
         'id': 6519,
         'country': 'FR',
         'sunrise': 1664430103,
         'sunset': 1664472769},
         'timezone': 7200,
         'id': 3032832,
         'name': 'Espondeilhan',
         'cod': 200}
'''

température()