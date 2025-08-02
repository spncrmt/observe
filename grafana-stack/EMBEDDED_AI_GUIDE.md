# 🤖 Embedding AI Agent in Grafana

## **Quick Start Options**

### **Option 1: Browser Console Chat (Easiest)**

1. **Import the AI Agent Dashboard**:
   ```bash
   # Copy the dashboard JSON to Grafana
   cp grafana-embedded-ai-dashboard.json grafana/dashboards/
   docker-compose restart grafana
   ```

2. **Open Grafana** (http://localhost:3000)

3. **Import the dashboard**:
   - Go to Dashboards → Import
   - Upload `grafana-embedded-ai-dashboard.json`
   - Select Prometheus as data source
   - Import

4. **Activate the AI Chat**:
   - Open the imported dashboard
   - Press `F12` to open Developer Tools
   - Go to Console tab
   - Copy and paste the JavaScript code from the dashboard panel
   - Press Enter

5. **Start chatting!** The AI chat interface will appear in the top-right corner.

### **Option 2: Standalone Chat Interface**

1. **Open the enhanced chat interface**:
   ```bash
   open enhanced-ai-chat.html
   ```

2. **Start chatting directly** with the AI agent

### **Option 3: Direct API Access**

1. **Test the AI agent**:
   ```bash
   # Test basic functionality
   curl -X POST http://localhost:5001/ai/api/process \
     -H "Content-Type: application/json" \
     -d '{"input": "Create a panel showing CPU usage"}'
   
   # Get current context
   curl http://localhost:5001/ai/api/context
   
   # Update context
   curl -X POST http://localhost:5001/ai/api/context \
     -H "Content-Type: application/json" \
     -d '{"dashboard_id": "test", "dashboard_title": "My Dashboard"}'
   ```

## **🎯 AI Agent Capabilities**

### **Natural Language Commands**
- "Create a panel showing CPU usage"
- "Analyze anomalies in memory"
- "Compare CPU vs memory"
- "Explain this query"
- "Get current context"

### **Real Actions**
- ✅ **Panel Creation** - Actually creates panels in dashboards
- ✅ **Anomaly Detection** - Analyzes metrics for anomalies
- ✅ **Query Explanation** - Explains PromQL queries
- ✅ **Metric Comparison** - Compares multiple metrics
- ✅ **Context Awareness** - Maintains dashboard context

### **Context Awareness**
The AI agent maintains awareness of:
- Current dashboard ID and title
- Selected panel ID
- Current time range
- Active queries
- Dashboard variables

## **🔧 Advanced Integration**

### **Custom Dashboard Integration**

Add this to any Grafana dashboard:

```javascript
// AI Agent Integration Script
(function() {
  // Create floating AI button
  const aiButton = document.createElement('button');
  aiButton.innerHTML = '🤖 AI';
  aiButton.style.cssText = `
    position: fixed; 
    top: 20px; 
    right: 20px; 
    z-index: 9999; 
    padding: 10px 15px; 
    background: #00d4ff; 
    color: #1e1e1e; 
    border: none; 
    border-radius: 5px; 
    cursor: pointer; 
    font-weight: bold;
  `;
  
  aiButton.onclick = function() {
    // Toggle AI chat interface
    const existingChat = document.getElementById('ai-chat-container');
    if (existingChat) {
      existingChat.remove();
    } else {
      createAIChat();
    }
  };
  
  document.body.appendChild(aiButton);
  
  function createAIChat() {
    // Chat interface code (same as in dashboard)
    // ... (copy the full chat interface code here)
  }
})();
```

### **Grafana Plugin Development**

For a fully integrated plugin:

1. **Build the plugin**:
   ```bash
   cd grafana-plugin
   npm install
   npm run build
   ```

2. **Install in Grafana**:
   ```bash
   # Copy to Grafana plugins directory
   cp -r dist/ /path/to/grafana/plugins/ai-agent/
   ```

3. **Restart Grafana**:
   ```bash
   docker-compose restart grafana
   ```

## **🚀 Testing the AI Agent**

### **Basic Tests**

```bash
# Test health
curl http://localhost:5001/health

# Test AI processing
curl -X POST http://localhost:5001/ai/api/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, what can you do?"}'

# Test context
curl http://localhost:5001/ai/api/context

# Test anomaly analysis
curl -X POST http://localhost:5001/ai/api/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Analyze anomalies in CPU usage"}'
```

### **Advanced Tests**

```bash
# Test panel creation (requires dashboard context)
curl -X POST http://localhost:5001/ai/api/context \
  -H "Content-Type: application/json" \
  -d '{"dashboard_id": "test", "dashboard_title": "Test Dashboard"}'

curl -X POST http://localhost:5001/ai/api/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Create a panel showing memory usage"}'

# Test query explanation
curl -X POST http://localhost:5001/ai/api/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Explain the query: up"}'
```

## **🔍 Troubleshooting**

### **AI Agent Not Responding**
```bash
# Check if service is running
docker-compose ps ai-service

# Check logs
docker-compose logs ai-service

# Restart service
docker-compose restart ai-service
```

### **Connection Issues**
```bash
# Test connectivity
curl http://localhost:5001/health

# Check if port is accessible
netstat -an | grep 5001
```

### **Grafana Integration Issues**
- Ensure CORS is enabled in the AI service
- Check browser console for errors
- Verify the AI service URL is correct

## **📊 Monitoring the AI Agent**

The AI agent exposes metrics at:
- **Health**: `http://localhost:5001/health`
- **Metrics**: `http://localhost:5001/metrics`
- **Prometheus**: Scraped by Prometheus automatically

### **Key Metrics**
- `ai_service_requests_total` - Total requests
- `ai_service_request_duration_seconds` - Request duration
- `ai_service_system_health_score` - System health

## **🎯 Next Steps**

1. **Try the browser console integration** (Option 1)
2. **Test the standalone chat interface** (Option 2)
3. **Explore the API directly** (Option 3)
4. **Customize the AI agent** for your specific needs
5. **Develop a full Grafana plugin** for production use

The AI agent is now fully embedded and ready to enhance your Grafana observability experience! 🚀 