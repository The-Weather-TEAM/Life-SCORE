'''
                        [UPDATE.PY]
                            V.10
          AVEC TELECHARGEMENT 125x PLUS RAPIDE !
                         
    Programme de téléchargement et mises à jour des données automatique



- Créé le dossier "data" avec tous les CSV dedans ;
- Télécharge et installe les fichiers lors de la première utilisation ;
- Recherche de mises à jour et retéléchargement des csv si nouvelle version disponible ;
- Internet pas indispensable pour le programme, mais bloque lors de la première utilisation ;
- Gestion d'erreur avancée (coupure d'internet, ...)
- Création du fichier options.csv qui permet de stocker des données pour l'application
- Implémentation de Tkinter


SOURCES :
Tout est basé sur nos cours, ou la documentation liée aux bibliothèques utilisés.
Chaque processus est pensé et écrit par Nathan 

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
from zipfile import BadZipFile

# Importation de la fonction de test de connexion :
from classes import is_connected as connexion
from classes import lire_fichier_dico          # Utile pour lire les parametres d'utilisateur
from classes import modifier_fichier_dico       # Utile pour changer les options (obvious)

# Pour deziper
from zipfile import ZipFile





def format_progress_pourcentage(pourcentage: float, id: str, message: str) -> str:
    """
    Fonction qui permet de formater un message pour le console du progress de telechargement des fichiers.

    ex: "44%  -  population  -> Fichier à jour

    - `pourcentage` contient le pourcentage du telechargement de tout les fichiers
    - `id` represent le nom du fichier (ex: population)
    - `message` contient le message à ajouter à la fin (ex: Fichier à jour)
    """

    pourcent_str = str(pourcentage)
    message = pourcent_str+"%"+" "*(4-len(pourcent_str)) + "-  "+id+"  -> " + message # n espaces depend de la longueur du nombre

    return message




def taille_zip(url):
    informations = requests.head(url, allow_redirects=True)
    content_length = informations.headers.get('Content-Length')
    if content_length is None:
        return None
    else:
        return int(content_length)




def telecharger(lien, nomfichier,barre,win,msg_prct, message):
    
    try :
        
        '''
        Animation du texte
        Conçu par Nathan
        '''
        message0 = 'Téléchargement des fichiers\nCela peut prendre quelques minutes.'
        message1 = ' Téléchargement des fichiers.\nLifeSCORE est une application de notation de commune personnalisée.'
        message2 = '  Téléchargement des fichiers..\nElle se base sur vos préférences pour vous dire à quel point une commune vous correspond.'
        message3 = '   Téléchargement des fichiers..\nElle est utile par exemple pour les personnes devant emménager quelque part.'
        message4 = 'C\'est presque terminé !\nMerci d\'avoir attendu.'
        liste_msg = [message0, message1, message2, message3, message4]
        
        message.configure(text = message0)
        msg_val = False
        nbr_msg = 0
        
        taille = taille_zip(lien)
        fichier_zip = requests.get(lien, stream=True)
        taille_cache = 1024
        bits_telecharges = 0
        with open(nomfichier, 'wb') as f:
            for chunk in fichier_zip.iter_content(chunk_size=taille_cache):
                if chunk:
                    f.write(chunk)
                    bits_telecharges += len(chunk)
                    
                    pourcentage = bits_telecharges / taille * 100 #.set prend que entre 0 et 1 donc faut pas mettre en %
                    barre.set(pourcentage/100)
                    msg_prct.configure(text = f"{round(pourcentage)}%")
                    
                    if not msg_val and round(pourcentage)%20 == 1 :
                        msg_val = True
                    
                    if round(pourcentage)%5 == 0 and msg_val :
                        message.configure(text = liste_msg[nbr_msg])
                        nbr_msg += 1
                        msg_val = False
                        
                    win.update()
                    
    except ConnectionError or ChunkedEncodingError or ProtocolError or IncompleteRead or ReadTimeoutError or ReadTimeout : 
        # Les erreurs ont étés récupéré en testant le code et sur internet, pour éviter la corruption des fichiers.
        delete_data(os.path.join(os.path.dirname(__file__)+'/donnees'))
        os.makedirs(os.path.join(os.path.dirname(__file__)+'/donnees'))
        lire_fichier_dico('APPARENCE')
        while not connexion('https://github.com/') :
            message.configure(text = 'Connexion perdue.')
            win.update()
            
        return executer(barre,win,message,msg_prct)
        
        




'''
FONCTION PRINCIPALE

'''
# Tout le code est dans une fonction pour return s'il y a une erreur ou non :
def executer(barre_progres,fenetre,message,message_pourcentage):



    # Temps en secondes entre les vérifications de mises à jour :
    #temps_maj = 2592000                #* Nombre de secondes dans un mois (30 jours) - Remplacée par le choix dans la page paramètres
    temps_maj = lire_fichier_dico("FREQ_MAJ") #  Renvoie vers la fonction de Thor dans classes.py
    derniere_maj = lire_fichier_dico("DERNIERE_MAJ") 


    # Passe la vérification des fichiers
    if time.time() - derniere_maj < temps_maj :
        return False


    # Variables boléennes (qui servent pour des conditions) :
    is_file_versions = is_modified = erreur_internet = mise_a_jour = False


    # Pour récupérer le chemin relatif vers le dossier data :
    repertoire_courant = os.path.dirname(__file__)
    repertoire_donnees = os.path.join(repertoire_courant+'/donnees')


    # Pour savoir si les fichiers existait avant le programme :
    is_file_versions = os.path.isfile(repertoire_donnees+'/versions.csv')

    



    # Test de connexion internet sur le site data.gouv.fr dans classes.py
    # Basé sur un ancien projet de Frédéric et Nathan
    test_connexion = connexion('https://www.data.gouv.fr')

    if test_connexion :





        '''
        BASE DE DONNEES DES CSV      
        par Frédéric et Nathan
        
        Idée de l'équipe, avec gestion des CSV
        '''
        
        # Base de données gérée par Frédéric et Nathan 
        # Frédéric : recherches
        # Nathan   : recherches et à la relation base de données et programme
        with open(repertoire_courant+"/systeme/base_de_donnees.json", "r") as fichier_json :
            liste_csv = json.load(fichier_json) # On le lance avec du JSON




        # Valeurs pour le calcul du pourcentage et le nombre de màj effectué(s) :
        nombre_total_csv = len(liste_csv)
        csv_courant = 0
        nombre_csv_modifies = 0



        # Création du dossier s'il n'existe pas :
        # Fait par nous même à l'aide de la documentation de la bibliothèque os
        if not os.path.exists(repertoire_donnees+'/csv'):
            
            '''
            TELECHARGEMENT AVEC FICHIER ZIP
            BCP BCP PLUS RAPIDE QU'AVANT 
            
            Pensé par Nathan
            Réalisé par Nathan (intégration à l'interface par Raphaël)
            
            '''
            lien = 'https://github.com/The-Weather-TEAM/Life-SCORE/raw/main/test.zip'
            fichier = repertoire_donnees+'/temp.zip'
            
            telecharger(lien, fichier,barre_progres,fenetre,message_pourcentage, message)
            
            try :
                with ZipFile(os.path.join(repertoire_donnees,'temp.zip'), 'r') as zObject:
            
                        # Extracting all the members of the zip 
                        # into a specific location.
                        zObject.extractall(
                            path=repertoire_donnees)
                        
                os.remove(os.path.join(repertoire_donnees,'temp.zip'))
                modifier_fichier_dico("DERNIERE_MAJ", time.time())
                    
                # RECURSIVITE pour vérifier si les fichiers téléchargés sont les derniers dispo
                return executer(barre_progres,fenetre,message,message_pourcentage)

            except BadZipFile :
                delete_data(os.path.join(os.path.dirname(__file__)+'/donnees'))
                os.makedirs(os.path.join(os.path.dirname(__file__)+'/donnees'))
                lire_fichier_dico('APPARENCE')
                while not connexion('https://github.com/') :
                    message.configure(text = 'Connexion perdue.')
                    fenetre.update()
                    
                return executer(barre_progres,fenetre,message,message_pourcentage)



        # Création du dictionnaire des nouvelles version installées :
        nouvelles_informations = {}



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
                Idée et code par Nathan
                
                Les métadonnées ont été trouvés avec la documentation de opendatasoft.com
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
                                             
                        # Message sur le terminal si on a pas internet :
                        msg_erreur = "\n\n\nAccès à internet impossible : nous ne pouvons pas télécharger les données nécessaires."
                        print (msg_erreur)

                            
                        erreur_internet = True
                    

                    # Si il y a pas de connexion mais on a déjà le fichier :
                    else :
                        
                        # Message sur le terminal si on a pas internet :
                        msg_pas_internet = "\n\n\nRecherche de mises à jour annulée"
                        print (msg_pas_internet)
                            
                        erreur_internet = False
                        
                    return erreur_internet
                
                
                
                
                '''
                CONVERSION DATE EN UNIX
                Imaginé par Nathan, basé sur un ancien projet de Frédéric et Nathan (v.4 de l'application)
                
                '''
                
                version = metadonnees['last_modified']                    # Récupération de la date
                version = version.split('T')                              # Séparation de la date et de l'heure
                version = version[0].split('-') + version[1].split(':')   # Séparation des jours/mois/années + heures/minutes/secondes
                
                # Transforme du str() en int() dans version :
                temp_conversion_version = 0
                for i in version :
                    
                    # Si ce n'est pas des données rondes (données avec milisecondes) :
                    i = i.split('.', 1)[0]
                    
                    #Supprimer les données des heures en UTC (pas besoin)
                    i = i.split('+', 1)[0]


                    # Transformation du str() en int() :
                    version[temp_conversion_version] = int(i)
                    temp_conversion_version += 1
            
            
                # Conversion du tableau version en UNIX :
                date_temps = datetime.datetime(*version) # *liste renvoie tout ce que contient la liste
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
                    Pensé et réalisé par Nathan
                    
                    Efface tout si il y a une coupure d'accès à internet pour éviter la corruption des fichiers
                    '''
                    
                    # On récupère le fichier .csv sur internet :
                    # Fait par Nathan à partir de la documentation de requests
                    try :
                        recup_csv_internet = requests.get(lien, allow_redirects=True, stream=True) # Stream enregistre avant que le fichier soit téléchargé (pour ChunkedEncodingError)
                        
                    except ConnectionError or ChunkedEncodingError or ProtocolError or IncompleteRead or ReadTimeoutError or ReadTimeout : 
                        # Les erreurs ont étés récupéré en testant le code et sur internet, pour éviter la corruption des fichiers.
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
                    # Fait par Nathan et Raphaël (pour la comptabilité Tkinter)
                    nombre_csv_modifies += 1
                    pourcentage = csv_courant/nombre_total_csv
                    barre_progres.configure(determinate_speed=pourcentage)
                    barre_progres.step()
                    barre_progres.set(pourcentage)
                    message_pourcentage.configure(text = f"{round(pourcentage*100)}%")
                    fenetre.update()
                    
                    
                    
                    
                '''  
                INTERFACE SUR TERMINAL + VARIABLES POUR TKINTER
                Fait par Nathan
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
                        
                        # Pour l'interface, dire la dernière màj
                        modifier_fichier_dico("DERNIERE_MAJ", time.time())
                        
                        
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
    Pesné et réalisé par Nathan, on a trouvé le "a" ligne 479 sur stackoverflow pour éviter de planter l'application
    '''
    
    if is_modified and not mise_a_jour :
        
        rajout_donnee = csv.writer(open(repertoire_donnees+'/versions.csv', "a")) # le "a" c'est l'équivalent de .append() pour les tableaux 
            
        for cle, val in nouvelles_informations.items():
            rajout_donnee.writerow([cle, val])  
                        
        
    print("\n\n\n\n\n")
    # Envoie sur le programme principal s'il y a une erreur ou non :
    return erreur_internet



# Fin du programme !