from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time
import threading

# =========================================================================
# 1. INITIALIZATION & SETUP
# =========================================================================

app = Flask(__name__)

# The 'SECRET_KEY' is used by Flask to sign session cookies for security.
# While not strictly required for simple WebSockets, it's good practice.
app.config['SECRET_KEY'] = 'secret!'

# Initialize SocketIO with the Flask app.
# 'cors_allowed_origins="*"' is a security setting. 
# In a real app, you'd only allow your own website.
# Here, "*" means "let any website connect to this server" (easy for learning).
socketio = SocketIO(app, cors_allowed_origins="*")

# Standard Flask route to show the HTML page (the "Dashboard")
@app.route('/')
def index():
    """Route to serve the main dashboard page."""
    return render_template('index.html')

# =========================================================================
# 2. SOCKET.IO EVENT HANDLERS (The "Listeners")
# =========================================================================

# This function runs automatically whenever a NEW user opens the website.
@socketio.on('connect')
def handle_connect():
    """Triggered when a new client (browser) connects."""
    print("A new user has connected!")
    
    # 'emit' sends a message BACK to the specific user who just connected.
    # Event name: 'server_response'
    # Data: A dictionary with our message
    emit('server_response', {'data': 'Welcome! You are now connected via WebSockets.'})

# This function runs when a user closes the tab or loses internet.
@socketio.on('disconnect')
def handle_disconnect():
    """Triggered when a client disconnects."""
    print("A user has left the session.")

# This is a CUSTOM event. The client (JavaScript) will send data to 'client_message'.
@socketio.on('client_message')
def handle_client_message(json_data):
    """
    Triggered when a user sends a chat message.
    'json_data' contains the user's name and their text.
    """
    print(f"Received from user: {json_data}")
    
    # 'broadcast=True' is the magic part! 
    # It sends the message to EVERY SINGLE PERSON connected to the server.
    # This is how a Group Chat works.
    emit('server_response', {
        'data': f"Broadcast from {json_data['user']}: {json_data['message']}"
    }, broadcast=True)

# =========================================================================
# 3. BACKGROUND TASKS (The "Server-Push")
# =========================================================================

def background_thread():
    """
    A separate thread that runs in the background.
    It doesn't wait for users to do anything; it just pushes data.
    Think of it like a live Stock Ticker or a Weather update.
    """
    while True:
        # We use socketio.sleep (not time.sleep) to keep things smooth
        socketio.sleep(5) 
        
        # Generate a random 'live' value (e.g., simulated CPU usage or stock price)
        random_value = random.randint(1, 100)
        print(f"Pushing live update to all users: {random_value}")
        
        # 'socketio.emit' (instead of just 'emit') is used when 
        # sending from outside a standard event handler.
        socketio.emit('live_update', {'value': random_value})

# Start the background logic as a 'daemon' thread.
# This means it will stop automatically when you stop the Flask server.
thread = threading.Thread(target=background_thread, daemon=True)
thread.start()

# =========================================================================
# 4. START THE SERVER
# =========================================================================

if __name__ == '__main__':
    # IMPORTANT: We use socketio.run(app) instead of app.run(debug=True).
    # This starts the special WebSocket-capable server.
    print("WebSocket Server starting on http://127.0.0.1:5000")
    socketio.run(app, debug=True)
