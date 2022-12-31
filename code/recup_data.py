'''
Programme de téléchargement des CSV
- créer le dossier data avec tous les csv dedans
- télécharge et installe les fichiers lors de la première utilisation
- recherche de mise à jour tous les mois et retéléchargement des csv si nouvelle version disponible
- base de csv stockée ici
'''

import requests
import os
import time
import internet as i
import csv
import pandas as p
import datetime
import time



#test de connexion internet sur le site data.gouv.fr
connexion = i.Internet('https://www.data.gouv.fr')
if connexion.connected() is True :



    #tous les csv ici
    #         NOM      ID DES METADONNEES                 CODE DE TELECHARGEMENT
    urls = {'gares':['59593619a3a7291dd09c8238','d22ba593-90a4-4725-977c-095d1f654d28'],
            'festivals':['62cf95993d99f22480f49334','47ac11c2-8a00-46a7-9fa8-9b802643f975']}

#                                          à remplir




    #chemin relatif vers le dossier data
    nom_du_rep = os.path.dirname(__file__)
    rep = os.path.join(nom_du_rep, 'data')

    #créer le dossier s'il n'existe pas
    if not os.path.exists(rep):
        os.makedirs(rep)


    #dictionnaire des nouvelles version installées
    infos = {}
    
    #variables boléennes
    if_file, modified = False, False
    

    #pour savoir si le fichier existait
    if os.path.isfile(rep+'/'+'versions.csv') :
        if_file = True
    
    
    #créer le fichier des infos s'il existe pas
    else :
        nom_fichier_infos = os.path.join(rep, 'versions.csv')
        csv.writer(open(rep+'/'+'versions.csv', "w")).writerow(['NOM', 'VERSION']) 
        
        
    #lecture du fichier csv
    recup_infos = p.read_csv(rep+'/versions.csv')





    for url in urls :
        
        #si le fichier csv n'existe pas ou si son téléchargement a plus de un mois
        if not os.path.isfile(rep+'/'+url+'.csv') or time.time() - os.path.getctime(rep+'/'+url+'.csv') > 2592000 :
            
            #données modifiées
            modified = True 
            
            #récupère les données du csv
            #https://help.opendatasoft.com/apis/ods-explore-v2/
            metadonnees = requests.get('https://www.data.gouv.fr/api/2/datasets/'+urls[url][0]).json()

            
            #conversion de la date donnée par data.gouv.fr en unix directement
            version = metadonnees['last_modified']
            version = version.split('T')
            version = version[0].split('-') + version[1].split(':')
            
            #transforme str en int dans version
            nbr = 0
            for i in version :
                version[nbr] = int(i)
                nbr += 1
        
            #conversion en unix
            date_time = datetime.datetime(version[0], version[1], version[2], version[3], version[4], version[5])
            version = time.mktime(date_time.timetuple())
                        
                        
            
            #remplissage du dictionnaire
            infos[url] = version
            
            
            
            #on récupère la version téléchargée initialement
            if if_file and os.path.isfile(rep+'/'+url+'.csv'):
                ligne = recup_infos[recup_infos["NOM"] == url]     # retient seulement la ligne du fichier csv
                recup_version = ligne.values[0][1]                 # retourne la version du fichier

            else : recup_version = 0
                
            
                
            #téléchargement si data n'existait pas ou si la version du csv était différente
            if not if_file or recup_version != version :
                
                #données modifiées
                modified = True
                            
                lien = 'https://www.data.gouv.fr/fr/datasets/r/'+urls[url][1]
                
                
                #on récupère le fichier csv
                r = requests.get(lien, allow_redirects=True)
                
                #on le sauvegarde avec le bon nom et l'extention
                nom_du_fichier = os.path.join(rep, url+'.csv')
                open(nom_du_fichier, 'wb').write(r.content)
                

                #provisoire
                print ("Fichier téléchargé")
            
               #provisoire
        else : print("Fichier csv à jour")
            
            
#rajout des csv téléchargés
if modified :
    w = csv.writer(open(rep+'/'+'versions.csv', "a")) #le "a" c'est pour le append
    for key, val in infos.items():
        w.writerow([key, val])       
    
    
    
    
    
'''

EXEMPLE DE METADONNEES QU'ON RECOIT
DE LA PART DE DATA.GOUV.FR
POUR UN CSV


{"id":"59593619a3a7291dd09c8238",
"title":"Liste des gares",
"acronym":null,
"slug":"liste-des-gares",
"description":"Liste des gares du R\u00e9seau Ferr\u00e9 National.\n\nCe jeu de donn\u00e9e liste les gares du r\u00e9seau, en pr\u00e9cisant leur type (gare voyageur ou gare de fret).\n\nCe jeu publie les donn\u00e9es en l\u2019\u00e9tat des bases au 31\/12\/2021. \n\nLes \u00e9l\u00e9ments d\u2019infrastructure sont localis\u00e9s par projection sur la ligne correspondante. Les coordonn\u00e9es propos\u00e9es sont celles de la projection de l\u2019objet sur la ligne. De ce fait, il peut y avoir un \u00e9cart avec la g\u00e9olocalisation de l\u2019objet.\n\nLorsqu\u2019un \u00e9l\u00e9ment se trouve \u00e0 proximit\u00e9 de plusieurs lignes, il est projet\u00e9 sur les diff\u00e9rentes lignes.\n\nLes coordonn\u00e9es g\u00e9ographiques sont une conversion des coordonn\u00e9es ferroviaires en Lambert 93 et en WGS84 (EPSG:3857).\n\ndate de mise \u00e0 jour le 10\/08\/2022",
"created_at":"2017-07-02T20:06:17.403000",
"last_modified":"2022-03-24T10:25:26",
"deleted":null,
"private":false,
"tags":["gares","geolocalisation","infrastructure","reseau","sncf-reseau"],
"badges":[],
"resources":{"rel":"subsection","href":"https:\/\/www.data.gouv.fr\/api\/2\/datasets\/59593619a3a7291dd09c8238\/resources\/?page=1&page_size=50",
"type":"GET","total":4},
"community_resources":{"rel":"subsection","href":"https:\/\/www.data.gouv.fr\/api\/1\/datasets\/community_resources\/?dataset=59593619a3a7291dd09c8238&page=1&page_size=50","type":"GET","total":0},
"frequency":"unknown",
"frequency_date":null,
"extras":{"transport:url":"https:\/\/transport.data.gouv.fr\/datasets\/liste-des-gares"},"metrics":{"discussions":3,"reuses":2,"followers":1,"views":507},"organization":{"name":"SNCF","acronym":null,"uri":"https:\/\/www.data.gouv.fr\/api\/1\/organizations\/sncf\/","slug":"sncf","page":"https:\/\/www.data.gouv.fr\/fr\/organizations\/sncf\/","logo":"https:\/\/static.data.gouv.fr\/avatars\/f3\/0b8ad932f74086a6ab3f291ee9243f-original.png","logo_thumbnail":"https:\/\/static.data.gouv.fr\/avatars\/f3\/0b8ad932f74086a6ab3f291ee9243f-100.png","badges":[{"kind":"public-service"},{"kind":"certified"}],"id":"534fffb0a3a7292c64a78115","class":"Organization"},"owner":null,"temporal_coverage":null,"spatial":null,"license":"odc-odbl","uri":"https:\/\/www.data.gouv.fr\/api\/1\/datasets\/liste-des-gares\/","page":"https:\/\/www.data.gouv.fr\/fr\/datasets\/liste-des-gares\/","last_update":"2022-03-24T10:25:26","archived":null,"quality":{"license":true,"temporal_coverage":false,"spatial":false,"update_frequency":false,"dataset_description_quality":true,"has_resources":true,"has_open_format":true,"all_resources_available":true,"resources_documentation":true,"score":0.5555555556},"harvest":{"backend":"OpenDataSoft","modified_at":"2022-03-24T10:25:26","source_id":"563dd01f88ee386a21e72046","remote_id":"liste-des-gares","domain":"ressources.data.sncf.com","last_update":"2022-12-30T05:00:40.406000","remote_url":"https:\/\/ressources.data.sncf.com\/explore\/dataset\/liste-des-gares\/","ods_url":"https:\/\/ressources.data.sncf.com\/explore\/dataset\/liste-des-gares\/","ods_has_records":true,"ods_geo":true}}

'''