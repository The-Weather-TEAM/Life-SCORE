'''
                        [UPDATE.PY]
                         
    Programme de téléchargement et mises à jour des données

        développé par Frédéric Marquet & Nathan Bosy



- Créé le dossier "data" avec tous les CSV dedans
- Télécharge et installe les fichiers lors de la première utilisation
- Recherche de mises à jour tous les mois et retéléchargement des csv si nouvelle version disponible
- Base de CSV stockée ici
- Internet pas indispensable pour le programme ducoup on passe si data.gouv.fr ne marche pas
- Bloque le programme si il n'y a pas intenret lors de la première utilisation
- Messages sous variables pour une compabilité efficace avec Tkinter

'''





# Bibliothèques et importation des classes
import requests
import os
import time
import classes as i
import csv
import pandas as p
import datetime
import time





# Variables boléennes (qui servent pour des conditions)
is_file, is_modified, erreur_internet = False, False, False



# Pour récupérer le chemin relatif vers le dossier data
nom_du_repertoire = os.path.dirname(__file__)
repertoire = os.path.join(nom_du_repertoire, 'data')



# Pour savoir si le fichier existait avant le programme
if os.path.isfile(repertoire+'/'+'versions.csv') :
    is_file = True





# Test de connexion internet sur le site data.gouv.fr
test_connexion = i.Internet('https://www.data.gouv.fr')
if test_connexion.is_connected() :





    '''
                                        [BASE DE DONNEES DES CSV]
                                               à compléter
    '''
    
    #         NOM                     ID DES METADONNEES                 CODE DE TELECHARGEMENT
    liste_csv = {'gares':               ['59593619a3a7291dd09c8238','d22ba593-90a4-4725-977c-095d1f654d28'],
                 'festivals':           ['62cf95993d99f22480f49334','47ac11c2-8a00-46a7-9fa8-9b802643f975'],
                 'carburants':          ['54101458a3a72937cb2c703c','64e02cff-9e53-4cb2-adfd-5fcc88b2dc09'],
                 'loi_montagne' :       ['600a90b60961636713297c87','87bc6d48-f1ed-4924-be55-0142660033de'],
                 'ZUS' :                ['5a67414888ee385f0ca521eb','0ba9346e-bc8a-4e68-9e07-73b70bcd1023'],
                 'potentiel_radon' :    ['53834c53a3a72906c7ec5c4c','817114f8-9b61-48fa-b7a4-0e3c1331a44c'],
                 'polluants' :          ['5b98b648634f415309d52a50','157ceed4-ce03-4c7d-9cd7-ae60ea07417b'],
                 'temp_quot_region' :   ['5a5ddc1ab5950825e3ecba32','50b3f76f-b20c-4095-b3f1-96f5e26cbac6'],
                 'observ_stat_meteo' :  ['5369932ca3a729239d204103','66f4cfd9-240d-4c6e-8c0b-532d26c2c1dc'],
                 'prix_m2_2017' :       ['5d6e64428b4c4179b3e88042','58b6b75e-4f15-4efb-adb5-3f7b939fb2d1'],
                 'etablissements_scol': ['5889d042a3a72974cbf0d5b8','b3b26ad1-a143-4651-afd6-dde3908196fc'],
                 'services_police' :    ['53ba5222a3a729219b7beade','2cb2f356-42b2-4195-a35c-d4e4d986c62b'],
                 'info_tourisitques' :  ['5b598be088ee387c0c353714','d6240a80-6c2c-44c1-9f13-66ffdf0b8231'],
                 'type_loyers' :        ['56fd8e8788ee387079c352f7','2ae4fb01-c69d-4a4d-bd09-f02c1b02882e'],
                 'eco_quartiers_2016' : ['588fb50dc751df5c03ae0a65','2b9cb88b-c05d-4c9e-a7dd-d71e6fd8ebb6']#,
                 
             # Données qui n'ont pas de csv directement téléchargeable sur data.gouv.fr
                 #'pesticides_eaux' :    ['594c298ec751df76726294d9','X'],
                 #'reseau_mobile' :      ['58c98b1888ee38770950152b','X'],
                 #'connexion_internet' : ['5e836644ca07c8558d91a6fc','X'],
                 #'haut_débit' :         ['547d8d7ac751df405d090fcb','X'],
                 #'musees' :             ['53699934a3a729239d2051a1','X'],
                 #'espaces_sportifs' :   ['53699ebba3a729239d205f4f','X']
                }





    # Valeurs pour le calcul du pourcentage et le nombre de màj effectué(s)
    nombre_total_csv = len(liste_csv)
    csv_courant = 0
    nombre_csv_modifies = 0



    # Création du dossier s'il n'existe pas
    if not os.path.exists(repertoire):
        os.makedirs(repertoire)



    # Création du dictionnaire des nouvelles version installées
    nouvelles_informations = {}


    
    # Création le fichier des infos s'il existe pas
    if not is_file :
        nom_fichier_infos = os.path.join(repertoire, 'versions.csv')
        csv.writer(open(repertoire+'/'+'versions.csv', "w")).writerow(['NOM', 'VERSION']) 
       
 
        
    # Lecture du fichier CSV des versions
    recup_versions = p.read_csv(repertoire+'/versions.csv')





    # Pour chaque fichier CSV de la base de données
    for id in liste_csv :
        
        
        # Comptage du fichier courant
        csv_courant += 1
        
        
        # Si le fichier csv n'existe pas ou si son téléchargement a plus de un mois
        if not os.path.isfile(repertoire+'/'+id+'.csv') or time.time() - os.path.getctime(repertoire+'/'+id+'.csv') > 2592000 : #2592000 = nombre de sec dans un mois
            
            # Données modifiées
            is_modified = True 
            
            
            # On récupère les données du CSV :
            #https://help.opendatasoft.com/apis/ods-explore-v2/
            metadonnees = requests.get('https://www.data.gouv.fr/api/2/datasets/'+liste_csv[id][0]).json()

            
            
            
            # Conversion de la date donnée par data.gouv.fr en unix directement
            version = metadonnees['last_modified']                    # Récupération de la date
            version = version.split('T')                              # Séparation de la date et de l'heure
            version = version[0].split('-') + version[1].split(':')   # Séparation des jours/mois/années + heures/minutes/secondes
            
            # Transforme du str() en int() dans version
            temp_conversion_version = 0
            for i in version :
                
                # Si ce n'est pas des données rondes (données avec milisecondes)
                i = i.split('.', 1)[0]
                
                # Transformation du str() en int()
                version[temp_conversion_version] = int(i)
                temp_conversion_version += 1
        
        
            # Conversion du tableau version en UNIX
            date_temps = datetime.datetime(version[0], version[1], version[2], version[3], version[4], version[5])
            version = time.mktime(date_temps.timetuple())
                        
                        
            
            
            
            # Remplissage du dictionnaire des modifications
            nouvelles_informations[id] = version
            
            
            
            # On récupère la version téléchargée initialement si le fichier existait déjà
            if is_file and os.path.isfile(repertoire+'/'+id+'.csv'):
                ligne = recup_versions[recup_versions["NOM"] == id]      # Retient seulement la ligne du fichier csv
                recup_version = ligne.values[0][1]                 # Retourne la version du fichier


            # Pour éviter une erreur, comme ça on télécharge le CSV même si on récupère pas la version
            else : recup_version = 0
                
                
                
                
            
            # Téléchargement si data n'existait pas ou si la version du csv était différente
            if not is_file or recup_version != version :
                
                # Données modifiées
                is_modified = True
                            
                lien = 'https://www.data.gouv.fr/fr/datasets/r/'+liste_csv[id][1]
                
                
                # On récupère le fichier CSV sur internet
                recup_csv_internet = requests.get(lien, allow_redirects=True)
                
                
                # On le sauvegarde avec le bon nom et l'extention
                nom_du_fichier = os.path.join(repertoire, id+'.csv')
                open(nom_du_fichier, 'wb').write(recup_csv_internet.content)
                
                
                
                # Calcul pourcentage et rajout du nombre de fichiers téléchargés
                nombre_csv_modifies += 1
                pourcentage = int(csv_courant/nombre_total_csv*100)
                
                
                
                
                
                '''
                
             [INTERFACE] 
     pour l'instant sur le terminal
                
                '''
                
                # Message sur le terminal (provisoire, à modifier pour du Tkinter)
                # avec gestion du nombre de caractères pour avoir du texte homogène
                if pourcentage < 10 :
                    msg_csv_courant = str(pourcentage)+"%   -  "+str(id)+"  -> Fichier téléchargé"
                elif pourcentage < 100 :
                    msg_csv_courant = str(pourcentage)+"%  -  "+str(id)+"  -> Fichier téléchargé"
                else :
                    msg_csv_courant = str(pourcentage)+"% -  "+str(id)+"  -> Fichier téléchargé"
                    
                print (msg_csv_courant)
                    
            
        # Message sur le terminal (provisoire, à modifier pour du Tkinter)
        # avec gestion du nombre de caractères pour avoir du texte homogène
        else : 
            pourcentage = int(csv_courant/nombre_total_csv*100)
            
            if pourcentage < 10 :
                msg_csv_courant = str(pourcentage)+"%   -  "+str(id)+"  -> Fichier à jour"
            elif pourcentage < 100 :
                msg_csv_courant = str(pourcentage)+"%  -  "+str(id)+"  -> Fichier à jour"
            else :
                msg_csv_courant = str(pourcentage)+"% -  "+str(id)+"  -> Fichier à jour"
                    
            print (msg_csv_courant)
    
    
    
    # Message provisoire pour dire le nombre de fichiers téléchargés
    # avec gestion du singulier / pluriel
    if nombre_csv_modifies < 2 :
        msg_reussite = "\nRecherche de mises à jour terminée ! "+str(nombre_csv_modifies)+" fichier téléchargé"    
    else :
        msg_reussite = "\nRecherche de mises à jour terminée ! "+str(nombre_csv_modifies)+" fichiers téléchargés"  
    
    print (msg_reussite)  
          
          
              
elif is_file :
    # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter)
    msg_pas_internet = "\n\n\nRecherche de mises à jour annulée"
    
    print (msg_pas_internet)
   

else :
    # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter)
    msg_erreur = "\n\n\nAccès à internet impossible : nous ne pouvons pas télécharger les données nécessaires."
    erreur_internet = True
    
    print (msg_erreur)
    
    
    
# Rajout des csv téléchargés sur le fichier versions.csv
if is_modified :
    ecriture = csv.writer(open(repertoire+'/'+'versions.csv', "a")) # le "a" c'est l'équivalent de .append() pour les tableaux
    for cle, val in nouvelles_informations.items():
        ecriture.writerow([cle, val])       
    
    
    

    
'''

  EXEMPLE DE METADONNEES QU'ON RECOIT
DE LA PART DE DATA.GOUV.FR POUR UN CSV 
          (ici avec gares.csv)





{"id":"59593619a3a7291dd09c8238",

 "title":"Liste des gares",
 
 "acronym":null,
 
 "slug":"liste-des-gares",
 
 "description":"Liste des gares du R\u00e9seau Ferr\u00e9 National.\n\nCe jeu de donn\u00e9e liste les gares du r\u00e9seau, en pr\u00e9cisant leur type (gare voyageur ou gare de fret).\n\nCe jeu publie les donn\u00e9es en l\u2019\u00e9tat des bases au 31\/12\/2021. \n\nLes \u00e9l\u00e9ments d\u2019infrastructure sont localis\u00e9s par projection sur la ligne correspondante. Les coordonn\u00e9es propos\u00e9es sont celles de la projection de l\u2019objet sur la ligne. De ce fait, il peut y avoir un \u00e9cart avec la g\u00e9olocalisation de l\u2019objet.\n\nLorsqu\u2019un \u00e9l\u00e9ment se trouve \u00e0 proximit\u00e9 de plusieurs lignes, il est projet\u00e9 sur les diff\u00e9rentes lignes.\n\nLes coordonn\u00e9es g\u00e9ographiques sont une conversion des coordonn\u00e9es ferroviaires en Lambert 93 et en WGS84 (EPSG:3857).\n\ndate de mise \u00e0 jour le 10\/08\/2022",
 
 "created_at":"2017-07-02T20:06:17.403000",
 
 "last_modified":"2022-03-24T10:25:26",
 
 "deleted":null,
 
 "private":false,
 
 "tags":["gares",
         "geolocalisation",
         "infrastructure",
         "reseau",
         "sncf-reseau"],
         
 "badges":[],
 
 "resources":{"rel":"subsection",
              "href":"https:\/\/www.data.gouv.fr\/api\/2\/datasets\/59593619a3a7291dd09c8238\/resources\/?page=1&page_size=50",
              "type":"GET",
              "total":4},
              "community_resources":{"rel":"subsection",
                                     "href":"https:\/\/www.data.gouv.fr\/api\/1\/datasets\/community_resources\/?dataset=59593619a3a7291dd09c8238&page=1&page_size=50",
                                     "type":"GET",
                                     "total":0},
                                           
 "frequency":"unknown",
 
 "frequency_date":null,
 
 "extras":{"transport:url":"https:\/\/transport.data.gouv.fr\/datasets\/liste-des-gares"},
 
 "metrics":{"discussions":3,
            "reuses":2,
            "followers":1,
            "views":507},
            "organization":{"name":"SNCF",
                            "acronym":null,
                            "uri":"https:\/\/www.data.gouv.fr\/api\/1\/organizations\/sncf\/",
                            "slug":"sncf",
                            "page":"https:\/\/www.data.gouv.fr\/fr\/organizations\/sncf\/",
                            "logo":"https:\/\/static.data.gouv.fr\/avatars\/f3\/0b8ad932f74086a6ab3f291ee9243f-original.png",
                            "logo_thumbnail":"https:\/\/static.data.gouv.fr\/avatars\/f3\/0b8ad932f74086a6ab3f291ee9243f-100.png",
                            "badges":[{"kind":"public-service"},{"kind":"certified"}],"id":"534fffb0a3a7292c64a78115",
                            "class":"Organization"},
            "owner":null,
            "temporal_coverage":null,
            "spatial":null,
            "license":"odc-odbl",
            "uri":"https:\/\/www.data.gouv.fr\/api\/1\/datasets\/liste-des-gares\/",
            "page":"https:\/\/www.data.gouv.fr\/fr\/datasets\/liste-des-gares\/",
            "last_update":"2022-03-24T10:25:26",
            "archived":null,
            "quality":{"license":true,
                       "temporal_coverage":false,
                       "spatial":false,
                       "update_frequency":false,
                       "dataset_description_quality":true,
                       "has_resources":true,
                       "has_open_format":true,
                       "all_resources_available":true,
                       "resources_documentation":true,
                       "score":0.5555555556},
            "harvest":{"backend":"OpenDataSoft",
                       "modified_at":"2022-03-24T10:25:26",
                       "source_id":"563dd01f88ee386a21e72046",
                       "remote_id":"liste-des-gares",
                       "domain":"ressources.data.sncf.com",
                       "last_update":"2022-12-30T05:00:40.406000",
                       "remote_url":"https:\/\/ressources.data.sncf.com\/explore\/dataset\/liste-des-gares\/",
                       "ods_url":"https:\/\/ressources.data.sncf.com\/explore\/dataset\/liste-des-gares\/",
                       "ods_has_records":true,
                       "ods_geo":true}}
'''