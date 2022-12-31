'''
Classe pourr savoir si il y a une connexion
'''
import requests
from requests.exceptions import ConnectionError
from time import sleep



class Internet :
    def __init__(self, url) :
        self.url = url
    
    def connected(self) :
        temp, essais = 0, 0
    
        while temp == 0 and essais < 3 :
            try :
                requests.get(self.url, timeout=5)
                temp = 1
                
                
            except ConnectionError :    
                print('\n\nProblème réseau.\nTentative de reconnexion en cours...')
                sleep(10)
                essais += 1
                
        assert essais != 3, ('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')
        
        return True



    
