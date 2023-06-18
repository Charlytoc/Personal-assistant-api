const websocketUrl = 'ws://' + window.location.host + '/ws/conversation/';
const socket = new WebSocket(websocketUrl);



function main () {
    // Event handler for when the connection is established
socket.onopen = function(event) {
    handleConnectionOpen();
};

// Event handler for receiving messages from the server
socket.onmessage = function(event) {
    handleReceivedMessage(event);
};

// Event handler for when the connection is closed
socket.onclose = function(event) {
    handleConnectionClose();
};

}
function handleConnectionOpen() {
    console.log("WebSocket connection established!");
    const message = { "message": "Hello" }; // Define the message to send
    sendMessage(JSON.stringify(message)); // Send the message
}

function handleReceivedMessage(event) {
    // Parse the received message
    const response = JSON.parse(event.data);

    // Access the message from the server
    const messageFromServer = response.message;

    // Process the message as needed
    processMessageFromServer(messageFromServer);
}

function handleConnectionClose() {
    console.log('WebSocket connection closed.');
}

function sendMessage(message) {
    socket.send(message);
}

function processMessageFromServer(message) {
    console.log('Message from server:', message);
}