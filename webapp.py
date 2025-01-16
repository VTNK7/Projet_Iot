from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Charger les données simulées à partir d'un fichier JSON
def load_example_data():
    with open('example_data.json', 'r') as file:
        return json.load(file)

# Route pour afficher les dernières données des capteurs
@app.route('/')
def index():
    # Charger les données simulées
    data = load_example_data()

    # Récupérer les dernières données de chaque capteur
    latest_data = {}
    for entry in data:
        sensor_type = entry['sensor_type']
        if sensor_type not in latest_data or entry['timestamp'] > latest_data[sensor_type]['timestamp']:
            latest_data[sensor_type] = entry

    return render_template('index.html', data=latest_data.values())

# Route pour afficher l'historique des données d'un capteur
@app.route('/history/<sensor_type>')
def history(sensor_type):
    # Charger les données simulées
    data = load_example_data()

    # Filtrer les données par type de capteur
    history_data = [entry for entry in data if entry['sensor_type'] == sensor_type]

    return render_template('history.html', sensor_type=sensor_type, data=history_data)

# API pour obtenir les données simulées en JSON (optionnel)
@app.route('/api/data', methods=['GET'])
def api_data():
    data = load_example_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
