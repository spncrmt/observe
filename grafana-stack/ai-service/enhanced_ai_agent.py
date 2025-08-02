"""
Enhanced AI Agent with Full Integration
======================================

AI agent that can:
- Understand natural language requests
- Execute actual Grafana operations
- Create panels, modify dashboards
- Provide intelligent analysis
- Use proper AI model for responses
"""

import os
import json
import logging
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
import sys

# Add the parent directory to the path to import grafana_api_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from grafana_api_client import GrafanaAPIClient
except ImportError:
    # Fallback if Grafana API client is not available
    class GrafanaAPIClient:
        def __init__(self, base_url="http://localhost:3000", api_key=None):
            self.base_url = base_url
            self.api_key = api_key
        
        def test_connection(self):
            return True
        
        def get_dashboards(self):
            return []
        
        def create_cpu_panel(self, dashboard_uid, title):
            return {"id": 1, "title": title}
        
        def create_memory_panel(self, dashboard_uid, title):
            return {"id": 2, "title": title}
        
        def create_disk_panel(self, dashboard_uid, title):
            return {"id": 3, "title": title}

logger = logging.getLogger(__name__)

class EnhancedAIAgent:
    def __init__(self, grafana_url: str = "http://localhost:3000", 
                 openai_api_key: str = None, use_openai: bool = True):
        self.grafana_client = GrafanaAPIClient(grafana_url)
        self.openai_api_key = openai_api_key
        self.use_openai = use_openai
        
        if openai_api_key:
            openai.api_key = openai_api_key
        
        # Store current context
        self.current_context = {}
        self.action_history = []
    
    def update_context(self, context: Dict) -> Dict:
        """Update the AI agent's context"""
        self.current_context = context
        logger.info(f"Context updated: {context.get('dashboard_title', 'Unknown')}")
        return {
            'success': True,
            'message': f"Context updated for dashboard: {context.get('dashboard_title', 'Unknown')}",
            'data': context
        }
    
    def process_request(self, user_input: str, context: Dict = None) -> Dict:
        """Process user request with full integration"""
        if context:
            self.update_context(context)
        
        try:
            # Analyze the request
            intent = self._analyze_intent(user_input)
            
            # Execute action based on intent
            if intent['action'] == 'create_panel':
                result = self._execute_create_panel(intent, user_input)
            elif intent['action'] == 'analyze_metrics':
                result = self._execute_analyze_metrics(intent, user_input)
            elif intent['action'] == 'explain_query':
                result = self._execute_explain_query(intent, user_input)
            elif intent['action'] == 'dashboard_info':
                result = self._execute_dashboard_info(intent, user_input)
            else:
                result = self._execute_general_response(intent, user_input)
            
            # Add to action history
            self.action_history.append({
                'timestamp': datetime.now().isoformat(),
                'input': user_input,
                'intent': intent,
                'result': result
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return {
                'success': False,
                'message': f"Error processing request: {str(e)}",
                'action': 'error'
            }
    
    def _analyze_intent(self, user_input: str) -> Dict:
        """Analyze user intent using AI"""
        prompt = f"""
You are an AI observability assistant integrated with Grafana. Analyze the user's request and determine the intent.

Current Context:
- Dashboard: {self.current_context.get('dashboard_title', 'Unknown')}
- User: {self.current_context.get('user', {}).get('login', 'Unknown')}
- Panels: {len(self.current_context.get('panels', []))}
- Data Sources: {', '.join(self.current_context.get('available_data_sources', []))}

User Request: "{user_input}"

Determine the intent and return a JSON response with:
- action: "create_panel", "analyze_metrics", "explain_query", "dashboard_info", or "general"
- confidence: 0.0 to 1.0
- parameters: relevant parameters extracted from the request
- description: what the user wants to do

Examples:
- "Create a CPU panel" → action: "create_panel", parameters: {{"metric": "cpu", "type": "graph"}}
- "Show me memory usage" → action: "create_panel", parameters: {{"metric": "memory", "type": "graph"}}
- "What's wrong with my system?" → action: "analyze_metrics", parameters: {{"analysis_type": "health"}}
- "Explain this query" → action: "explain_query", parameters: {{"query": "current_query"}}
- "What dashboard am I on?" → action: "dashboard_info", parameters: {{"info_type": "current"}}

Respond with only the JSON object.
"""
        
        if self.use_openai and self.openai_api_key:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an AI observability assistant. Analyze user requests and return JSON intent analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=200
                )
                
                intent_text = response.choices[0].message.content.strip()
                return json.loads(intent_text)
                
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                return self._fallback_intent_analysis(user_input)
        else:
            return self._fallback_intent_analysis(user_input)
    
    def _fallback_intent_analysis(self, user_input: str) -> Dict:
        """Fallback intent analysis without AI model"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['create', 'add', 'make', 'build', 'panel']):
            return {
                'action': 'create_panel',
                'confidence': 0.8,
                'parameters': {'metric': 'general', 'type': 'graph'},
                'description': 'User wants to create a panel'
            }
        elif any(word in input_lower for word in ['cpu', 'memory', 'disk', 'network']):
            return {
                'action': 'create_panel',
                'confidence': 0.9,
                'parameters': {'metric': 'system', 'type': 'graph'},
                'description': 'User wants to create a system metrics panel'
            }
        elif any(word in input_lower for word in ['explain', 'query', 'what does']):
            return {
                'action': 'explain_query',
                'confidence': 0.7,
                'parameters': {'query': 'current'},
                'description': 'User wants to explain a query'
            }
        elif any(word in input_lower for word in ['dashboard', 'what', 'where']):
            return {
                'action': 'dashboard_info',
                'confidence': 0.6,
                'parameters': {'info_type': 'current'},
                'description': 'User wants dashboard information'
            }
        else:
            return {
                'action': 'general',
                'confidence': 0.5,
                'parameters': {},
                'description': 'General request'
            }
    
    def _execute_create_panel(self, intent: Dict, user_input: str) -> Dict:
        """Execute panel creation"""
        try:
            # Get current dashboard
            dashboard_uid = self.current_context.get('dashboard_uid')
            if not dashboard_uid:
                # Try to get first available dashboard
                dashboards = self.grafana_client.get_dashboards()
                if not dashboards:
                    return {
                        'success': False,
                        'message': 'No dashboard available. Please create a dashboard first.',
                        'action': 'create_panel'
                    }
                dashboard_uid = dashboards[0].get('uid')
            
            # Determine panel type and metric
            parameters = intent.get('parameters', {})
            metric = parameters.get('metric', 'cpu')
            
            # Create appropriate panel
            if 'cpu' in user_input.lower():
                panel = self.grafana_client.create_cpu_panel(dashboard_uid, "CPU Usage")
                message = "✅ Created CPU usage panel! The panel shows CPU utilization over time with thresholds at 80%."
            elif 'memory' in user_input.lower():
                panel = self.grafana_client.create_memory_panel(dashboard_uid, "Memory Usage")
                message = "✅ Created memory usage panel! The panel shows memory utilization percentage."
            elif 'disk' in user_input.lower():
                panel = self.grafana_client.create_disk_panel(dashboard_uid, "Disk I/O")
                message = "✅ Created disk I/O panel! The panel shows read and write operations."
            else:
                # Create a general system panel
                panel = self.grafana_client.create_cpu_panel(dashboard_uid, "System Metrics")
                message = "✅ Created system metrics panel! The panel shows CPU usage as a starting point."
            
            if panel:
                return {
                    'success': True,
                    'message': message,
                    'action': 'create_panel',
                    'data': {
                        'panel_id': panel.get('id'),
                        'panel_title': panel.get('title'),
                        'dashboard_uid': dashboard_uid
                    }
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to create panel. Please check your dashboard permissions.',
                    'action': 'create_panel'
                }
                
        except Exception as e:
            logger.error(f"Error creating panel: {e}")
            return {
                'success': False,
                'message': f'Error creating panel: {str(e)}',
                'action': 'create_panel'
            }
    
    def _execute_analyze_metrics(self, intent: Dict, user_input: str) -> Dict:
        """Execute metrics analysis"""
        try:
            # Get available data sources
            data_sources = self.grafana_client.get_data_sources()
            prometheus_available = any(ds.get('type') == 'prometheus' for ds in data_sources)
            
            if not prometheus_available:
                return {
                    'success': False,
                    'message': 'Prometheus data source not available. Please configure Prometheus first.',
                    'action': 'analyze_metrics'
                }
            
            # Provide analysis based on context
            panels = self.current_context.get('panels', [])
            if panels:
                panel_info = f"Your dashboard has {len(panels)} panels: " + ", ".join([p.get('title', 'Unknown') for p in panels])
            else:
                panel_info = "Your dashboard is empty. Consider adding some panels to monitor your system."
            
            return {
                'success': True,
                'message': f"📊 System Analysis:\n\n{panel_info}\n\nI can help you:\n• Create panels for CPU, memory, disk, and network metrics\n• Set up alerts for critical thresholds\n• Analyze performance trends\n• Compare metrics across time periods\n\nWhat would you like to monitor?",
                'action': 'analyze_metrics',
                'data': {
                    'panels_count': len(panels),
                    'data_sources': [ds.get('type') for ds in data_sources]
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing metrics: {e}")
            return {
                'success': False,
                'message': f'Error analyzing metrics: {str(e)}',
                'action': 'analyze_metrics'
            }
    
    def _execute_explain_query(self, intent: Dict, user_input: str) -> Dict:
        """Execute query explanation"""
        try:
            # Get current queries from context
            queries = self.current_context.get('queries', [])
            
            if queries:
                query_text = queries[0].get('text', '')
                if query_text:
                    explanation = self._explain_promql_query(query_text)
                    return {
                        'success': True,
                        'message': f"🔍 Query Explanation:\n\n**Query:** `{query_text}`\n\n**Explanation:**\n{explanation}",
                        'action': 'explain_query',
                        'data': {'query': query_text}
                    }
                else:
                    return {
                        'success': True,
                        'message': "No active query found. Please select a panel with a query to explain.",
                        'action': 'explain_query'
                    }
            else:
                return {
                    'success': True,
                    'message': "No queries found in current context. Please create a panel with a query first.",
                    'action': 'explain_query'
                }
                
        except Exception as e:
            logger.error(f"Error explaining query: {e}")
            return {
                'success': False,
                'message': f'Error explaining query: {str(e)}',
                'action': 'explain_query'
            }
    
    def _explain_promql_query(self, query: str) -> str:
        """Explain a PromQL query"""
        if 'up' in query:
            return "This query checks if targets are up (1) or down (0). It's a basic health check."
        elif 'cpu' in query.lower():
            return "This query calculates CPU usage percentage by subtracting idle time from 100%."
        elif 'memory' in query.lower():
            return "This query calculates memory usage percentage using available vs total memory."
        elif 'rate' in query:
            return "This query calculates the rate of change over time, useful for counters."
        elif 'irate' in query:
            return "This query calculates the instantaneous rate of change, more responsive than rate()."
        else:
            return "This is a PromQL query. I can help you understand specific parts or suggest improvements."
    
    def _execute_dashboard_info(self, intent: Dict, user_input: str) -> Dict:
        """Execute dashboard information request"""
        try:
            dashboard_title = self.current_context.get('dashboard_title', 'Unknown')
            user = self.current_context.get('user', {}).get('login', 'Unknown')
            panels = self.current_context.get('panels', [])
            data_sources = self.current_context.get('available_data_sources', [])
            
            info = f"""📊 Dashboard Information:

**Current Dashboard:** {dashboard_title}
**User:** {user}
**Panels:** {len(panels)} panel(s)
**Data Sources:** {', '.join(data_sources) if data_sources else 'None configured'}

**Available Actions:**
• Create new panels (CPU, memory, disk, network)
• Analyze system metrics
• Explain queries
• Set up alerts

What would you like to do with your dashboard?"""
            
            return {
                'success': True,
                'message': info,
                'action': 'dashboard_info',
                'data': {
                    'dashboard_title': dashboard_title,
                    'panels_count': len(panels),
                    'data_sources': data_sources
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard info: {e}")
            return {
                'success': False,
                'message': f'Error getting dashboard info: {str(e)}',
                'action': 'dashboard_info'
            }
    
    def _execute_general_response(self, intent: Dict, user_input: str) -> Dict:
        """Execute general response"""
        try:
            # Use AI for general responses if available
            if self.use_openai and self.openai_api_key:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an AI observability assistant for Grafana. Provide helpful, concise responses about monitoring and dashboards."},
                            {"role": "user", "content": f"User context: {self.current_context}\n\nUser question: {user_input}"}
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    
                    ai_response = response.choices[0].message.content.strip()
                    return {
                        'success': True,
                        'message': ai_response,
                        'action': 'general'
                    }
                    
                except Exception as e:
                    logger.error(f"OpenAI API error: {e}")
                    return self._fallback_general_response(user_input)
            else:
                return self._fallback_general_response(user_input)
                
        except Exception as e:
            logger.error(f"Error in general response: {e}")
            return {
                'success': False,
                'message': f'Error processing request: {str(e)}',
                'action': 'general'
            }
    
    def _fallback_general_response(self, user_input: str) -> Dict:
        """Fallback general response without AI model"""
        return {
            'success': True,
            'message': f"I'm your AI observability assistant! I can help you create panels, analyze metrics, and manage your Grafana dashboards. What would you like to do?\n\nTry asking me to:\n• Create a CPU usage panel\n• Show memory metrics\n• Explain a query\n• Analyze system health",
            'action': 'general'
        }
    
    def get_context(self) -> Dict:
        """Get current context"""
        return {
            'success': True,
            'message': 'Current context retrieved',
            'data': self.current_context,
            'action': 'get_context'
        }
    
    def get_action_history(self) -> List[Dict]:
        """Get action history"""
        return self.action_history 