console.log("HELLO WORLD");
var floatingBall = document.querySelector('.open-sidebar');
var threatsSideComponent = document.querySelector('.threats-side-component');

document.querySelector('.open-sidebar').addEventListener('click', function() {
    
    
    if (threatsSideComponent.style.display === 'block') {
        threatsSideComponent.style.display = 'none';
        floatingBall.style.display = 'none';
    } else {
        threatsSideComponent.style.display = 'block';
        floatingBall.style.display = 'none';
    }
});
document.querySelector('.hide-sidebar').addEventListener('click', function() {
        threatsSideComponent.style.display = 'none';
        floatingBall.style.display = 'flex';
});
document.getElementById('submit-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    const agentId = document.getElementById('agents').value;
    const documentId = document.getElementById('documents').value;
    const conversationId = document.getElementById('conversation-id').value; 
    console.log('SENDING MESSAGE');
    // Retrieve the conversation_id
      sendMessage(userInput, agentId, documentId, conversationId);
     });
  
  function sendMessage(question, agentId, documentId, conversationId) {
   // You still need to replace this with the way you are getting your conversation ID
    
    const url = `v1/aitools/conversation/${conversationId}/message`;
  
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
        console.log(data);
      })
      .catch(error => {
        // Handle any errors
        console.error(error);
      });
  }