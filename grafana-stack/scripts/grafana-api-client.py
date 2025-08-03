"""
Grafana API Client
==================

Direct integration with Grafana API to perform actual dashboard operations:
- Create panels
- Modify dashboards  
- Execute queries
- Manage dashboards
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class GrafanaAPIClient:
    def __init__(self, base_url: str = "http://localhost:3000", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
        else:
            # Try to use admin/admin for local development
            self.session.auth = ('admin', 'admin')
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make API request to Grafana"""
        url = f"{self.base_url}/api{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def get_dashboards(self) -> List[Dict]:
        """Get all dashboards"""
        try:
            response = self._make_request('GET', '/search?type=dash-db')
            return response
        except Exception as e:
            logger.error(f"Failed to get dashboards: {e}")
            return []
    
    def get_dashboard(self, dashboard_uid: str) -> Optional[Dict]:
        """Get specific dashboard by UID"""
        try:
            response = self._make_request('GET', f'/dashboards/uid/{dashboard_uid}')
            return response.get('dashboard', {})
        except Exception as e:
            logger.error(f"Failed to get dashboard {dashboard_uid}: {e}")
            return None
    
    def create_dashboard(self, dashboard_data: Dict) -> Optional[Dict]:
        """Create a new dashboard"""
        try:
            payload = {
                "dashboard": dashboard_data,
                "overwrite": False
            }
            response = self._make_request('POST', '/dashboards/db', payload)
            return response
        except Exception as e:
            logger.error(f"Failed to create dashboard: {e}")
            return None
    
    def update_dashboard(self, dashboard_data: Dict) -> Optional[Dict]:
        """Update existing dashboard"""
        try:
            payload = {
                "dashboard": dashboard_data,
                "overwrite": True
            }
            response = self._make_request('POST', '/dashboards/db', payload)
            return response
        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")
            return None
    
    def create_panel(self, dashboard_uid: str, panel_config: Dict) -> Optional[Dict]:
        """Create a new panel in existing dashboard"""
        try:
            # Get current dashboard
            dashboard = self.get_dashboard(dashboard_uid)
            if not dashboard:
                logger.error(f"Dashboard {dashboard_uid} not found")
                return None
            
            # Add new panel
            if 'panels' not in dashboard:
                dashboard['panels'] = []
            
            # Generate panel ID
            max_id = max([p.get('id', 0) for p in dashboard['panels']]) if dashboard['panels'] else 0
            panel_config['id'] = max_id + 1
            
            # Add panel to dashboard
            dashboard['panels'].append(panel_config)
            
            # Update dashboard
            result = self.update_dashboard(dashboard)
            if result:
                logger.info(f"Created panel {panel_config['id']} in dashboard {dashboard_uid}")
                return panel_config
            return None
            
        except Exception as e:
            logger.error(f"Failed to create panel: {e}")
            return None
    
    def create_cpu_panel(self, dashboard_uid: str, title: str = "CPU Usage") -> Optional[Dict]:
        """Create a CPU usage panel"""
        panel_config = {
            "title": title,
            "type": "graph",
            "targets": [
                {
                    "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
                    "refId": "A",
                    "datasource": "Prometheus"
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "custom": {
                        "drawStyle": "line",
                        "lineInterpolation": "linear",
                        "barAlignment": 0,
                        "lineWidth": 1,
                        "fillOpacity": 10,
                        "gradientMode": "none",
                        "spanNulls": False,
                        "showPoints": "auto",
                        "pointSize": 5,
                        "stacking": {
                            "mode": "none",
                            "group": "A"
                        },
                        "axisLabel": "",
                        "scaleDistribution": {
                            "type": "linear"
                        },
                        "hideFrom": {
                            "legend": False,
                            "tooltip": False,
                            "vis": False
                        },
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {
                                    "color": "green",
                                    "value": None
                                },
                                {
                                    "color": "red",
                                    "value": 80
                                }
                            ]
                        }
                    },
                    "color": {
                        "mode": "palette-classic"
                    },
                    "mappings": [],
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {
                                "color": "green",
                                "value": None
                            },
                            {
                                "color": "red",
                                "value": 80
                            }
                        ]
                    },
                    "unit": "percent"
                }
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 0,
                "y": 0
            },
            "options": {
                "legend": {
                    "calcs": [],
                    "displayMode": "list",
                    "placement": "bottom"
                },
                "tooltip": {
                    "mode": "single"
                }
            }
        }
        
        return self.create_panel(dashboard_uid, panel_config)
    
    def create_memory_panel(self, dashboard_uid: str, title: str = "Memory Usage") -> Optional[Dict]:
        """Create a memory usage panel"""
        panel_config = {
            "title": title,
            "type": "graph",
            "targets": [
                {
                    "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
                    "refId": "A",
                    "datasource": "Prometheus"
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "custom": {
                        "drawStyle": "line",
                        "lineInterpolation": "linear",
                        "barAlignment": 0,
                        "lineWidth": 1,
                        "fillOpacity": 10,
                        "gradientMode": "none",
                        "spanNulls": False,
                        "showPoints": "auto",
                        "pointSize": 5,
                        "stacking": {
                            "mode": "none",
                            "group": "A"
                        },
                        "axisLabel": "",
                        "scaleDistribution": {
                            "type": "linear"
                        },
                        "hideFrom": {
                            "legend": False,
                            "tooltip": False,
                            "vis": False
                        },
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {
                                    "color": "green",
                                    "value": None
                                },
                                {
                                    "color": "red",
                                    "value": 80
                                }
                            ]
                        }
                    },
                    "color": {
                        "mode": "palette-classic"
                    },
                    "mappings": [],
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {
                                "color": "green",
                                "value": None
                            },
                            {
                                "color": "red",
                                "value": 80
                            }
                        ]
                    },
                    "unit": "percent"
                }
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 12,
                "y": 0
            },
            "options": {
                "legend": {
                    "calcs": [],
                    "displayMode": "list",
                    "placement": "bottom"
                },
                "tooltip": {
                    "mode": "single"
                }
            }
        }
        
        return self.create_panel(dashboard_uid, panel_config)
    
    def create_disk_panel(self, dashboard_uid: str, title: str = "Disk I/O") -> Optional[Dict]:
        """Create a disk I/O panel"""
        panel_config = {
            "title": title,
            "type": "graph",
            "targets": [
                {
                    "expr": "rate(node_disk_read_bytes_total[5m])",
                    "refId": "A",
                    "datasource": "Prometheus",
                    "legendFormat": "Read"
                },
                {
                    "expr": "rate(node_disk_written_bytes_total[5m])",
                    "refId": "B",
                    "datasource": "Prometheus",
                    "legendFormat": "Write"
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "custom": {
                        "drawStyle": "line",
                        "lineInterpolation": "linear",
                        "barAlignment": 0,
                        "lineWidth": 1,
                        "fillOpacity": 10,
                        "gradientMode": "none",
                        "spanNulls": False,
                        "showPoints": "auto",
                        "pointSize": 5,
                        "stacking": {
                            "mode": "none",
                            "group": "A"
                        },
                        "axisLabel": "",
                        "scaleDistribution": {
                            "type": "linear"
                        },
                        "hideFrom": {
                            "legend": False,
                            "tooltip": False,
                            "vis": False
                        }
                    },
                    "color": {
                        "mode": "palette-classic"
                    },
                    "mappings": [],
                    "unit": "bytes"
                }
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 0,
                "y": 8
            },
            "options": {
                "legend": {
                    "calcs": [],
                    "displayMode": "list",
                    "placement": "bottom"
                },
                "tooltip": {
                    "mode": "single"
                }
            }
        }
        
        return self.create_panel(dashboard_uid, panel_config)
    
    def create_custom_panel(self, dashboard_uid: str, title: str, query: str, 
                           panel_type: str = "graph", datasource: str = "Prometheus") -> Optional[Dict]:
        """Create a custom panel with specific query"""
        panel_config = {
            "title": title,
            "type": panel_type,
            "targets": [
                {
                    "expr": query,
                    "refId": "A",
                    "datasource": datasource
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "custom": {
                        "drawStyle": "line",
                        "lineInterpolation": "linear",
                        "barAlignment": 0,
                        "lineWidth": 1,
                        "fillOpacity": 10,
                        "gradientMode": "none",
                        "spanNulls": False,
                        "showPoints": "auto",
                        "pointSize": 5,
                        "stacking": {
                            "mode": "none",
                            "group": "A"
                        },
                        "axisLabel": "",
                        "scaleDistribution": {
                            "type": "linear"
                        },
                        "hideFrom": {
                            "legend": False,
                            "tooltip": False,
                            "vis": False
                        }
                    },
                    "color": {
                        "mode": "palette-classic"
                    },
                    "mappings": []
                }
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 0,
                "y": 0
            },
            "options": {
                "legend": {
                    "calcs": [],
                    "displayMode": "list",
                    "placement": "bottom"
                },
                "tooltip": {
                    "mode": "single"
                }
            }
        }
        
        return self.create_panel(dashboard_uid, panel_config)
    
    def delete_panel(self, dashboard_uid: str, panel_id: int) -> bool:
        """Delete a panel from dashboard"""
        try:
            dashboard = self.get_dashboard(dashboard_uid)
            if not dashboard:
                return False
            
            # Remove panel
            dashboard['panels'] = [p for p in dashboard['panels'] if p.get('id') != panel_id]
            
            # Update dashboard
            result = self.update_dashboard(dashboard)
            return result is not None
            
        except Exception as e:
            logger.error(f"Failed to delete panel {panel_id}: {e}")
            return False
    
    def get_data_sources(self) -> List[Dict]:
        """Get available data sources"""
        try:
            response = self._make_request('GET', '/datasources')
            return response
        except Exception as e:
            logger.error(f"Failed to get data sources: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Test connection to Grafana API"""
        try:
            response = self._make_request('GET', '/user')
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Grafana API: {e}")
            return False

# Example usage
if __name__ == "__main__":
    client = GrafanaAPIClient()
    
    if client.test_connection():
        print("✅ Connected to Grafana API")
        
        # Get dashboards
        dashboards = client.get_dashboards()
        print(f"Found {len(dashboards)} dashboards")
        
        # Create a test panel if we have a dashboard
        if dashboards:
            dashboard_uid = dashboards[0].get('uid')
            if dashboard_uid:
                panel = client.create_cpu_panel(dashboard_uid, "AI Created CPU Panel")
                if panel:
                    print(f"✅ Created panel: {panel['title']}")
                else:
                    print("❌ Failed to create panel")
    else:
        print("❌ Could not connect to Grafana API") 