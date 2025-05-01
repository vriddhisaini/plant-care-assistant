const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

let welcomeMessageShown = false;  // Flag to track if welcome message has been shown

window.addEventListener('DOMContentLoaded', function() {
  if (!welcomeMessageShown) {  // Check if the welcome message has already been shown
    const welcomeMsg = document.createElement('div');
    welcomeMsg.className = 'bot-message';
    welcomeMsg.innerHTML = "<b><u>AI Powered Plant Care Assistant</b></u>.<br>This chat bot utilizes decision trees with the support of LLM fallback.<br>To enable LLM fallback directly, enter \"gemini: user-input\"";
    chatBox.appendChild(welcomeMsg);
    welcomeMessageShown = true;  // Set flag to true after showing the welcome message
  }
});

form.addEventListener('submit', async function (e) {
  e.preventDefault();
  const userText = input.value.trim();
  if (!userText) return;

  // Add user message to chat
  const userMsg = document.createElement('div');
  userMsg.className = 'user-message';
  userMsg.textContent = userText;
  chatBox.appendChild(userMsg);

  // Clear input field
  input.value = '';
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    console.log('Sending message:', userText);  // Log the message
    // Send message to FastAPI backend
    const response = await fetch('http://localhost:8000/chat', { //replace with backend deployment url
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_message: userText })
    });

    // Check if response is OK
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Log the entire response object
    const data = await response.json();
    console.log('Response data:', data);  // Log the response data
    
    const botMsg = document.createElement('div');
    botMsg.className = 'bot-message';
    
    // Handling different possible responses
    if (data.response) {
      let formattedResponse = data.response;
      formattedResponse = formattedResponse.replace(/\n/g, '<br>');
      formattedResponse = formattedResponse.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>'); //formatting response
      formattedResponse = formattedResponse.replace(/\*(.*?)\*/g, '<b>$1</b>');
      
      botMsg.innerHTML = formattedResponse;
    } else if (data.error) {
      botMsg.textContent = "Error: " + data.error;
    } else {
      botMsg.textContent = "Unexpected response. Please try again.";
    }

    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (error) {
    const errorMsg = document.createElement('div');
    errorMsg.className = 'bot-message';
    errorMsg.textContent = "Something went wrong. Please try again later.";
    chatBox.appendChild(errorMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
    console.error("Chatbot error:", error);  // Log full error for debugging
  }
});