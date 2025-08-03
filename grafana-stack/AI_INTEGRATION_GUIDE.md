# 🤖 AI Integration Guide - Grafana + AI Assistant

This guide shows you how to integrate the AI assistant **directly into Grafana** like Cursor's AI integration with VS Code.

## 🎯 **What We're Building**

```
┌─────────────────────────────────────────────────────────────┐
│                    Grafana Dashboard                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   CPU Panel     │  │  Memory Panel   │  │  AI Chat    │ │
│  │                 │  │                 │  │  🤖         │ │
│  │                 │  │                 │  │  "Show me   │ │
│  │                 │  │                 │  │   anomalies"│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              AI Sidebar (Floating)                     │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │  🤖 AI Assistant                              │   │ │
│  │  │                                               │   │ │
│  │  │  User: "Create a CPU panel"                  │   │ │
│  │  │  AI: "I'll create a CPU usage panel..."      │   │ │
│  │  │                                               │   │ │
│  │  │  [Quick Actions: CPU, Memory, Anomalies]     │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 **Two Integration Methods**

### **Method 1: App Plugin (Recommended)**
- AI appears as a **dedicated page** in Grafana navigation
- Full-screen AI interface
- Accessible via sidebar menu

### **Method 2: Sidebar Panel (Cursor-like)**
- AI appears as a **floating sidebar** on every page
- Always accessible via toggle button
- Context-aware (knows current dashboard)

## 📦 **Installation Steps**

### **1. Build the Plugin**
```bash
cd grafana-stack/grafana-plugin
npm install
npm run build
```

### **2. Install in Grafana**
```bash
# Copy the built plugin to Grafana's plugin directory
cp -r dist /var/lib/grafana/plugins/ai-assistant-app

# Or for Docker deployment, add to docker-compose.yml:
volumes:
  - ./grafana-plugin/dist:/var/lib/grafana/plugins/ai-assistant-app
```

### **3. Configure Grafana**
```yaml
# grafana.ini
[plugins]
allow_loading_unsigned_plugins = ai-assistant-app

[ai_assistant]
enabled = true
service_url = http://ai-service:5000
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
# AI Service URL
REACT_APP_AI_SERVICE_URL=http://ai-service:5000

# Grafana API
GRAFANA_API_URL=http://grafana:3000
GRAFANA_API_KEY=your_api_key
```

### **Plugin Settings**
```json
{
  "aiServiceUrl": "http://ai-service:5000",
  "enableContextAwareness": true,
  "defaultModel": "gpt-4",
  "autoExpand": false,
  "quickActions": [
    "Analyze CPU",
    "Check Memory", 
    "Find Anomalies",
    "Create Dashboard"
  ]
}
```

## 🎨 **Features**

### **🤖 AI Capabilities**
- **Natural Language Queries**: "Show me CPU usage"
- **Dashboard Creation**: "Create a memory dashboard"
- **Anomaly Detection**: "Find unusual patterns"
- **Query Explanation**: "What does this PromQL do?"
- **Context Awareness**: Knows current dashboard/panel

### **💬 Chat Interface**
- **Real-time Chat**: Like Cursor's AI
- **Message Types**: Text, Queries, Charts, Insights
- **Quick Actions**: One-click common tasks
- **History**: Persistent conversation history
- **Auto-scroll**: Smooth chat experience

### **🔗 Integration Points**
- **Dashboard Context**: AI knows current dashboard
- **Panel Creation**: AI can create new panels
- **Query Execution**: AI can run PromQL queries
- **Data Sources**: AI can access Prometheus data
- **Grafana API**: Full Grafana API integration

## 🛠️ **Usage Examples**

### **Creating Dashboards**
```
User: "Create a dashboard for system monitoring"
AI: "I'll create a comprehensive system monitoring dashboard with CPU, memory, disk, and network panels..."
```

### **Analyzing Data**
```
User: "Why is CPU usage spiking?"
AI: "Looking at the CPU metrics, I can see spikes every 5 minutes. This appears to be a scheduled task..."
```

### **Explaining Queries**
```
User: "What does 'rate(node_cpu_seconds_total[5m])' mean?"
AI: "This PromQL query calculates the rate of CPU time consumption over 5-minute windows..."
```

### **Finding Anomalies**
```
User: "Find anomalies in the last hour"
AI: "I've detected 3 anomalies: 1) Memory usage spike at 2:30 PM, 2) CPU spike at 2:45 PM..."
```

## 🔄 **Data Flow**

```
1. User types message in AI chat
2. AI service receives message + current dashboard context
3. AI queries Prometheus for relevant data
4. AI analyzes data and generates response
5. AI can create panels, execute queries, or provide insights
6. Response appears in chat with appropriate formatting
```

## 🎯 **Cursor-like Experience**

### **Similarities to Cursor AI:**
- ✅ **Floating Chat Panel**: Always accessible
- ✅ **Context Awareness**: Knows current "file" (dashboard)
- ✅ **Natural Language**: Human-like interactions
- ✅ **Quick Actions**: One-click common tasks
- ✅ **Real-time Responses**: Instant feedback
- ✅ **Code Generation**: Creates panels/queries
- ✅ **Explanation**: Explains complex queries

### **Grafana-specific Features:**
- 📊 **Dashboard Creation**: AI creates entire dashboards
- 🔍 **Data Analysis**: AI analyzes metrics and trends
- ⚠️ **Anomaly Detection**: AI finds unusual patterns
- 📈 **Chart Generation**: AI creates visualizations
- 🔗 **Data Source Integration**: AI works with Prometheus

## 🚀 **Deployment**

### **Docker Compose Integration**
```yaml
version: '3.8'
services:
  grafana:
    image: grafana/grafana:latest
    volumes:
      - ./grafana-plugin/dist:/var/lib/grafana/plugins/ai-assistant-app
      - ./grafana.ini:/etc/grafana/grafana.ini
    environment:
      - GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=ai-assistant-app
      - GF_AI_ASSISTANT_ENABLED=true
      - GF_AI_ASSISTANT_SERVICE_URL=http://ai-service:5000
```

### **Render Deployment**
```yaml
# render.yaml
services:
  - type: web
    name: grafana-with-ai
    env: docker
    dockerfilePath: ./grafana-stack/Dockerfile.grafana
    dockerContext: ./grafana-stack
    envVars:
      - key: GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS
        value: ai-assistant-app
      - key: GF_AI_ASSISTANT_ENABLED
        value: true
      - key: GF_AI_ASSISTANT_SERVICE_URL
        value: https://ai-service.onrender.com
```

## 🎉 **Result**

You now have a **fully integrated AI assistant** in Grafana that:

1. **Appears as a floating chat panel** (like Cursor)
2. **Understands your dashboards** and current context
3. **Can create panels and dashboards** with natural language
4. **Analyzes your metrics** and finds anomalies
5. **Explains complex queries** in plain English
6. **Provides intelligent insights** about your system

The AI becomes your **intelligent monitoring companion** - always there to help you understand and optimize your system! 🚀 