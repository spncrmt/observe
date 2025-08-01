#!/usr/bin/env python3
"""
Monitoring Status Checker
========================

This script checks if the system monitoring is currently running
and provides status information.
"""

import os
import psutil
import json
from datetime import datetime

def check_monitoring_status():
    """Check if system monitoring is currently running."""
    monitoring_processes = []
    
    # Look for system_monitor.py processes
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'system_monitor.py' in ' '.join(cmdline):
                monitoring_processes.append({
                    'pid': proc.info['pid'],
                    'cmdline': ' '.join(cmdline),
                    'create_time': datetime.fromtimestamp(proc.create_time()).isoformat()
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return monitoring_processes

def get_latest_metrics():
    """Get the latest metrics from the data files."""
    metrics_file = "data/real_metrics.csv"
    logs_file = "data/real_logs.csv"
    
    status = {
        'metrics_file_exists': os.path.exists(metrics_file),
        'logs_file_exists': os.path.exists(logs_file),
        'latest_metrics': None,
        'metrics_count': 0,
        'logs_count': 0
    }
    
    if status['metrics_file_exists']:
        try:
            import pandas as pd
            metrics_df = pd.read_csv(metrics_file, parse_dates=["timestamp"])
            status['metrics_count'] = len(metrics_df)
            if not metrics_df.empty:
                status['latest_metrics'] = metrics_df.iloc[-1].to_dict()
        except Exception as e:
            status['metrics_error'] = str(e)
    
    if status['logs_file_exists']:
        try:
            import pandas as pd
            logs_df = pd.read_csv(logs_file, parse_dates=["timestamp"])
            status['logs_count'] = len(logs_df)
        except Exception as e:
            status['logs_error'] = str(e)
    
    return status

def main():
    """Main function to check and display monitoring status."""
    print("🔍 Monitoring Status Check")
    print("=" * 40)
    
    # Check for running processes
    processes = check_monitoring_status()
    
    if processes:
        print("✅ Monitoring is ACTIVE")
        print(f"📊 Found {len(processes)} monitoring process(es):")
        for proc in processes:
            print(f"   PID: {proc['pid']}")
            print(f"   Started: {proc['create_time']}")
            print(f"   Command: {proc['cmdline']}")
            print()
    else:
        print("❌ Monitoring is INACTIVE")
        print("   No monitoring processes found")
        print()
    
    # Check data files
    print("📁 Data Files Status:")
    status = get_latest_metrics()
    
    if status['metrics_file_exists']:
        print(f"   ✅ Metrics file: {status['metrics_count']} records")
        if status['latest_metrics']:
            latest = status['latest_metrics']
            print(f"   📈 Latest CPU: {latest.get('cpu_usage', 'N/A')}%")
            print(f"   📈 Latest Memory: {latest.get('memory_usage', 'N/A')}%")
            print(f"   📈 Latest Time: {latest.get('timestamp', 'N/A')}")
    else:
        print("   ❌ No metrics file found")
    
    if status['logs_file_exists']:
        print(f"   ✅ Logs file: {status['logs_count']} records")
    else:
        print("   ❌ No logs file found")
    
    print()
    print("💡 To start monitoring:")
    print("   python scripts/system_monitor.py --local-only --interval 60")
    print()
    print("💡 To start monitoring from dashboard:")
    print("   Open your dashboard and click 'Start Monitoring'")

if __name__ == "__main__":
    main() 