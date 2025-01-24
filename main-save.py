# -*- coding: utf-8 -*-
import json
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
log_file = 'data_logs.json'

def load_existing_data():
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    if data:
        # Load existing data
        log_data = load_existing_data()
        
        # Create new log entry
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