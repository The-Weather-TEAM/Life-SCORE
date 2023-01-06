'''
                  [CALCUL_COEFFICIENTS.PY]
                         
             Cacul de l'importance des notations 
              en fonction des résultats du QCM

'''





def calculCoefficients(valeursIdeals :dict, valeursSaisit: dict, coefs: dict) -> float:
    """
    Calcule coefficients de tout les differents valeurs pour ensuite en deduire une note
    
    - `valeursIdeals` et `valeursSaisit` doivent avoir les memes noms de clefs.

    """

    for dictionary in (valeursIdeals, valeursSaisit): # verifie que les valeurs des dictionaires sont numerique
        toutInt = [type(valeur) == int or type(valeur) == float for valeur in dictionary.values()]
        assert set(toutInt) == {True}, "Les dictionares d'entré doivent contenir des int/float en valeurs"


    # calcule le rapport entre les donnes local est la moyenne global
    listDeNotesCriteres = []

    for critere in valeursIdeals.keys(): # pour chaque critere dont on a un valeur desiré


    
        distanceDesValeurs = abs(valeursIdeals[critere] - valeursSaisit[critere]) # calcule la difference entre les valeurs local et global

        noteSurCent = 1 - (distanceDesValeurs/valeursIdeals[critere]) # evalue un note par rapport a cette distance

        # if noteSurCent < 0: noteSurCent = 0 # ex: quand temperature est sous 0, souvent la note est sous 0.

        print(f"Global: {valeursIdeals[critere]}; Local: {valeursSaisit[critere]}") # affiche les valeurs pour les tests
        print(critere, distanceDesValeurs, noteSurCent)

        listDeNotesCriteres.append(noteSurCent) # ajoute le note au list de notes des criteres

    
    noteMoyenneDesCriteres = sum(listDeNotesCriteres)/len(listDeNotesCriteres) # calcule la note moyenne du ville

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
    print(dicoMeteoVille)



    valeursIdeals = { # info meteo ideal
        "humidite": 60, # en %
        "temperature": 27.5, # en Celcius
        "visibilite": 10, # en km | 10 a l'aire d'etre le max avec l'api, donc on veut le max
        "nuages": 20, # en %
        "pression": 1.013, # en hPa | L'ideal est le pression au niveau de mer, donc 1.013 hPa
        "vent": 20, # en m/s
    }


    # ceci cera remplacé par les resultats du quiz, il faut just chercher comment l'apliquer.
    coeffsDico = {
        "humidite": 0,
        "temperature": 1,
        "visibilite": 1
    }
    
    print(calculCoefficients(valeursIdeals, dicoMeteoVille, coeffsDico))
