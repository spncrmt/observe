# Real Context Capture Guide

## 🎯 Overview

This guide shows you how to use the **Real Context Capture** system that provides true dashboard context awareness to your AI agent in Grafana.

## 📋 What We Built

1. **Enhanced Context Capture Script** (`real-context-capture.js`)
   - Captures real dashboard data from `grafanaBootData`
   - Extracts user info, dashboard details, panels, queries
   - Sends context to AI service automatically

2. **Enhanced AI Service** (`ai-service/app.py`)
   - Receives and stores real dashboard context
   - Processes requests with full context awareness
   - Provides intelligent responses based on current state

3. **Test Script** (`test-context-capture.js`)
   - Verifies all components are working
   - Tests context capture, storage, and AI processing

## 🚀 How to Use

### Step 1: Test the System

1. **Open Grafana**: http://localhost:3000
2. **Open Developer Tools**: Press F12
3. **Go to Console tab**
4. **Copy and paste the test script**:

```javascript
// Copy the entire content from test-context-capture.js
```

5. **Run the test** and verify all components work

### Step 2: Load the Real AI Agent

1. **Copy the enhanced AI agent script**:

```javascript
// Copy the entire content from real-context-capture.js
```

2. **Paste into Grafana console** and press Enter

3. **Look for the "🤖 AI" button** in the top-right corner

### Step 3: Use the AI Agent

1. **Click the "🤖 AI" button** to open the chat interface
2. **Click "Capture Context"** to manually capture current dashboard state
3. **Click "Show Context"** to see what was captured
4. **Ask questions** like:
   - "What dashboard am I on?"
   - "How many panels do I have?"
   - "Create a panel showing CPU usage"
   - "Explain this query"

## 🔍 What Context is Captured

The system captures:

- **Dashboard Info**: Title, ID, UID
- **User Info**: Login, email, ID
- **Panels**: ID, title, type
- **Queries**: Text, data source
- **Time Range**: Current time selection
- **Data Sources**: Available data sources
- **Grafana Version**: Version info
- **URL**: Current page URL

## 🧪 Testing Examples

### Test 1: Basic Context Capture
```javascript
// Test basic context capture
const context = {
  dashboard_title: "System Monitoring",
  user: { login: "admin" },
  panels: [{ id: "1", title: "CPU Usage" }],
  queries: [{ text: "up", data_source: "Prometheus" }]
};
```

### Test 2: AI Processing
```javascript
// Test AI with context
fetch('http://localhost:5001/ai/api/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    input: "What dashboard am I on?",
    context: context
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### Test 3: Context Verification
```javascript
// Verify context storage
fetch('http://localhost:5001/ai/api/test-context')
.then(r => r.json())
.then(data => console.log(data));
```

## 🎯 Real-World Usage

### Scenario 1: Dashboard Analysis
1. Open a dashboard with panels
2. Load the AI agent script
3. Ask: "What panels do I have and what do they show?"
4. The AI will analyze your actual dashboard context

### Scenario 2: Panel Creation
1. Open an empty dashboard
2. Load the AI agent script
3. Ask: "Create a panel showing CPU usage"
4. The AI will provide specific guidance based on your data sources

### Scenario 3: Query Explanation
1. Open a dashboard with PromQL queries
2. Load the AI agent script
3. Ask: "Explain this query"
4. The AI will explain the specific query in your panel

## 🔧 Troubleshooting

### Issue: "AI Agent Offline"
- Check if the AI service is running: `curl http://localhost:5001/health`
- Restart the service if needed

### Issue: "No Context Available"
- Click "Capture Context" button
- Check browser console for errors
- Verify the script loaded properly

### Issue: "Error connecting to AI agent"
- Check if port 5001 is accessible
- Verify CORS is enabled
- Check browser network tab for errors

## 📊 Monitoring

### Check AI Service Health
```bash
curl http://localhost:5001/health
```

### Check Context Status
```bash
curl http://localhost:5001/ai/api/test-context
```

### Check AI Capabilities
```bash
curl http://localhost:5001/api/capabilities
```

## 🎉 Success Indicators

✅ **Context Capture Working**: You see dashboard info in "Show Context"
✅ **AI Processing Working**: AI responds with relevant information
✅ **Real-time Updates**: Context updates when you change dashboards
✅ **Action Recognition**: AI recognizes create/analyze/explain requests

## 🚀 Next Steps

1. **Test with real dashboards** - Create panels and ask the AI about them
2. **Try different queries** - Ask the AI to explain PromQL queries
3. **Test panel creation** - Ask the AI to help create new panels
4. **Explore data sources** - Ask about available metrics and data sources

## 💡 Tips

- **Refresh context** when switching dashboards
- **Use specific questions** for better AI responses
- **Check the context summary** to see what the AI knows
- **Test with different panel types** to see how context varies

The real context capture system now provides true dashboard awareness to your AI agent! 🎯 