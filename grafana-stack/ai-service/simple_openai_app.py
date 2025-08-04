from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key-here')
GRAFANA_URL = os.environ.get('GRAFANA_URL', 'https://awtospx.com')
GRAFANA_USER = os.environ.get('GRAFANA_USER', 'admin')
GRAFANA_PASSWORD = os.environ.get('GRAFANA_PASSWORD', 'admin')

def simulate_openai_response(user_message):
    """Simulate OpenAI responses for testing"""
    responses = {
        "create": [
            "I'll create a CPU usage dashboard for you! Here's what I'm building:\n\n**Dashboard: System Performance Monitor**\n\n📊 **Panels:**\n- CPU Usage (Graph)\n- Memory Utilization (Graph)\n- Network Traffic (Graph)\n- System Load (Stat)\n\n🔗 **Dashboard URL:** [View Dashboard](https://awtospx.com)\n\n**PromQL Queries Used:**\n- `100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)`\n- `node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes`\n\nWould you like me to create this dashboard now?",
            "I'll help you create a comprehensive monitoring dashboard! Here's my plan:\n\n**Dashboard: Application Performance**\n\n📊 **Panels:**\n- Response Time (Graph)\n- Error Rate (Graph)\n- Throughput (Graph)\n- Database Connections (Stat)\n\n🔗 **Dashboard URL:** [View Dashboard](https://awtospx.com)\n\n**PromQL Queries:**\n- `rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])`\n- `rate(http_requests_total{status=~\"5..\"}[5m])`\n\nThis will give you real-time insights into your application performance!",
        ],
        "analyze": [
            "Based on your request, here's my analysis:\n\n🔍 **Key Metrics to Monitor:**\n- CPU usage should stay below 80%\n- Memory utilization under 85%\n- Disk I/O latency under 100ms\n- Network packet loss under 1%\n\n📈 **Recommended Alerts:**\n- High CPU usage (>80% for 5 minutes)\n- Memory pressure (>85% for 2 minutes)\n- Disk space low (<10% remaining)\n\n🎯 **Action Items:**\n1. Set up the monitoring dashboard\n2. Configure alerting rules\n3. Review historical trends\n\nWould you like me to create these alerts for you?",
            "Here's my performance analysis:\n\n📊 **Current System Health:**\n- CPU: Normal (45% average)\n- Memory: Good (60% used)\n- Disk: Healthy (25% used)\n- Network: Stable (low latency)\n\n⚠️ **Potential Issues:**\n- Memory usage trending upward\n- Consider scaling if trend continues\n\n✅ **Recommendations:**\n1. Monitor memory usage closely\n2. Set up alerts for >80% memory\n3. Consider memory optimization\n\nWould you like me to create a memory-focused dashboard?",
        ],
        "query": [
            "Here are some useful PromQL queries for your monitoring:\n\n**CPU Usage:**\n```\n100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)\n```\n\n**Memory Usage:**\n```\n(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100\n```\n\n**Disk Usage:**\n```\n100 - (node_filesystem_avail_bytes{mountpoint=\"/\"} / node_filesystem_size_bytes{mountpoint=\"/\"} * 100)\n```\n\n**Network Traffic:**\n```\nrate(node_network_receive_bytes_total[5m])\n```\n\nWould you like me to create a dashboard with these queries?",
            "Here are some advanced PromQL queries for deeper monitoring:\n\n**Error Rate:**\n```\nrate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100\n```\n\n**Response Time 95th Percentile:**\n```\nhistogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))\n```\n\n**Database Connections:**\n```\npg_stat_activity_count\n```\n\n**Custom Business Metric:**\n```\nrate(orders_processed_total[5m])\n```\n\nThese queries will help you monitor application performance and business metrics!",
        ]
    }
    
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['create', 'build', 'make', 'dashboard']):
        return responses['create'][0]
    elif any(word in message_lower for word in ['analyze', 'analysis', 'performance', 'health']):
        return responses['analyze'][0]
    elif any(word in message_lower for word in ['query', 'promql', 'metric']):
        return responses['query'][0]
    else:
        return "I'm here to help you with Grafana monitoring! I can:\n\n✅ **Create dashboards** with custom panels\n✅ **Write PromQL queries** for metrics\n✅ **Analyze system performance**\n✅ **Set up alerts** and monitoring\n\nTry asking me to:\n- \"Create a CPU usage dashboard\"\n- \"Analyze system performance\"\n- \"Write a PromQL query for memory usage\"\n- \"Build a comprehensive monitoring dashboard\""

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Observability Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #1e1e1e; color: white; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .chat-container { background: #2d2d2d; border-radius: 10px; padding: 20px; }
            .messages { height: 400px; overflow-y: auto; margin-bottom: 20px; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user { background: #0066cc; margin-left: 20%; }
            .ai { background: #2d2d2d; border: 1px solid #404040; margin-right: 20%; }
            .input-container { display: flex; gap: 10px; }
            input[type="text"] { flex: 1; padding: 10px; border: 1px solid #404040; border-radius: 5px; background: #1e1e1e; color: white; }
            button { padding: 10px 20px; background: #0066cc; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .dashboard-link { color: #00cc66; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Observability Assistant</h1>
                <p>Ask me to create dashboards, analyze metrics, or write PromQL queries!</p>
            </div>
            <div class="chat-container">
                <div id="messages" class="messages"></div>
                <div class="input-container">
                    <input type="text" id="userInput" placeholder="Ask me to create a CPU dashboard..." />
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>
        <script>
            let messages = [];
            
            function addMessage(content, isUser = false) {
                const messagesDiv = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'ai'}`;
                messageDiv.innerHTML = content;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            async function sendMessage() {
                const input = document.getElementById('userInput');
                const message = input.value.trim();
                if (!message) return;
                
                addMessage(message, true);
                input.value = '';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    });
                    const data = await response.json();
                    addMessage(data.response);
                } catch (error) {
                    addMessage('Error: ' + error.message);
                }
            }
            
            document.getElementById('userInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
            
            // Add welcome message
            addMessage('Hello! I can help you create dashboards, analyze metrics, and write PromQL queries. Try asking me to "create a CPU usage dashboard" or "analyze system performance"!');
        </script>
    </body>
    </html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Get AI response
        ai_response = simulate_openai_response(user_message)
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'response': f'Error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'AI Observability Platform (Simulated)',
        'timestamp': datetime.now().isoformat(),
        'features': [
            'Dashboard Creation (Simulated)',
            'PromQL Query Generation',
            'Metric Analysis',
            'Grafana Integration'
        ],
        'note': 'This is a simulated version. Set OPENAI_API_KEY for real AI responses.'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 