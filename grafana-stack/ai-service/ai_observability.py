"""
AI-Integrated Observability Platform
===================================

This module provides an AI assistant that can:
- Understand Grafana context (dashboards, panels, time ranges)
- Execute actions (create/modify panels, queries)
- Provide intelligent insights and explanations
- Maintain contextual awareness
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActionType(Enum):
    CREATE_PANEL = "create_panel"
    MODIFY_PANEL = "modify_panel"
    DELETE_PANEL = "delete_panel"
    EXPLAIN_QUERY = "explain_query"
    ANALYZE_ANOMALY = "analyze_anomaly"
    COMPARE_METRICS = "compare_metrics"
    GENERATE_INSIGHT = "generate_insight"

@dataclass
class GrafanaContext:
    """Represents the current Grafana context"""
    dashboard_id: Optional[str] = None
    panel_id: Optional[str] = None
    time_range: Optional[Dict] = None
    variables: Optional[Dict] = None
    data_sources: Optional[List[str]] = None
    selected_metrics: Optional[List[str]] = None

@dataclass
class AIAction:
    """Represents an action the AI can perform"""
    action_type: ActionType
    parameters: Dict[str, Any]
    description: str
    confidence: float

class AIObservabilityService:
    """Main AI service for observability platform"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.grafana_url = "http://grafana:3000"
        self.prometheus_url = "http://prometheus:9090"
        
        if self.api_key:
            openai.api_key = self.api_key
        
        # Context management
        self.current_context = GrafanaContext()
        self.action_history = []
        
        # Available data sources and their schemas
        self.data_source_schemas = {
            "prometheus": {
                "metrics": [
                    "node_cpu_seconds_total",
                    "node_memory_MemTotal_bytes", 
                    "node_memory_MemAvailable_bytes",
                    "node_disk_read_bytes_total",
                    "node_disk_written_bytes_total",
                    "node_network_receive_bytes_total",
                    "node_network_transmit_bytes_total",
                    "node_load1", "node_load5", "node_load15"
                ],
                "labels": ["instance", "job", "mode", "device", "interface"]
            }
        }
    
    def update_context(self, context_data: Dict[str, Any]) -> None:
        """Update the current Grafana context"""
        if "dashboard_id" in context_data:
            self.current_context.dashboard_id = context_data["dashboard_id"]
        if "panel_id" in context_data:
            self.current_context.panel_id = context_data["panel_id"]
        if "time_range" in context_data:
            self.current_context.time_range = context_data["time_range"]
        if "variables" in context_data:
            self.current_context.variables = context_data["variables"]
        if "data_sources" in context_data:
            self.current_context.data_sources = context_data["data_sources"]
        if "selected_metrics" in context_data:
            self.current_context.selected_metrics = context_data["selected_metrics"]
        
        logger.info(f"Updated context: {self.current_context}")
    
    def get_grafana_dashboards(self) -> List[Dict]:
        """Get all available dashboards"""
        try:
            response = requests.get(f"{self.grafana_url}/api/search", 
                                 auth=("admin", "admin"))
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching dashboards: {e}")
            return []
    
    def get_dashboard_details(self, dashboard_id: str) -> Optional[Dict]:
        """Get detailed dashboard information"""
        try:
            response = requests.get(f"{self.grafana_url}/api/dashboards/uid/{dashboard_id}",
                                 auth=("admin", "admin"))
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching dashboard details: {e}")
            return None
    
    def create_panel(self, panel_config: Dict) -> Optional[Dict]:
        """Create a new panel in the current dashboard"""
        if not self.current_context.dashboard_id:
            return {"error": "No dashboard context available"}
        
        try:
            dashboard = self.get_dashboard_details(self.current_context.dashboard_id)
            if not dashboard:
                return {"error": "Dashboard not found"}
            
            # Add the new panel
            dashboard["dashboard"]["panels"].append(panel_config)
            
            # Update the dashboard
            response = requests.post(f"{self.grafana_url}/api/dashboards/db",
                                  json=dashboard,
                                  auth=("admin", "admin"))
            
            if response.status_code == 200:
                return {"success": True, "panel_id": panel_config.get("id")}
            else:
                return {"error": f"Failed to create panel: {response.text}"}
                
        except Exception as e:
            logger.error(f"Error creating panel: {e}")
            return {"error": str(e)}
    
    def modify_panel(self, panel_id: str, modifications: Dict) -> Optional[Dict]:
        """Modify an existing panel"""
        if not self.current_context.dashboard_id:
            return {"error": "No dashboard context available"}
        
        try:
            dashboard = self.get_dashboard_details(self.current_context.dashboard_id)
            if not dashboard:
                return {"error": "Dashboard not found"}
            
            # Find and modify the panel
            for panel in dashboard["dashboard"]["panels"]:
                if panel["id"] == int(panel_id):
                    panel.update(modifications)
                    break
            
            # Update the dashboard
            response = requests.post(f"{self.grafana_url}/api/dashboards/db",
                                  json=dashboard,
                                  auth=("admin", "admin"))
            
            if response.status_code == 200:
                return {"success": True}
            else:
                return {"error": f"Failed to modify panel: {response.text}"}
                
        except Exception as e:
            logger.error(f"Error modifying panel: {e}")
            return {"error": str(e)}
    
    def execute_promql_query(self, query: str) -> Optional[Dict]:
        """Execute a PromQL query and return results"""
        try:
            response = requests.get(f"{self.prometheus_url}/api/v1/query",
                                 params={"query": query})
            return response.json()
        except Exception as e:
            logger.error(f"Error executing PromQL query: {e}")
            return None
    
    def analyze_anomaly(self, metric: str, time_range: str = "1h") -> Dict:
        """Analyze anomalies in a specific metric"""
        try:
            # Get current value
            current_query = f"{metric}"
            current_result = self.execute_promql_query(current_query)
            
            # Get historical data for comparison
            historical_query = f"{metric}[{time_range}]"
            historical_result = self.execute_promql_query(historical_query)
            
            # Simple anomaly detection (can be enhanced)
            if current_result and historical_result:
                current_value = float(current_result["data"]["result"][0]["value"][1])
                historical_values = [float(r["value"][1]) for r in historical_result["data"]["result"]]
                
                if historical_values:
                    avg_value = sum(historical_values) / len(historical_values)
                    max_value = max(historical_values)
                    
                    if current_value > avg_value * 1.5:  # 50% above average
                        return {
                            "anomaly_detected": True,
                            "current_value": current_value,
                            "average_value": avg_value,
                            "severity": "high" if current_value > max_value else "medium",
                            "explanation": f"Current value ({current_value:.2f}) is significantly above average ({avg_value:.2f})"
                        }
            
            return {"anomaly_detected": False}
            
        except Exception as e:
            logger.error(f"Error analyzing anomaly: {e}")
            return {"error": str(e)}
    
    def generate_promql_query(self, user_request: str) -> Optional[str]:
        """Generate PromQL query from natural language"""
        try:
            prompt = f"""
            Generate a PromQL query based on this request: "{user_request}"
            
            Available metrics: {', '.join(self.data_source_schemas['prometheus']['metrics'])}
            Available labels: {', '.join(self.data_source_schemas['prometheus']['labels'])}
            
            Return only the PromQL query, nothing else.
            """
            
            if not self.api_key:
                # Fallback to simple pattern matching
                return self._simple_query_generation(user_request)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating PromQL query: {e}")
            return self._simple_query_generation(user_request)
    
    def _simple_query_generation(self, user_request: str) -> str:
        """Simple pattern-based query generation"""
        request_lower = user_request.lower()
        
        if "cpu" in request_lower and "usage" in request_lower:
            return '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
        elif "memory" in request_lower and "usage" in request_lower:
            return '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100'
        elif "disk" in request_lower and "io" in request_lower:
            return 'rate(node_disk_read_bytes_total[5m]) + rate(node_disk_written_bytes_total[5m])'
        elif "network" in request_lower:
            return 'rate(node_network_receive_bytes_total[5m]) + rate(node_network_transmit_bytes_total[5m])'
        else:
            return 'node_cpu_seconds_total'  # Default fallback
    
    def process_user_request(self, user_input: str, context: Dict = None) -> Dict:
        """Process a user request and return appropriate actions/responses"""
        if context:
            self.update_context(context)
        
        # Analyze the user input to determine intent
        intent = self._analyze_intent(user_input)
        
        if intent["action_type"] == ActionType.CREATE_PANEL:
            return self._handle_create_panel(user_input, intent)
        elif intent["action_type"] == ActionType.MODIFY_PANEL:
            return self._handle_modify_panel(user_input, intent)
        elif intent["action_type"] == ActionType.EXPLAIN_QUERY:
            return self._handle_explain_query(user_input, intent)
        elif intent["action_type"] == ActionType.ANALYZE_ANOMALY:
            return self._handle_analyze_anomaly(user_input, intent)
        elif intent["action_type"] == ActionType.COMPARE_METRICS:
            return self._handle_compare_metrics(user_input, intent)
        else:
            return self._handle_general_question(user_input, intent)
    
    def _analyze_intent(self, user_input: str) -> Dict:
        """Analyze user input to determine intent and action type"""
        input_lower = user_input.lower()
        
        # Pattern matching for different intents
        if any(word in input_lower for word in ["create", "add", "new", "panel"]):
            return {
                "action_type": ActionType.CREATE_PANEL,
                "confidence": 0.9,
                "parameters": {"query": user_input}
            }
        elif any(word in input_lower for word in ["modify", "change", "edit", "update"]):
            return {
                "action_type": ActionType.MODIFY_PANEL,
                "confidence": 0.8,
                "parameters": {"query": user_input}
            }
        elif any(word in input_lower for word in ["explain", "what does", "how does"]):
            return {
                "action_type": ActionType.EXPLAIN_QUERY,
                "confidence": 0.9,
                "parameters": {"query": user_input}
            }
        elif any(word in input_lower for word in ["anomaly", "spike", "problem", "issue"]):
            return {
                "action_type": ActionType.ANALYZE_ANOMALY,
                "confidence": 0.8,
                "parameters": {"query": user_input}
            }
        elif any(word in input_lower for word in ["compare", "difference", "vs"]):
            return {
                "action_type": ActionType.COMPARE_METRICS,
                "confidence": 0.7,
                "parameters": {"query": user_input}
            }
        else:
            return {
                "action_type": ActionType.GENERATE_INSIGHT,
                "confidence": 0.5,
                "parameters": {"query": user_input}
            }
    
    def _handle_create_panel(self, user_input: str, intent: Dict) -> Dict:
        """Handle panel creation requests"""
        try:
            # Generate PromQL query
            promql_query = self.generate_promql_query(user_input)
            
            # Create panel configuration
            panel_config = {
                "id": len(self.action_history) + 1,  # Simple ID generation
                "title": f"AI Generated Panel - {datetime.now().strftime('%H:%M')}",
                "type": "timeseries",
                "targets": [{
                    "expr": promql_query,
                    "legendFormat": "{{instance}}",
                    "refId": "A"
                }],
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "palette-classic"},
                        "custom": {
                            "drawStyle": "line",
                            "lineInterpolation": "linear",
                            "fillOpacity": 10
                        },
                        "unit": "short"
                    }
                },
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
            }
            
            # Create the panel
            result = self.create_panel(panel_config)
            
            if result.get("success"):
                return {
                    "type": "action",
                    "action": "create_panel",
                    "success": True,
                    "message": f"Created new panel with query: {promql_query}",
                    "panel_config": panel_config
                }
            else:
                return {
                    "type": "error",
                    "message": f"Failed to create panel: {result.get('error')}"
                }
                
        except Exception as e:
            logger.error(f"Error handling create panel: {e}")
            return {"type": "error", "message": str(e)}
    
    def _handle_modify_panel(self, user_input: str, intent: Dict) -> Dict:
        """Handle panel modification requests"""
        return {
            "type": "response",
            "message": "Panel modification feature coming soon!",
            "suggestions": ["Try creating a new panel instead"]
        }
    
    def _handle_explain_query(self, user_input: str, intent: Dict) -> Dict:
        """Handle query explanation requests"""
        try:
            # Extract query from user input (simple approach)
            if "query" in user_input.lower():
                # Extract the actual query part
                query_start = user_input.find("query") + 5
                query = user_input[query_start:].strip()
            else:
                query = self.generate_promql_query(user_input)
            
            # Execute the query to get sample data
            result = self.execute_promql_query(query)
            
            explanation = f"""
            **Query Explanation:**
            - **Query**: `{query}`
            - **Type**: PromQL (Prometheus Query Language)
            - **Purpose**: {self._explain_query_purpose(query)}
            
            **Sample Data:**
            {self._format_query_result(result)}
            """
            
            return {
                "type": "response",
                "message": explanation,
                "query": query,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error explaining query: {e}")
            return {"type": "error", "message": str(e)}
    
    def _handle_analyze_anomaly(self, user_input: str, intent: Dict) -> Dict:
        """Handle anomaly analysis requests"""
        try:
            # Extract metric from user input
            metric = self._extract_metric_from_input(user_input)
            if not metric:
                metric = "node_cpu_seconds_total"  # Default
            
            # Analyze anomaly
            analysis = self.analyze_anomaly(metric)
            
            if analysis.get("anomaly_detected"):
                return {
                    "type": "anomaly",
                    "message": f"🚨 Anomaly detected in {metric}!",
                    "analysis": analysis,
                    "recommendations": [
                        "Check system logs for errors",
                        "Monitor resource usage",
                        "Review recent deployments"
                    ]
                }
            else:
                return {
                    "type": "response",
                    "message": f"✅ No anomalies detected in {metric}",
                    "analysis": analysis
                }
                
        except Exception as e:
            logger.error(f"Error analyzing anomaly: {e}")
            return {"type": "error", "message": str(e)}
    
    def _handle_compare_metrics(self, user_input: str, intent: Dict) -> Dict:
        """Handle metric comparison requests"""
        return {
            "type": "response",
            "message": "Metric comparison feature coming soon!",
            "suggestions": ["Try asking about specific metrics individually"]
        }
    
    def _handle_general_question(self, user_input: str, intent: Dict) -> Dict:
        """Handle general questions and provide insights"""
        try:
            if not self.api_key:
                return {
                    "type": "response",
                    "message": "I can help you with observability! Try asking me to create panels, explain queries, or analyze anomalies.",
                    "suggestions": [
                        "Create a panel showing CPU usage",
                        "Explain the current query",
                        "Check for anomalies in memory usage"
                    ]
                }
            
            # Use OpenAI for general questions
            prompt = f"""
            You are an AI observability assistant. The user asks: "{user_input}"
            
            Current context:
            - Dashboard ID: {self.current_context.dashboard_id}
            - Available metrics: {', '.join(self.data_source_schemas['prometheus']['metrics'])}
            
            Provide a helpful response about observability and monitoring.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            return {
                "type": "response",
                "message": response.choices[0].message.content,
                "suggestions": [
                    "Create a new panel",
                    "Analyze current metrics",
                    "Explain a query"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error handling general question: {e}")
            return {
                "type": "response",
                "message": "I'm here to help with your observability needs! What would you like to know?",
                "suggestions": ["Create panels", "Analyze metrics", "Explain queries"]
            }
    
    def _explain_query_purpose(self, query: str) -> str:
        """Explain what a PromQL query does"""
        if "cpu" in query.lower():
            return "Measures CPU utilization"
        elif "memory" in query.lower():
            return "Measures memory usage"
        elif "disk" in query.lower():
            return "Measures disk I/O activity"
        elif "network" in query.lower():
            return "Measures network traffic"
        else:
            return "Retrieves metric data"
    
    def _format_query_result(self, result: Dict) -> str:
        """Format query result for display"""
        if not result or "data" not in result:
            return "No data available"
        
        try:
            data = result["data"]["result"]
            if not data:
                return "No data points found"
            
            # Show first few results
            formatted = []
            for i, item in enumerate(data[:3]):
                metric = item.get("metric", {})
                value = item.get("value", [])
                formatted.append(f"- {metric.get('instance', 'unknown')}: {value[1] if len(value) > 1 else 'N/A'}")
            
            return "\n".join(formatted)
        except Exception:
            return "Data available (formatting error)"
    
    def _extract_metric_from_input(self, user_input: str) -> Optional[str]:
        """Extract metric name from user input"""
        input_lower = user_input.lower()
        
        if "cpu" in input_lower:
            return "node_cpu_seconds_total"
        elif "memory" in input_lower:
            return "node_memory_MemTotal_bytes"
        elif "disk" in input_lower:
            return "node_disk_read_bytes_total"
        elif "network" in input_lower:
            return "node_network_receive_bytes_total"
        
        return None

# Flask app for the AI service
app = Flask(__name__)
CORS(app)

# Initialize the AI service
ai_service = AIObservabilityService()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ai-observability"})

@app.route('/api/context', methods=['POST'])
def update_context():
    """Update the current Grafana context"""
    try:
        context_data = request.json
        ai_service.update_context(context_data)
        return jsonify({"success": True, "message": "Context updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_request():
    """Process a user request"""
    try:
        data = request.json
        user_input = data.get("input", "")
        context = data.get("context", {})
        
        result = ai_service.process_user_request(user_input, context)
        return jsonify(result)
    except Exception as e:
        return jsonify({"type": "error", "message": str(e)}), 500

@app.route('/api/query', methods=['POST'])
def execute_query():
    """Execute a PromQL query"""
    try:
        data = request.json
        query = data.get("query", "")
        
        result = ai_service.execute_promql_query(query)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_anomaly():
    """Analyze anomalies in a metric"""
    try:
        data = request.json
        metric = data.get("metric", "")
        time_range = data.get("time_range", "1h")
        
        result = ai_service.analyze_anomaly(metric, time_range)
        return jsonify({"success": True, "analysis": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 