// Chatbot Widget JavaScript
(function() {
    'use strict';
    
    const CHATBOT_API_URL = '/chatbot/api/chat/';
    const STORAGE_KEY = 'chatbot_conversation_id';
    const STORAGE_MESSAGES_KEY = 'chatbot_messages';
    
    let conversationId = localStorage.getItem(STORAGE_KEY) || null;
    let isTyping = false;
    
    // Suggested questions
    const SUGGESTED_QUESTIONS = [
        "What is the school address?",
        "Tell me about admission requirements",
        "What events are coming up?",
        "Who is the principal?"
    ];
    
    // Initialize chatbot when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initializeChatbot();
    });
    
    function initializeChatbot() {
        const chatButton = document.getElementById('chatWidgetButton');
        const chatWindow = document.getElementById('chatWindow');
        const closeButton = document.getElementById('chatClose');
        const chatForm = document.getElementById('chatForm');
        const chatInput = document.getElementById('chatInput');
        
        if (!chatButton || !chatWindow) return;
        
        // Toggle chat window
        chatButton.addEventListener('click', function() {
            const isOpen = chatWindow.classList.contains('open');
            if (isOpen) {
                closeChatWindow();
            } else {
                openChatWindow();
            }
        });
        
        // Close button
        if (closeButton) {
            closeButton.addEventListener('click', closeChatWindow);
        }
        
        // Chat form submission
        if (chatForm) {
            chatForm.addEventListener('submit', handleFormSubmit);
        }
        
        // Load conversation history if exists
        loadConversationHistory();
    }
    
    function openChatWindow() {
        const chatWindow = document.getElementById('chatWindow');
        const chatButton = document.getElementById('chatWidgetButton');
        
        chatWindow.classList.add('open');
        chatButton.classList.add('active');
        
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.focus();
        }
        
        // Show suggested questions if no messages
        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer && messagesContainer.children.length === 0) {
            showSuggestedQuestions();
        }
    }
    
    function closeChatWindow() {
        const chatWindow = document.getElementById('chatWindow');
        const chatButton = document.getElementById('chatWidgetButton');
        
        chatWindow.classList.remove('open');
        chatButton.classList.remove('active');
    }
    
    function showSuggestedQuestions() {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        // Add welcome message
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-message';
        welcomeDiv.innerHTML = `
            <h4>👋 Welcome to St. Joseph International School!</h4>
            <p>I'm your AI assistant. How can I help you today?</p>
        `;
        messagesContainer.appendChild(welcomeDiv);
        
        // Add suggested questions
        const suggestedDiv = document.createElement('div');
        suggestedDiv.className = 'suggested-questions';
        suggestedDiv.id = 'suggestedQuestions';
        
        SUGGESTED_QUESTIONS.forEach(question => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'suggested-question';
            button.textContent = question;
            button.addEventListener('click', () => sendSuggestedQuestion(question));
            suggestedDiv.appendChild(button);
        });
        
        messagesContainer.appendChild(suggestedDiv);
        scrollToBottom();
    }
    
    function sendSuggestedQuestion(question) {
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.value = question;
            handleFormSubmit(new Event('submit'));
        }
        
        // Remove suggested questions
        const suggestedDiv = document.getElementById('suggestedQuestions');
        if (suggestedDiv) {
            suggestedDiv.remove();
        }
        
        const welcomeMsg = document.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
    }
    
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        if (isTyping) return;
        
        const chatInput = document.getElementById('chatInput');
        const sendButton = document.getElementById('chatSendButton');
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Disable input
        chatInput.disabled = true;
        sendButton.disabled = true;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        chatInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Send message to API
            const response = await sendMessage(message);
            
            // Hide typing indicator
            hideTypingIndicator();
            
            // Add bot response
            if (response.success) {
                addMessage(response.response, 'bot');
                
                // Save conversation ID
                if (response.conversation_id) {
                    conversationId = response.conversation_id;
                    localStorage.setItem(STORAGE_KEY, conversationId);
                }
                
                // Save to history
                saveToHistory();
            } else {
                addMessage(
                    'Sorry, I encountered an error. Please try again.',
                    'bot'
                );
            }
        } catch (error) {
            console.error('Chat error:', error);
            hideTypingIndicator();
            addMessage(
                'Sorry, I\'m having trouble connecting. Please check your internet connection and try again.',
                'bot'
            );
        }
        
        // Re-enable input
        chatInput.disabled = false;
        sendButton.disabled = false;
        chatInput.focus();
    }
    
    async function sendMessage(message) {
        const requestBody = {
            message: message
        };
        
        if (conversationId) {
            requestBody.conversation_id = conversationId;
        }
        
        const response = await fetch(CHATBOT_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    function addMessage(content, role) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.textContent = role === 'user' ? '👤' : '🤖';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        
        // Parse markdown-like formatting (simple)
        const formattedContent = formatMessageContent(content);
        bubbleDiv.innerHTML = formattedContent;
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(bubbleDiv);
        
        messagesContainer.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function formatMessageContent(content) {
        // Simple formatting for bold, links, and lists
        let formatted = content;
        
        // Bold text (**text**)
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Convert URLs to links
        formatted = formatted.replace(
            /(https?:\/\/[^\s]+)/g,
            '<a href="$1" target="_blank">$1</a>'
        );
        
        // Convert newlines to <br>
        formatted = formatted.replace(/\n/g, '<br>');
        
        return formatted;
    }
    
    function showTypingIndicator() {
        isTyping = true;
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.classList.add('active');
            scrollToBottom();
        }
    }
    
    function hideTypingIndicator() {
        isTyping = false;
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.classList.remove('active');
        }
    }
    
    function scrollToBottom() {
        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer) {
            setTimeout(() => {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 100);
        }
    }
    
    function saveToHistory() {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        try {
            const messages = Array.from(messagesContainer.querySelectorAll('.message')).map(msg => ({
                role: msg.classList.contains('user') ? 'user' : 'bot',
                content: msg.querySelector('.message-bubble').textContent
            }));
            
            localStorage.setItem(STORAGE_MESSAGES_KEY, JSON.stringify(messages.slice(-20))); // Keep last 20
        } catch (error) {
            console.error('Error saving history:', error);
        }
    }
    
    function loadConversationHistory() {
        try {
            const savedMessages = localStorage.getItem(STORAGE_MESSAGES_KEY);
            if (savedMessages) {
                const messages = JSON.parse(savedMessages);
                messages.forEach(msg => {
                    addMessage(msg.content, msg.role);
                });
            }
        } catch (error) {
            console.error('Error loading history:', error);
            // Clear corrupted data
            localStorage.removeItem(STORAGE_MESSAGES_KEY);
        }
    }
})();
