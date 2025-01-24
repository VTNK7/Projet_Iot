from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import requests
import json
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)


# Charger les données simulées à partir d'un fichier JSON
def load_example_data():
    with open('data_logs.json', 'r') as file:
        return json.load(file)
    
def load_existing_data():
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)




# URL de l'API Open-Meteo pour la météo actuelle de Toulouse
URL = "https://api.open-meteo.com/v1/forecast"

# Nom du fichier où enregistrer les données
log_file = 'data_logs.json'

# Paramètres pour récupérer la température de Toulouse en degrés Celsius
params = {
    'latitude': 43.6047,  # Latitude de Toulouse
    'longitude': 1.4442,   # Longitude de Toulouse
    'current_weather': 'true',  # Récupérer la météo actuelle
    'temperature_unit': 'celsius'  # Unité de température en Celsius
}


# Récupération des données les plus récentes
def get_latests_data(): 
    data = load_example_data()
    latest_data = {}
    for entry in data:
        sensor_id = entry['data']['id']
        if sensor_id not in latest_data or entry['timestamp'] > latest_data[sensor_id]['timestamp']:
            latest_data[sensor_id] = entry
    return latest_data
  

# Route pour afficher les dernières données des capteurs
@app.route('/')
def index():
    print("ONLANCE INDEX")
       
    socketio.emit('notification', {'message': 'Voici une notification!'})
    # Récupérer les dernières données de chaque capteur
    latest_data = get_latests_data()

    # Transformer les données pour l'affichage
    display_data = []
    for sensor_id, entry in latest_data.items():
        sensor_type = "Température/Humidité" if sensor_id == 0 else "Fermeture de porte"
        sensor_info = {
            "sensor_type": sensor_type,
            "timestamp": entry["timestamp"]
        }
        if sensor_id == 0:  # Température/Humidité
            sensor_info["temperature"] = entry["data"]["temperature"]
            sensor_info["humidity"] = entry["data"]["humidity"]
        elif sensor_id == 1:  # Fermeture de porte
            sensor_info["door"] = "Fermé" if entry["data"]["door"] == 0 else "Ouvert"
        display_data.append(sensor_info)
    print(display_data)

        # Check conditions and send notifications if needed
    if display_data[0]["door"] == "Ouvert":  # Door is open
        print("dooropen")
        outside_temp = fetch_outside_temperature()
        print(f"Outside temp: {outside_temp}")
        if outside_temp is not None and display_data[1]["temperature"] is not None:
            if outside_temp < display_data[1]["temperature"]:
                print("IL FAIT FROID DE ZINZIN")
                socketio.emit('notification', {'message': "attentioun"})

    return render_template('index.html', data=display_data)

# Route pour afficher l'historique des données d'un capteur
@app.route('/history/<int:sensor_id>')
def history(sensor_id):
    # Charger les données simulées
    data = load_example_data()

    # Filtrer les données par ID de capteur
    history_data = [entry for entry in data if entry['data']['id'] == sensor_id]

    # Transformer les données pour l'affichage
    display_data = []
    for entry in history_data:
        display_entry = {
            "timestamp": entry["timestamp"]
        }
        if sensor_id == 0:  # Température/Humidité
            display_entry["temperature"] = entry["data"]["temperature"]
            display_entry["humidity"] = entry["data"]["humidity"]
        elif sensor_id == 1:  # Fermeture de porte
            display_entry["door"] = "Fermé" if entry["data"]["door"] == 0 else "Ouvert"
        display_data.append(display_entry)

    sensor_type = "Température/Humidité" if sensor_id == 0 else "Fermeture de porte"
    return render_template('history.html', sensor_type=sensor_type, data=display_data)

# API pour obtenir les données simulées en JSON (optionnel)
@app.route('/api/data', methods=['GET'])
def api_data():
    data = load_example_data()
    return jsonify(data)

@app.route('/latest_data', methods=['GET'])
def latest_data():
    # Récupérer les dernières données des capteurs
    latest_data = get_latests_data()
    return jsonify(latest_data)

# Fetch outside temperature from meteo.json
def fetch_outside_temperature():
    try:
        with open("meteo.json", "r") as file:
            data = json.load(file)
            return data.get("temperature")
    except Exception as e:
        print(f"Error reading meteo.json: {e}")
    return None

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
            with open('meteo.json', 'a') as f:
                json.dump(meteo_data, f)
                f.write('\n')  
            print(f"Données sauvegardées : {meteo_data}")
        else:
            print(f"Erreur lors de la requête : {data}")
    except Exception as e:
        print(f"Erreur lors de la connexion à l'API : {e}")

@app.route('/data', methods=['POST'])
def receive_data():
    # Récupérer les données JSON envoyées par le client
    data = request.json
    if data:
        id = data.get('id')


        log_data = load_existing_data()
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        }
        
        # Add to existing data
        log_data.append(log_entry)
        
        # Save updated data
        save_data(log_data)
        
        return "Données reçues", 200
    else:
        return "Aucune donnée reçue", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
