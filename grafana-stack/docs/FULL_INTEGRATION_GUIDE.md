# Full Integration AI Agent Guide

## 🎯 Overview

This guide shows you how to use the **Full Integration AI Agent** that can actually execute actions in Grafana, not just provide guidance. The AI can:

- ✅ **Create panels automatically** (CPU, memory, disk, network)
- ✅ **Analyze system metrics** in real-time
- ✅ **Explain queries** and provide insights
- ✅ **Execute actions** directly through Grafana API
- ✅ **No manual inspection required** - fully automated

## 🚀 What We Built

### 1. **Grafana API Client** (`grafana-api-client.py`)
- Direct integration with Grafana API
- Can create, modify, and delete panels
- Supports CPU, memory, disk, and custom panels
- Handles authentication and error management

### 2. **Enhanced AI Agent** (`ai-service/enhanced_ai_agent.py`)
- Uses proper AI model (OpenAI GPT-3.5-turbo)
- Intent analysis and action execution
- Context-aware responses
- Fallback to rule-based responses if AI unavailable

### 3. **Full Integration Frontend** (`full-integration-ai.js`)
- Automatic context capture
- Real-time AI processing
- Direct action execution
- Beautiful chat interface

## 🎯 How to Use

### Step 1: Start the AI Service

```bash
# Navigate to the AI service directory
cd grafana-stack/ai-service

# Install dependencies (if needed)
pip install openai requests flask flask-cors

# Set OpenAI API key (optional, for enhanced AI responses)
export OPENAI_API_KEY="your-openai-api-key"

# Start the AI service
python app.py
```

The service will start on `http://localhost:5001`

### Step 2: Load the Full Integration Script

1. **Open Grafana**: http://localhost:3000
2. **Open Developer Tools**: Press F12
3. **Go to Console tab**
4. **Copy and paste the full integration script**:

```javascript
// Copy the entire content from full-integration-ai.js
```

5. **Press Enter** to load the script

### Step 3: Use the AI Agent

1. **Look for the "🤖 AI" button** in the top-right corner
2. **Click the button** to open the chat interface
3. **Ask the AI to perform actions**:

```
"Create a CPU usage panel"
"Show memory metrics"
"Analyze system health"
"Explain this query"
```

## 🎯 What the AI Can Do

### Panel Creation
- **CPU Usage**: `"Create a CPU usage panel"`
- **Memory Usage**: `"Show memory metrics"`
- **Disk I/O**: `"Create a disk panel"`
- **Custom Panels**: `"Create a panel showing network traffic"`

### Analysis
- **System Health**: `"Analyze system health"`
- **Performance**: `"What's wrong with my system?"`
- **Metrics**: `"Compare CPU and memory usage"`

### Query Explanation
- **PromQL**: `"Explain this query"`
- **Query Help**: `"How do I write a CPU query?"`

### Dashboard Management
- **Dashboard Info**: `"What dashboard am I on?"`
- **Panel Count**: `"How many panels do I have?"`

## 🧪 Testing Examples

### Test 1: Basic Panel Creation
```javascript
// Ask the AI to create a CPU panel
"Create a CPU usage panel"
```

**Expected Result**: AI creates a CPU panel with proper PromQL query and visualization

### Test 2: System Analysis
```javascript
// Ask the AI to analyze your system
"Analyze system health"
```

**Expected Result**: AI provides system analysis and recommendations

### Test 3: Query Explanation
```javascript
// Ask the AI to explain a query
"Explain this query"
```

**Expected Result**: AI explains the current PromQL query in detail

## 🔧 Troubleshooting

### Issue: "AI Agent Offline"
```bash
# Check if service is running
curl http://localhost:5001/health

# Start the service if needed
cd grafana-stack/ai-service
python app.py
```

### Issue: "Failed to create panel"
```bash
# Check Grafana API connection
python grafana-api-client.py

# Verify dashboard exists
curl http://localhost:3000/api/search
```

### Issue: "No context available"
- Click "Auto Capture" button in the AI chat
- Check browser console for errors
- Verify the script loaded properly

## 📊 Monitoring

### Check AI Service Health
```bash
curl http://localhost:5001/health
```

### Check Context Status
```bash
curl http://localhost:5001/ai/api/test-context
```

### Test Panel Creation
```bash
curl -X POST http://localhost:5001/ai/api/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Create a CPU panel", "context": {"dashboard_uid": "1"}}'
```

## 🎉 Success Indicators

✅ **Panel Creation**: AI creates panels and you see them in Grafana
✅ **Real Actions**: AI actually executes actions, not just provides guidance
✅ **Context Awareness**: AI knows your current dashboard and panels
✅ **No Manual Steps**: Everything works automatically

## 💡 Advanced Features

### OpenAI Integration
Set your OpenAI API key for enhanced AI responses:

```bash
export OPENAI_API_KEY="your-api-key"
```

### Custom Panel Creation
Ask for specific panels:

```
"Create a panel showing 95th percentile response time"
"Add a memory usage panel with alerts at 80%"
"Create a disk I/O panel with read/write metrics"
```

### System Analysis
Get intelligent insights:

```
"What's causing high CPU usage?"
"Are there any anomalies in my metrics?"
"How can I optimize my dashboard?"
```

## 🚀 Next Steps

1. **Test with real dashboards** - Create panels and ask the AI about them
2. **Try different queries** - Ask the AI to explain complex PromQL
3. **Test panel creation** - Ask the AI to create various types of panels
4. **Explore data sources** - Ask about available metrics and data sources

## 🎯 Key Benefits

- **No Manual Inspection**: Context is captured automatically
- **Real Actions**: AI actually creates panels and modifies dashboards
- **Intelligent Responses**: Uses proper AI model for understanding
- **Seamless Integration**: Works directly with Grafana API
- **Context Aware**: Knows your current dashboard state

The Full Integration AI Agent now provides true AI-powered observability with real action execution! 🎯 