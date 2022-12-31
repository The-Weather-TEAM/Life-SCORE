'''
Programme de téléchargement et de vérification (màj) des csv

'''

import requests
import os
import time
import internet as i


#test de connexion internet sur le site data.gouv.fr
connexion = i.Internet('https://www.data.gouv.fr')
if connexion.connected() is True :



    #tous les csv ici
    urls = {'gares' : 'https://www.data.gouv.fr/fr/datasets/r/d22ba593-90a4-4725-977c-095d1f654d28'}


    #chemin relatif vers le dossier data
    nom_du_rep = os.path.dirname(__file__)
    rep = os.path.join(nom_du_rep, 'data')

    #créer le dossier s'il n'existe pas
    if not os.path.exists(rep):
        os.makedirs(rep)



    for url in urls :
        
        #contrôle si le fichier existe et si il a plus de un mois
        if os.path.isfile(rep+'/'+url+'.csv') is False or time.time() - os.path.getctime(rep+'/'+url+'.csv') > 2592000 :
                
            #on récupère le fichier csv
            r = requests.get(urls[url], allow_redirects=True)
            
            #on le sauvegarde avec le bon nom et l'extention
            nom_du_fichier = os.path.join(rep, url+'.csv')
            open(nom_du_fichier, 'wb').write(r.content)
            
            print ("téléchargé")
        
        else :
           print("à jour")