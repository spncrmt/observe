#!/usr/bin/env python3
"""
Dashboard Troubleshooting Script
===============================

This script helps diagnose issues with the observability dashboard.
"""

import os
import sys
import pandas as pd
from datetime import datetime

def check_file_permissions():
    """Check if data files are accessible."""
    print("🔍 Checking file permissions...")
    
    files_to_check = [
        "data/real_metrics.csv",
        "data/real_logs.csv", 
        "data/metrics.csv",
        "data/logs.csv"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    f.read(1)
                print(f"✅ {file_path} - Readable")
                
                # Check file size
                size = os.path.getsize(file_path)
                print(f"   📏 Size: {size} bytes")
                
                # Try to read as CSV
                try:
                    df = pd.read_csv(file_path)
                    print(f"   📊 Records: {len(df)}")
                except Exception as e:
                    print(f"   ❌ CSV Error: {e}")
                    
            except Exception as e:
                print(f"❌ {file_path} - Error: {e}")
        else:
            print(f"⚠️  {file_path} - Not found")

def check_data_integrity():
    """Check if data files have valid content."""
    print("\n🔍 Checking data integrity...")
    
    # Check real metrics
    if os.path.exists("data/real_metrics.csv"):
        try:
            df = pd.read_csv("data/real_metrics.csv")
            print(f"📊 Real metrics: {len(df)} records")
            if not df.empty:
                print(f"   📅 Latest: {df.iloc[-1]['timestamp'] if 'timestamp' in df.columns else 'No timestamp'}")
                print(f"   📈 Columns: {list(df.columns)}")
        except Exception as e:
            print(f"❌ Real metrics error: {e}")
    
    # Check real logs
    if os.path.exists("data/real_logs.csv"):
        try:
            df = pd.read_csv("data/real_logs.csv")
            print(f"📋 Real logs: {len(df)} records")
            if not df.empty:
                print(f"   📅 Latest: {df.iloc[-1]['timestamp'] if 'timestamp' in df.columns else 'No timestamp'}")
                print(f"   📈 Columns: {list(df.columns)}")
        except Exception as e:
            print(f"❌ Real logs error: {e}")

def check_streamlit_config():
    """Check Streamlit configuration."""
    print("\n🔍 Checking Streamlit configuration...")
    
    # Check if we can import streamlit
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except Exception as e:
        print(f"❌ Streamlit import error: {e}")
    
    # Check plotly
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except Exception as e:
        print(f"❌ Plotly import error: {e}")
    
    # Check pandas
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except Exception as e:
        print(f"❌ Pandas import error: {e}")

def check_monitoring_status():
    """Check if monitoring is running."""
    print("\n🔍 Checking monitoring status...")
    
    try:
        import psutil
        
        monitoring_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and 'system_monitor.py' in ' '.join(cmdline):
                    monitoring_processes.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if monitoring_processes:
            print(f"✅ Monitoring active - PIDs: {monitoring_processes}")
        else:
            print("❌ No monitoring processes found")
            
    except Exception as e:
        print(f"❌ Error checking monitoring: {e}")

def main():
    """Run all diagnostic checks."""
    print("🔧 Dashboard Troubleshooting")
    print("=" * 40)
    
    check_file_permissions()
    check_data_integrity()
    check_streamlit_config()
    check_monitoring_status()
    
    print("\n💡 Troubleshooting Tips:")
    print("1. If file permissions are wrong, run: chmod 644 data/*.csv")
    print("2. If monitoring isn't running, start it from the dashboard")
    print("3. If JavaScript errors occur, try refreshing the browser")
    print("4. If data is corrupted, delete data/*.csv and restart monitoring")
    print("5. If Streamlit won't start, check: pip install streamlit plotly pandas")

if __name__ == "__main__":
    main() 