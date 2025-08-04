// Working AI Assistant Bookmarklet (Simplified)
// Copy this entire code and create a bookmark with it as the URL
// Click the bookmark on any Grafana page to automatically inject the AI chat

javascript:(function(){
    // Check if already injected
    if (document.getElementById('ai-assistant-container')) {
        console.log('🤖 AI Assistant already injected!');
        return;
    }

    // AI Service URL
    const AI_SERVICE_URL = 'https://ai-service.onrender.com';

    // Create AI container
    const aiContainer = document.createElement('div');
    aiContainer.id = 'ai-assistant-container';
    aiContainer.style.cssText = `
        position: fixed;
        top: 0;
        right: -400px;
        width: 400px;
        height: 100vh;
        background: #1e1e1e;
        border-left: 1px solid #404040;
        box-shadow: -4px 0 12px rgba(0, 0, 0, 0.3);
        z-index: 9999;
        transition: right 0.3s ease;
        display: flex;
        flex-direction: column;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    // Create toggle button
    const toggleButton = document.createElement('button');
    toggleButton.id = 'ai-toggle-button';
    toggleButton.innerHTML = '🤖';
    toggleButton.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        background: #0066cc;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: inherit;
    `;

    // Create header
    const header = document.createElement('div');
    header.style.cssText = `
        background: #2d2d2d;
        padding: 16px 20px;
        border-bottom: 1px solid #404040;
        display: flex;
        align-items: center;
        justify-content: space-between;
    `;

    const title = document.createElement('div');
    title.style.cssText = `
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
    `;
    title.innerHTML = '🤖 AI Assistant';

    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✕';
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: #b0b0b0;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        font-size: 18px;
        font-family: inherit;
    `;

    // Create chat content
    const chatContent = document.createElement('div');
    chatContent.style.cssText = `
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    `;

    // Create messages container
    const messagesContainer = document.createElement('div');
    messagesContainer.id = 'ai-messages';
    messagesContainer.style.cssText = `
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    `;

    // Add welcome message
    const welcomeMessage = document.createElement('div');
    welcomeMessage.style.cssText = `
        text-align: center;
        color: #b0b0b0;
        padding: 2rem;
    `;
    welcomeMessage.innerHTML = `
        <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
        <div><strong>AI Observability Assistant</strong></div>
        <div style="margin-top: 1rem; font-size: 0.9rem;">
            I can help you create dashboards, write PromQL queries, and analyze metrics!
        </div>
        <div style="margin-top: 1rem; font-size: 0.8rem; color: #808080;">
            Try: "Create a CPU usage dashboard" or "Analyze system performance"
        </div>
    `;
    messagesContainer.appendChild(welcomeMessage);

    // Create input container
    const inputContainer = document.createElement('div');
    inputContainer.style.cssText = `
        padding: 1rem;
        border-top: 1px solid #404040;
        background: #1e1e1e;
    `;

    const inputForm = document.createElement('form');
    inputForm.style.cssText = `
        display: flex;
        gap: 0.75rem;
        align-items: flex-end;
    `;

    const inputField = document.createElement('textarea');
    inputField.placeholder = 'Ask me to create dashboards, analyze metrics...';
    inputField.style.cssText = `
        flex: 1;
        background: #2d2d2d;
        border: 1px solid #404040;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        color: #ffffff;
        font-family: inherit;
        font-size: 0.9rem;
        resize: none;
        min-height: 40px;
        max-height: 120px;
    `;

    const sendButton = document.createElement('button');
    sendButton.textContent = 'Send';
    sendButton.style.cssText = `
        background: #0066cc;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        cursor: pointer;
        font-size: 0.9rem;
        min-width: 80px;
        height: 40px;
    `;

    // Add event listeners
    toggleButton.onclick = function() {
        const container = document.getElementById('ai-assistant-container');
        if (container) {
            const isVisible = container.style.right === '0px';
            container.style.right = isVisible ? '-400px' : '0px';
            toggleButton.style.right = isVisible ? '20px' : '420px';
        }
    };

    closeBtn.onclick = function() {
        const container = document.getElementById('ai-assistant-container');
        if (container) {
            container.style.right = '-400px';
            toggleButton.style.right = '20px';
        }
    };

    // Chat functionality
    let messages = [];
    let isLoading = false;

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            display: flex;
            gap: 0.75rem;
            align-items: flex-start;
            max-width: 80%;
            ${isUser ? 'align-self: flex-end; flex-direction: row-reverse;' : 'align-self: flex-start;'}
        `;

        const avatar = document.createElement('div');
        avatar.style.cssText = `
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            flex-shrink: 0;
            background: ${isUser ? '#0066cc' : '#00cc66'};
        `;
        avatar.textContent = isUser ? '👤' : '🤖';

        const bubble = document.createElement('div');
        bubble.style.cssText = `
            padding: 0.75rem 1rem;
            border-radius: 1rem;
            max-width: 100%;
            word-wrap: break-word;
            background: ${isUser ? '#0066cc' : '#2d2d2d'};
            color: ${isUser ? 'white' : '#ffffff'};
            border: ${isUser ? 'none' : '1px solid #404040'};
        `;
        
        // Handle markdown-like formatting
        let formattedContent = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" style="color: #00cc66;">$1</a>')
            .replace(/\n/g, '<br>');
        
        bubble.innerHTML = formattedContent;
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function sendToAI(message) {
        try {
            const response = await fetch(`${AI_SERVICE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('AI Service Error:', error);
            return `❌ Error connecting to AI service: ${error.message}\n\nPlease check if the AI service is deployed and running.`;
        }
    }

    inputForm.onsubmit = async function(e) {
        e.preventDefault();
        const message = inputField.value.trim();
        if (message && !isLoading) {
            addMessage(message, true);
            inputField.value = '';
            
            // Show loading state
            isLoading = true;
            sendButton.disabled = true;
            inputField.disabled = true;
            sendButton.textContent = '...';
            
            try {
                const aiResponse = await sendToAI(message);
                addMessage(aiResponse, false);
            } catch (error) {
                addMessage(`❌ Error: ${error.message}`, false);
            } finally {
                isLoading = false;
                sendButton.disabled = false;
                inputField.disabled = false;
                sendButton.textContent = 'Send';
                inputField.focus();
            }
        }
    };

    // Assemble the components
    inputForm.appendChild(inputField);
    inputForm.appendChild(sendButton);
    inputContainer.appendChild(inputForm);
    
    chatContent.appendChild(messagesContainer);
    chatContent.appendChild(inputContainer);
    
    header.appendChild(title);
    header.appendChild(closeBtn);
    aiContainer.appendChild(header);
    aiContainer.appendChild(chatContent);

    // Add to page
    document.body.appendChild(aiContainer);
    document.body.appendChild(toggleButton);

    // Keyboard shortcut (Ctrl/Cmd + K)
    document.addEventListener('keydown', function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            toggleButton.click();
        }
    });

    // Auto-show the chat
    setTimeout(() => {
        aiContainer.style.right = '0px';
        toggleButton.style.right = '420px';
    }, 100);

    // Success message
    console.log('🤖 AI Assistant automatically injected! Press Ctrl+K to toggle.');
    
    // Show notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: #00cc66;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-family: inherit;
        font-size: 14px;
        z-index: 10001;
        box-shadow: 0 4px 12px rgba(0, 204, 102, 0.3);
        animation: slideIn 0.3s ease;
    `;
    notification.innerHTML = '🤖 AI Assistant loaded! Press Ctrl+K to toggle.';
    document.body.appendChild(notification);

    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

})(); 