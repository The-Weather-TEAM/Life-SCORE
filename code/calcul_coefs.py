'''
                      [CALCUL_COEFS.PY]
                         
             Cacul de l'importance des notations 
              en fonction des résultats du QCM

'''



def calculCoefficients(valeursIdeales :dict, valeursSaisies: dict) -> float:
    '''
    Calcule coefficients de tout les differents valeurs pour ensuite en deduire une note
    
    La structure du dictionaire `valeursIdeales` doit etre: `{critere: (valeurMinimal, valeursIdeal, valeurMaximal)}`

    Et la structure du dictionaire `valeursSaisies` doit etre: `{critere: valeur}`

    - `valeursIdeales` et `valeursSaisies` doivent avoir les memes noms de clefs.
    - Un critere de `valeursIdeales` ne peut pas avoir 3 valeurs identiques. Mais il peut en avoir 2 si l'ideal est soit le Minimum ou le Maximum.
    
    - Idée de Thor : L'idée s'apparente à celle du calcul du pourcentage d'une pente sauf qu'ici on cherche l'écart 
                    de la valeur en fonction de la longueur d'étude de ces valeurs
    '''
    assert type(valeursIdeales) == type(valeursIdeales) == dict, "Les valeurs saisit doivent etre dans des dictionaires."
    
    # calcule le rapport entre les donnes local est la moyenne global
    listDeNotes = []

    for critere in valeursIdeales.keys(): # pour chaque critere dont on a un valeur desiré
        valMin, valIdeal, valMax = valeursIdeales[critere]
        valSaisit = valeursSaisies[critere]

        assert len(set((valMin, valIdeal, valMax))) != 1, f"Les valeurs ideales de `{critere}` ne peuvent pas etre 3 valeurs identiques (Mais ils peuvent en etre 2)."
        assert valMin <= valIdeal <= valMax, f"Les valeurs ideales de `{critere}` ne sont pas en ordre croissant."
        

        if valSaisit == valIdeal: # si on a la valeur exacte que l'on recherche
            noteSurCent = 1

        elif valMin <= valSaisit <= valMax: # si la valeur locale est entre les limites données

            # on cherche la domain de valSaisit, donc si il est inferieur ou superieur a valIdeal
            domainDuValeur = valMin if valSaisit <= valIdeal else valMax   
            longeurDuDomain = abs(valIdeal - domainDuValeur) # "longeur" du domaine ou se trouve valSaisit

            distanceDesValeurs = abs(valIdeal - valSaisit) # difference entire valSaisit et valIdeal
            noteSurCent = 1 - (distanceDesValeurs/longeurDuDomain) # calcule un note par rapport a cette difference et la longeur du domain

        else: # si la valeur est en-dehors des limites, on ne l'accepte pas
            noteSurCent = 0


        listDeNotes.append(noteSurCent) # ajoute le note a la liste de notes des criteres

    
    noteMoyenneDesCriteres = sum(listDeNotes)/len(listDeNotes) # calcule la note moyenne totale

    return round(noteMoyenneDesCriteres, 2) # renvoie la note finale



if __name__ == "__main__": # pour tester le code et demontrer comment l'appliquer

    dicoMeteoVille = { #class_ville.meteo() # just pour le test
        "humidite": 75,
        "temperature": 26,
        "visibilite": 9.9,
        "nuages": 18,
        "pression": 1.013,
        "vent": 10
    }



    valeursIdeales = { # format (minimum, l'ideal, maximum)
        "humidite": (0, 40, 100), # en % | moyenne de 30%-50% (https://humiditycheck.com/comfortable-humidity-level-outside)
        "temperature": (0, 27.5, 46), # en Celcius | Le temperature maximum est le temperature record de France (https://fr.wikipedia.org/wiki/Records_de_temp%C3%A9rature_en_France_m%C3%A9tropolitaine)
        "visibilite": (0, 10, 10), # en km | 10 a l'aire d'etre le max avec l'api, donc on veut le max
        "nuages": (0, 20, 100), # en %
        "pression": (0.967, 1, 1.035), # en atm | (les plus haut est bas pressions en france par: https://en.wikipedia.org/wiki/List_of_atmospheric_pressure_records_in_Europe#France)
        "vent": (0, 7, 17.5) # en m/s | (0, table 1 pieton, moyenne table 2) du source: https://cppwind.com/outdoor-comfort-criteria/
    }
    
    print(calculCoefficients(valeursIdeales, dicoMeteoVille))
