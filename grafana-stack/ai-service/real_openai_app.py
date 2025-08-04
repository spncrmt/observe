from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import openai
import json
import os
import requests
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key-here')
openai.api_key = OPENAI_API_KEY

# Grafana Configuration
GRAFANA_URL = os.environ.get('GRAFANA_URL', 'https://awtospx.com')
GRAFANA_USER = os.environ.get('GRAFANA_USER', 'admin')
GRAFANA_PASSWORD = os.environ.get('GRAFANA_PASSWORD', 'admin')

class GrafanaManager:
    def __init__(self, url, user, password):
        self.url = url.rstrip('/')
        self.auth = (user, password)
        self.headers = {'Content-Type': 'application/json'}
    
    def create_dashboard(self, title, panels):
        """Create a new dashboard with specified panels"""
        dashboard = {
            "dashboard": {
                "title": title,
                "panels": panels,
                "time": {
                    "from": "now-1h",
                    "to": "now"
                },
                "refresh": "5s"
            },
            "folderId": 0,
            "overwrite": False
        }
        
        response = requests.post(
            f"{self.url}/api/dashboards/db",
            json=dashboard,
            auth=self.auth,
            headers=self.headers
        )
        return response.json()
    
    def get_dashboards(self):
        """Get all dashboards"""
        response = requests.get(
            f"{self.url}/api/search",
            auth=self.auth
        )
        return response.json()

def create_panel_promql(metric, title, panel_type="graph"):
    """Create a panel with PromQL query"""
    panel = {
        "id": None,  # Will be auto-assigned
        "title": title,
        "type": panel_type,
        "targets": [
            {
                "expr": metric,
                "refId": "A"
            }
        ],
        "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 0
        }
    }
    return panel

def analyze_with_openai(user_message, context=""):
    """Analyze user request with real OpenAI"""
    system_prompt = f"""
You are an AI assistant for Grafana observability. You can:
1. Create dashboards and panels
2. Write PromQL queries
3. Analyze metrics and data
4. Provide insights about system performance

Current context: {context}

When asked to create dashboards or panels, respond with JSON in this format:
{{
    "action": "create_dashboard",
    "title": "Dashboard Title",
    "panels": [
        {{
            "title": "Panel Title",
            "type": "graph",
            "query": "promql_query_here",
            "description": "Panel description"
        }}
    ]
}}

When asked to analyze data, provide insights and recommendations.
Be helpful, concise, and actionable.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to OpenAI: {str(e)}"

def parse_ai_response(response):
    """Parse AI response and extract actions"""
    try:
        # Try to parse as JSON for dashboard creation
        if '"action":' in response and '"create_dashboard"' in response:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        
        # Return as regular response
        return {"type": "message", "content": response}
    except:
        return {"type": "message", "content": response}

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real AI Observability Assistant</title>
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
                <h1>🤖 Real AI Observability Assistant</h1>
                <p>Powered by OpenAI GPT-4 - Ask me anything about monitoring!</p>
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
            addMessage('Hello! I\'m powered by OpenAI GPT-4 and can help you create dashboards, analyze metrics, and write PromQL queries. Try asking me to "create a CPU usage dashboard" or "analyze system performance"!');
        </script>
    </body>
    </html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Get context from Grafana
        context = ""
        try:
            grafana = GrafanaManager(GRAFANA_URL, GRAFANA_USER, GRAFANA_PASSWORD)
            dashboards = grafana.get_dashboards()
            context += f"Available dashboards: {len(dashboards)} dashboards found. "
        except:
            context += "Grafana connection issue. "
        
        # Get real AI response
        ai_response = analyze_with_openai(user_message, context)
        parsed_response = parse_ai_response(ai_response)
        
        # Handle dashboard creation
        if parsed_response.get('action') == 'create_dashboard':
            try:
                panels = []
                for i, panel_data in enumerate(parsed_response.get('panels', [])):
                    panel = create_panel_promql(
                        panel_data.get('query', 'up'),
                        panel_data.get('title', f'Panel {i+1}'),
                        panel_data.get('type', 'graph')
                    )
                    panel['gridPos']['x'] = (i % 2) * 12
                    panel['gridPos']['y'] = (i // 2) * 8
                    panels.append(panel)
                
                result = grafana.create_dashboard(
                    parsed_response.get('title', 'AI Created Dashboard'),
                    panels
                )
                
                if 'url' in result:
                    dashboard_url = f"{GRAFANA_URL}{result['url']}"
                    response_text = f"✅ Dashboard created successfully!\n\n**{parsed_response.get('title')}**\n\n"
                    response_text += f"📊 **Panels created:** {len(panels)}\n"
                    response_text += f"🔗 **View dashboard:** [Open Dashboard]({dashboard_url})\n\n"
                    response_text += "**AI Analysis:**\n" + ai_response
                else:
                    response_text = f"❌ Error creating dashboard: {result}\n\n**AI Analysis:**\n" + ai_response
                
            except Exception as e:
                response_text = f"❌ Error creating dashboard: {str(e)}\n\n**AI Analysis:**\n" + ai_response
        else:
            response_text = ai_response
        
        return jsonify({
            'response': response_text,
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
        'service': 'Real OpenAI AI Observability Platform',
        'timestamp': datetime.now().isoformat(),
        'features': [
            'OpenAI GPT-4 Integration',
            'Real Dashboard Creation',
            'PromQL Query Generation',
            'Intelligent Analysis',
            'Grafana Integration'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 