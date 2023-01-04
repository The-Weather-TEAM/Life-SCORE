'''
                  [CALCUL_COEFFICIENTS.PY]
                         
             Cacul de l'importance des notations 
              en fonction des résultats du QCM

'''





def calculCoefficients(globalmeteo, localmeteo, coefs):
    """
    Calcule coefficients de tout les differents moyenns pour ensuite en deduire une note du ville
    """

    # calcule le rapport entre les donnes local est la moyenne global
    listDeNotesCriteres = []

    for critere in globalmeteo.keys(): # pour chaque critere dont on a un valeur desiré


    
        distanceDesValeurs = abs(globalmeteo[critere] - localmeteo[critere]) # calcule la difference entre les valeurs local et global

        if distanceDesValeurs == 0: # si c'est la valeur exact, c'est 100% ce qu'on veut
            noteSurCent = 1
        # elif globalmeteo[critere] == 0: # pour les valeurs ou on veut etre le plus pres de 0 que possible
        #     noteSurCent = (1/distanceDesValeurs)
        else:
            noteSurCent = 1 - (distanceDesValeurs/globalmeteo[critere]) # evalue un note par rapport a cette distance

        # if noteSurCent < 0: noteSurCent = 0 # ex: quand temperature est sous 0, souvent la note est sous 0.

        print(f"Global: {globalmeteo[critere]}; Local: {localmeteo[critere]}") # affiche les valeurs pour les tests
        print(critere, distanceDesValeurs, noteSurCent)

        listDeNotesCriteres.append(noteSurCent) # ajoute le note au list de notes des criteres

    
    noteMoyenneDesCriteres = sum(listDeNotesCriteres)/len(listDeNotesCriteres) # calcule la note moyenne du ville

    return round(noteMoyenneDesCriteres, 2) # renvoi la note 

def note_finale(ville):
    """
    Récupère la ville sous forme de classe et appelle toutes ses fonctions de note pour faire la note finale
    """
    print(ville.__dict__.values())

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


    # les criters qui doivent etre 0 ont encore des bugs. Just utiliser 1/1000 ne marche pas vraiment
    globalDico = { # info meteo ideal
        "humidite": 60, # en %
        "temperature": 27.5, # en Celcius
        "visibilite": 10, # en km | 10 a l'aire d'etre le max avec l'api, donc on veut le max
        "nuages": 20, # en % | on veut mettre 0%, mais on met 0.001 ici pour eviter ZeroDivisionError
        "pression": 1.013, # en hPa | L'ideal est le pression au niveau de mer, donc 1.013 hPa
        "vent": 20, # en m/s | on veut le plus bas possible
    }


    # ceci cera remplacé par les resultats du quiz, il faut just chercher comment l'apliquer.
    coeffsDico = {
        "humidite": 0,
        "temperature": 1,
        "visibilite": 1
    }
    
    print(calculCoefficients(globalDico, dicoMeteoVille, coeffsDico))
