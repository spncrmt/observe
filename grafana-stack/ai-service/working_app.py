from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

# Simple chat interface HTML
CHAT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Observability Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1e1e1e; color: #ffffff; height: 100vh; overflow: hidden;
        }
        .container { 
            display: flex; flex-direction: column; height: 100vh; max-width: 1200px; 
            margin: 0 auto; background: #1e1e1e;
        }
        .header { 
            background: #2d2d2d; padding: 1rem 2rem; border-bottom: 1px solid #404040;
            display: flex; align-items: center; justify-content: space-between;
        }
        .header-title { font-size: 1.5rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }
        .content { flex: 1; display: flex; overflow: hidden; }
        .chat-container { flex: 1; display: flex; flex-direction: column; border-right: 1px solid #404040; }
        .messages { flex: 1; overflow-y: auto; padding: 1rem; display: flex; flex-direction: column; gap: 1rem; }
        .message { display: flex; gap: 0.75rem; align-items: flex-start; max-width: 80%; }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .message.assistant { align-self: flex-start; }
        .message-avatar { 
            width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; 
            justify-content: center; font-size: 1rem; flex-shrink: 0;
        }
        .message.user .message-avatar { background: #0066cc; }
        .message.assistant .message-avatar { background: #00cc66; }
        .message-bubble { 
            padding: 0.75rem 1rem; border-radius: 1rem; max-width: 100%; word-wrap: break-word;
        }
        .message.user .message-bubble { background: #0066cc; color: white; }
        .message.assistant .message-bubble { background: #2d2d2d; border: 1px solid #404040; }
        .input-container { padding: 1rem; border-top: 1px solid #404040; background: #1e1e1e; }
        .input-form { display: flex; gap: 0.75rem; align-items: flex-end; }
        .input-field { 
            flex: 1; background: #2d2d2d; border: 1px solid #404040; border-radius: 0.5rem;
            padding: 0.75rem 1rem; color: #ffffff; font-family: inherit; font-size: 0.9rem;
            resize: none; min-height: 40px; max-height: 120px;
        }
        .send-button { 
            background: #0066cc; color: white; border: none; border-radius: 0.5rem;
            padding: 0.75rem 1rem; cursor: pointer; font-size: 0.9rem; min-width: 80px; height: 40px;
        }
        .sidebar { width: 300px; background: #2d2d2d; border-left: 1px solid #404040; padding: 1rem; overflow-y: auto; }
        .sidebar-section { margin-bottom: 2rem; }
        .sidebar-title { font-size: 1rem; font-weight: 600; margin-bottom: 1rem; color: #ffffff; }
        .capability-item { 
            background: #1e1e1e; border: 1px solid #404040; border-radius: 0.5rem; 
            padding: 1rem; margin-bottom: 0.75rem;
        }
        .capability-title { font-weight: 600; margin-bottom: 0.5rem; color: #ffffff; }
        .capability-description { font-size: 0.8rem; color: #b0b0b0; line-height: 1.4; }
        .welcome-message { text-align: center; color: #b0b0b0; padding: 2rem; }
        .welcome-icon { font-size: 3rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <div class="header-title">🤖 AI Observability Assistant</div>
                <div style="font-size: 0.9rem; color: #b0b0b0; margin-top: 0.25rem;">
                    Ask questions, create dashboards, and analyze your metrics
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #00ff00; animation: pulse 2s infinite;"></div>
                <span>Connected</span>
            </div>
        </div>

        <div class="content">
            <div class="chat-container">
                <div class="messages" id="messages">
                    <div class="welcome-message">
                        <div class="welcome-icon">🤖</div>
                        <div>Ask me about your metrics, create dashboards, or analyze anomalies!</div>
                    </div>
                </div>

                <div class="input-container">
                    <form class="input-form" id="chatForm">
                        <textarea 
                            class="input-field" 
                            id="messageInput" 
                            placeholder="Ask about your metrics, create dashboards, or analyze data..."
                            rows="1"
                        ></textarea>
                        <button type="submit" class="send-button" id="sendButton">Send</button>
                    </form>
                </div>
            </div>

            <div class="sidebar">
                <div class="sidebar-section">
                    <div class="sidebar-title">🤖 AI Capabilities</div>
                    <div class="capability-item">
                        <div class="capability-title">Natural Language Queries</div>
                        <div class="capability-description">
                            Ask questions in plain English like "Show me CPU usage" or "Find memory anomalies"
                        </div>
                    </div>
                    <div class="capability-item">
                        <div class="capability-title">Dashboard Creation</div>
                        <div class="capability-description">
                            Create complete dashboards with natural language commands
                        </div>
                    </div>
                    <div class="capability-item">
                        <div class="capability-title">Anomaly Detection</div>
                        <div class="capability-description">
                            Automatically find unusual patterns in your metrics
                        </div>
                    </div>
                    <div class="capability-item">
                        <div class="capability-title">Query Explanation</div>
                        <div class="capability-description">
                            Get explanations of complex PromQL queries in plain English
                        </div>
                    </div>
                </div>

                <div class="sidebar-section">
                    <div class="sidebar-title">📊 Connected Services</div>
                    <div class="capability-item">
                        <div class="capability-title">Prometheus</div>
                        <div class="capability-description">
                            Time-series database for metrics collection
                        </div>
                    </div>
                    <div class="capability-item">
                        <div class="capability-title">Grafana</div>
                        <div class="capability-description">
                            Dashboard and visualization platform
                        </div>
                    </div>
                    <div class="capability-item">
                        <div class="capability-title">AI Service</div>
                        <div class="capability-description">
                            Intelligent analysis and insights
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const messagesContainer = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const chatForm = document.getElementById('chatForm');

        let messages = [];
        let isLoading = false;

        // Auto-resize textarea
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        // Handle form submission
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const message = messageInput.value.trim();
            if (message && !isLoading) {
                sendMessage(message);
                messageInput.value = '';
                messageInput.style.height = 'auto';
            }
        });

        // Handle Enter key
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });

        async function sendMessage(content) {
            if (isLoading) return;

            const userMessage = {
                role: 'user',
                content: content,
                timestamp: new Date()
            };

            addMessage(userMessage);
            setLoading(true);

            try {
                // Simulate AI response for now
                const response = await simulateAIResponse(content);
                
                const assistantMessage = {
                    role: 'assistant',
                    content: response,
                    timestamp: new Date()
                };

                addMessage(assistantMessage);

            } catch (error) {
                console.error('Failed to send message:', error);
                addErrorMessage('Failed to get response from AI service.');
            } finally {
                setLoading(false);
            }
        }

        function simulateAIResponse(userInput) {
            return new Promise((resolve) => {
                setTimeout(() => {
                    const responses = [
                        "I can help you analyze your metrics! What specific data would you like to look at?",
                        "Great question! I can help you create dashboards and analyze your system performance.",
                        "I'm here to help with your observability needs. What would you like to know about your system?",
                        "I can assist with PromQL queries, dashboard creation, and anomaly detection. What's on your mind?",
                        "Let me help you understand your metrics better. What aspect of your system would you like to explore?"
                    ];
                    resolve(responses[Math.floor(Math.random() * responses.length)]);
                }, 1000);
            });
        }

        function addMessage(message) {
            messages.push(message);
            renderMessages();
        }

        function addErrorMessage(errorText) {
            const errorDiv = document.createElement('div');
            errorDiv.style.cssText = `
                background: #cc0000; color: white; padding: 0.75rem 1rem; 
                border-radius: 0.5rem; margin: 1rem; font-size: 0.9rem;
            `;
            errorDiv.textContent = errorText;
            messagesContainer.appendChild(errorDiv);
            scrollToBottom();
        }

        function renderMessages() {
            // Clear welcome message if there are actual messages
            if (messages.length > 0) {
                const welcomeMessage = messagesContainer.querySelector('.welcome-message');
                if (welcomeMessage) {
                    welcomeMessage.remove();
                }
            }

            // Remove existing messages (except welcome)
            const existingMessages = messagesContainer.querySelectorAll('.message, .loading, .error');
            existingMessages.forEach(msg => msg.remove());

            // Render messages
            messages.forEach(message => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${message.role}`;

                const avatar = document.createElement('div');
                avatar.className = 'message-avatar';
                avatar.textContent = message.role === 'user' ? '👤' : '🤖';

                const bubble = document.createElement('div');
                bubble.className = 'message-bubble';
                bubble.innerHTML = `
                    <div>${message.content}</div>
                    <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.25rem;">
                        ${message.timestamp.toLocaleTimeString()}
                    </div>
                `;

                messageDiv.appendChild(avatar);
                messageDiv.appendChild(bubble);
                messagesContainer.appendChild(messageDiv);
            });

            scrollToBottom();
        }

        function setLoading(loading) {
            isLoading = loading;
            sendButton.disabled = loading;
            messageInput.disabled = loading;

            if (loading) {
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'message assistant';
                loadingDiv.id = 'loading-message';
                loadingDiv.innerHTML = `
                    <div class="message-avatar">🤖</div>
                    <div class="message-bubble">
                        <div style="display: flex; align-items: center; gap: 0.5rem; color: #b0b0b0; font-size: 0.9rem;">
                            <span>AI is thinking</span>
                            <div style="display: flex; gap: 0.25rem;">
                                <div style="width: 4px; height: 4px; border-radius: 50%; background: #b0b0b0; animation: loading 1.4s infinite;"></div>
                                <div style="width: 4px; height: 4px; border-radius: 50%; background: #b0b0b0; animation: loading 1.4s infinite; animation-delay: 0.2s;"></div>
                                <div style="width: 4px; height: 4px; border-radius: 50%; background: #b0b0b0; animation: loading 1.4s infinite; animation-delay: 0.4s;"></div>
                            </div>
                        </div>
                    </div>
                `;
                messagesContainer.appendChild(loadingDiv);
            } else {
                const loadingMessage = document.getElementById('loading-message');
                if (loadingMessage) {
                    loadingMessage.remove();
                }
            }

            scrollToBottom();
        }

        function scrollToBottom() {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            messageInput.focus();
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "service": "AI Observability Platform",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "test": "/test",
            "chat": "/chat"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "AI Observability Platform",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({
        "status": "running",
        "message": "AI service is working!",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/chat', methods=['GET'])
def chat():
    """Full chat interface"""
    return CHAT_HTML

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 