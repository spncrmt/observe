#!/bin/bash

# 🖥️ System Monitoring Deployment Script
# ======================================

set -e

echo "🚀 Setting up System Monitoring for Observe AI Dashboard"
echo "========================================================"

# Configuration
DASHBOARD_URL=""
INTERVAL=60
DURATION=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            DASHBOARD_URL="$2"
            shift 2
            ;;
        --interval)
            INTERVAL="$2"
            shift 2
            ;;
        --duration)
            DURATION="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --url DASHBOARD_URL    Your dashboard domain (e.g., https://your-domain.com)"
            echo "  --interval SECONDS     Collection interval (default: 60)"
            echo "  --duration SECONDS     Run for specific duration (optional)"
            echo "  --help                 Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if we're on Mac or Windows
if [[ "$OSTYPE" == "darwin"* ]]; then
    SYSTEM="Mac"
    PYTHON_CMD="python3"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    SYSTEM="Windows"
    PYTHON_CMD="python"
else
    SYSTEM="Linux"
    PYTHON_CMD="python3"
fi

echo "📱 Detected system: $SYSTEM"
echo "🐍 Python command: $PYTHON_CMD"

# Check if Python is installed
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Error: Python is not installed or not in PATH"
    echo "Please install Python from https://python.org"
    exit 1
fi

echo "✅ Python found: $(which $PYTHON_CMD)"

# Install dependencies
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install psutil requests flask

echo "✅ Dependencies installed"

# Test the system monitor
echo "🧪 Testing system monitor..."
$PYTHON_CMD scripts/system_monitor.py --local-only --interval 5 --duration 10

echo "✅ System monitor test completed"

# Ask for dashboard URL if not provided
if [[ -z "$DASHBOARD_URL" ]]; then
    echo ""
    echo "🌐 Enter your dashboard URL (e.g., https://your-domain.com):"
    read -r DASHBOARD_URL
fi

if [[ -z "$DASHBOARD_URL" ]]; then
    echo "⚠️  No dashboard URL provided. Running in local-only mode."
    LOCAL_ONLY="--local-only"
else
    echo "🎯 Dashboard URL: $DASHBOARD_URL"
    LOCAL_ONLY=""
fi

# Create monitoring command
MONITOR_CMD="$PYTHON_CMD scripts/system_monitor.py --target $DASHBOARD_URL --interval $INTERVAL"

if [[ -n "$DURATION" ]]; then
    MONITOR_CMD="$MONITOR_CMD --duration $DURATION"
fi

if [[ -n "$LOCAL_ONLY" ]]; then
    MONITOR_CMD="$PYTHON_CMD scripts/system_monitor.py $LOCAL_ONLY --interval $INTERVAL"
    if [[ -n "$DURATION" ]]; then
        MONITOR_CMD="$MONITOR_CMD --duration $DURATION"
    fi
fi

echo ""
echo "🎯 Monitoring Command:"
echo "$MONITOR_CMD"
echo ""

# Ask if user wants to start monitoring now
echo "🚀 Start monitoring now? (y/n):"
read -r START_NOW

if [[ "$START_NOW" == "y" || "$START_NOW" == "Y" ]]; then
    echo "🔄 Starting system monitoring..."
    echo "Press Ctrl+C to stop"
    echo ""
    
    eval "$MONITOR_CMD"
else
    echo ""
    echo "📋 To start monitoring later, run:"
    echo "$MONITOR_CMD"
    echo ""
    
    # Create startup script
    if [[ "$SYSTEM" == "Mac" ]]; then
        echo "📝 Creating startup script for Mac..."
        cat > start_monitoring.sh << EOF
#!/bin/bash
cd "$(dirname "\$0")"
$MONITOR_CMD
EOF
        chmod +x start_monitoring.sh
        echo "✅ Created start_monitoring.sh"
        
        echo ""
        echo "🔧 To run as a background service on Mac:"
        echo "1. Open Terminal"
        echo "2. Run: ./start_monitoring.sh"
        echo "3. Or add to Login Items in System Preferences"
        
    elif [[ "$SYSTEM" == "Windows" ]]; then
        echo "📝 Creating startup script for Windows..."
        cat > start_monitoring.bat << EOF
@echo off
cd /d "%~dp0"
$MONITOR_CMD
pause
EOF
        echo "✅ Created start_monitoring.bat"
        
        echo ""
        echo "🔧 To run as a background service on Windows:"
        echo "1. Open Task Scheduler"
        echo "2. Create Basic Task"
        echo "3. Set trigger to 'At startup'"
        echo "4. Action: Start a program"
        echo "5. Program: $(which $PYTHON_CMD)"
        echo "6. Arguments: scripts/system_monitor.py --target $DASHBOARD_URL --interval $INTERVAL"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📊 Your system monitoring is now configured."
echo "📈 Metrics will be collected every $INTERVAL seconds."
echo "🌐 Dashboard URL: $DASHBOARD_URL"
echo ""
echo "📚 For more information, see MONITORING_SETUP.md" 