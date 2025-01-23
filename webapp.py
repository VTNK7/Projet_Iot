from flask import Flask, render_template, jsonify, request
from pywebpush import webpush, WebPushException
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_CLAIMS = {"sub": "mailto:your_email@example.com"}


app = Flask(__name__)

# Charger les données simulées à partir d'un fichier JSON
def load_example_data():
    with open('data_logs.json', 'r') as file:
        return json.load(file)

# Route pour afficher les dernières données des capteurs
@app.route('/')
def index():
    # Charger les données simulées
    data = load_example_data()

    # Récupérer les dernières données de chaque capteur
    latest_data = {}
    for entry in data:
        sensor_id = entry['data']['id']
        if sensor_id not in latest_data or entry['timestamp'] > latest_data[sensor_id]['timestamp']:
            latest_data[sensor_id] = entry

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

        # Check conditions and send notifications if needed
        if display_data[0]["door"] == 1:  # Door is open
            outside_temp = fetch_outside_temperature()
            if outside_temp is not None and display_data[0]["temperature"] is not None:
                if outside_temp < display_data[0]["temperature"]:
                    send_notification(
                        f"The door is open! Outside temp: {outside_temp}°C, Inside temp: {display_data[0]['temperature']}°C"
                    )

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

# Route to save subscription
@app.route("/subscribe", methods=["POST"])
def subscribe():
    subscription_info = requests.json
    subscriptions.append(subscription_info)
    return jsonify({"message": "Subscription saved!"}), 201

# Route to send notifications
@app.route("/send_notification", methods=["POST"])
def send_notification():
    message = requests.json.get("message", "Default Notification")
    for subscription in subscriptions:
        try:
            webpush(
                subscription_info=subscription,
                data=message,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS,
            )
        except WebPushException as e:
            print(f"Error sending push notification: {e}")
    return jsonify({"message": "Notifications sent!"}), 200

subscriptions = []

# Fetch outside temperature from meteo.json
def fetch_outside_temperature():
    try:
        with open("meteo.json", "r") as file:
            data = json.load(file)
            return data.get("temperature")
    except Exception as e:
        print(f"Error reading meteo.json: {e}")
    return None

@app.route("/send-test-notification", methods=["GET"])
def send_test_notification():
    message = "Ceci est une notification de test !"
    for subscription in subscriptions:
        try:
            webpush(
                subscription_info=subscription,
                data=message,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS,
            )
        except WebPushException as e:
            print(f"Erreur d'envoi de notification : {e}")
    return jsonify({"message": "Notification envoyée !"}), 200

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
