# Projet_Iot

## How to use : 
```
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python ./webapp.py

```

Or just `./setup_and_run.py`

## Pour aller plus loin : 
On peut faire en sorte que data_logs.json s'update et que l'app soit run. Je capte pas bien où sont receptionnées les données.

Sinon on peut juste tout mettre dans une seule app, le fetch des données météo, la reception des données des capteurs.

On peut aussi supprimer l'historique des données des capteurs j'ai pas check si ca marchait bien.

## Data format : 
Format json :
Capteur Température/humidité
{"id": 0, "temperature": 23.5, "humidity": 60}

Capteur Porte
{"id": 1, "door": 1} 
door = 0/1 si fermé/ouvert

