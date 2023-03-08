"""
SERA DANS CLASS.PY QUAND C'EST SUR D'ETRE FINI!!


"""

import requests
from calcul_coefs import calculCoefficients


def notes_meteo_ville(ville: str) -> dict:
    """
    Determiner des notes sur les donnees meteorologique/climatique de 2022 d'une ville par rapport a des valeurs ideals
    
    - Idée de tout le Groupe (idée initial du projet) & Implementé par Thor

    TODO: Voir api Qualité de l'Aire
    """


    geoloc_ville = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={ville}") # pour longitude et latitude du ville
    if geoloc_ville.status_code != 200: return None # renvoi rien si la requete succede pas
    geoloc_ville = geoloc_ville.json()["results"][0] # on recupere les donnes qui nous interess dans la reponse

    # recuperation de tout les donnees meteorologique et climatique de la ville
    ville_data = requests.get(f"https://archive-api.open-meteo.com/v1/archive?latitude={geoloc_ville['latitude']}&longitude={geoloc_ville['longitude']}&start_date=2022-01-01&end_date=2023-01-01&hourly=relativehumidity_2m,surface_pressure,cloudcover,windspeed_10m&daily=temperature_2m_mean,precipitation_sum&timezone=Europe%2FBerlin")
    if ville_data.status_code != 200: return None # renvoi rien si la requete succede pas
    ville_data = ville_data.json() # on transforme le reponse json en dictionaire

    # on supprime les timestamps pour pouvoir iterer les donnees plus facilement sans problem de type
    del ville_data["daily"]["time"]
    del ville_data["hourly"]["time"]

    donnees_moy = {} # va contenir les donnees moyennes de chaque critere

    tout_les_donnees = list(ville_data["hourly"].items()) + list(ville_data["daily"].items())  # on concatine les donnes "par heur" et "par jour"

    for key, values in tout_les_donnees: # on calcule la moyenne annuelle de chaque critere
        keymoy = sum(values)/len(values) # calcule moyenne
        if key == "surface_pressure": keymoy = keymoy*0.00098692 # transforme hPa -> atm
        if key == "windspeed_10m": keymoy = keymoy*0.27778 # transforme km/h -> m/s
        donnees_moy[key] = round(keymoy, 2) # on sauvegarde cette moyenne dans le dictionaire


    valeursIdeales = { # le criteres qu'on va utiliser pour determiner des notes
        "relativehumidity_2m": (0, 40, 100), # en % | moyenne de 30%-50% (https://humiditycheck.com/comfortable-humidity-level-outside)
        "temperature_2m_mean": (0, 27.5, 46), # en Celcius | Le temperature maximum est le temperature record de France (https://fr.wikipedia.org/wiki/Records_de_temp%C3%A9rature_en_France_m%C3%A9tropolitaine)
        "cloudcover": (0, 20, 100), # en %
        "surface_pressure": (0.967, 1, 1.035), # en atm | (les plus haut est bas pressions en france par: https://en.wikipedia.org/wiki/List_of_atmospheric_pressure_records_in_Europe#France)
        "windspeed_10m": (0, 7, 17.5) # en m/s | (0, table 1 pieton, moyenne table 2) du source: https://cppwind.com/outdoor-comfort-criteria/
    }

    # calcule du note de chaque critere present dans valeursIdeales et donnees_moy
    notes = calculCoefficients(valeursIdeales, donnees_moy)

    return notes

if __name__ == "__main__":
    notes = notes_meteo_ville("Le Thor")
    note_moy = sum(notes.values())/len(notes.values())
    print(round(note_moy, 4))