'''
                      [CALCUL_COEFS.PY]
                         
             Cacul de l'importance des notations 
              en fonction des résultats du QCM

'''





def calculCoefficients(valeursIdeals :dict, valeursSaisit: dict) -> float:
    """
    Calcule coefficients de tout les differents valeurs pour ensuite en deduire une note
    
    Le structure du dictionaire `valeursIdeals` doit etre: `{critere: (valeurMinimal, valeursIdeal, valeurMaximal)}`

    Et le structure du dictionaire `valeursSaisit` doit etre: `{critere: valeur}`

    - `valeursIdeals` et `valeursSaisit` doivent avoir les memes noms de clefs.
    - Un critere de `valeursIdeals` ne peut pas avoir 3 valeurs identiques, mais il peut en avoir 2 si l'ideal est le maximum ou minimum.
    """
    assert type(valeursIdeals) == type(valeursIdeals) == dict, "Les valeurs saisit doivent etre dans des dictionaires."
    
    # calcule le rapport entre les donnes local est la moyenne global
    listDeNotes = []

    for critere in valeursIdeals.keys(): # pour chaque critere dont on a un valeur desiré
        valMin, valIdeal, valMax = valeursIdeals[critere]
        valSaisit = valeursSaisit[critere]

        assert len(set((valMin, valIdeal, valMax))) != 1, f"Les valeurs ideal de `{critere}` ne peuvent pas etre 3 valeurs identiques (Mais ils peuvent etre 2 identiques)."
        assert valMin <= valIdeal <= valMax, f"Les valeurs ideal de `{critere}` ne sont pas en ordre croissant."
        

        if valSaisit == valIdeal: # si on a la valeur exact qu'on cherche
            noteSurCent = 1

        elif valMin <= valSaisit <= valMax: # si il inclus au limits données
            # trouve a quel limite appartient la le valeur saisit
            domainDuValeur = valMin if valSaisit <= valIdeal else valMax
            # pour trouver la distance entre valIdeal est la domainDuValeur (on l'utilise pour calc du pourcentage)    
            domainDuValeur = abs(valIdeal - domainDuValeur)

            distanceDesValeurs = abs(valIdeal - valSaisit) # calcule la difference entre les valeurs Saisit et Ideal
            noteSurCent = 1 - (distanceDesValeurs/domainDuValeur) # calcule un note par rapport a cette distance

        else: # si la valeur est endehors des limits, on ne l'accept pas
            noteSurCent = 0


        listDeNotes.append(noteSurCent) # ajoute le note au list de notes des criteres

    
    noteMoyenneDesCriteres = sum(listDeNotes)/len(listDeNotes) # calcule la note moyenne du ville

    return round(noteMoyenneDesCriteres, 2) # renvoi la note 


if __name__ == "__main__": # pour tester le code et demontrer comment l'appliquer


    import classes as recupMeteo
    class_ville = recupMeteo.Donnees("oslo")

    dicoMeteoVille = { #class_ville.meteo() # just pour le test
        "humidite": 75,
        "temperature": 26,
        "visibilite": 9.9,
        "nuages": 18,
        "pression": 1.013,
        "vent": 10
    }



    valeursIdeals = { # format (minimum, l'ideal, maximum)
        "humidite": (0, 40, 100), # en % | moyenne de 30%-50% (https://humiditycheck.com/comfortable-humidity-level-outside)
        "temperature": (0, 27.5, 46), # en Celcius | Le temperature maximum est le temperature record de France (https://fr.wikipedia.org/wiki/Records_de_temp%C3%A9rature_en_France_m%C3%A9tropolitaine)
        "visibilite": (0, 10, 10), # en km | 10 a l'aire d'etre le max avec l'api, donc on veut le max
        "nuages": (0, 20, 100), # en %
        "pression": (0.967, 1, 1.035), # en atm | (les plus haut est bas pressions en france par: https://en.wikipedia.org/wiki/List_of_atmospheric_pressure_records_in_Europe#France)
        "vent": (0, 7, 17.5) # en m/s | (0, table 1 pieton, moyenne table 2) du source: https://cppwind.com/outdoor-comfort-criteria/
    }
    
    print(calculCoefficients(valeursIdeals, dicoMeteoVille))
