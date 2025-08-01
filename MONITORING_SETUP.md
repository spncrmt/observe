# 🖥️ **Real System Monitoring Setup Guide**

## Overview

Now that your observability dashboard is running on a domain, you can monitor your actual Mac and PC systems. This guide shows you how to set up real-time monitoring for both machines.

## 🚀 **Quick Start (Mac)**

### 1. Install Dependencies

```bash
# Install psutil for system monitoring
pip install psutil requests flask

# Or add to requirements.txt
echo "psutil" >> requirements.txt
echo "flask" >> requirements.txt
```

### 2. Test Local Monitoring

```bash
# Test the system monitor on your Mac
python scripts/system_monitor.py --local-only --interval 30 --duration 300
```

This will collect real metrics from your Mac and save them to `data/real_metrics.csv`.

### 3. Start API Endpoint

```bash
# Start the API endpoint to receive metrics
python api_endpoint.py --port 8000
```

### 4. Send Metrics to Your Dashboard

```bash
# Replace YOUR_DOMAIN with your actual dashboard domain
python scripts/system_monitor.py --target https://YOUR_DOMAIN.com --interval 60
```

## 🖥️ **PC Setup (Windows)**

### 1. Install Python and Dependencies

```bash
# Install Python from python.org if not already installed
# Then install dependencies
pip install psutil requests
```

### 2. Download the Monitoring Script

Copy `scripts/system_monitor.py` to your PC and run:

```bash
# Test local monitoring on PC
python system_monitor.py --local-only --interval 30 --duration 300
```

### 3. Send to Your Dashboard

```bash
# Replace YOUR_DOMAIN with your actual dashboard domain
python system_monitor.py --target https://YOUR_DOMAIN.com --interval 60
```

## 🔧 **Advanced Setup Options**

### **Option 1: Background Service (Recommended)**

#### Mac (using launchd)

Create a plist file for automatic startup:

```bash
# Create the plist file
cat > ~/Library/LaunchAgents/com.observe.monitor.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.observe.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/your/observe_ai/scripts/system_monitor.py</string>
        <string>--target</string>
        <string>https://YOUR_DOMAIN.com</string>
        <string>--interval</string>
        <string>60</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load the service
launchctl load ~/Library/LaunchAgents/com.observe.monitor.plist
```

#### Windows (using Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "At startup"
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\system_monitor.py --target https://YOUR_DOMAIN.com --interval 60`

### **Option 2: Docker Container**

Create a Dockerfile for easy deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY scripts/system_monitor.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "system_monitor.py", "--target", "https://YOUR_DOMAIN.com", "--interval", "60"]
```

### **Option 3: Cloud Deployment**

Deploy the monitoring agent to cloud services:

#### AWS EC2
```bash
# Launch EC2 instance
# Install Python and dependencies
sudo yum install python3-pip
pip3 install psutil requests

# Run the monitor
python3 system_monitor.py --target https://YOUR_DOMAIN.com --interval 60
```

#### Google Cloud Run
```bash
# Deploy as a containerized service
gcloud run deploy observe-monitor --source .
```

## 📊 **Dashboard Integration**

### **Option 1: Use the API Endpoint**

1. Deploy the API endpoint alongside your dashboard
2. Configure your monitoring agents to send to the API
3. The API saves data to CSV files that your dashboard can read

### **Option 2: Direct File Integration**

1. Run monitoring agents that save directly to CSV files
2. Configure your dashboard to read from these files
3. Update your `app.py` to use real data:

```python
# In app.py, modify load_data() function
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load real metrics and logs from CSV."""
    try:
        # Try to load real data first
        metrics_df = pd.read_csv("data/real_metrics.csv", parse_dates=["timestamp"])
        logs_df = pd.read_csv("data/real_logs.csv", parse_dates=["timestamp"])
    except FileNotFoundError:
        # Fall back to synthetic data
        if not os.path.exists(METRICS_FILE) or not os.path.exists(LOGS_FILE):
            generate_data(DATA_DIR)
        metrics_df = pd.read_csv(METRICS_FILE, parse_dates=["timestamp"])
        logs_df = pd.read_csv(LOGS_FILE, parse_dates=["timestamp"])
    return metrics_df, logs_df
```

## 🔍 **Monitoring Multiple Systems**

### **System Identification**

Each system will be identified by:
- **Hostname**: Automatically detected
- **System Type**: Mac (Darwin) or Windows
- **Unique Metrics**: CPU, memory, disk, network

### **Dashboard Views**

Your dashboard can show:
- **Individual System Views**: Monitor each machine separately
- **Aggregated Views**: Combined metrics from all systems
- **Comparison Views**: Side-by-side system comparisons

## 🚨 **Alerting and Notifications**

### **Built-in Alerts**

The monitoring agent automatically detects:
- High CPU usage (>80%)
- High memory usage (>85%)
- Low disk space (>90%)
- System errors and warnings

### **Custom Alerts**

Add custom alerting rules:

```python
# In system_monitor.py, add custom alerts
def check_custom_alerts(self, metrics):
    alerts = []
    
    # Custom CPU alert
    if metrics['cpu_usage'] > 90:
        alerts.append("CRITICAL: CPU usage above 90%")
    
    # Custom memory alert
    if metrics['memory_usage'] > 95:
        alerts.append("CRITICAL: Memory usage above 95%")
    
    return alerts
```

## 📈 **Performance Optimization**

### **Collection Intervals**

- **Development**: 30 seconds (frequent updates)
- **Production**: 60-300 seconds (balanced performance)
- **Long-term**: 600 seconds (minimal overhead)

### **Data Retention**

Configure data retention policies:

```python
# Keep last 7 days of data
import os
from datetime import datetime, timedelta

def cleanup_old_data():
    cutoff = datetime.now() - timedelta(days=7)
    # Remove data older than cutoff
```

## 🔐 **Security Considerations**

### **API Security**

1. **HTTPS Only**: Always use HTTPS for dashboard communication
2. **Authentication**: Add API keys or tokens for secure communication
3. **Rate Limiting**: Prevent abuse of your API endpoints

### **Data Privacy**

1. **Local Storage**: Keep sensitive data local when possible
2. **Encryption**: Encrypt data in transit and at rest
3. **Access Control**: Limit who can access your monitoring data

## 🎯 **Next Steps**

1. **Deploy the API endpoint** alongside your dashboard
2. **Set up monitoring agents** on your Mac and PC
3. **Configure your dashboard** to use real data
4. **Add custom alerts** for your specific needs
5. **Scale to more systems** as needed

Your observability dashboard is now ready to monitor real systems! 🚀 