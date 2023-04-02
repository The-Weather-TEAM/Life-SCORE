import requests
import time
from zipfile import ZipFile
import os

repertoire_courant = os.path.dirname(__file__)
repertoire_donnees = os.path.join(repertoire_courant)

lien = 'https://github.com/The-Weather-TEAM/Life-SCORE/raw/main/test.zip'



def taille_zip(url):
    informations = requests.head(url, allow_redirects=True)
    content_length = informations.headers.get('Content-Length')
    if content_length is None:
        return None
    else:
        return int(content_length)
    


download_size = taille_zip(lien)










def telecharger(lien, nomfichier):
    fichier_zip = requests.get(lien, stream=True)
    taille_cache = 1024
    bits_telecharges = 0
    debut = time.time()
    with open(nomfichier, 'wb') as f:
        for chunk in fichier_zip.iter_content(chunk_size=taille_cache):
            if chunk:
                f.write(chunk)
                bits_telecharges += len(chunk)
                pourcentage = bits_telecharges / download_size * 100
                print(pourcentage)
                
                
fichier= 'tests/ouioui.zip'
telecharger(lien, fichier)



with ZipFile(os.path.join(repertoire_donnees,'ouioui.zip'), 'r') as zObject:
  
    # Extracting all the members of the zip 
    # into a specific location.
    zObject.extractall(
        path=os.path.join(repertoire_donnees,'csv'))
    
os.remove(os.path.join(repertoire_donnees,'ouioui.zip'))