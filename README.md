# Life SCORE
Life score est une application pensée et conçue par cinq étudiants du lycée Henri IV Béziers. Il permet, après une analyse de l'utilisateur, d'évaluer des villes et villages sur 100 par rapport à des centaines de critères, de partout en France.

Réalisé par :
- Frédéric M.
- Nathan B.
- Raphël F.
- Thor N.
- Noémie L.





# Le projet
Le logiciel est reparti en 2 sections : la première est le test afin de connaître au maximum les attentes de l'utilisateur. Le deuxième permet de choisir une ville et défini le résultat (avec détails) du niveau de compatibilité par rapport à la demande.



### La notation
Pour chaque critère, on définit une note sur 100 ainsi qu'un coefficient qui est de base 1. Le plus de critères sont réunis afin d'avoir le plus de précision possible. Ils sont répartis en 4 catégories :

 - Le climat *(pluie en un an / pollution de l'air / températures / vent / ...)*
 - La qualité de vie (activités / patrimoine / ville fleurie / ...)
 - Le prix *(essence / gaz / loyer / prix de la vie / salaire moyen / ...)*
 - La sécurité *(taux d'accidents / vols / risques / ...)*


### La personnalisation 
Chaque utilisateur va devoir remplir un formulaire de quelques minutes. Chaque réponse impactera le coefficient de plusieurs critères, pouvant devenir nul à très important. La note sera donc en fonction de l'utilisateur qui utilise notre application !


### La gestion d'erreurs
Notre projet porte une grande importance sur la gestion des bugs et erreurs. Nous faisons tout le possible pour, quoi qu'il arrive, trouver une alternative face à un problème tout en anticipant les erreurs possibles :
- Système de l'utilisateur pas aux normes
- Connexion internet
- Corruption et mise à jour des fichiers...





# Version actuelle : v0.5.2

> Gère le téléchargement des données des villes, avec système de mise à jour automatique / Répère les préférences de l'utilisateur à l'aide d'un QCM / Recupère les données des villes et nous donne la note en fonction de l'utilisateur.

> Ne prend en compte que le nombre d'établissements sportifs par nombre d'habitants dans la ville

Lien vers la liste complète des changements : https://github.com/The-Weather-TEAM/Life-SCORE/releases


- LifeSCORE.py : *Code principal avec l'interface graphique et utilise tous les programmes. Réalise le QCM et affiche la note et les données.*
- classes.py : *Répertorie la classes Donnees (calcule les données), ainsi que toutes les fonctions comme is_connected*
- update.py : *Programme de téléchargement et mises à jour des données*
- calcul_coefficients.py : *Cacul de l'importance des notations en fonction des résultats du QCM*


Changements :
- Les demandes de villes s'adaptent, il n'y a plus d'erreur ;
- Changement de style (clair / foncé) et sauvegarde des paramètres ;
- Les arrondissements marchent ;
- Nouvelle base de donnée et récupération automatique et plus rapide des données ;
- Il n'y a plus de changement de fenêtres : les transitions sont plus fluides ;
- Gestion automatique des bibliothèques et mises à jour ;
- Animation de la note (avec fonction maths) et nouvelle police d'écriture.




## Bibliothèques utilisées :
- requests
- os
- ssl 
- time
- csv
- pandas
- datetime
- time
- tkinter
- shutil
- urllib3
- http
- customtkinter (source : https://github.com/TomSchimansky/CustomTkinter)
- pyglet
- subprocess
- sys
- json
- random
- re




## Configuration recommandée :
- Windows 10 / 11
- Python 3.11.x
- Bibliothèques utilisés (téléchargeables avec requirements.txt) :
>Téléchargement automatique sur l'application depuis la v0.5.2.





# Journal de bord
Toutes les modifications reprtoriées ici : https://github.com/The-Weather-TEAM/Life-SCORE/commits/main

8 Décembre 2022
> Mise en place de l'idée générale : faire une application qui permet de noter les villes. 

> Travail sur la personnalisation : comment faire pour avoir un logiciel personnalisé.

> Première répartition du travail : 
>-  Raphaël et Noémie -> Interface graphique
>-  Frédéric -> Traitement de données des API pour la météo et le climat
>-  Thor -> Programmation des coefficients entre le formulaire et la notation 
>-  Nathan -> Traitement de bases de données + Graphisme



10 Décembre 2022
> Interface : première page créée avec la fonction pour le QCM à réponse binaire (0,1 mais vue par l'utilisateur comme un adjectif/nom).

> Il faut trouver les questions (je suis parti sur une base de 10 Questions ca me semble pas mal). N'hésitez pas a jeter un coup d'oeil au code fréquemment pour comprendre les ajouts et me demander s'il y a des soucis.



11 Décembre 2022
> Interface : Fin de la première page au niveau fonctionnel (on pose les questions et ensuite on envoie sur la seconde page) et création de la seconde page(vide pour l'instant).

> Même chose, chercher les questions mais maintenant c'est que l'aspect esthétique de la page et ses questions à trouver (Thor si le dico ne te vas pas dis le moi).



14 Décembre 2022
> Ajout de quelques questions (+5).

> Agrandissement automatique (plein écran) et essais avec la fenêtre de l'utilisateur.

> Création de la seconde Page avec une entrée (Il faut créer le bouton).

> Création de la 3 ème page et tentative de bouton de retour (nous renvoie à la seconde page).



17 Décembre 2022
> Creation du fichier recup_meteo_classe qui utilise le même fonctionnement que l'autre mais sous forme de classe (plus facile à appeler).

> Ajout de "la ville existe ?" : Fonction qui vérifie mis dans 'fenetre.py'.

> Il faut désormais vérifier qu'elle soit en France.

> Protoype de la fonction de couleur.



18 Décembre 2022
> Mise en place de la page finale.

> Ajout de la liste des 5 avantages/inconvénients (5 meilleurees et pires note dans le dico).

> tentative de test_connection (pas ouf empeche le lancement du programme si il n'y a pas de connexion.



26 Décembre 2022
> Mise en place d'une classe qui récupère toutes les données météo de la ville demandée. On récupère tout ça sous un dictionnaire.

> Mise à jour de la méthode pour savoir si la ville est Française. (sans passer par un autre CSV).

> Création d'un répertoire de fichiers CSV qui vont nous aider à mettre en place la note.



31 Décembre 2022
> Création d'un code "recup_data.py" qui sert à plusieurs choses : 
>- créer le dossier data avec tous les csv dedans
>- télécharge et installe les fichiers lors de la première utilisation
>- recherche de mise à jour tous les mois et retéléchargement des csv si nouvelle version disponible
>- avec la base de csv stockée dessus.

> J'ai renommé les fichiers notamment 'recup_meteo_classe' en 'recup_meteo', c'est plus simple et j'ai modifié les codes qui les utilisent comme ça pas de souci.

> Création d'un code avec une classe qui vérifie si le site marche (internet.py), comme ça on peut faire le test avec data.gouv.fr ou un autre site d'api, c'est plus simple et efficace. Pas d'arrêt du programme mais seulement un retour d'une valeur booléenne.



1 Janvier 2023
> Bonne année ! Modification de l'organisation des fichiers : toutes les classes sont dans le fichier classes.py. J'ai modifié les codes pour qu'ils marchent avec cette nouvelle organisation.

> Finitions du récup_data.py : ajout d'un pourcentage, gestion du singulier/pluriel qui sera utile après pour afficher les messages sur tkinter. Ajout des csv qui n'ont pas besoin de modifications (data.gouv.fr).



2 Janvier 2023
> J'ai renommé récup_data.py en update.py, et rajouté des commentaires pour que le code soit plus compréhensible.

> Mis a jour du system pour noter les villes. Il note maintenant par rapport au distance du valeurs desiré au lieux d'un taux calculé. Il reste encore des choses a regler (ex: contourner un erreur de division par 0 quand la valeur desiré est 0).



3 Janvier 2023
> Correction du big de update.py : si c'est la première utilisation et qu'il y a pas accès à internet, on active une variable erreur (utilisable pour stopper un tkinter).

> Tous les messages sont maintenant des variables pour tkinter dans update.py.

> Changement du nom du fichier principal fenetre.py -> TheWeatherTeam.py.

> amélioration du système de pages d'aides et de retour aux pages précédentes (possibilité de suppression de certaines pages en remettant à zéro.



4 Janvier 2023 : **Nouvelle version v0.5**
>Changement de update.py en une énorme fonction pour l'utiliser dans d'autres codes.

>Intégration des mises à jour et du gestionnaire de téléchargements sur le code principal.

>Désactivation temporaire des classes qui utilisent internet (OpenWeatherAPI) car on ne l'utlise pas encore et ça plante si on a pas internet.

>Renomage du code principal pour LifeSCORE.py.

>Création du document requirements.txt qui permet de télécharger toutes les bibliothèques d'un coup

>Modifictation de la note principale : prend en compte le nombre d'habitants

>J'ai mis tous les print() en commentaires sauf pour update.py et calcul_coefficients.py



5 Janvier 2023 :

>**Première présentation de notre logiciel à la classe d'informatique.**



6 Janvier 2023 :
> Publication de la 2ème version de UPDATE.PY : fonctionne à 100% et la nouvelle version est plus rapide. Correction des bugs (certains crtitiques) :
>- https://github.com/The-Weather-TEAM/Life-SCORE/issues/43
>- https://github.com/The-Weather-TEAM/Life-SCORE/issues/40
>- https://github.com/The-Weather-TEAM/Life-SCORE/issues/39

> Ajout des prévisions météo dans CLASSE.PY.

> Mise à jour de requirements.txt et calcul_coefficients.py.


7 Janvier 2023 : **Nouvelle version v0.5.1**
> Correction des derniers bugs dans UPDATE.PY, Rajout de la gestion si coupure d'internet en plein téléchargement (ça passe en V3) :
> - https://github.com/The-Weather-TEAM/Life-SCORE/issues/30
> - https://github.com/The-Weather-TEAM/Life-SCORE/issues/41
> - https://github.com/The-Weather-TEAM/Life-SCORE/issues/51 (bug que Twitter et Mozilla avait, pour vous dire)

> Normalement il y a plus aucun bug dans update.py, si vous en trouvez n'hésitez pas à rajouter ça dans issues.

> Correction du bug de la notation : tout remarche https://github.com/The-Weather-TEAM/Life-SCORE/issues/47
mbre de pi

> Nouveau système pour `calcul_coefficients.py` plus précis pour determiner les notes des villes en utilisant des encadrement minimum et maximum entourant la valeur ideal. Il y a aussi l'ajout des sources ou j'ai trouvé les valeurs ideals et leurs encadrements.

> Transformation des pages de Tkinter vers CustomTkinter qui permet une approche plus "graphique", corrections de quelques bugs graphiques, adaptation du nombre de pixels,...



8 Janvier 2023 :
> Transformation des pages d'aide de `CTk()` à `CTkTopLevel()`

> Implémentation du fichier `style.txt` ( permet de changer le style de la page ) Que l'on accède grâce au volet d'options dans la page paramètre

> Correction du bug qui ne trouvait pas de ville si l'on mettait des espaces (ex : 'Beziers  ')

> Correction du bug qui ne faisait pas marcher les villes avec accents (ex : 'Béziers') en remplaçant les caractères spéciaux (é,û,à,...) par leurs lettres respectives (e,u,a,...) 

> Suppression de la troisième colonne dans la recherche de noms vu que les accents ne sont plus pris en compte (ça doit un petit peut accélérer le processus ducoup)



13 Janvier 2023 : 
> Ajout d'un csv rempli et vérifié à chaque lancement de programme (pour le qcm)



14 Janvier 2023 :
> Réglage du bug des arrondissements (peut encore s'améliorer genre autoriser : "Paris 1", "Paris1" et "Paris_1" pour l'instant, seul ce dernier marche

> Messages d'erreurs plus "performants"

> Création d'une méthode qui recupère toutes les données de tous les csv en fonction des ses métadonnées (colonnes, délimiteur, INSEE ou nom de ville, ...)

> Essais pour faire une animation afin d'afficher la note finale, mais ne marche pas (bugs à corriger)

> Modifications du CSV pour le nom des villes et les habitants, les nouveaux sont compatibles avec UPDATE.PY !



15 Janvier 2023 :
> Création d'un fichier `database.json` qui stocke :
>- Toutes les données pour obtenir les métadonnées d'un csv ;
>- Son code de téléchargement ;
>- Ses données qu'on veut (colonnes, ect) ;
>- Comment le fichier csv est délimité.

> Modification du programme `UPDATE.PY` pour qu'il obtienne la base de données directement depuis la nouvelle.

> Utilisation de la nouvelle méthode de récupération automatique de données pour obtenir le nombre d'habitant d'une commune.

> Correction d'erreurs :
>- https://github.com/The-Weather-TEAM/Life-SCORE/issues/56
>- https://github.com/The-Weather-TEAM/Life-SCORE/issues/45
>- https://github.com/The-Weather-TEAM/Life-SCORE/issues/28

>Correction de l'erreur qui plantait le programme si notre connexion était trop lente : https://github.com/The-Weather-TEAM/Life-SCORE/issues/57

>Code nettoyé et restructuré pour l'ajout de nouvelles fonctionnalités.

>Modification de la gestion de la couleur du score (avant ça tendait vers le rose, plus maintenant) : Rouge foncé -> Rouge -> Orange/Jaune -> Vert Pastel -> Vert. Les couleurs ne sont pas trop claires et sont donc compatibles pour une interface claire comme foncée.

>Ajout d'un logo provisoire pour la dernière fenêtre et la précédente.

>Ajout de la fenêtre d'erreur qui marche désormais

>Corrections finales sur les arrondissements (on peut désormais mettre "Paris 7", "Paris7", et "Paris_7" :)

>Tentative de reproduction de style.txt s'il n'existe pas (échec)



16 Janvier 2023 :
> Création du fichier options.csv pour sauvegarder les options de l'application (interface, fréquence de màj)



17 Janiver 2023 :
> Mise en place du fichier options.csv, il manque plus que le code pour modifier les valeurs.

> Correction du bug sur les icônes de l'application : https://github.com/The-Weather-TEAM/Life-SCORE/issues/64



18 Janvier 2023 : **Nouvelle version v0.5.2**
>Corrrection du problème empêchant d'écrire "cazouls d'hérault" alors que la ville est dans le CSV avec manipulation de tous les accents et suites de caractères (d', l', lès,...) 

>Les 3 fenêtres principales passent sur une seule (plus d'erreurs bizzares sur les scaling et tout). C'est top : https://github.com/The-Weather-TEAM/Life-SCORE/issues/62

>Nouvelle animation de la note : c'est fluide et c'est beau, quoi demander de mieux : https://github.com/The-Weather-TEAM/Life-SCORE/issues/61

>Gestion des installations des bibliothèques sur `UPDATE.PY` : https://github.com/The-Weather-TEAM/Life-SCORE/issues/37

>Le programme utilise maintenant des polices d'écriture personnalisées !

>Nettoyage du code et rajout de commentaires.
