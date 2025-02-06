from flask import Flask, jsonify
from flask_socketio import SocketIO
import eventlet
import time

# Monkey patch to enable async functionality
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 

@app.route('/')
def index():
    return "Tailgating alert server is running..."

@app.route('/send_alert', methods=['POST'])
def send_alert():
    gate = 'Gate 08'
    alert = "🚨 Tailgating Alert! More people detected than scanned!"
    first_tailgating_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    
    socketio.emit('tailgating_alert', {
        'gate': gate,
        'time': first_tailgating_time,
        'alert': alert
    })
    
    return jsonify({
        'message': 'Tailgating alert sent!',
        'gate': gate,
        'time': first_tailgating_time,
        'alert': alert
    })

if __name__ == '__main__':
    # Use eventlet server to support WebSockets
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
