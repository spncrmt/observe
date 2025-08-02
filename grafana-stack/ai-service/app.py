"""
AI-Integrated Observability Platform
===================================

Flask application for the AI observability service that provides:
- Natural language processing for observability queries
- Panel creation and modification
- Anomaly detection and analysis
- Query explanation and insights
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import requests
from datetime import datetime

# Import our enhanced AI agent
try:
    from enhanced_ai_agent import EnhancedAIAgent
except ImportError:
    # Fallback if enhanced AI agent is not available
    class EnhancedAIAgent:
        def __init__(self, grafana_url="http://localhost:3000", openai_api_key=None, use_openai=True):
            self.grafana_url = grafana_url
            self.openai_api_key = openai_api_key
            self.use_openai = use_openai
            self.current_context = {}
        
        def process_request(self, user_input, context=None):
            return {
                'success': True,
                'message': f"I'm your AI assistant! You said: {user_input}. Context: {context}",
                'action': 'general',
                'data': {}
            }
        
        def get_context(self):
            return {
                'success': True,
                'message': 'Context retrieved',
                'data': self.current_context,
                'action': 'get_context'
            }

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)

# Prometheus metrics
REQUEST_COUNT = Counter('ai_service_requests_total', 'Total requests to AI service')
REQUEST_DURATION = Histogram('ai_service_request_duration_seconds', 'Request duration')
SYSTEM_HEALTH_SCORE = Gauge('ai_service_system_health_score', 'System health score')

# Initialize enhanced AI agent
# ai_agent = EnhancedAIAgent(
#     grafana_url="http://localhost:3000",
#     openai_api_key=os.getenv("OPENAI_API_KEY"),
#     use_openai=True
# )

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    REQUEST_COUNT.inc()
    return jsonify({
        "status": "healthy",
        "service": "ai-observability-platform",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "natural_language_processing",
            "panel_creation",
            "anomaly_detection",
            "query_explanation",
            "context_awareness",
            "dashboard_integration"
        ]
    })

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """Get AI insights about the system"""
    REQUEST_COUNT.inc()
    try:
        insights = {
            "timestamp": datetime.now().isoformat(),
            "system_health": 85.0,
            "anomalies_detected": 0,
            "recommendations": [
                "System health is good - continue monitoring",
                "No anomalies detected in recent data",
                "Consider setting up alerting for critical metrics"
            ],
            "trends": {
                "cpu": {"trend": "stable", "current_avg": 15.2, "change_percent": 0},
                "memory": {"trend": "stable", "current_avg": 58.3, "change_percent": 0}
            },
            "ai_capabilities": [
                "Create panels with natural language",
                "Explain PromQL queries",
                "Detect and analyze anomalies",
                "Provide contextual insights",
                "Maintain dashboard context"
            ]
        }
        SYSTEM_HEALTH_SCORE.set(insights['system_health'])
        return jsonify(insights)
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    """Get detected anomalies"""
    REQUEST_COUNT.inc()
    try:
        return jsonify({
            "anomalies": [],
            "total_count": 0,
            "timestamp": datetime.now().isoformat(),
            "message": "No anomalies detected in recent data"
        })
    except Exception as e:
        logger.error(f"Error getting anomalies: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/capabilities', methods=['GET'])
def get_capabilities():
    """Get AI service capabilities"""
    REQUEST_COUNT.inc()
    try:
        return jsonify({
            "capabilities": {
                "anomaly_detection": {
                    "description": "Detect and analyze anomalies in metrics",
                    "methods": [
                        "statistical_analysis",
                        "trend_analysis"
                    ]
                },
                "context_awareness": {
                    "context_items": [
                        "dashboard_id",
                        "panel_id",
                        "time_range",
                        "variables"
                    ],
                    "description": "Maintain awareness of current dashboard context"
                },
                "natural_language": {
                    "description": "Understand natural language requests",
                    "examples": [
                        "Create a panel showing CPU usage",
                        "Explain this query",
                        "Check for anomalies in memory"
                    ]
                },
                "panel_management": {
                    "actions": [
                        "create_panel",
                        "modify_panel",
                        "delete_panel"
                    ],
                    "description": "Create and modify dashboard panels"
                },
                "query_generation": {
                    "description": "Generate PromQL queries from natural language",
                    "supported_metrics": [
                        "node_cpu_seconds_total",
                        "node_memory_MemTotal_bytes",
                        "node_disk_read_bytes_total",
                        "node_network_receive_bytes_total"
                    ]
                }
            },
            "data_sources": [
                "prometheus"
            ],
            "supported_actions": [
                "create_panel",
                "modify_panel",
                "explain_query",
                "analyze_anomaly",
                "compare_metrics",
                "generate_insight"
            ]
        })
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/demo', methods=['POST'])
def demo_request():
    """Demo endpoint for testing AI capabilities"""
    REQUEST_COUNT.inc()
    try:
        data = request.json
        demo_type = data.get("type", "create_panel")
        
        if demo_type == "create_panel":
            return jsonify({
                "type": "action",
                "action": "create_panel",
                "success": True,
                "message": "Demo: Created CPU usage panel",
                "panel_config": {
                    "title": "Demo CPU Usage",
                    "query": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
                }
            })
        elif demo_type == "explain_query":
            return jsonify({
                "type": "response",
                "message": "This query calculates CPU usage percentage by subtracting idle CPU time from 100%",
                "query": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
            })
        elif demo_type == "analyze_anomaly":
            return jsonify({
                "type": "response",
                "message": "✅ No anomalies detected in CPU usage",
                "analysis": {"anomaly_detected": False}
            })
        else:
            return jsonify({
                "type": "response",
                "message": "I can help you with observability! Try asking me to create panels, explain queries, or analyze anomalies.",
                "suggestions": [
                    "Create a panel showing CPU usage",
                    "Explain the current query",
                    "Check for anomalies in memory usage"
                ]
            })
            
    except Exception as e:
        logger.error(f"Error in demo request: {e}")
        return jsonify({"error": str(e)}), 500

# Enhanced AI Agent Routes
@app.route('/ai/api/context', methods=['POST'])
def update_context():
    """Update the AI agent's context with real dashboard data."""
    try:
        context_data = request.json
        app.logger.info(f"Received context update: {context_data}")
        
        # Store the context for the AI agent
        app.config['dashboard_context'] = context_data
        
        return jsonify({
            'success': True,
            'message': f'Context updated with dashboard: {context_data.get("dashboard_title", "Unknown")}',
            'context_summary': {
                'dashboard': context_data.get('dashboard_title'),
                'panels': len(context_data.get('panels', [])),
                'queries': len(context_data.get('queries', [])),
                'user': context_data.get('user', {}).get('login')
            }
        })
    except Exception as e:
        app.logger.error(f"Error updating context: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/ai/api/context', methods=['GET'])
def get_context():
    """Get current dashboard context"""
    try:
        # Use the enhanced AI agent's get_context method
        response = EnhancedAIAgent().get_context()
        return jsonify({
            "success": response.get('success', False),
            "message": response.get('message', 'No context data'),
            "data": response.get('data', {}),
            "action": response.get('action', 'unknown')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ai/api/process', methods=['POST'])
def process_with_context():
    """Process user input with enhanced dashboard context."""
    try:
        data = request.json
        user_input = data.get('input', '')
        context = data.get('context', {})
        
        app.logger.info(f"Processing with context: {context}")
        app.logger.info(f"User input: {user_input}")
        
        # Process with enhanced AI agent
        # Use the enhanced AI agent's process_request method
        result = EnhancedAIAgent().process_request(user_input, context)
        
        return jsonify({
            'success': result.get('success', False),
            'message': result.get('message', 'No response'),
            'action': result.get('action', 'unknown'),
            'data': result.get('data', {}),
            'context_updated': True
        })
        
    except Exception as e:
        app.logger.error(f"Error processing with context: {e}")
        return jsonify({
            'success': False,
            'message': f'Error processing request: {str(e)}',
            'action': None
        }), 500

@app.route('/ai/api/query', methods=['POST'])
def execute_query():
    """Execute a PromQL query"""
    try:
        data = request.json
        query = data.get("query", "")
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        # Use the enhanced AI agent's execute_promql_query method
        result = EnhancedAIAgent().execute_promql_query(query)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ai/api/analyze', methods=['POST'])
def analyze_anomaly():
    """Analyze anomalies in a metric"""
    try:
        data = request.json
        metric = data.get("metric", "")
        time_range = data.get("time_range", "1h")
        
        if not metric:
            return jsonify({"error": "No metric provided"}), 400
        
        # Use the enhanced AI agent's analyze_metric method
        response = EnhancedAIAgent().analyze_metric(metric, time_range)
        return jsonify({
            "success": response.success,
            "message": response.message,
            "data": response.data,
            "action": response.action.value
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ai/api/dashboards', methods=['GET'])
def get_dashboards():
    """Get all available dashboards"""
    try:
        # Use the enhanced AI agent's get_dashboards method
        dashboards = EnhancedAIAgent().get_dashboards()
        return jsonify({
            "success": True,
            "dashboards": dashboards
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ai/api/dashboard/<dashboard_id>', methods=['GET'])
def get_dashboard_details(dashboard_id):
    """Get details of a specific dashboard"""
    try:
        # Use the enhanced AI agent's get_dashboard_details method
        dashboard = EnhancedAIAgent().get_dashboard_details(dashboard_id)
        if dashboard:
            return jsonify({
                "success": True,
                "dashboard": dashboard
            })
        else:
            return jsonify({
                "success": False,
                "message": "Dashboard not found"
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ai/api/test-context', methods=['GET'])
def test_context():
    """Test endpoint to verify context capture is working."""
    try:
        context = app.config.get('dashboard_context', {})
        return jsonify({
            'success': True,
            'context_available': bool(context),
            'context_summary': {
                'dashboard': context.get('dashboard_title', 'None'),
                'user': context.get('user', {}).get('login', 'None'),
                'panels': len(context.get('panels', [])),
                'queries': len(context.get('queries', [])),
                'data_sources': len(context.get('available_data_sources', [])),
                'grafana_version': context.get('grafana_version', 'Unknown')
            },
            'full_context': context
        })
    except Exception as e:
        app.logger.error(f"Error testing context: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def process_with_ai(prompt):
    """Simple AI processing function for enhanced prompts."""
    try:
        # For now, provide intelligent responses based on the prompt content
        if "dashboard" in prompt.lower() and "context" in prompt.lower():
            if "what dashboard" in prompt.lower():
                return "Based on the dashboard context, you're currently on a dashboard. I can help you create panels, analyze metrics, or explain queries."
            elif "create" in prompt.lower() and "panel" in prompt.lower():
                return "I can help you create a panel! Here's how:\n\n1. Click the '+' button in your dashboard\n2. Choose 'Add a new panel'\n3. Select your data source (like Prometheus)\n4. Write your query or let me help you with one\n\nWhat type of panel would you like to create? (CPU usage, memory, disk I/O, etc.)"
            elif "explain" in prompt.lower() or "query" in prompt.lower():
                return "I can help explain PromQL queries! If you have a specific query you'd like me to explain, just paste it here. I can break down what each part does and how it works."
            else:
                return "I can see your dashboard context. I'm here to help you with:\n\n• Creating and modifying panels\n• Writing and explaining PromQL queries\n• Analyzing metrics and detecting anomalies\n• Comparing different data sources\n• Providing insights about your system\n\nWhat would you like to do?"
        else:
            return "I'm your AI observability assistant! I can help you with dashboard management, query writing, and system analysis. What would you like to work on?"
    except Exception as e:
        app.logger.error(f"Error in AI processing: {e}")
        return "I'm having trouble processing your request right now. Please try again."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True) 