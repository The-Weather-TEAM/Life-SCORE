

def calculeCoefficients(globalmeteo, localmeteo, coefs):
    """
    Calcule coefficients de tout les differents moyenns pour ensuite en deduire une note du ville
    """

    # calcule le rapport entre les donnes local est la moyenne global
    listDeNotesCriteres = []

    for critere in ("visibilite", "temperature", "humidite"):



        # pour assurer [-1 < note < 1] 
        if globalmeteo[critere]<localmeteo[critere]: 
            note = coefs[critere]-globalmeteo[critere]/localmeteo[critere] 

        elif globalmeteo[critere]>localmeteo[critere]:
            note = localmeteo[critere]/globalmeteo[critere]-coefs[critere]

        else:
            note = 0 # sera neutre (note 0.5)

        note = 0.5 + (note/2) # pour avoir un note entre 0 et 1, tout en gardant la meme equivalence avec les note negative
        # print(critere,note)
        listDeNotesCriteres.append(note) # ajoute chaque note au liste
    
    noteMoyenneDesCriteres = sum(listDeNotesCriteres)/len(listDeNotesCriteres) # calcule la note moyenne du ville

    return round(noteMoyenneDesCriteres, 2) # renvoi la note 


if __name__ == "__main__": # pour tester le code


    import recup_meteo_classe as recupMeteo
    class_ville = recupMeteo.Donnees("Paris")

    dicoMeteoVille = class_ville.meteo()
    # print(dicoMeteoVille)

    globalDico = { # info meteo ideal
        "humidite": 60, # pourcent
        "temperature": 27.5, # Celcius
        "visibilite": 10 # km
    }

    
    coeffsDico = { # 0: on veut moins que la moyenne global | 1: on veut plus que la moyenne global
        "humidite": 0,
        "temperature": 1,
        "visibilite": 1
    }
    
    print(calculeCoefficients(globalDico, dicoMeteoVille, coeffsDico))
