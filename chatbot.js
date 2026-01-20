// AI Chatbot functionality

document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotMessages = document.getElementById('chatbot-messages');
    
    if (!chatbotToggle || !chatbotWindow) return;
    
    // Toggle chatbot window
    chatbotToggle.addEventListener('click', function() {
        chatbotWindow.classList.toggle('hidden');
        if (!chatbotWindow.classList.contains('hidden')) {
            chatbotInput.focus();
            // Add welcome message if empty
            if (chatbotMessages.children.length === 0) {
                addBotMessage('Hello! I\'m MJ, your AI assistant. How can I help you today?');
            }
        }
    });
    
    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        chatbotWindow.classList.add('hidden');
    });
    
    // Send message
    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;
        
        // Add user message
        addUserMessage(message);
        chatbotInput.value = '';
        
        // Send to backend
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                addBotMessage('Sorry, I encountered an error. Please try again.');
            } else {
                addBotMessage(data.response);
            }
        })
        .catch(error => {
            console.error('Chatbot error:', error);
            addBotMessage('Sorry, I\'m having trouble connecting. Please try again later.');
        });
    }
    
    // Send on button click
    chatbotSend.addEventListener('click', sendMessage);
    
    // Send on Enter key
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Add user message
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chatbot-message user';
        messageDiv.textContent = message;
        chatbotMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // Add bot message
    function addBotMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chatbot-message bot';
        messageDiv.textContent = message;
        chatbotMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // Scroll to bottom of messages
    function scrollToBottom() {
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
});

