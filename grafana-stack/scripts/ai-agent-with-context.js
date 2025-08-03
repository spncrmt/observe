// Enhanced AI Agent with Dashboard Context
(function() {
  const AI_SERVICE_URL = 'http://localhost:5001';
  
  // Dashboard context tracking
  let currentContext = {
    dashboard_id: null,
    dashboard_title: null,
    panel_id: null,
    current_query: null,
    time_range: null
  };
  
  // Function to capture current dashboard context
  function captureDashboardContext() {
    try {
      // Get dashboard info from Grafana's internal state
      const dashboard = window.grafanaBootData?.settings?.dashboard;
      if (dashboard) {
        currentContext.dashboard_id = dashboard.uid || dashboard.id;
        currentContext.dashboard_title = dashboard.title || document.title.replace(' - Grafana', '');
      }
      
      // Get current panel info
      const activePanel = document.querySelector('.panel-container.active');
      if (activePanel) {
        const panelId = activePanel.getAttribute('data-panel-id');
        if (panelId) {
          currentContext.panel_id = panelId;
        }
      }
      
      // Get current query from active panel
      const queryEditor = document.querySelector('.query-editor-row__query-key');
      if (queryEditor) {
        const queryInput = queryEditor.querySelector('input, textarea');
        if (queryInput) {
          currentContext.current_query = queryInput.value;
        }
      }
      
      // Get time range
      const timeRange = document.querySelector('.time-range-input');
      if (timeRange) {
        currentContext.time_range = timeRange.value;
      }
      
      // Update context with AI service
      updateAIContext();
      
      console.log('Dashboard context captured:', currentContext);
    } catch (error) {
      console.error('Error capturing dashboard context:', error);
    }
  }
  
  // Function to update AI service context
  function updateAIContext() {
    fetch(`${AI_SERVICE_URL}/ai/api/context`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentContext)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('AI context updated:', data.message);
      }
    })
    .catch(error => {
      console.error('Error updating AI context:', error);
    });
  }
  
  // Function to create AI chat interface
  function createAIChat() {
    const chatDiv = document.createElement('div');
    chatDiv.id = 'ai-chat-container';
    chatDiv.style.cssText = 'position: fixed; top: 20px; right: 20px; width: 400px; height: 500px; background: #2d2d2d; border: 2px solid #00d4ff; border-radius: 10px; z-index: 9999; display: flex; flex-direction: column;';
    
    chatDiv.innerHTML = `
      <div style='background: #3d3d3d; padding: 10px; border-radius: 8px 8px 0 0; border-bottom: 1px solid #4d4d4d;'>
        <h3 style='margin: 0; color: #00d4ff;'>🤖 AI Agent</h3>
        <div id='ai-status' style='font-size: 12px; color: #cccccc;'>Connecting...</div>
        <div id='ai-context' style='font-size: 10px; color: #888888; margin-top: 5px;'>Context: None</div>
      </div>
      <div id='ai-messages' style='flex: 1; overflow-y: auto; padding: 10px; background: #2d2d2d;'></div>
      <div style='padding: 10px; background: #3d3d3d; border-radius: 0 0 8px 8px;'>
        <div style='display: flex; gap: 10px;'>
          <input id='ai-input' type='text' placeholder='Ask me anything...' style='flex: 1; padding: 8px; border: none; border-radius: 5px; background: #4d4d4d; color: white;'>
          <button id='ai-send' style='padding: 8px 15px; background: #00d4ff; color: #1e1e1e; border: none; border-radius: 5px; cursor: pointer;'>Send</button>
        </div>
        <div style='margin-top: 5px; display: flex; gap: 5px;'>
          <button id='ai-capture-context' style='padding: 4px 8px; background: #4d4d4d; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 10px;'>Capture Context</button>
          <button id='ai-show-context' style='padding: 4px 8px; background: #4d4d4d; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 10px;'>Show Context</button>
        </div>
      </div>
    `;
    
    document.body.appendChild(chatDiv);
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '×';
    closeBtn.style.cssText = 'position: absolute; top: 5px; right: 10px; background: none; border: none; color: #ff6b6b; font-size: 20px; cursor: pointer;';
    closeBtn.onclick = () => chatDiv.remove();
    chatDiv.querySelector('h3').appendChild(closeBtn);
    
    // Initialize chat
    initAIChat();
  }
  
  function initAIChat() {
    const messagesDiv = document.getElementById('ai-messages');
    const input = document.getElementById('ai-input');
    const sendBtn = document.getElementById('ai-send');
    const statusDiv = document.getElementById('ai-status');
    const contextDiv = document.getElementById('ai-context');
    const captureBtn = document.getElementById('ai-capture-context');
    const showContextBtn = document.getElementById('ai-show-context');
    
    function updateContextDisplay() {
      const contextText = currentContext.dashboard_title 
        ? `Dashboard: ${currentContext.dashboard_title} | Panel: ${currentContext.panel_id || 'None'} | Query: ${currentContext.current_query || 'None'}`
        : 'Context: None';
      contextDiv.textContent = contextText;
    }
    
    function addMessage(text, isUser = false, action = null, success = true) {
      const messageDiv = document.createElement('div');
      messageDiv.style.cssText = `margin-bottom: 10px; padding: 8px; border-radius: 5px; max-width: 80%; word-wrap: break-word; ${isUser ? 'background: #0066cc; color: white; margin-left: auto; text-align: right;' : success ? 'background: #2d5a2d; color: white;' : 'background: #5a2d2d; color: white;'}`;
      messageDiv.innerHTML = text + (action ? ` <span style='background: #00d4ff; color: #1e1e1e; padding: 2px 6px; border-radius: 10px; font-size: 10px; margin-left: 5px;'>${action}</span>` : '');
      messagesDiv.appendChild(messageDiv);
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function sendMessage() {
      const message = input.value.trim();
      if (!message) return;
      
      addMessage(message, true);
      input.value = '';
      
      // Show loading
      const loadingDiv = document.createElement('div');
      loadingDiv.style.cssText = 'margin-bottom: 10px; padding: 8px; border-radius: 5px; background: #4d4d4d; color: white;';
      loadingDiv.textContent = '🤔 Processing...';
      messagesDiv.appendChild(loadingDiv);
      
      // Capture context before sending
      captureDashboardContext();
      
      fetch(`${AI_SERVICE_URL}/ai/api/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: message })
      })
      .then(response => response.json())
      .then(data => {
        messagesDiv.removeChild(loadingDiv);
        addMessage(data.message || 'Sorry, I could not process your request.', false, data.action, data.success);
        
        // Update context display if context was updated
        if (data.context_updated) {
          updateContextDisplay();
        }
      })
      .catch(error => {
        messagesDiv.removeChild(loadingDiv);
        addMessage('❌ Error connecting to AI agent.', false, null, false);
      });
    }
    
    // Check connection and get initial context
    fetch(`${AI_SERVICE_URL}/health`)
      .then(response => response.json())
      .then(data => {
        statusDiv.textContent = '✅ AI Agent Online';
        statusDiv.style.color = '#90ee90';
        
        // Capture initial context
        captureDashboardContext();
        updateContextDisplay();
        
        addMessage('Hello! I\'m your AI observability agent with dashboard context awareness. I can help you with:\n• Creating panels and dashboards\n• Explaining PromQL queries\n• Analyzing anomalies\n• Comparing metrics\n\nI\'m aware of your current dashboard context. What would you like to do?', false);
      })
      .catch(error => {
        statusDiv.textContent = '❌ AI Agent Offline';
        statusDiv.style.color = '#ff6b6b';
        addMessage('❌ Cannot connect to AI Agent. Please check if the service is running.', false, null, false);
      });
    
    // Event listeners
    sendBtn.onclick = sendMessage;
    input.onkeypress = (e) => {
      if (e.key === 'Enter') sendMessage();
    };
    
    captureBtn.onclick = () => {
      captureDashboardContext();
      updateContextDisplay();
      addMessage('✅ Dashboard context captured and sent to AI agent.', false, 'context_update', true);
    };
    
    showContextBtn.onclick = () => {
      const contextInfo = `Current Context:\n• Dashboard: ${currentContext.dashboard_title || 'Unknown'}\n• Panel ID: ${currentContext.panel_id || 'None'}\n• Query: ${currentContext.current_query || 'None'}\n• Time Range: ${currentContext.time_range || 'Default'}`;
      addMessage(contextInfo, false, 'context_info', true);
    };
    
    // Auto-capture context periodically
    setInterval(captureDashboardContext, 30000); // Every 30 seconds
  }
  
  // Create floating AI button
  const aiButton = document.createElement('button');
  aiButton.innerHTML = '🤖 AI';
  aiButton.style.cssText = `
    position: fixed; 
    top: 20px; 
    right: 20px; 
    z-index: 9998; 
    padding: 10px 15px; 
    background: #00d4ff; 
    color: #1e1e1e; 
    border: none; 
    border-radius: 5px; 
    cursor: pointer; 
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  `;
  
  aiButton.onclick = function() {
    const existingChat = document.getElementById('ai-chat-container');
    if (existingChat) {
      existingChat.remove();
    } else {
      createAIChat();
    }
  };
  
  document.body.appendChild(aiButton);
  
  // Auto-capture context when page loads
  setTimeout(captureDashboardContext, 2000);
  
  console.log('Enhanced AI Agent with Dashboard Context loaded!');
})(); 