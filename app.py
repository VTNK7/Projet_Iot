from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Variable to monitor
X = 0

# Function to simulate variable changes
def monitor_variable():
    global X
    while True:
        time.sleep(2)  # Simulate variable updates every 2 seconds
        X += 1  # Increment X
        if X > 10:  # Check if X exceeds the threshold
            socketio.emit('notification', {'message': f'X has exceeded 10! Current value: {X}'})
            X = 0  # Reset X for demonstration

# Route for the main page
@app.route('/')
def index():
    return render_template('send_notification.html')

# Start a background thread to monitor the variable
threading.Thread(target=monitor_variable, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
