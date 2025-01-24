# -*- coding: utf-8 -*-
import json
from flask import Flask, request
from datetime import datetime

# Initialiser l'application Flask
app = Flask(__name__)

# Nom du fichier où enregistrer les données
log_file = 'data_logs.json'

@app.route('/data', methods=['POST'])
def receive_data():
    # Récupérer les données JSON envoyées par le client
    data = request.json

    if data:
        id = data.get('id')
        log_entry = {
            "timestamp": datetime.now().isoformat(),  # Heure ISO 8601
            "data": data
        }
        # Écrire l'entrée JSON dans le fichier
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        if id == 0:
            # Afficher les données dans la console
            print("Données reçues :")
            print(f" - Température : {data.get('temperature')}°C")
            print(f" - Humidité : {data.get('humidity')}%")
            return "Données reçues", 200
        elif id == 1:
            # Afficher les données dans la console
            print("Données reçues :")
            print(f" - Porte : {data.get('door')}")
            return "Données reçues", 200
        return "data received", 400
    else:
        # Créer une entrée d'erreur si aucune donnée n'est reçue
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "error": "Aucune donnée reçue"
        }
        # Écrire l'entrée d'erreur dans le fichier
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        return "Aucune donnée reçue", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
