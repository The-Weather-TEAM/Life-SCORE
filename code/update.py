'''
                        [UPDATE.PY]
                            V.7
                         
    Programme de téléchargement et mises à jour des données



- Créé le dossier "data" avec tous les CSV dedans ;
- Télécharge et installe les fichiers lors de la première utilisation ;
- Recherche de mises à jour tous les mois et retéléchargement des csv si nouvelle version disponible ;
- Internet pas indispensable pour le programme, mais bloque lors de la première utilisation ;
- Messages sous variables pour une compabilité efficace avec Tkinter
- Code dans une fonction pour return sur le code principal une variable d'erreur
- Gestion si coupure d'internet en plein téléchargement
- Création du fichier options.csv qui permet de stocker des données pour l'application
- Implémentation de Tkinter


SOURCES :
Tout est basé sur nos cours, ou la documentation liée aux bibliothèques utilisés.
Chaque processus est pensé et écrit par notre équipe.

'''





'''
BIBLIOTHEQUES ET PROGRAMMES
 
'''
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


# Importation de la fonction de test de connexion :
from classes import is_connected as connexion
from classes import lire_option          # Utile pour lire les parametres d'utilisateur





'''
La partie des variables Tkinter est gérée par Raphaël, le reste par Nathan

'''

def format_progress_pourcentage(pourcentage: float, id: str, message: str) -> str:
    """
    Fonction qui permet de formater un message pour le console du progress de telechargement des fichiers.

    ex: "44%  -  population  -> Fichier à jour"

    - `pourcentage` contient le pourcentage du telechargement de tout les fichiers
    - `id` represent le nom du fichier (ex: population)
    - `message` contient le message à ajouter à la fin (ex: Fichier à jour)
    """
    pourcent_str = str(pourcentage)
    message = pourcent_str+"%"+" "*(4-len(pourcent_str)) + "-  "+id+"  -> " + message # n espaces depend du longeur du nombre

    return message

# Tout le code est dans une fonction pour return s'il y a une erreur ou non :
def executer(barre_progres,fenetre,message,message_pourcentage):



    # Temps en secondes entre les vérifications de mises à jour :
    #temps_maj = 2592000       #* Nombre de secondes dans un mois (30 jours)
    temps_maj = lire_option("FREQ_MAJ")





    # Variables boléennes (qui servent pour des conditions) :
    is_file_versions = is_modified = erreur_internet = mise_a_jour = False


    # Pour récupérer le chemin relatif vers le dossier data :
    repertoire_courant = os.path.dirname(__file__)
    repertoire_donnees = os.path.join(repertoire_courant+'/donnees')


    # Pour savoir si les fichiers existait avant le programme :
    is_file_versions = os.path.isfile(repertoire_donnees+'/versions.csv')

    



    # Test de connexion internet sur le site data.gouv.fr :
    # Basé sur un ancien projet de Frédéric et Nathan
    test_connexion = connexion('https://www.data.gouv.fr')

    if test_connexion :





        '''
        BASE DE DONNEES DES CSV      
                                   
        '''
        
        # Base de données gérée par Frédéric et Nathan
        with open(repertoire_courant+"/systeme/base_de_donnees.json", "r") as fichier_json :
            liste_csv = json.load(fichier_json)




        # Valeurs pour le calcul du pourcentage et le nombre de màj effectué(s) :
        nombre_total_csv = len(liste_csv)
        csv_courant = 0
        nombre_csv_modifies = 0



        # Création du dossier s'il n'existe pas :
        # Faitr par nous même à l'aide de la documentation de os
        if not os.path.exists(repertoire_donnees):
            os.makedirs(repertoire_donnees)
            os.makedirs(repertoire_donnees+'/csv')
            os.makedirs(repertoire_donnees+'/utilisateur')



        # Création du dictionnaire des nouvelles version installées :
        nouvelles_informations = {}


        
        # Création le fichier des infos s'il existe pas :
        # Source : cours de première sur l'utilisation des CSV
        if not is_file_versions :
            os.path.join(repertoire_donnees, 'versions.csv')
            csv.writer(open(repertoire_donnees+'/versions.csv', "w")).writerow(['NOM', 'VERSION'])
    
    
    
            

        # Lecture du fichier CSV des versions :
        # Source : cours de première sur la bibliothèque Pandas
        lire_versions = p.read_csv(repertoire_donnees+'/versions.csv')




        '''
        ETUDE PAR CAS DE CHAQUE FICHIER CSV
        
        '''
        # Pour chaque fichier CSV de la base de données :
        # Imaginé et codé par Nathan
        for id in liste_csv :
            
            # Initialisation de variable boolnéenne pour savoir si le csv courant est modifié :
            is_courant_modified = False
            
            
            # Comptage du fichier courant + variable boolnéenne pour savoir si le fichier existait déjà
            csv_courant += 1
            is_courant_csv = os.path.isfile(repertoire_donnees+'/csv/'+id+'.csv')
            
            
            # Si le fichier csv n'existe pas ou si son téléchargement a plus de tant de secondes :
            if not is_courant_csv or time.time() - os.path.getctime(repertoire_donnees+'/csv/'+id+'.csv') > temps_maj : 
                
                
                
                
                
                '''
                VERIFICATION VERSION
                
                '''
                
                # On récupère les données du CSV à l'aide d'un protocole :
                # Except : cours de terminale sur la gestion d'erreurs
                #https://help.opendatasoft.com/apis/ods-explore-v2/
                try :
                    metadonnees = requests.get('https://www.data.gouv.fr/api/2/datasets/'+liste_csv[id][0]).json()
                    
                except ConnectionError or ReadTimeoutError or ReadTimeout or TimeoutError : 
                    test_connexion = connexion('https://www.data.gouv.fr')
                    
                    # Si il n'y a pas de connexion et c'est le premier lancement :
                    if not test_connexion and not is_file_versions :
                                             
                        # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter) :
                        msg_erreur = "\n\n\nAccès à internet impossible : nous ne pouvons pas télécharger les données nécessaires."
                        print (msg_erreur)

                            
                        erreur_internet = True
                    

                    # Si il y a pas de connexion mais on a déjà le fichier :
                    else :
                        
                        # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter) :
                        msg_pas_internet = "\n\n\nRecherche de mises à jour annulée"
                        print (msg_pas_internet)
                            
                        erreur_internet = False
                        
                    return erreur_internet
                
                
                
                
                '''
                CONVERSION DATE EN UNIX
                Imaginé par Nathan, basé sur un ancien projet de Frédéric et Nathan
                
                '''
                
                version = metadonnees['last_modified']                    # Récupération de la date
                version = version.split('T')                              # Séparation de la date et de l'heure
                version = version[0].split('-') + version[1].split(':')   # Séparation des jours/mois/années + heures/minutes/secondes
                
                # Transforme du str() en int() dans version :
                temp_conversion_version = 0
                for i in version :
                    
                    # Si ce n'est pas des données rondes (données avec milisecondes) :
                    i = i.split('.', 1)[0]
                    
                    # Transformation du str() en int() :
                    version[temp_conversion_version] = int(i)
                    temp_conversion_version += 1
            
            
                # Conversion du tableau version en UNIX :
                date_temps = datetime.datetime(*version)
                version = time.mktime(date_temps.timetuple())
                            
                       
                       
                       
                       
                # On récupère la version téléchargée initialement si le fichier existait déjà :
                if is_file_versions and is_courant_csv:
                    message.configure(text = f"Vérification de la présence de {id}...")
                    ligne = lire_versions[lire_versions["NOM"] == id]        # Retient seulement la ligne du fichier csv
                    recup_version = ligne.values[0][1]                       # Retourne la version du fichier
                    pourcentage = csv_courant/nombre_total_csv
                    #barre_progres.configure(determinate_speed=1)
                    barre_progres.set(pourcentage)
                    message_pourcentage.configure(text = f"{round(pourcentage*100)}%")
                    
                    fenetre.update()                  # Retourne la version du fichier


                # Pour éviter une erreur, comme ça on télécharge le CSV même si on récupère pas la version :
                else : recup_version = 0    
                            
                
                
                
                # On modifie mise_a_jour ssi le .csv exisatait et si la version de l'utilisateur est différente de la dernière disponible :
                if is_courant_csv and recup_version != version :
                    mise_a_jour = True
                
                
                # Remplissage du dictionnaire des modifications ssi c'est un nouveau .csv ou si il y a une mise à jour disponible :
                if not is_courant_csv or mise_a_jour :
                    nouvelles_informations[id] = version
                
                
                
                
                # Téléchargement si data n'existait pas ou si la version du .csv était différente :
                if not is_file_versions or recup_version != version :
                    
                    
                    # Supprime la version actuelle ssi il y avait le fichier .csv :
                    if is_file_versions and is_courant_csv :
                        os.remove(repertoire_donnees+'/csv/'+id+'.csv')
                    
                    
                    # Données modifiées (courant et en général) :
                    is_courant_modified = is_modified = True
                                
                                
                    # Lien de téléchargement :    
                    lien = 'https://www.data.gouv.fr/fr/datasets/r/'+liste_csv[id][1]
                    message.configure(text = "Téléchargement du fichier "+id)
                    fenetre.update()
                    
                    
                    
                    
                    '''
                    TELECHARGEMENT DU CSV
                    
                    '''
                    
                    # On récupère le fichier .csv sur internet :
                    # Fait par Nathan à partir de la documentation de requests
                    try :
                        recup_csv_internet = requests.get(lien, allow_redirects=True, stream=True) # Stream enregistre avant que le fichier soit téléchargé (pour ChunkedEncodingError)
                        
                    except ConnectionError or ChunkedEncodingError or ProtocolError or IncompleteRead or ReadTimeoutError or ReadTimeout : 
                        test_connexion = connexion('https://www.data.gouv.fr')
                        
                        # Si il ,'y a pas de connexion et c'est le premier lancement :
                        if not test_connexion and not is_file_versions :
                            
                            # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter) :
                            msg_erreur = "\n\n\nAccès à internet impossible : nous ne pouvons pas télécharger les données nécessaires."
                            print (msg_erreur)
                            
                            # Tout supprimer pour refaire une installation propore :
                            delete_data(repertoire_donnees+'/csv')
                            
                            erreur_internet = True
                        
                        
                        # Si il y a pas de connexion mais on a déjà le fichier :
                        else :
                            
                            # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter) :
                            msg_pas_internet = "\n\n\nRecherche de mises à jour annulée"
                            print (msg_pas_internet)
                            
                            erreur_internet = False
                        
                        return erreur_internet
                    
                    
                    
                    
                    
                    # On le sauvegarde avec le bon nom et l'extention :
                    nom_du_fichier = os.path.join(repertoire_donnees+'/csv/'+id+'.csv')
                    open(nom_du_fichier, 'wb').write(recup_csv_internet.content)
                    
                    
                    
                    # Calcul pourcentage et rajout du nombre de fichiers téléchargés :
                    nombre_csv_modifies += 1
                    pourcentage = csv_courant/nombre_total_csv
                    barre_progres.configure(determinate_speed=pourcentage)
                    barre_progres.step()
                    barre_progres.set(pourcentage)
                    message_pourcentage.configure(text = f"{round(pourcentage*100)}%")
                    fenetre.update()
                    
                    
                    
                    
                '''  
                INTERFACE SUR TERMINAL + VARIABLES POUR TKINTER
                    
                '''
                pourcentage = round(pourcentage*100)

                if is_courant_modified:
                    # Message sur le terminal (provisoire, à modifier pour du Tkinter)
                    # avec gestion du nombre de caractères pour avoir du texte homogène

                    msg_csv_courant = format_progress_pourcentage(pourcentage, id, "Fichier téléchargé")

                    print (msg_csv_courant)
                    
                    # Si le fichier a été mis à jour :
                    if mise_a_jour :
                        
                        for cle, val in nouvelles_informations.items():
                            
                            # On prend seulement la  clé qui correspond au fichier courant :
                            if cle == id :
                                
                                # On actualise la version téléchargée :
                                lire_versions.loc[lire_versions["NOM"] == id, "VERSION"] = val
                                lire_versions.to_csv(repertoire_donnees+'/versions.csv', index=False)
                                
                        # On supprime les informations du dictionnaire (si en même temps il y a des nouveaux fichiers) :
                        del nouvelles_informations[id]
                        
                        # On réinitialise mise_a_jour pour les prochains .csv :
                        mise_a_jour = False
                    
                    

                          
                # Message sur le terminal (provisoire, à modifier pour du Tkinter) :
                # avec gestion du nombre de caractères pour avoir du texte homogène          
                else :
                    msg_csv_courant = format_progress_pourcentage(pourcentage, id, "Fichier à jour")

                    print (msg_csv_courant)
                        
                        
            # Message sur le terminal (provisoire, à modifier pour du Tkinter) :
            # avec gestion du nombre de caractères pour avoir du texte homogène
            else :
                pourcentage = int(csv_courant/nombre_total_csv*100)
                
                msg_csv_courant = format_progress_pourcentage(pourcentage, id, "Fichier à jour")
                        
                print (msg_csv_courant)
        
        
        
        # Message provisoire pour dire le nombre de fichiers téléchargés :
        # avec gestion du singulier / pluriel
        
            msg_reussite = "\nRecherche de mises à jour terminée !\n"
            
        if nombre_csv_modifies == 0 :
            msg_reussite += "Aucun fichier téléchargé."   
        elif nombre_csv_modifies < 2 :
            msg_reussite += str(nombre_csv_modifies)+" fichier téléchargé."    
        else :
            msg_reussite += str(nombre_csv_modifies)+" fichiers téléchargés."  
        
        print (msg_reussite)  
            
            
                
    elif is_file_versions :
        # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter) :
        msg_pas_internet = "\n\n\nRecherche de mises à jour annulée"
        
        print (msg_pas_internet)
    

    else :
        # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter) :
        msg_erreur = "\n\n\nAccès à internet impossible : nous ne pouvons pas télécharger les données nécessaires."
        erreur_internet = True
        
        print (msg_erreur)
        
        
        
        
    
    '''
    AJOUT DES INFOS DES NOUVELLES VERSIONS TELECHARGEES
    
    '''
    
    if is_modified and not mise_a_jour :
        
        rajout_donnee = csv.writer(open(repertoire_donnees+'/versions.csv', "a")) # le "a" c'est l'équivalent de .append() pour les tableaux 
            
        for cle, val in nouvelles_informations.items():
            rajout_donnee.writerow([cle, val])  
                        
        
        
    # Envoie sur le programme principal s'il y a une erreur ou non :
    return erreur_internet