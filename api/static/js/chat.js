
const textarea = document.getElementById('user-input');
// console.log("HELLO WORLD");
const floatingBall = document.querySelector('.open-sidebar');
const threatsSideComponent = document.querySelector('.threats-side-component');
const draggableElement = document.getElementById("draggableElement");

hideSiderBar()
openSideBar()
addEventHandlers()



function addEventHandlers() {
  document.getElementById('submit-btn').addEventListener('click',onSubmitMessage);


  textarea.addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
      event.preventDefault(); 
      onSubmitMessage();
    }
  });
}

// Functions




function onSubmitMessage() {
  let userInput = document.getElementById('user-input');
  const agentId = document.getElementById('agents').value;
  const documentId = document.getElementById('documents').value;
  const conversationId = document.getElementById('conversation-id').value;
  sendMessage(userInput.value, agentId, documentId, conversationId);
  userInput.value = '';
};

function sendMessage(question, agentId, documentId, conversationId) {
  // You still need to replace this with the way you are getting your conversation ID
  const url = `v1/aitools/conversation/${conversationId}/message`;
  addUserMessage(question)
  // Payload data
  const payload = {
    question: question,
    conversation_id: conversationId,
    document_id: documentId,
    agent_id: agentId,
  };

  // Fetch request
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_AUTH_TOKEN', // Replace with your actual authorization token
    },
    body: JSON.stringify(payload),
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response data
      addBotMessage(data.answer)
      // console.log(data.answer);
    })
    .catch(error => {
      // Handle any errors
      console.error(error);
    });
}


function openSideBar() {
  document.querySelector('.open-sidebar').addEventListener('click', function () {
    if (threatsSideComponent.style.display === 'block') {
      threatsSideComponent.style.display = 'none';
      floatingBall.style.display = 'none';
    } else {
      threatsSideComponent.style.display = 'block';
      floatingBall.style.display = 'none';
    }
  });
}

function hideSiderBar() {
  document.querySelector('.hide-sidebar').addEventListener('click', function () {
    threatsSideComponent.style.display = 'none';
    floatingBall.style.display = 'flex';
  });
}

function addUserMessage(message) {
  // Create a new div element for the user message
  const userMessageDiv = document.createElement("div");
  userMessageDiv.classList.add("message-bubble", "user-message");
  userMessageDiv.innerText = message;
  // Get the chat-messages container and append the new user message
  const chatMessagesContainer = document.querySelector(".chat-messages");
  chatMessagesContainer.appendChild(userMessageDiv);
}

function addBotMessage(message) {
  // Create a new div element for the user message
  const userMessageDiv = document.createElement("div");
  userMessageDiv.classList.add("message-bubble", "bot-message");
  userMessageDiv.innerText = message;
  // Get the chat-messages container and append the new user message
  const chatMessagesContainer = document.querySelector(".chat-messages");
  chatMessagesContainer.appendChild(userMessageDiv);
}















