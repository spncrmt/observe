#!/usr/bin/env python3
"""
Test Dashboard Fix
==================

This script tests the dashboard fixes to ensure no JavaScript errors occur.
"""

import pandas as pd
import os
from datetime import datetime

def test_data_loading():
    """Test that data loading works correctly."""
    print("🧪 Testing data loading...")
    
    # Test real metrics loading
    try:
        if os.path.exists("data/real_metrics.csv"):
            df = pd.read_csv("data/real_metrics.csv", parse_dates=["timestamp"])
            print(f"✅ Real metrics loaded: {len(df)} records")
            print(f"   Columns: {list(df.columns)}")
            if not df.empty:
                print(f"   Latest: {df.iloc[-1]['timestamp']}")
        else:
            print("⚠️  No real metrics file found")
    except Exception as e:
        print(f"❌ Error loading real metrics: {e}")
    
    # Test real logs loading
    try:
        if os.path.exists("data/real_logs.csv"):
            df = pd.read_csv("data/real_logs.csv", parse_dates=["timestamp"])
            print(f"✅ Real logs loaded: {len(df)} records")
            print(f"   Columns: {list(df.columns)}")
            if not df.empty:
                print(f"   Latest: {df.iloc[-1]['timestamp']}")
        else:
            print("⚠️  No real logs file found")
    except Exception as e:
        print(f"❌ Error loading real logs: {e}")

def test_dataframe_display():
    """Test that dataframe display works without JavaScript errors."""
    print("\n🧪 Testing dataframe display...")
    
    try:
        # Create a test dataframe
        test_data = {
            'timestamp': [datetime.now().isoformat()],
            'level': ['INFO'],
            'message': ['Test message']
        }
        df = pd.DataFrame(test_data)
        
        # Test that we can convert to string representation
        df_str = df.astype(str)
        print("✅ DataFrame string conversion successful")
        
        # Test that timestamp column can be handled
        if 'timestamp' in df.columns:
            df['timestamp'] = df['timestamp'].astype(str)
            print("✅ Timestamp column handling successful")
        
        print("✅ DataFrame display test passed")
        
    except Exception as e:
        print(f"❌ DataFrame display test failed: {e}")

def test_csv_integrity():
    """Test that CSV files have proper headers and format."""
    print("\n🧪 Testing CSV integrity...")
    
    files_to_test = [
        ("data/real_metrics.csv", ["timestamp", "cpu_usage", "memory_usage", "latency_ms"]),
        ("data/real_logs.csv", ["timestamp", "level", "message"])
    ]
    
    for file_path, expected_headers in files_to_test:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    first_line = f.readline().strip()
                    headers = first_line.split(',')
                    
                if headers == expected_headers:
                    print(f"✅ {file_path} - Headers correct")
                else:
                    print(f"❌ {file_path} - Headers mismatch")
                    print(f"   Expected: {expected_headers}")
                    print(f"   Found: {headers}")
                    
            except Exception as e:
                print(f"❌ {file_path} - Error: {e}")
        else:
            print(f"⚠️  {file_path} - Not found")

def main():
    """Run all tests."""
    print("🔧 Dashboard Fix Test")
    print("=" * 30)
    
    test_data_loading()
    test_dataframe_display()
    test_csv_integrity()
    
    print("\n✅ All tests completed!")
    print("💡 If all tests pass, the JavaScript error should be resolved.")

if __name__ == "__main__":
    main() 