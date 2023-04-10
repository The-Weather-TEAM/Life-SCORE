'''
                        [UPDATE.PY]
                                  
 Programme de téléchargement et mises à jour des données automatique



- Créé le dossier "donnees" avec tous les CSV dedans ;
- Télécharge et installe les fichiers lors de la première utilisation (sous un fichier .zip) ;
- Recherche de mises à jour et retéléchargement des csv si nouvelle version disponible ;
- Internet pas indispensable pour le programme, mais bloque lors de la première utilisation ;
- Implémentation graphique.


SOURCES :
Tout est basé sur nos cours, ou la documentation liée aux bibliothèques utilisés.

Chaque processus est pensé et écrit par Nathan 
'''





'''
BIBLIOTHEQUES ET FONCTIONS EXTERNES
 
'''
# Bibliothèques souvent utilisées :
import os                                         # Pour utiliser les répertoires
from shutil import rmtree as supprimer_repertoire # Pour supprimer le dossier si coupure de réseau
import requests                                   # Demandes de connexion

# Bibliothèques pour la modification de documents :
import csv                                        # Lecture des CSV
import pandas as p                                # Lecture et écriture des CSV
import json                                       # Pour lire notre base de données

# Bibliothèques pour les conversions de temps :
import datetime                                   # Conversion UNIX + vérification des versions
import time                                       # Conversion UNIX
    
# Bibliothèques pour éviter erreurs de coupure réseau :
from requests.exceptions import ConnectionError, ChunkedEncodingError, ReadTimeout
from urllib3.exceptions import ProtocolError, ReadTimeoutError
from http.client import IncompleteRead
from zipfile import BadZipFile

# Importation de la fonction de test de connexion :
from classes import est_connecte
from classes import lire_fichier_dico           # Utile pour lire les parametres d'utilisateur
from classes import modifier_fichier_dico       # Utile pour changer les options (logique)

# Pour deziper les csv
from zipfile import ZipFile





def terminal_progession(pourcentage: float, id: str, message: str) -> str:
    '''
    Fonction qui permet de formater un message pour le console du progress de telechargement des fichiers.

    ex: "44%  -  population  -> Fichier à jour

    - `pourcentage` contient le pourcentage du telechargement de tout les fichiers
    - `id` represent le nom du fichier (ex: population)
    - `message` contient le message à ajouter à la fin (ex: Fichier à jour)
    '''

    pourcent_str = str(pourcentage)
    message = pourcent_str+"%"+" "*(4-len(pourcent_str)) + "-  "+id+"  -> " + message # n espaces depend de la longueur du nombre

    return message




def taille_fichier(lien):
    '''
    Fonction qui envoie une requête à GitHUB pour savoir la longueur du fichier zip qu'on télécharge.
    
    Pensé par Nathan, aidé par la documentation de requests (pour le request.head)
    '''
    informations = requests.head(lien, allow_redirects=True) # On récupère seulement les informations du fichier (léger)
    taille_du_fichier = informations.headers.get('Content-Length')
    return int(taille_du_fichier)




def telecharger_fichier(lien, nom_fichier, barre_de_chargement, fenetre, msg_pourcentage, msg_information):
    '''
    Fonction qui permet de télécharger le fichier .zip tout en affichant l'avancement
    
    Pensé et réalisé par Nathan
    Compatibilité graphique par Raphaël
    
    '''
    try :
        msg_information.configure(text = 'Téléchargement des fichiers\nCela peut prendre quelques temps.')

        # On recupère la taille du fichier, et le cache ect.
        taille = taille_fichier(lien)
        fichier_zip = requests.get(lien, stream=True)
        taille_cache = 2**16 # Modifiable, en bit le nombre de données téléchargées par fragment
        bits_telecharges = 0
        
        with open(nom_fichier, 'wb') as f:
            
            # Pour chaque partie du fichier, on avance
            for fragment in fichier_zip.iter_content(chunk_size=taille_cache):
                if fragment:
                    f.write(fragment)
                    bits_telecharges += len(fragment)
                    
                    # Affichage du pourcentage
                    pourcentage = bits_telecharges / taille * 100
                    barre_de_chargement.set(pourcentage/100)
                    msg_pourcentage.configure(text = f"{round(pourcentage)}%")

                    fenetre.update()
                    
    # Si il y a une coupure de connexion
    except ConnectionError or ChunkedEncodingError or ProtocolError or IncompleteRead or ReadTimeoutError or ReadTimeout : 
        
        # On supprime le dossier donnees puis on le reconfigure
        supprimer_repertoire(os.path.join(os.path.dirname(__file__)+'/donnees'))
        os.makedirs(os.path.join(os.path.dirname(__file__)+'/donnees'))
        
        lire_fichier_dico('APPARENCE') # Pour créer le fichier options.txt (fait par Thor)
        
        # Tant qu'on a pas une connexion établie
        while not est_connecte('https://github.com/') :
            msg_information.configure(text = 'Connexion perdue.\nVeuillez vérifier votre connexion à internet.')
            fenetre.update()
        
        # Récurvivité pour relacer le téléchargement de 0, et éviter les problèmes de corruption de fichiers
        return mise_a_jour(barre_de_chargement, fenetre, msg_information, msg_pourcentage)
        
        


def mettre_a_jour() :
    '''
    Fonction qui permet de savoir si on doit mettre à jour ou non
    
    Pensé et réalisé par Nathan
    pour éviter qu'une fenêtre s'ouvre même si on doit pas mettre à jour.
    '''
    # Temps en secondes entre les vérifications de mises à jour :
    frequence_maj = lire_fichier_dico("FREQ_MAJ") #  Renvoie vers la fonction de Thor dans classes.py
    derniere_maj = lire_fichier_dico("DERNIERE_MAJ") 
    if time.time() - derniere_maj < frequence_maj :
        return False
    
    else :
        return True





'''
FONCTION PRINCIPALE

'''
# Tout le code est dans une fonction pour return s'il y a une erreur ou non :
def mise_a_jour(barre_de_chargement, fenetre, msg_information, msg_pourcentage):


    # Variables boléennes (qui servent pour des conditions) :
    est_modifie = erreur_internet = est_mise_a_jour = False


    # Pour récupérer le chemin relatif vers le dossier data :
    repertoire_courant = os.path.dirname(__file__)
    repertoire_donnees = os.path.join(repertoire_courant+'/donnees')


    # Pour savoir si les fichiers existait avant le programme :
    est_fichier_versions = os.path.isfile(repertoire_donnees+'/versions.csv')

    



    # Test de connexion internet sur le site data.gouv.fr dans classes.py
    # Basé sur un ancien projet de Frédéric et Nathan
    test_connexion = est_connecte('https://www.data.gouv.fr')

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
        numero_csv_courant = 0
        nombre_csv_modifies = 0



        # Création du dossier s'il n'existe pas :
        # Fait par nous même à l'aide de la documentation de la bibliothèque os
        if not os.path.exists(repertoire_donnees+'/csv'):
            
            '''
            TELECHARGEMENT AVEC FICHIER ZIP
            Plus rapide que de télécharger les fichiers csv un par un.
            
            Pensé par Nathan
            Réalisé par Nathan (intégration à l'interface par Raphaël)
            '''
            lien = 'https://github.com/The-Weather-TEAM/Life-SCORE/raw/main/test.zip' #! à changer une fois le code terminé
            fichier = repertoire_donnees+'/temp.zip'
            
            telecharger_fichier(lien, fichier, barre_de_chargement, fenetre, msg_pourcentage, msg_information)
            
            try :
                # On dézipe le fichier
                with ZipFile(os.path.join(repertoire_donnees,'temp.zip'), 'r') as fichier_zip:
                    
                        fichier_zip.extractall(
                            path=repertoire_donnees)
                
                # On supprime le fichier téléchargé
                os.remove(os.path.join(repertoire_donnees,'temp.zip'))
                    
                # Récursivité pour vérifier si les fichiers téléchargés sont les derniers dispo
                return mise_a_jour(barre_de_chargement, fenetre, msg_information, msg_pourcentage)

            # Si jamais le fichier .zip est corrompu
            except BadZipFile :
                # On supprime puis réinitialise le repertoire
                supprimer_repertoire(os.path.join(os.path.dirname(__file__)+'/donnees'))
                os.makedirs(os.path.join(os.path.dirname(__file__)+'/donnees'))
                lire_fichier_dico('APPARENCE') # Pour créer le fichier options.txt
                
                # Tant qu'on a pas de connexion à internet
                while not est_connecte('https://github.com/') :
                    msg_information.configure(text = 'Connexion perdue.\nVeuillez vérifier votre connexion à internet.')
                    fenetre.update()
                
                # Récurvivité ici aussi
                return mise_a_jour(barre_de_chargement, fenetre, msg_information, msg_pourcentage)



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
        for csv_courant in liste_csv :
            
            # Initialisation de variable boolnéenne pour savoir si le csv courant est modifié :
            est_courant_modifie = False
            
            
            # Comptage du fichier courant + variable boolnéenne pour savoir si le fichier existait déjà
            numero_csv_courant += 1
            est_courant_csv = os.path.isfile(repertoire_donnees+'/csv/'+csv_courant+'.csv')
            
            
            # Si le fichier csv n'existe pas ou si son téléchargement a plus de tant de secondes :
            if not est_courant_csv or time.time() - os.path.getctime(repertoire_donnees+'/csv/'+csv_courant+'.csv') > lire_fichier_dico("FREQ_MAJ") : 
                
                
                '''
                VERIFICATION VERSION
                Idée et code par Nathan
                
                Les métadonnées ont été trouvés avec la documentation de opendatasoft.com
                '''
                
                # On récupère les données du CSV à l'aide d'un protocole :
                # Except : cours de terminale sur la gestion d'erreurs
                #https://help.opendatasoft.com/apis/ods-explore-v2/
                try :
                    metadonnees = requests.get('https://www.data.gouv.fr/api/2/datasets/'+liste_csv[csv_courant][0]).json()
                    
                except ConnectionError or ReadTimeoutError or ReadTimeout or TimeoutError : 
                    test_connexion = est_connecte('https://www.data.gouv.fr')
                    
                    # Si il n'y a pas de connexion et c'est le premier lancement :
                    if not test_connexion and not est_fichier_versions :
                                             
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
                tempo_conversion_version = 0
                for indice in version :
                    
                    # Si ce n'est pas des données rondes (données avec milisecondes) :
                    indice = indice.split('.', 1)[0]
                    
                    #Supprimer les données des heures en UTC (pas besoin)
                    indice = indice.split('+', 1)[0]


                    # Transformation du str() en int() :
                    version[tempo_conversion_version] = int(indice)
                    tempo_conversion_version += 1
            
            
                # Conversion du tableau version en UNIX :
                date_temps = datetime.datetime(*version) # *liste renvoie tout ce que contient la liste
                version = time.mktime(date_temps.timetuple())
                            
                       
                       
                       
                       
                # On récupère la version téléchargée initialement si le fichier existait déjà :
                if est_fichier_versions and est_courant_csv:
                    msg_information.configure(text = f"Vérification de la présence de {csv_courant}...")
                    ligne = lire_versions[lire_versions["NOM"] == csv_courant]      # Retient seulement la ligne du fichier csv
                    recuperation_version = ligne.values[0][1]                       # Retourne la version du fichier
                    pourcentage = numero_csv_courant/nombre_total_csv
                    barre_de_chargement.set(pourcentage)
                    msg_pourcentage.configure(text = f"{round(pourcentage*100)}%")
                    
                    fenetre.update()                  # Retourne la version du fichier


                # Pour éviter une erreur, comme ça on télécharge le CSV même si on récupère pas la version :
                else : recuperation_version = 0    
                            
                
                
                
                # On modifie mise_a_jour ssi le .csv exisatait et si la version de l'utilisateur est différente de la dernière disponible :
                if est_courant_csv and recuperation_version != version :
                    est_mise_a_jour = True
                
                
                # Remplissage du dictionnaire des modifications ssi c'est un nouveau .csv ou si il y a une mise à jour disponible :
                if not est_courant_csv or est_mise_a_jour :
                    nouvelles_informations[csv_courant] = version
                
                
                
                
                # Téléchargement si data n'existait pas ou si la version du .csv était différente :
                if not est_fichier_versions or recuperation_version != version :
                    
                    
                    # Supprime la version actuelle ssi il y avait le fichier .csv :
                    if est_fichier_versions and est_courant_csv :
                        os.remove(repertoire_donnees+'/csv/'+csv_courant+'.csv')
                    
                    
                    # Données modifiées (courant et en général) :
                    est_courant_modifie = est_modifie = True
                                
                                
                    # Lien de téléchargement :    
                    lien = 'https://www.data.gouv.fr/fr/datasets/r/'+liste_csv[csv_courant][1]
                    msg_information.configure(text = "Téléchargement du fichier "+csv_courant)
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
                        test_connexion = est_connecte('https://www.data.gouv.fr')
                        
                        # Si il ,'y a pas de connexion et c'est le premier lancement :
                        if not test_connexion and not est_fichier_versions :
                            
                            # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter) :
                            msg_erreur = "\n\n\nAccès à internet impossible : nous ne pouvons pas télécharger les données nécessaires."
                            print (msg_erreur)
                            
                            # Tout supprimer pour refaire une installation propore :
                            supprimer_repertoire(repertoire_donnees+'/csv')
                            
                            erreur_internet = True
                        
                        
                        # Si il y a pas de connexion mais on a déjà le fichier :
                        else :
                            
                            # Message sur le terminal si on a pas internet (provisoire, à modifier pour du Tkinter) :
                            msg_pas_internet = "\n\n\nRecherche de mises à jour annulée"
                            print (msg_pas_internet)
                            
                            erreur_internet = False
                        
                        return erreur_internet
                    
                    
                    
                    
                    
                    # On le sauvegarde avec le bon nom et l'extention :
                    nom_du_fichier = os.path.join(repertoire_donnees+'/csv/'+csv_courant+'.csv')
                    open(nom_du_fichier, 'wb').write(recup_csv_internet.content)
                    
                    
                    
                    # Calcul pourcentage et rajout du nombre de fichiers téléchargés :
                    # Fait par Nathan et Raphaël (pour la comptabilité Tkinter)
                    nombre_csv_modifies += 1
                    pourcentage = numero_csv_courant/nombre_total_csv
                    barre_de_chargement.configure(determinate_speed=pourcentage)
                    barre_de_chargement.step()
                    barre_de_chargement.set(pourcentage)
                    msg_pourcentage.configure(text = f"{round(pourcentage*100)}%")
                    fenetre.update()
                    
                    
                    
                    
                '''  
                INTERFACE SUR TERMINAL + VARIABLES POUR TKINTER
                Fait par Nathan
                '''
                pourcentage = round(pourcentage*100)

                if est_courant_modifie:
                    # Message sur le terminal (provisoire, à modifier pour du Tkinter)
                    # avec gestion du nombre de caractères pour avoir du texte homogène

                    msg_csv_courant = terminal_progession(pourcentage, csv_courant, "Fichier téléchargé")

                    print (msg_csv_courant)
                    
                    # Si le fichier a été mis à jour :
                    if est_mise_a_jour :
                        
                        for cle, val in nouvelles_informations.items():
                            
                            # On prend seulement la  clé qui correspond au fichier courant :
                            if cle == csv_courant :
                                
                                # On actualise la version téléchargée :
                                lire_versions.loc[lire_versions["NOM"] == csv_courant, "VERSION"] = val
                                lire_versions.to_csv(repertoire_donnees+'/versions.csv', index=False)
                                
                        # On supprime les informations du dictionnaire (si en même temps il y a des nouveaux fichiers) :
                        del nouvelles_informations[csv_courant]
                        
                        
                        # On réinitialise mise_a_jour pour les prochains .csv :
                        est_mise_a_jour = False
                    
                    

                          
                # Message sur le terminal (provisoire, à modifier pour du Tkinter) :
                # avec gestion du nombre de caractères pour avoir du texte homogène          
                else :
                    msg_csv_courant = terminal_progession(pourcentage, csv_courant, "Fichier à jour")

                    print (msg_csv_courant)
                        
                        
            # Message sur le terminal (provisoire, à modifier pour du Tkinter) :
            # avec gestion du nombre de caractères pour avoir du texte homogène
            else :
                pourcentage = int(numero_csv_courant/nombre_total_csv*100)
                
                msg_csv_courant = terminal_progession(pourcentage, csv_courant, "Fichier à jour")
                        
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
            
            
                
    elif est_fichier_versions :
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
    
    if est_modifie and not est_mise_a_jour :
        
        try :
            os.remove(repertoire_donnees+'/cache.txt')
        except :
            print('Fichier cache innexistant.')


        rajout_donnee = csv.writer(open(repertoire_donnees+'/versions.csv', "a")) # le "a" c'est l'équivalent de .append() pour les tableaux 
            
        for cle, val in nouvelles_informations.items():
            rajout_donnee.writerow([cle, val])  
                        
        
    print("\n\n\n\n\n")
    
    # Pour l'interface, dire la dernière màj
    modifier_fichier_dico("DERNIERE_MAJ", time.time())
    
    # Envoie sur le programme principal s'il y a une erreur ou non :
    return erreur_internet



# Fin du programme !