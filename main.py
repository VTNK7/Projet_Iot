import requests
import time
import json
from datetime import datetime

# URL de l'API Open-Meteo pour la météo actuelle de Toulouse
URL = "https://api.open-meteo.com/v1/forecast"

# Paramètres pour récupérer la température de Toulouse en degrés Celsius
params = {
    'latitude': 43.6047,  # Latitude de Toulouse
    'longitude': 1.4442,   # Longitude de Toulouse
    'current_weather': 'true',  # Récupérer la météo actuelle
    'temperature_unit': 'celsius'  # Unité de température en Celsius
}

def get_temperature():
    try:
        # Effectuer la requête vers l'API Open-Meteo
        response = requests.get(URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            # Extraire la température actuelle
            temperature = data['current_weather']['temperature']
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            
            # Créer un json avec la température et l'horodatage
            meteo_data = {
                "timestamp": timestamp,
                "temperature": temperature
            }

            # Sauvegarder les données dans le fichier meteo.json
            with open('meteo.json', 'w') as f:
                json.dump(meteo_data, f)
                f.write('\n')  
            print(f"Données sauvegardées : {meteo_data}")
        else:
            print(f"Erreur lors de la requête : {data}")
    except Exception as e:
        print(f"Erreur lors de la connexion à l'API : {e}")

def main():
    while True:
        get_temperature()  
        time.sleep(10)  # Attendre 10 minutes

if __name__ == '__main__':
    main()
