// =========================================================================
// 1. INITIALIZE THE CONNECTION
// =========================================================================

// 'io()' comes from the Socket.IO library we loaded in the HTML file.
// It automatically finds our server and opens the "live pipe" (the WebSocket).
const socket = io();

// Grab all the HTML elements we need so we can update them later.
const statusLabel = document.getElementById('status');
const liveValueLabel = document.getElementById('live-value');
const messageBox = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const usernameInput = document.getElementById('username');

// =========================================================================
// 2. RECEIVING DATA FROM SERVER (The "Listeners")
// =========================================================================

// Triggered when the browser successfully connects to the Flask server.
socket.on('connect', () => {
    statusLabel.innerText = "Connected";
    statusLabel.className = "connected"; // Changes color to green in CSS
    addMessageToUI("System", "You are now connected to the real-time server!");
});

// Triggered if the server goes down or your internet cuts out.
socket.on('disconnect', () => {
    statusLabel.innerText = "Disconnected";
    statusLabel.className = "disconnected"; // Changes color to red in CSS
});

// Listener for 'server_response' (Used for Chat Messages).
// This runs whenever the server sends an 'emit' with this name.
socket.on('server_response', (msg) => {
    addMessageToUI("Server", msg.data);
});

// Listener for 'live_update' (Used for the background random number).
// This runs every 5 seconds because of the server's background thread.
socket.on('live_update', (data) => {
    // Update the number on the screen
    liveValueLabel.innerText = data.value;
    
    // Quick visual effect: Flash the number red when it changes
    liveValueLabel.style.color = '#ff0000';
    setTimeout(() => { 
        liveValueLabel.style.color = '#fbbc05'; // Change back to yellow/gold
    }, 500);
});

// =========================================================================
// 3. SENDING DATA TO SERVER (The "Emitters")
// =========================================================================

/**
 * Reads the input fields and sends the data to the server.
 */
function sendMessage() {
    const messageText = messageInput.value;
    const userName = usernameInput.value;

    // Only send if the message isn't empty!
    if (messageText.trim() !== "") {
        
        // 'socket.emit' sends a message TO the server.
        // 1st param: Event name ('client_message')
        // 2nd param: The data (a JavaScript object)
        socket.emit('client_message', {
            'user': userName,
            'message': messageText
        });

        // Clear the text box so the user can type the next message
        messageInput.value = ""; 
    }
}

/**
 * Helper function to create a new message bubble on the webpage.
 */
function addMessageToUI(user, text) {
    const div = document.createElement('div');
    div.className = 'message';
    div.innerHTML = `<strong>${user}:</strong> ${text}`;
    
    // Append the new message to our chat box
    messageBox.appendChild(div);
    
    // Auto-scroll to the bottom so you always see the latest message
    messageBox.scrollTop = messageBox.scrollHeight;
}

// CONVENIENCE: Let the user press the "Enter" key to send messages.
messageInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});
