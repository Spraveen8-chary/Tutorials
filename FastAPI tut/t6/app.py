"""
========================================================
                FastAPI WebSockets
========================================================

Scenario:
---------
You are building a live chat application or a real-time dashboard 
where the server needs to push updates to the user instantly.

Topic:
------
1. WebSocket Protocol
2. Bidirectional Communication
3. Broadcasting to all clients

What it is used for:
--------------------
Real-time features like chat, live notifications, stock tickers, 
and multiplayer games.

Problem it solves:
------------------
Standard HTTP is "request-response" — the server can't talk to the user 
unless the user asks first. WebSockets keep a permanent "tunnel" open, 
allowing both sides to talk at any time.

How it is different from Flask:
-------------------------------
1. Native Support: FastAPI (via Starlette) has WebSockets built-in. 
   Flask requires external libraries like `Flask-SocketIO`.
2. Async by Design: FastAPI WebSockets are natively async, making it 
   much easier to handle thousands of concurrent connections.
3. Simple API: You just use the `websocket: WebSocket` type hint.

Run:
----
uvicorn app:app --reload

========================================================
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# ======================================================
# 1. CONNECTION MANAGER
# ======================================================

class ConnectionManager:
    """
    Manages active WebSocket connections.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# ======================================================
# 2. WEBSOCKET ROUTE
# ======================================================

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    Handles WebSocket connections.
    """
    await manager.connect(websocket)
    try:
        # Send a welcome message
        await manager.send_personal_message(f"Welcome Client #{client_id}!", websocket)
        # Inform everyone about the new user
        await manager.broadcast(f"Client #{client_id} has joined the chat.")
        
        while True:
            # Wait for messages from this client
            data = await websocket.receive_text()
            # Broadcast the message to EVERYONE
            await manager.broadcast(f"Client #{client_id} says: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left.")

# ======================================================
# 3. TEST HTML PAGE
# ======================================================

from fastapi.responses import HTMLResponse

@app.get("/")
async def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI WebSockets</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <input type="text" id="messageText" autocomplete="off"/>
            <button onclick="sendMessage()">Send</button>
            <ul id='messages'></ul>
            <script>
                var client_id = Date.now()
                var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                function sendMessage() {
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                }
            </script>
        </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
