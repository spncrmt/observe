#!/usr/bin/env python3
"""
API Endpoint for Receiving System Metrics
========================================

This creates a simple API endpoint that your monitoring agents can send
metrics to. You can integrate this with your Streamlit dashboard or run
it as a separate service.

Usage:
    python api_endpoint.py --port 8000
"""

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import pandas as pd
from typing import Dict, Any

app = Flask(__name__)

# Data storage
METRICS_FILE = "data/received_metrics.csv"
LOGS_FILE = "data/received_logs.csv"

def ensure_data_directory():
    """Ensure the data directory exists."""
    os.makedirs("data", exist_ok=True)

def save_metrics(metrics: Dict[str, Any]):
    """Save received metrics to CSV file."""
    ensure_data_directory()
    
    # Convert to CSV format
    csv_line = f"{metrics['timestamp']},{metrics['cpu_usage']},{metrics['memory_usage']},{metrics.get('latency_ms', 0)}\n"
    
    # Create file with headers if it doesn't exist
    if not os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "w") as f:
            f.write("timestamp,cpu_usage,memory_usage,latency_ms\n")
    
    # Append the new data
    with open(METRICS_FILE, "a") as f:
        f.write(csv_line)

def save_logs(logs: list):
    """Save received logs to CSV file."""
    ensure_data_directory()
    
    # Create file with headers if it doesn't exist
    if not os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, "w") as f:
            f.write("timestamp,level,message\n")
    
    # Append the new logs
    for log in logs:
        csv_line = f"{log['timestamp']},{log['level']},{log['message']}\n"
        with open(LOGS_FILE, "a") as f:
            f.write(csv_line)

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    """Receive metrics from monitoring agents."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        metrics = data.get('metrics', {})
        logs = data.get('logs', [])
        hostname = data.get('hostname', 'unknown')
        system = data.get('system', 'unknown')
        
        print(f"Received metrics from {hostname} ({system})")
        print(f"CPU: {metrics.get('cpu_usage', 'N/A')}%, Memory: {metrics.get('memory_usage', 'N/A')}%")
        
        # Save the data
        if metrics:
            save_metrics(metrics)
        
        if logs:
            save_logs(logs)
        
        return jsonify({
            "status": "success",
            "message": "Metrics received and saved",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error processing metrics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get the collected data."""
    try:
        metrics_data = []
        logs_data = []
        
        if os.path.exists(METRICS_FILE):
            metrics_df = pd.read_csv(METRICS_FILE)
            metrics_data = metrics_df.to_dict('records')
        
        if os.path.exists(LOGS_FILE):
            logs_df = pd.read_csv(LOGS_FILE)
            logs_data = logs_df.to_dict('records')
        
        return jsonify({
            "metrics": metrics_data,
            "logs": logs_data,
            "metrics_count": len(metrics_data),
            "logs_count": len(logs_data)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="API Endpoint for System Metrics")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the API on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    
    args = parser.parse_args()
    
    print(f"Starting API endpoint on {args.host}:{args.port}")
    print("Available endpoints:")
    print("  POST /api/metrics - Receive metrics from monitoring agents")
    print("  GET  /api/health  - Health check")
    print("  GET  /api/data    - Get collected data")
    
    app.run(host=args.host, port=args.port, debug=True) 