'''
                      [NOTE_IDEALE.PY]
                         
             Cacul de l'importance des notations 
              en fonction des résultats du QCM

'''



def calcul_note_ideale(dict_valeursIdeales :dict, dict_valeursSaisies: dict) -> dict:
    '''
    Calcule les notes de tout les differents valeurs par rapport a leur valeur ideal ou preferable

    La structure du dictionaire `dict_valeursIdeales` doit etre: `{critere: (valeurMinimal, valeursIdeal, valeurMaximal)}`

    Et la structure du dictionaire `dict_valeursSaisies` doit etre: `{critere: valeur}`

    Renvoi un dictoinaire de type `{critere: note}`

    - `dict_valeursIdeales` et `dict_valeursSaisies` doivent avoir les memes noms de clefs.
    - Un critere de `dict_valeursIdeales` ne peut pas avoir 3 valeurs identiques. Mais il peut en avoir 2 si l'ideal est soit le Minimum ou le Maximum.
    
    ---

    - Idée de Thor : L'idée s'apparente à celle du calcul du pourcentage d'une pente sauf qu'ici on cherche l'écart 
                    de la valeur en fonction de la longueur d'étude de ces valeurs
    '''
    assert type(dict_valeursIdeales) == type(dict_valeursIdeales) == dict, "Les valeurs saisit doivent etre dans des dictionaires."
    
    dict_notes = {}

    for critere in dict_valeursSaisies.keys(): # pour chaque critere dont on a un valeur desiré
        # recupere les donnees pour ce critere
        valMin, valIdeal, valMax = dict_valeursIdeales[critere]
        valSaisit = dict_valeursSaisies[critere]

        assert len(set((valMin, valIdeal, valMax))) != 1, f"Les valeurs ideales de `{critere}` ne peuvent pas etre 3 valeurs identiques (Mais ils peuvent en etre 2)."
        assert valMin <= valIdeal <= valMax, f"Les valeurs ideales et limites de `{critere}` ne sont pas en ordre croissant."
        

        if valSaisit == valIdeal: # si on a la valeur exacte que l'on recherche
            noteSurCent = 1

        elif valMin <= valSaisit <= valMax: # si la valeur locale est entre les limites données

            # on cherche la domain de valSaisit, donc si il est inferieur ou superieur a valIdeal
            domainDuValeur = valMin if valSaisit <= valIdeal else valMax   
            longeurDuDomain = abs(valIdeal - domainDuValeur) # "longeur" du domaine ou se trouve valSaisit

            distanceDesValeurs = abs(valIdeal - valSaisit) # difference entre valSaisit et valIdeal
            noteSurCent = 1 - (distanceDesValeurs/longeurDuDomain) # calcule un note par rapport a cette difference et la longeur du domain

        else: # si la valeur est en-dehors des limites, on ne l'accepte pas
            noteSurCent = 0


        dict_notes[critere] = round(noteSurCent*100, 4) # ajoute le note au dictionaire de notes (et les multiplie par 100 pour un pourcentage)

    return dict_notes # renvoi la dictionaire avec tout les notes



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
    
    notes = calcul_note_ideale(valeursIdeales, dicoMeteoVille)
    note_moy = sum(notes.values())/len(notes.values())
    #print(notes)
    #print(note_moy)
