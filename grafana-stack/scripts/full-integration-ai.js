// Full Integration AI Agent for Grafana
// ====================================
// 
// This script provides complete AI integration with Grafana:
// - Real context capture from Grafana
// - Direct panel creation and modification
// - AI-powered responses and actions
// - No manual inspection required

(function() {
  const AI_SERVICE_URL = 'http://localhost:5001';
  
  // Enhanced context capture with automatic detection
  function captureRealGrafanaContext() {
    const context = {
      dashboard_id: null,
      dashboard_title: null,
      dashboard_uid: null,
      user: null,
      panels: [],
      queries: [],
      time_range: null,
      url: window.location.href,
      grafana_version: null,
      available_data_sources: []
    };
    
    console.log('🔍 Capturing real Grafana context automatically...');
    
    // Method 1: Extract from grafanaBootData (most reliable)
    if (window.grafanaBootData) {
      // Get user info
      if (window.grafanaBootData.user) {
        context.user = {
          id: window.grafanaBootData.user.id,
          login: window.grafanaBootData.user.login,
          email: window.grafanaBootData.user.email
        };
      }
      
      // Get settings info
      if (window.grafanaBootData.settings) {
        context.grafana_version = window.grafanaBootData.settings.buildInfo?.version;
      }
      
      // Get dashboard info from settings
      if (window.grafanaBootData.settings?.dashboard) {
        const dashboard = window.grafanaBootData.settings.dashboard;
        context.dashboard_id = dashboard.id;
        context.dashboard_uid = dashboard.uid;
        context.dashboard_title = dashboard.title;
      }
    }
    
    // Method 2: Extract from URL
    if (!context.dashboard_id) {
      const urlMatch = window.location.pathname.match(/\/d\/([^\/]+)/);
      if (urlMatch) {
        context.dashboard_id = urlMatch[1];
      }
    }
    
    // Method 3: Extract from page title
    if (!context.dashboard_title) {
      context.dashboard_title = document.title.replace(' - Dashboards - Grafana', '');
    }
    
    // Method 4: Look for panels in the DOM
    const panelElements = document.querySelectorAll('[data-panel-id], .panel-container, .dashboard-panel');
    if (panelElements.length > 0) {
      panelElements.forEach((panel, index) => {
        const panelInfo = {
          id: panel.getAttribute('data-panel-id') || `panel-${index}`,
          title: panel.querySelector('.panel-title')?.textContent || `Panel ${index + 1}`,
          type: panel.getAttribute('data-panel-type') || 'unknown'
        };
        context.panels.push(panelInfo);
      });
    }
    
    // Method 5: Look for query editors
    const queryElements = document.querySelectorAll('.query-editor-row, [data-testid*="query"], .query-editor');
    if (queryElements.length > 0) {
      queryElements.forEach((query, index) => {
        const queryInfo = {
          id: `query-${index}`,
          text: query.querySelector('input, textarea')?.value || '',
          data_source: query.getAttribute('data-datasource') || 'unknown'
        };
        context.queries.push(queryInfo);
      });
    }
    
    // Method 6: Look for time range
    const timeElements = document.querySelectorAll('.time-range-input, [data-testid*="time"], .time-picker-input');
    if (timeElements.length > 0) {
      context.time_range = timeElements[0].value || timeElements[0].textContent;
    }
    
    // Method 7: Look for data sources in navTree
    if (window.grafanaBootData?.navTree) {
      const dataSources = window.grafanaBootData.navTree
        .filter(item => item.id === 'datasources')
        .flatMap(item => item.children || [])
        .map(item => item.id);
      context.available_data_sources = dataSources;
    }
    
    console.log('📊 Captured context:', context);
    return context;
  }
  
  // Function to update AI service context
  function updateAIContext(context) {
    return fetch(`${AI_SERVICE_URL}/ai/api/context`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(context)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('✅ AI context updated:', data.message);
        return data;
      } else {
        console.error('❌ Failed to update AI context:', data.error);
        throw new Error(data.error);
      }
    })
    .catch(error => {
      console.error('❌ Error updating AI context:', error);
      throw error;
    });
  }
  
  // Function to process AI request with full integration
  function processAIRequest(userInput, context) {
    return fetch(`${AI_SERVICE_URL}/ai/api/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        input: userInput,
        context: context
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('🤖 AI Response:', data);
      return data;
    })
    .catch(error => {
      console.error('❌ Error processing AI request:', error);
      throw error;
    });
  }
  
  // Function to create enhanced AI chat interface
  function createFullIntegrationAIChat() {
    const chatDiv = document.createElement('div');
    chatDiv.id = 'full-integration-ai-chat';
    chatDiv.style.cssText = `
      position: fixed; 
      top: 20px; 
      right: 20px; 
      width: 500px; 
      height: 650px; 
      background: #2d2d2d; 
      border: 2px solid #00d4ff; 
      border-radius: 10px; 
      z-index: 9999; 
      display: flex; 
      flex-direction: column;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;
    
    chatDiv.innerHTML = `
      <div style='background: #3d3d3d; padding: 15px; border-radius: 8px 8px 0 0; border-bottom: 1px solid #4d4d4d;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
          <h3 style='margin: 0; color: #00d4ff; font-size: 16px;'>🤖 AI Observability Agent</h3>
          <button id='close-full-ai-chat' style='background: none; border: none; color: #ff6b6b; font-size: 20px; cursor: pointer;'>×</button>
        </div>
        <div id='ai-status' style='font-size: 12px; color: #cccccc; margin-top: 5px;'>Connecting...</div>
        <div id='ai-context-summary' style='font-size: 10px; color: #888888; margin-top: 5px; max-height: 60px; overflow-y: auto;'>Context: Loading...</div>
        <div id='ai-actions' style='font-size: 10px; color: #00d4ff; margin-top: 5px;'>Actions: Ready</div>
      </div>
      <div id='ai-messages' style='flex: 1; overflow-y: auto; padding: 15px; background: #2d2d2d;'></div>
      <div style='padding: 15px; background: #3d3d3d; border-radius: 0 0 8px 8px;'>
        <div style='display: flex; gap: 10px; margin-bottom: 10px;'>
          <input id='ai-input' type='text' placeholder='Ask me to create panels, analyze metrics, explain queries...' 
                 style='flex: 1; padding: 10px; border: none; border-radius: 5px; background: #4d4d4d; color: white; font-size: 14px;'>
          <button id='ai-send' style='padding: 10px 15px; background: #00d4ff; color: #1e1e1e; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;'>Send</button>
        </div>
        <div style='display: flex; gap: 5px; flex-wrap: wrap;'>
          <button id='auto-capture-context' style='padding: 6px 12px; background: #4d4d4d; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 11px;'>Auto Capture</button>
          <button id='show-context' style='padding: 6px 12px; background: #4d4d4d; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 11px;'>Show Context</button>
          <button id='test-actions' style='padding: 6px 12px; background: #4d4d4d; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 11px;'>Test Actions</button>
        </div>
      </div>
    `;
    
    document.body.appendChild(chatDiv);
    initFullIntegrationChat();
  }
  
  function initFullIntegrationChat() {
    const messagesDiv = document.getElementById('ai-messages');
    const input = document.getElementById('ai-input');
    const sendBtn = document.getElementById('ai-send');
    const statusDiv = document.getElementById('ai-status');
    const contextDiv = document.getElementById('ai-context-summary');
    const actionsDiv = document.getElementById('ai-actions');
    const autoCaptureBtn = document.getElementById('auto-capture-context');
    const showContextBtn = document.getElementById('show-context');
    const testActionsBtn = document.getElementById('test-actions');
    const closeBtn = document.getElementById('close-full-ai-chat');
    
    let currentContext = null;
    let lastAction = null;
    
    function updateContextDisplay() {
      if (currentContext) {
        const summary = `Dashboard: ${currentContext.dashboard_title || 'Unknown'} | Panels: ${currentContext.panels.length} | Queries: ${currentContext.queries.length}`;
        contextDiv.textContent = summary;
      } else {
        contextDiv.textContent = 'Context: None';
      }
    }
    
    function updateActionsDisplay(action) {
      if (action) {
        actionsDiv.textContent = `Last Action: ${action}`;
        actionsDiv.style.color = '#00d4ff';
      } else {
        actionsDiv.textContent = 'Actions: Ready';
        actionsDiv.style.color = '#888888';
      }
    }
    
    function addMessage(text, isUser = false, action = null, success = true) {
      const messageDiv = document.createElement('div');
      messageDiv.style.cssText = `
        margin-bottom: 12px; 
        padding: 10px; 
        border-radius: 8px; 
        max-width: 85%; 
        word-wrap: break-word; 
        font-size: 14px;
        line-height: 1.4;
        ${isUser 
          ? 'background: #0066cc; color: white; margin-left: auto; text-align: right;' 
          : success 
            ? 'background: #2d5a2d; color: white;' 
            : 'background: #5a2d2d; color: white;'
        }
      `;
      messageDiv.innerHTML = text + (action ? ` <span style='background: #00d4ff; color: #1e1e1e; padding: 2px 6px; border-radius: 10px; font-size: 10px; margin-left: 5px;'>${action}</span>` : '');
      messagesDiv.appendChild(messageDiv);
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    async function sendMessage() {
      const message = input.value.trim();
      if (!message) return;
      
      addMessage(message, true);
      input.value = '';
      
      // Show loading
      const loadingDiv = document.createElement('div');
      loadingDiv.style.cssText = 'margin-bottom: 12px; padding: 10px; border-radius: 8px; background: #4d4d4d; color: white; font-size: 14px;';
      loadingDiv.textContent = '🤔 Processing with full integration...';
      messagesDiv.appendChild(loadingDiv);
      
      try {
        // Auto-capture context
        currentContext = captureRealGrafanaContext();
        await updateAIContext(currentContext);
        updateContextDisplay();
        
        // Process with AI
        const result = await processAIRequest(message, currentContext);
        
        messagesDiv.removeChild(loadingDiv);
        
        if (result.success) {
          addMessage(result.message, false, result.action, true);
          lastAction = result.action;
          updateActionsDisplay(result.action);
          
          // If panel was created, show success message
          if (result.action === 'create_panel' && result.data) {
            addMessage(`🎉 Panel "${result.data.panel_title}" created successfully! Check your dashboard.`, false, 'success', true);
          }
        } else {
          addMessage(`❌ ${result.message}`, false, 'error', false);
        }
        
      } catch (error) {
        messagesDiv.removeChild(loadingDiv);
        addMessage(`❌ Error: ${error.message}`, false, 'error', false);
      }
    }
    
    // Check connection and get initial context
    fetch(`${AI_SERVICE_URL}/health`)
      .then(response => response.json())
      .then(data => {
        statusDiv.textContent = '✅ AI Agent Online';
        statusDiv.style.color = '#90ee90';
        
        // Auto-capture initial context
        currentContext = captureRealGrafanaContext();
        updateAIContext(currentContext);
        updateContextDisplay();
        
        addMessage(`🚀 **Full Integration AI Agent** is ready!

I can now:
• **Create panels automatically** (CPU, memory, disk, network)
• **Analyze your system** in real-time
• **Explain queries** and provide insights
• **Execute actions** directly in Grafana

Current Context:
• Dashboard: ${currentContext.dashboard_title || 'Unknown'}
• User: ${currentContext.user?.login || 'Unknown'}
• Panels: ${currentContext.panels.length}

Try asking me to:
• "Create a CPU usage panel"
• "Show memory metrics"
• "Analyze system health"
• "Explain this query"`, false);
      })
      .catch(error => {
        statusDiv.textContent = '❌ AI Agent Offline';
        statusDiv.style.color = '#ff6b6b';
        addMessage('❌ Cannot connect to AI Agent. Please check if the service is running on port 5001.', false, null, false);
      });
    
    // Event listeners
    sendBtn.onclick = sendMessage;
    input.onkeypress = (e) => {
      if (e.key === 'Enter') sendMessage();
    };
    
    autoCaptureBtn.onclick = async () => {
      try {
        currentContext = captureRealGrafanaContext();
        await updateAIContext(currentContext);
        updateContextDisplay();
        addMessage('✅ Context captured and sent to AI agent automatically.', false, 'context_update', true);
      } catch (error) {
        addMessage(`❌ Error capturing context: ${error.message}`, false, 'error', false);
      }
    };
    
    showContextBtn.onclick = () => {
      if (currentContext) {
        const contextInfo = `**Current Context:**
• Dashboard: ${currentContext.dashboard_title || 'Unknown'}
• Dashboard ID: ${currentContext.dashboard_id || 'None'}
• Dashboard UID: ${currentContext.dashboard_uid || 'None'}
• User: ${currentContext.user?.login || 'Unknown'}
• Panels: ${currentContext.panels.length}
• Queries: ${currentContext.queries.length}
• Time Range: ${currentContext.time_range || 'Default'}
• Data Sources: ${currentContext.available_data_sources.join(', ') || 'None'}
• Grafana Version: ${currentContext.grafana_version || 'Unknown'}`;
        addMessage(contextInfo, false, 'context_info', true);
      } else {
        addMessage('❌ No context available. Click "Auto Capture" first.', false, null, false);
      }
    };
    
    testActionsBtn.onclick = async () => {
      addMessage('🧪 Testing AI actions...', false, 'test', true);
      
      try {
        // Test panel creation
        const testContext = {
          ...currentContext,
          dashboard_uid: currentContext.dashboard_uid || 'test'
        };
        
        const result = await processAIRequest("Create a CPU usage panel", testContext);
        if (result.success) {
          addMessage('✅ AI actions working! Panel creation test successful.', false, 'test_success', true);
        } else {
          addMessage('❌ AI actions test failed. Check service logs.', false, 'test_failed', false);
        }
      } catch (error) {
        addMessage(`❌ Test failed: ${error.message}`, false, 'test_error', false);
      }
    };
    
    closeBtn.onclick = () => {
      chatDiv.remove();
    };
    
    // Auto-capture context periodically
    setInterval(async () => {
      try {
        currentContext = captureRealGrafanaContext();
        await updateAIContext(currentContext);
        updateContextDisplay();
      } catch (error) {
        console.error('Auto-capture error:', error);
      }
    }, 30000); // Every 30 seconds
  }
  
  // Create floating AI button
  const aiButton = document.createElement('button');
  aiButton.innerHTML = '🤖 AI';
  aiButton.style.cssText = `
    position: fixed; 
    top: 20px; 
    right: 20px; 
    z-index: 9998; 
    padding: 12px 18px; 
    background: #00d4ff; 
    color: #1e1e1e; 
    border: none; 
    border-radius: 6px; 
    cursor: pointer; 
    font-weight: bold;
    font-size: 14px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    transition: all 0.2s ease;
  `;
  
  aiButton.onmouseover = () => {
    aiButton.style.transform = 'scale(1.05)';
    aiButton.style.boxShadow = '0 6px 12px rgba(0,0,0,0.4)';
  };
  
  aiButton.onmouseout = () => {
    aiButton.style.transform = 'scale(1)';
    aiButton.style.boxShadow = '0 4px 8px rgba(0,0,0,0.3)';
  };
  
  aiButton.onclick = function() {
    const existingChat = document.getElementById('full-integration-ai-chat');
    if (existingChat) {
      existingChat.remove();
    } else {
      createFullIntegrationAIChat();
    }
  };
  
  document.body.appendChild(aiButton);
  
  // Auto-capture context when page loads
  setTimeout(async () => {
    try {
      const initialContext = captureRealGrafanaContext();
      await updateAIContext(initialContext);
    } catch (error) {
      console.error('Initial context capture error:', error);
    }
  }, 2000);
  
  console.log('🚀 Full Integration AI Agent loaded! No manual inspection required.');
})(); 