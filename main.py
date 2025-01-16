# -*- coding: utf-8 -*-
from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    # Récupérer les données JSON envoyées par le client
    data = request.json
    print(data)
    if data:
        id = data.get('id')
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
    else:
        return "Aucune donnée reçue", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
