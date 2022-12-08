# Life SCORE
Life score est une application pensée et conçu par cinq étudiants du lycée Henri IV Béziers. Il permet, après une analyse de l'utilisateur, d'évaluer des villes et villages sur 100 par rapport à des dizaines de critères, de partout en France.

## Le projet
Le logiciel est reparti en 2 sections : la première est le test afin de connaître au maximum les attentes de l'utilisateur. Le deuxième permet de choisir une ville et défini le résultat (avec détails) du niveau de compatibilité par rapport à la demande.


### La notation
Pour chaque critère, on définit une note sur 100 ainsi qu'un coefficient qui est de base 1. Le plus de critères sont réunis afin d'avoir le plus de précision possible. Ils sont répartis en 4 catégories :

 - Le climat *(pluie en un an / pollution de l'air / températures / vent / ...)*
 - La qualité de vie (activités / patrimoine / ville fleurie / ...)
 - Le prix *(essence / gaz / loyer / prix de la vie / salaire moyen / ...)*
 - La sécurité *(taux d'accidents / vols / risques / ...)*


### La personnalisation 
Chaque utilisateur va devoir remplir un formulaire de quelques minutes. Chaque réponse impactera le coefficient de plusieurs critères, pouvant devenir nul à très important. La note sera donc en fonction de l'utilisateur qui utilise notre application !


## Version actuelle : v0.4

> Affiche les données météorologiques de la ville souhaitée

fait par Frédéric MARQUET & Nathan BOSY

 - Sans interface graphique
 - Fonctionne uniquement avec un terminal Python
 - Aucun fonction de notation ou de personnalisation : c'est juste le prototype de notre application.

## Journal de bord (travail en groupe)
Jeudi 8 Décembre
>- Mise en place de l'idée générale : faire une application qui permet de noter les villes. 
>- Travail sur la personnalisation : comment faire pour avoir un logiciel personnalisé
>- Première répartition du travail : 
>Raphaël et Noémie -> Interface graphique
>Frédéric -> Traitement de données des API pour la météo et le climat
>Thor -> Programmation des coefficients entre le formulaire et la notation
>Nathan -> Traitement de bases de données / Graphisme
