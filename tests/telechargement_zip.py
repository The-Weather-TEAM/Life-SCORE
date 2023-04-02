lien = 'https://github.com/The-Weather-TEAM/Life-SCORE/raw/main/test.zip'


# Bibliothèques souvent utilisées :
import os                                # Pour utiliser les répertoires
from shutil import rmtree as delete_data # Pour supprimer le dossier si coupure de réseau
import requests                          # Demandes de connexion

# Bibliothèques pour la modification de documents :
import csv                               # Lecture des CSV
import pandas as p                       # Lecture et écriture des CSV
import json                              # Pour lire notre base de données

# Bibliothèques pour les conversions de temps :
import datetime                          # Conversion UNIX + vérification des versions
import time                              # Conversion UNIX
    
# Bibliothèques pour éviter erreurs de coupure réseau :
from requests.exceptions import ConnectionError, ChunkedEncodingError, ReadTimeout
from urllib3.exceptions import ProtocolError, ReadTimeoutError
from http.client import IncompleteRead


repertoire_courant = os.path.dirname(__file__)
recup_csv_internet = requests.get(lien, allow_redirects=True, stream=True)
repertoire_donnees = os.path.join(repertoire_courant+'/tests')
nom_du_fichier = os.path.join(repertoire_donnees+'testifuhfiuh.zip')
open(nom_du_fichier, 'wb').write(recup_csv_internet.content)




#https://www.geeksforgeeks.org/unzipping-files-in-python/

# importing the zipfile module
from zipfile import ZipFile
  
# loading the temp.zip and creating a zip object
with ZipFile(repertoire_donnees+'testifuhfiuh.zip', 'r') as zObject:
  
    # Extracting all the members of the zip 
    # into a specific location.
    zObject.extractall(
        path=repertoire_donnees)
    
os.remove(repertoire_donnees+'testifuhfiuh.zip')