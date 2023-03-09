"""
SERA DANS CLASS.PY QUAND C'EST SUR D'ETRE FINI!!


"""

import requests
from calcul_coefs import calculCoefficients


def notes_meteo_ville(ville: str) -> ("dict | None"):
    """
    Determiner des notes sur les donnees meteorologique/climatique de 2022 d'une ville par rapport a des valeurs ideals
    
    Renvoi un `dict` avec les notes ou `None` si on n'a pas pue recuperer les donnes pour calculer des notes

    - Idée de tout le Groupe (idée initial du projet) & Implementé par Thor

    Sources:
    - [API Geolocation](https://open-meteo.com/en/docs/geocoding-api)
    - [API Meteo Historique](https://open-meteo.com/en/docs/historical-weather-api)
    - [API Qualité D'air](https://open-meteo.com/en/docs/air-quality-api) (Utilise pas des donnes historique, mais des previsons du present a +4jours)

    TODO: Voir api Qualité de l'Aire
    """

    tout_les_donnees = []
    geoloc_ville = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={ville}") # pour recuperer longitude et latitude du ville

    # recuperation de tout les donnees
    if geoloc_ville.status_code == 200:
        geoloc_ville = geoloc_ville.json()["results"][0] # on recupere les donnes qui nous interess dans la reponse

        # on demande tout les donnees meteogologique et de qualité d'air des APIs
        ville_meteo = requests.get(f"https://archive-api.open-meteo.com/v1/archive?latitude={geoloc_ville['latitude']}&longitude={geoloc_ville['longitude']}&start_date=2022-01-01&end_date=2023-01-01&hourly=relativehumidity_2m,surface_pressure,cloudcover,windspeed_10m&daily=temperature_2m_mean,precipitation_sum&timezone=Europe%2FBerlin")
        ville_air = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={geoloc_ville['latitude']}&longitude={geoloc_ville['longitude']}&hourly=uv_index,european_aqi_pm2_5,european_aqi_pm10,european_aqi_no2,european_aqi_o3,european_aqi_so2")

        if ville_meteo.status_code == 200: # si on recoi les données meteorologique de la ville
            ville_meteo = ville_meteo.json() # on prend le json du reponse

            # on supprime les timestamps pour pouvoir iterer les donnees plus facilement sans problem de type
            del ville_meteo["daily"]["time"]
            del ville_meteo["hourly"]["time"]

            tout_les_donnees += list(ville_meteo["hourly"].items()) + list(ville_meteo["daily"].items())  # on ajoute tout ces donnes a la liste de donnes 
        
        if ville_air.status_code == 200: # si on recoi les données de qualité d'air de la ville
            ville_air = ville_air.json() # on prend le json du reponse

            del ville_air["hourly"]["time"] # pour iterer plus facilement les valeurs

            tout_les_donnees += list(ville_air["hourly"].items()) # on ajoute tout ces donnes a la liste de donnees
    else:
        return None
    if len(tout_les_donnees) == 0: return None # si vide, il y a pas de notes a faire

    donnees_moy = {} # va contenir les donnees moyennes de chaque critere

    

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
        "windspeed_10m": (0, 7, 17.5), # en m/s | (0, table 1 pieton, moyenne table 2) du source: https://cppwind.com/outdoor-comfort-criteria/

        "uv_index": (0,0,7.5), # en UVI (Index Ultra Violet) | valeurs par rapport aux recommendations de WHO (https://www.who.int/news-room/questions-and-answers/item/radiation-the-ultraviolet-(uv)-index)
        "european_aqi_pm2_5": (0, 0, 50), # en AQI (Index de Qualité d'Aire) | Source des valleurs vien du documentation du API (voir haut du fonctino)
        "european_aqi_pm10": (0, 0, 100), # meme que precedent pour le rest 
        "european_aqi_no2": (0, 0, 230),
        "european_aqi_o3": (0, 0, 240),
        "european_aqi_so2": (0, 0, 500),
        
    }

    # calcule du note de chaque critere present dans valeursIdeales et donnees_moy
    notes = calculCoefficients(valeursIdeales, donnees_moy)

    return notes

if __name__ == "__main__":
    notes = notes_meteo_ville("Le Thor")
    print(notes)
    note_moy = sum(notes.values())/len(notes.values())
    print(round(note_moy, 4))