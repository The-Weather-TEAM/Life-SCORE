

def main(globalmeteo, localmeteo, coefs):
    """
    Calcule coefficients de tout les differents moyenns pour ensuite en deduire une note du ville
    """

    # calcule le rapport entre les donnes local est la moyenne global

    if globalmeteo["precipitation"]<localmeteo["precipitation"]: # pour assurer [-1 < note < 1] 
        note = coefs["pluie"]-globalmeteo["precipitation"]/localmeteo["precipitation"] 
    elif globalmeteo["precipitation"]>localmeteo["precipitation"]:
        note = localmeteo["precipitation"]/globalmeteo["precipitation"]-coefs["pluie"]
    else:
        return 0.5

    # print(taux)
    note = 0.5 + (note/2) # pour avoir un note entre 0 et 1, tout en gardant la meme equivalence avec les note negative


    return round(note, 2) # renvoi la note 


if __name__ == "__main__":
  
  

    globaldico = { # info meteo de france
        "precipitation": 0.6 # 0.25
    }

    localdico = { # info meteo du ville
        "precipitation": 0.25 # 0.6
    }

    coeffsdico = { # serait le dico de questions dans le future
        "pluie": 1
    }
    
    print(main(globaldico, localdico, coeffsdico))
