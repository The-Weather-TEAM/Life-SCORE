Raf
fenetrePrincipale = interface.CTk() # fenetre de tkinter
fenetrePrincipale.title('LifeScore  |  Menu principal')
fenetrePrincipale.iconphoto(False, icone)
fenetrePrincipale.minsize(width=1280  , height=848) # Taille minimum de la fenetre



Fred 
"festivals":
    ["62cf95993d99f22480f49334","47ac11c2-8a00-46a7-9fa8-9b802643f975", { "insee" : 1,
                                                                          "delimiteur" : ";",
                                                                          "colonne_ville" : 6,
                                                                          "colonne_donnee" : [7],
                                                                          "source" : "www.data.gouv.fr",
                                                                          "type" : "oui_non",
                                                                          "categorie": "qualité_de_vie",
                                                                          "nom": "Les festivals"


    }]

    
Thor
qcm_to_criteres = { # Chaque reponse du QCM et ses notes qui sont en relation
    
    # ex: si Activite est 0 dans le QCM, la note 'Les festivales' aura un moindre coefficent dans la note final
    "Scolarite": ["Les écoles","Les collèges", "Les lycées"],
    "Enseignement_Superieur" : ["Possibilité d'études"],
    "Citadin" : ["population"] if self.population else [],            
    "Culture": ["Les musées","Les monuments historiques"],
    "Activite": ['Les festivals'],
    "Precarite" : ["Le prix des maisons","Le prix des appartements"]
}
