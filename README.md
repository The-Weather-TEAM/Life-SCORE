![LIFESCORE](https://user-images.githubusercontent.com/104134380/233164637-02f39f0a-0e24-474b-a315-11dfad56b244.png)

Vous souhaitez aménager d'ici peu dans une nouvelle commune, mais vous ne savez pas si celle-ci vous correspond ?

**Life SCORE est une application qui, basée sur vos préférences, va noter n'importe quelle commune française et va vous donner un score de compatibilité pour savoir si cette dernière est faite pour vous, basé sur de nombreux critères.**

Elle comporte :
- Un système de mise à jour pour avoir les dernières données ;
- Une base de données non exhaustive ;
- Un questionnaire pour connaître l'utilisateur ;
- Les résultats avec carte, détail des notes ainsi que la comparaison avec les communes voisines.

Elle a été réalisée par quatre étudiants du lycée Henri IV Béziers pour les Trophées NSI 2023-2024 :
- Frédéric M.
- Nathan B.
- Raphaël F.
- Thor N.



![RELEASE](https://img.shields.io/github/release-date/The-Weather-TEAM/Life-SCORE?style=for-the-badge)
![DOWNLOADS](https://img.shields.io/github/downloads/The-Weather-TEAM/Life-SCORE/total?style=for-the-badge)
![LIGNES](https://img.shields.io/tokei/lines/github/The-Weather-TEAM/Life-SCORE?style=for-the-badge)
![LICENSE](https://img.shields.io/github/license/The-Weather-TEAM/Life-SCORE?style=for-the-badge)



# Le projet
Le logiciel est reparti en 2 sections : la première est un questionnaire afin de connaître les attentes de l'utilisateur. La seconde permet de choisir une ville et défini le résultat (avec détails) du niveau de compatibilité par rapport à la demande.





### La notation
Pour chaque critère, on définit une note sur 100 ainsi qu'un coefficient qui dépend de l'utilisateur. Le plus de critères sont réunis afin d'avoir le plus de précision possible. Chaque question est reliée à un ou plusieurs csv, ce qui impactera la note en fonction des resultats obtenus.





### La personnalisation 
Chaque utilisateur va devoir remplir un formulaire de quelques questions. Chaque réponse impactera le coefficient de plusieurs critères, pouvant aller de 0.5 à 3. La note ne sera donc pas la même en fonction des besoins de l'utilisateur!





### La gestion d'erreurs
Notre projet porte une grande importance sur la gestion des bugs et erreurs. Nous faisons tout le possible pour, quoi qu'il arrive, trouver une alternative face à un problème tout en anticipant les erreurs possibles :
- Système de l'utilisateur pas aux normes ;
- Connexion internet ;
- Corruption et mise à jour des fichiers ;
- Comptabilité système...





# Version actuelle : v1.0

> Version finale pour les Trophées NSI.

Lien vers la liste complète des changements : https://github.com/The-Weather-TEAM/Life-SCORE/releases

Fichiers Python :
- LifeSCORE.py : *Code principal avec l'interface graphique*
- notation.py : *Calcule les note*
- mise_a_jour.py : *Programme de téléchargement et mises à jour des données*

Dossiers : 
- systeme : *Où est stocké toutes les données obligatoire au fonctionnement de l'application*
- donnees : *Dossier facultatif qui stocke les données, réglages utilisateurs ainsi que le cache de l'application*





## Modules utilisés :
*(téléchargés automatiquement)*
- os
- shutil
- requests
- csv
- pandas
- json
- datetime
- time
- urllib3
- http
- zipfile
- subprocess
- sys
- tkinter
- PIL
- math
- random
- re
- ssl
- win32gui
- win32con
- customtkinter (source : https://github.com/TomSchimansky/CustomTkinter)
- tkintermapview (source: https://github.com/TomSchimansky/TkinterMapView)





# Lancement

> *Lors du premier lancement, un terminal de débogage va s’ouvrir pour installer les modules manquants, il peut redémarrer s’il manque des modules ou s’il y a eu des mises à jour. Ensuite, l’application se lance normalement !*

### CONFIGURATION RECOMMANDÉE :

- Windows 10 ou 11 (64 bits) ou Ubuntu (22) ;
- 1 Go de RAM ou plus ;
- 200 Mo de disponible sur le disque dur ;
- Conçu pour un écran d’au moins 1366x768 ;
- Python 3.9.0 ou plus récent avec TKINTER et PIP ;
- Une connexion internet lors du premier lancement.



### WINDOWS : 

- Installer la dernière version de Python ici : https://www.python.org/downloads/
> Faire l’installation personnalisée en sélectionnant pip et tcl/tk !

- Lancer LifeSCORE.py avec Python



### LINUX : 
- Ouvrir le terminal et installer les modules tkinter manquants de base dans Ubuntu :
`sudo apt install python3-pip python3-tk python3-pil.imagetk`

- Lancer LifeSCORE.py sur le terminal : 
`sudo python3 {chemin}/LifeSCORE.py`









# Interface actuelle
### Page d'accueil :
![Capture d'écran_20230420_101229](https://user-images.githubusercontent.com/104134380/233303209-a761cec8-2482-4cf9-b3d1-9c6facfe8d55.png)

### Page de paramètres :
![Capture d'écran_20230420_101234](https://user-images.githubusercontent.com/104134380/233303233-a22148b0-b4c7-4150-8069-80ddacfa9dae.png)

### Page d'informations/aide/détail des notes :
![Capture d'écran_20230420_101239](https://user-images.githubusercontent.com/104134380/233303255-0e363442-8f5a-4ef5-8b98-b642ac646c60.png)

### Page de téléchargement :
![Capture d'écran_20230420_101243](https://user-images.githubusercontent.com/104134380/233303269-e340ccb1-43ea-4e7c-88d4-d57294b111e5.png)

### Page de notation :
![Capture d'écran_20230420_101253](https://user-images.githubusercontent.com/104134380/233303292-887e8d56-eb0e-4eee-a835-1ccd7786aa53.png)





# Journal de bord
Toutes les modifications repertoriées ici : https://github.com/The-Weather-TEAM/Life-SCORE/commits/main



8 Décembre 2022
> Mise en place de l'idée générale : faire une application qui permet de noter les villes. 

> Travail sur la personnalisation : comment faire pour avoir un logiciel personnalisé.

> Première répartition du travail : 
>-  Raphaël -> Interface graphique
>-  Frédéric -> Traitement de données des API pour la météo et le climat
>-  Thor -> Programmation des coefficients entre le questionnaire et la notation 
>-  Nathan -> Traitement des bases de données + Graphisme



10 Décembre 2022
> Interface : première page créée avec la fonction pour le questionnaire à réponses binaire (0,1 mais vue par l'utilisateur comme un adjectif/nom).

> Il faut trouver les questions (je suis parti sur une base de 10 Questions cela me semble pas mal). N'hésitez pas a jeter un coup d'oeil au code fréquemment pour comprendre les ajouts et me demander s'il y a des soucis.



11 Décembre 2022
> Interface : Fin de la première page au niveau fonctionnel (on pose les questions et ensuite on envoie sur la seconde page) et création de la seconde page(vide pour l'instant).

> Même chose, chercher les questions mais maintenant c'est que l'aspect esthétique de la page et ses questions à trouver.



14 Décembre 2022
> Ajout de quelques questions (+5).

> Agrandissement automatique (plein écran) et essais avec la fenêtre de l'utilisateur.

> Création de la seconde Page avec une entrée (Il faut créer le bouton).

> Création de la 3 ème page et tentative de bouton de retour (nous renvoie à la seconde page).



17 Décembre 2022
> Creation du fichier recup_meteo_classe qui utilise le même fonctionnement que l'autre mais sous forme de classe (plus facile à appeler).

> Ajout de "la ville existe ?" : Fonction qui vérifie mise dans 'fenetre.py'.

> Il faut désormais vérifier qu'elle soit en France.

> Protoype de la fonction de couleur.



18 Décembre 2022
> Mise en place de la page finale.

> Ajout de la liste des 5 avantages/inconvénients (5 meilleurees et pires notes dans le dico).

> tentative de test_connection (empêche le lancement du programme si il n'y a pas de connexion).



26 Décembre 2022
> Mise en place d'une classe qui récupère toutes les données météo de la ville demandée. On récupère tout ça dans un dictionnaire.

> Mise à jour de la méthode pour savoir si la ville est Française. (sans passer par un autre CSV).

> Création d'un répertoire de fichiers CSV qui vont nous aider à mettre en place la note.



31 Décembre 2022
> Création d'un code "recup_data.py" qui sert à : 
>- Créer le dossier data avec tous les csv dedans
>- Télécharger et installer les fichiers lors de la première utilisation
>- Rechercher de mise à jour tous les mois et mettre à jour des csv si nouvelle version disponible
> avec la base de csv stockée dessus.

> J'ai renommé les fichiers notamment 'recup_meteo_classe' en 'recup_meteo', c'est plus simple et j'ai modifié les codes qui les utilisent comme ça pas de souci.

> Création d'un code avec une classe qui vérifie si le site marche (internet.py), comme ça on peut faire le test avec data.gouv.fr ou un autre site d'api, c'est plus simple et efficace. Pas d'arrêt du programme mais seulement un retour d'une valeur booléenne.



1 Janvier 2023
> Bonne année ! Modification de l'organisation des fichiers : toutes les classes sont dans le fichier classes.py. J'ai modifié les codes pour qu'ils marchent avec cette nouvelle organisation.

> Finitions dz rzcup_data.py : ajout d'un pourcentage, gestion du singulier/pluriel qui sera utile après pour afficher les messages sur tkinter. Ajout des csv qui n'ont pas besoin de modifications (data.gouv.fr).



2 Janvier 2023
> J'ai renommé recup_data.py en update.py, et rajouté des commentaires pour que le code soit plus compréhensible.

> Mise a jour du sysème pour noter les villes. Il note maintenant par rapport à l'écart des valeurs desirées plutôt qu'un taux calculé. Il reste encore des choses a régler (ex: contourner un erreur de division par 0 quand la valeur desiré est 0).



3 Janvier 2023
> Correction du bug de update.py : si c'est la première utilisation et qu'il n'y a aucun accès à internet, on active une variable erreur (utilisable pour stopper un tkinter).

> Tous les messages sont maintenant des variables pour tkinter dans update.py `Tk.Message()`.

> Changement de nom du fichier principal fenetre.py -> TheWeatherTeam.py.

> Amélioration du système de pages d'aides et de retour aux pages précédentes (possibilité de suppression de certaines pages en remettant à zéro).



4 Janvier 2023 : **Nouvelle version v0.5**
>Changement de update.py en une énorme fonction pour l'utiliser dans d'autres codes.

>Intégration des mises à jour et du gestionnaire de téléchargements sur le code principal.

>Désactivation temporaire des classes qui utilisent internet (OpenWeatherAPI) car on ne l'utlise pas encore et ça plante si on a pas internet.

>Modification du nom du fichier principal en LifeSCORE.py.

>Création du document requirements.txt qui permet de télécharger toutes les bibliothèques d'un coup.

>Modifictation de la note principale : prend en compte le nombre d'habitants.

>J'ai mis tous les print() en commentaires sauf pour update.py et calcul_coefficients.py.



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
> - https://github.com/The-Weather-TEAM/Life-SCORE/issues/51 (bug que Twitter et Mozilla ont aussi subi)

> Normalement il y a plus aucun bug dans update.py, si vous en trouvez n'hésitez pas à rajouter ça dans issues.

> Correction du bug de la notation : tout remarche ! https://github.com/The-Weather-TEAM/Life-SCORE/issues/47

> Nouveau système pour `calcul_coefficients.py` plus précis pour determiner les notes des villes en utilisant des encadrement minimum et maximum entourant la valeur idéale. Il y a aussi l'ajout des sources ou j'ai trouvé les valeurs idéales et leurs encadrements.

> Transformation des pages de Tkinter vers CustomTkinter qui permet une approche plus "graphique", corrections de quelques bugs graphiques, adaptation du nombre de pixels,...



8 Janvier 2023 :
> Transformation des pages d'aide de `CTk()` à `CTkTopLevel()`.

> Implémentation du fichier `style.txt` ( permet de changer le style de la page ) Que l'on accède grâce au volet d'options dans la page paramètre.

> Correction du bug qui ne trouvait pas de ville si l'on mettait des espaces (ex : 'Beziers  ').

> Correction du bug qui ne faisait pas marcher les villes avec accents (ex : 'Béziers') en remplaçant les caractères spéciaux (é,û,à,...) par leurs lettres respectives (e,u,a,...).

> Suppression de la troisième colonne dans la recherche de noms vu que les accents ne sont plus pris en compte (ça doit un petit peut accélérer le processus).



13 Janvier 2023 : 
> Ajout d'un csv rempli et vérifié à chaque lancement de programme (pour le questionnaire).



14 Janvier 2023 :
> Correction du bug des arrondissements (peut encore s'améliorer genre autoriser : "Paris 1", "Paris1" et "Paris_1" pour l'instant, seul ce dernier marche.

> Messages d'erreurs plus "performants".

> Création d'une méthode qui recupère toutes les données de tous les csv en fonction des ses métadonnées (colonnes, délimiteur, INSEE ou nom de ville, ...).

> Essais pour faire une animation afin d'afficher la note finale, mais ne marche pas (bugs à corriger).

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

>Ajout de la fenêtre d'erreur qui marche désormais.

>Corrections finales sur les arrondissements (on peut désormais mettre "Paris 7", "Paris7", et "Paris_7" :)

>Tentative de reproduction de style.txt s'il n'existe pas (échec).



16 Janvier 2023 :
> Création du fichier options.csv pour sauvegarder les options de l'application (interface, fréquence de màj).



17 Janiver 2023 :
> Mise en place du fichier options.csv, il manque plus que le code pour modifier les valeurs.

> Correction du bug sur les icônes de l'application : https://github.com/The-Weather-TEAM/Life-SCORE/issues/64



18 Janvier 2023 : **Nouvelle version v0.5.2**
>Corrrection du problème empêchant d'écrire "cazouls d'hérault" alors que la ville est dans le CSV avec manipulation de tous les accents et suites de caractères (d', l', lès,...) .

>Les 3 fenêtres principales passent sur une seule (empêche certaines erreurs sur les widgets d'arriver). C'est top : https://github.com/The-Weather-TEAM/Life-SCORE/issues/62

>Nouvelle animation de la note : c'est fluide et c'est beau, quoi demander de mieux : https://github.com/The-Weather-TEAM/Life-SCORE/issues/61

>Gestion des installations des bibliothèques sur `UPDATE.PY` : https://github.com/The-Weather-TEAM/Life-SCORE/issues/37

>Le programme utilise maintenant des polices d'écriture personnalisées !

>Nettoyage du code et rajout de commentaires.



21 Janvier 2023 :
>Rajout d'une interface de téléchargement.

>Correction du bug de nouveaux csv dans la base de données : https://github.com/The-Weather-TEAM/Life-SCORE/issues/73

>Ajout de csv dans la base de données.

>Correction du bug pour télécharger les bibliothèques : https://github.com/The-Weather-TEAM/Life-SCORE/issues/69



22 Janvier 2023 :
>Amélioration de l'option menu qui affiche les styles, maintenant il affiche le style courant .

>Amélioration de la taille de police avec une fonction qui calcule la taille en fonction de la longueur de la ville (sous la forme d'une fonction affine mx +p).



23 Janvier 2023 :
>Réglage d'un problème qui faisait planter le programme si `csv_dico.csv` n'était pas présent (issues https://github.com/The-Weather-TEAM/Life-SCORE/issues/77 et https://github.com/The-Weather-TEAM/Life-SCORE/issues/78)

>Réglage du problème avec `style.txt` (le programme n'était pas capable de recréer le fichier s'il n'existait pas mais il le peut désormais).

>Tests avec un camarade de classe permetant de trouvre des erreurs et imprévus.


24 Janvier 2023 :
>Changement de la fonction `note_sport()` pour note_par_habitant() qui prend en parametres le nom du csv, le delimiteur, les colonnes utilisees et les coefficients m et p (mx+p) servant a calculer les notes.

>Correction de bugs apparu après l'implémentation de la dernière fonction (changements de variables mal effectués).

>Correction du bug sur le fichier csv_dico.csv qui le réécrivait avec un csv vide (si le csv était déja rempli, il attendait un tableau de réponse qui n'est jamais venu :( Ainsi, il enlevait les données ce qui force la réutilisation du questionnaire au lancement suivant).



25 Janvier 2023 :
>Grosse réorganisation des fichiers :
>- Toutes les données modifiables / supprimables / téléchargeables par l'utilisateur sont dans `\donnees\*` :
>     - Les csv dans `\donnees\csv\*`;
>     - Les options et données personnelles dans `\donnees\utilisateur\*`;
>- Toutes les données que l'applciation utilise (seulement modifiables avec une mise-à-jour) dans `\systeme\*`.

>Modification des titres : maintenant, le titre de la fenêtre donne toujours le nom de l'application, et elle est personnalisée en fonction de la commune.

>Modification des textes affichés.

>"Note" n'est plus affiché en couleur.

>Ajout du menu pour changer la couleur des boutons


28 Janvier 2023 :
>Nouvelle méthode pour récupérer automatiquement les données d'un csv en fonction de son type et du nombre de données à récuperer.

>Les résultats sont donnés sous forme de tableau.




29 Janvier 2023 : **Nouvelle version v0.5.3**
>Premier prototype final de l'interface de l'application : https://github.com/The-Weather-TEAM/Life-SCORE/#projet-dinterface-finale

>Les options sont stockées dans un fichier txt. Et ça marche !

>Ajout de code pour créer automatiquement tous les fichiers dans données : maintenant le dossier n'est plus indispensable pour le premier lancement.

>Ajout d'un pourcentage pour savoir où le téléchargement en est.

>Correction de bugs pour la mise à jour + correction de grammaire



15 Fevrier 2023:
>Ajout d'une carte sur la page de notation montrant la ville



20 Fevrier 2023:
>Fix des issues #85 et #86 découvertes aujourd'hui 



25 Fevrier 2023:
>Début des améliorations graphiques pour se rapprocher de l'idée du projet d'interface finale https://github.com/The-Weather-TEAM/Life-SCORE/#projet-dinterface-finale

>Modifications des pages d'aides (ajout de "MessageBox" pour contenir le texte et correction de l'indentation pour avoir une meilleure lisibilité)



2 Mars 2023 :
>Nettoyage du code et ajouts de commentaires



3 Mars 2023 :
>Grand nettoyage et amélioration de la logique (l'enchaînement des fonctions) de `LifeScore.py`, il faudrait le faire pour les autres fichiers

>Ajout des sources dans `LifeScore.py`, `calculscoefs.py` et `update.py`



5 Mars 2023 :
>Nouvelle animation de la note basée sur un fonction trigonométrique

>Aout des sources dans `classes.py`

>Prise en compte d'auutres CSV "par habitants" dans la note finale !

>Ajout des crédits au début de `LifeScore.py` (permet de remplir l'espace vide)



6 Mars 2023 : **Nouvelle version v0.5.4**
>Modification des crédits (pour éviter qu'on puisse les sélectionner)

>Correction de problèmes avec les csv

>Modification des paramètres dans la base de données

>Nouveau logo et importation d'images qui correspondent à la charte graphique verte de l'appli

>La note finale prend maintenant en compte les csv de type simple, par population, comptage par population et simple avec fonction affine !! Lez go 

>Ajout de la fonctionnalité pour voir la dernière màj dans la page des paramètres



8 Mars 2023 : 
>Ajout des diviseurs dans certains csv (qui repertorient des données sur plusieurs années)

>Modification de la map avec Openmap (et plus google), ajoût d'un pin pour voir la ville de loin

>Centralisation des paramètres sur un fichier

>Page des paramètres interactive (les données marquées sont celles de l'utilisateur)


Petite pause pour se concentrer sur nos épreuves de spécialités
-------------


22 Mars 2023:
>Ajout des notes de météo et de qualité d'air d'un ville.



23 Mars 2023:
>Fix d'un bug qui ne mettait pas les bonnes questions avec des problèmes d'indices



24 Mars 2023:
>Modification de la fonction qui défini la taille de la police de la ville par une fonction contenant un logarithme néperien (plus efficace pour les grandes et petites villes)


28 Mars 2023:
>Implémentation quasi complète (il manque plus que els résultats de l'API) des avantages et inconvénients

>Repositionnements, ajustement des polices

>Résolution d'un problème de lecture de caractères spéciaux (accents)

<sub>Je suis très confiant quant à l'avancée du projet, on pourrait dire que l'on est entré dans la phase finale des retouches pour avoir le meilleur code possible :)</sub>





29 Mars 2023:
>On a remarqué que l'issue #101 est causée par le caractère unicode dit 'invisible' `feff`, on essaie de la réssoudre dans les plus brefs délais

>Modification de la gestion d'ouvertures des fichiers & répertoires pour être compatible avec linux.




31 Mars 2023:
>Résolution de l'issue #101 en changeant le nom des colonnes en indices (puis on repasse au nom automatiquement et non pas "à la main") : Alors, tous caractère spécial est compté est l'issue #101 a été résolue

>L'application est maintenant disponible sur linux ! Testé sur Ubuntu  22.04.2 LTS. 

>Dernière ligne droite ! Nous nous sommes répartis le "tâches finales" :
- Raphaël  -> issue : #101
- Nathan   -> terminer la fonction qui prend en compte les csv sans code insee et ajout de la comptabilité linux
- Thor     -> mise en forme de l'api de météo (pour afficher les résultats en français) 
- Frédéric -> polissage du code



01 Avril 2023 :
>Prise en charge des CSV sans code INSEE, maintenant la base de données peut être agrandie sans toucher au code, car il est compatible :
>- Avec les fichiers avec et sans code INSEE
>- Les CSV simples, comptant une donnée par rapport à la population, comptant plusieurs données par rapport à la population, ou les CSV booléens (oui ou non).

>Suppression de communes_modifiee.csv : on utilise maintenant le fichier commune de notre base de données

>Modification de la gestion des arrondissements (temporaire)

>Mis en forme de l'API de météo, touts les criteres sont affiché en Français maintenant.

> Passe la vérification des fichiers csv en fonction du temps de maj

> Première modification des polices pour la compatibilité linux / windows



02 Avril 2023 :
> Les boutons utilisent maintenant des images.;

> Modification complète des polices d'écriture pour Windows / Linux Ubuntu.

> Correction d'un problème avec la fonction avantages_inconvenients

> Téléchargement maintenant par un fichier zip (c'est 125x plus rapide) & implémentation de l'interface. Marche avec la récusrsivité pour revérifier les fichiers après une première installation.

> Plus de fichiers ou de csv test ! (suppression du fichier sport_test.csv)

> Récursivité pour les fichiers ayant pas de code insee, et avec arrondissement (ex : Paris 2e arrondissement), si jamais on a que des données sur la ville et pas sur l'arrondissement, on refait la recherche pour toute la ville. à voir si on peut aussi le faire avec le code insee.



05 Avril 2023 : Présenation des avancés en classe
> Nouvelle animation lors du premier téléchargement

> Désactivation du bouton "SUPPRIMER" les données si on a toujours pas fait le QCM.



06 Avril 2023 :
> Intégration complète des 10 plus proches villes et de leur notes puis du tri (cela rajoute une quinzainne de secondes au processus ce qui n'est pas énorme)



08 Avril 2023 :
> Fix d'un bug qui affichait plusieurs fois le même avantage/inconvénient (si la ville avait moins de 5 notes > 50 ou moins de 5 notes < 50)
On résout le bug en vérifiant si les valeurs n'ont pas déjà été posées dans la liste

> Ajout d'un fichier, le fichier `temporaire.txt` (nom sujet à changer) qui récupère la note des villes voisines (ainsi, en faisant plusieurs calculs dans un même entourage on ne recalcule pas plusieurs fois la même ville). Cela fait donc gagner du temps sur les futures recherches 



09 Avril 2023 :
> Modification des notations : on utilise maintenant une fonction sigmoide pour accentuer les valeurs (qui sont proches des moyennes nationales).

> Texte animé du premier téléchargement modifié pour expliquer à quoi sert l'application + le texte est maintenant centré

> Couleur des crédits modifié pour le mode sombre.

> La fichier temporaire.txt est supprimé si on supprime les données.

> Une coupure internet bloque le téléchargement mais n'arrête pas l'appli, on attend de récupérer l'accès à internet.

> Ajout de titres pour les pages d'aide et d'information.

> Modification des données pour retourner 0 pour compter_par_habitant, et maintenant la note finale passe par la fonction sigmoide.

> Création d'une page de détail de la note à la fin de la fonction w_score() qui permet d'afficher la note de chaque csv (critère)

> La page de téléchargement ne s'affiche plus si on ne demande pas de vérification. Correction du bug qui ne modifiait pas la valeur "dernière maj" si aucun fichier n'était mis à jour.



10 avril 2023 : 
> Homogénisation de LifeSCORE.py : les variables ont étées formattées pour être aisément compréhensibles par une personne tierce et certaines variables globales ont perdu ce statut (jugé inutile, notamment pour la liste_Questionnaire

> Correction des pages d'aides (le texte indiqué n'était plus d'actualité)



11 Avril 2023 :
> Renomage de classes.py en notation.py et update.py en mise_a_jour.py.

> https://github.com/The-Weather-TEAM/Life-SCORE/issues/126 n'est pas encore résolu.



16 Avril 2023 : **Nouvelle version v0.6**
> Correction bugs si un module n'était pas installé.

> Test sur des machines virtuelles pour savoir le minimum requis de l'application.

> Nottoyage du code : on enlève la majorité des print qui ne servent à rien.



19 Avril 2023 : Enregistrement de la vidéo de présentation



24 Avril 2023
> Dernières résolutions de cohérences

> On bloque l'accès à l'écriture une fois que la recherche est lancée (sinon on peut écrire "BeziersJJJJJj" c'est pas joli)
