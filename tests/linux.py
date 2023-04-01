'''
A GARDER PROVISOIREMENT, NOTES DE COMPATIBILITEES LINUX


installer pip sur le terminal, tkinter aussi et pil.imagetk
(j'ai testé avec ubuntu sans avoir mis à jour python et mise à part les trois trucs tt fonctionne)

apt get install python3-pip
apt get install python3-tk
apt get install python3-pil.imagetk
'''

'''


# à mettre si jamais on a pas déjà import tout ça

import os
import json # Pour la lecture des données csv



# OUVERTURE DE LA BASE DE DONNEES, à mettre avant d'utiliser la fonction pour la variable infos_csv
nom_du_repertoire = os.path.dirname(__file__)
with open(os.path.join(nom_du_repertoire, "systeme/base_de_donnees.json"), "r") as fichier_json :
    infos_csv = json.load(fichier_json)
    

# Fonction qui permet de récupérer la description du csv
def texte_csv(nom_du_csv) :
    return infos_csv[nom_du_csv][2]['nom']


'''









'''
Pour varier les polices / code en fonction du système d'exploitation

Source :
https://www.quennec.fr/trucs-astuces/langages/python/python-connaitre-le-nom-du-syst%C3%A8me-et-le-nom-dh%C3%B4te-de-la-machine

'''



import platform
print(platform.system())

#Windows, Linux & Darwin (pour Macos)













#! Nathan : c'est une fonction que j'ai utilisé l'année dernière pour reload un programme, ça peut être simpa pour l'installation de modules / rede de l'application

def restart():      
    os.execl(sys.executable,             # Execute l'executable python
             os.path.abspath(__file__),  # Le fichier actuel
             *sys.argv)                  # Avec les arguments actuels
