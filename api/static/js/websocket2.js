let socket;

function initializeWebSocket() {
  const websocketUrl = 'wss://' + window.location.host + '/ws/conversation/';
  socket = new WebSocket(websocketUrl);

  // Event handler for when the connection is established
  socket.onopen = function(event) {
    console.log("WebSocket connection established!");
  };

  // Event handler for receiving messages from the server
  socket.onmessage = function(event) {
    handleReceivedMessage(event);
  };

  // Event handler for when the connection is closed
  socket.onclose = function(event) {
    console.log('WebSocket connection closed.');
  };
}

function sendMessage(question, agentId, documentId, conversationId) {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    console.log('Socket is not open. Reconnecting...');
    initializeWebSocket();
    setTimeout(() => sendMessage(question, agentId, documentId, conversationId), 1000); // Delay before retrying
    return;
  }

  addUserMessage(question);
  
  // Payload data
  const payload = {
    question: question,
    conversation_id: conversationId,
    document_id: documentId,
    agent_id: agentId,
  };

  // Send the message
  socket.send(JSON.stringify(payload));
}

function handleReceivedMessage(event) {
  // Parse the received message
  const response = JSON.parse(event.data);

  // Access the message from the server
  const messageFromServer = response.message;

  // Process the message as needed
  addBotMessage(messageFromServer);
}

// Call this when you start your application
// initializeWebSocket();