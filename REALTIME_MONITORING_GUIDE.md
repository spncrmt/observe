# 🔄 **Real-Time Monitoring Guide**

## 🎯 **Overview**

Your observability dashboard now includes **real-time monitoring capabilities**! You can start monitoring directly from the web interface and watch data come in live over time.

## 🚀 **How to Use Real-Time Monitoring**

### **Step 1: Access Your Dashboard**
1. Open your dashboard in a web browser
2. Log in with your credentials (admin/admin)
3. Look for the **"🖥️ Real-time Monitoring"** section in the sidebar

### **Step 2: Start Monitoring**
1. In the sidebar, you'll see:
   - **⏸️ Monitoring Inactive** (when not running)
   - **Collection Interval** slider (30-300 seconds)
   - **▶️ Start Monitoring** button

2. Adjust the collection interval:
   - **30 seconds**: Very frequent updates (good for testing)
   - **60 seconds**: Balanced performance (recommended)
   - **300 seconds**: Less frequent (good for long-term monitoring)

3. Click **"▶️ Start Monitoring"**

### **Step 3: Watch Live Data**
Once monitoring starts, you'll see:

#### **📊 Live System Status**
- **CPU Usage**: Current percentage with trend indicator
- **Memory Usage**: Current percentage with trend indicator  
- **Latency**: Response time (if available)
- **Monitoring Time**: Number of samples collected

#### **📈 Real-Time Charts**
- **Live Data Indicator**: Shows "🔄 Live Data - Monitoring Active"
- **Auto-refreshing charts**: Updates every 10 seconds
- **Anomaly detection**: Red X markers for detected issues
- **Interactive hover**: See exact values and timestamps

#### **📋 Live Logs**
- **Real-time log entries**: System warnings and errors
- **Auto-updating table**: Shows latest 100 log entries
- **Error categorization**: WARN, ERROR, INFO levels

## 🎮 **Dashboard Features**

### **Real-Time vs Historical Mode**
- **When monitoring is ACTIVE**: Shows live data with auto-refresh
- **When monitoring is INACTIVE**: Shows historical data (synthetic or real)

### **Data Source Indicator**
- **🔄 Live Data**: Real-time monitoring active
- **📊 Historical Data**: Viewing stored data

### **Monitoring Controls**
- **Start/Stop**: Toggle monitoring on/off
- **Interval Control**: Adjust collection frequency
- **Status Indicators**: Clear visual feedback

## 📊 **What You'll See**

### **Live Metrics**
- **CPU Usage**: Real-time percentage from your system
- **Memory Usage**: Actual RAM usage
- **System Load**: Process count and system activity
- **Network Activity**: Bytes sent/received
- **Disk Usage**: Storage space utilization

### **Live Alerts**
- **High CPU**: >80% usage warnings
- **High Memory**: >85% usage warnings
- **Low Disk Space**: >90% usage errors
- **System Errors**: Real error messages

### **AI Analysis**
- **Real-time AI**: Ask questions about live data
- **Anomaly Detection**: Automatic detection of issues
- **Root Cause Analysis**: Correlate metrics with logs
- **Predictive Insights**: AI explanations of trends

## ⏱️ **Monitoring Duration**

### **Short-term Monitoring (1-2 hours)**
- **Interval**: 30-60 seconds
- **Use case**: Debugging issues, performance testing
- **Data retention**: Last 2 hours shown

### **Long-term Monitoring (Days/Weeks)**
- **Interval**: 300 seconds (5 minutes)
- **Use case**: Trend analysis, capacity planning
- **Data retention**: All data saved to CSV files

## 🔧 **Advanced Features**

### **Multiple System Monitoring**
You can monitor multiple systems simultaneously:
1. **Mac**: Run monitoring from your Mac
2. **PC**: Copy `scripts/system_monitor.py` to your PC
3. **Dashboard**: View combined data from all systems

### **Custom Alerts**
The system automatically detects:
- **Performance issues**: High CPU/memory usage
- **System errors**: Application crashes, warnings
- **Resource exhaustion**: Low disk space, memory pressure

### **Data Export**
All monitoring data is saved to:
- `data/real_metrics.csv`: System metrics
- `data/real_logs.csv`: System logs
- **Format**: CSV with timestamps for analysis

## 🚨 **Troubleshooting**

### **Monitoring Won't Start**
1. **Check Python**: Ensure Python is installed
2. **Check Dependencies**: Run `pip install psutil requests`
3. **Check Permissions**: Ensure script is executable
4. **Check Logs**: Look for error messages in the dashboard

### **No Data Appearing**
1. **Wait 30-60 seconds**: First data point takes time
2. **Check File Permissions**: Ensure data directory is writable
3. **Check System Resources**: Ensure system has available resources
4. **Restart Monitoring**: Stop and start again

### **Dashboard Not Updating**
1. **Refresh Browser**: Manual refresh if needed
2. **Check Auto-refresh**: Should update every 10 seconds
3. **Check Network**: Ensure stable internet connection
4. **Check Console**: Look for JavaScript errors

## 🎯 **Best Practices**

### **For Development**
- **Interval**: 30 seconds (frequent updates)
- **Duration**: 1-2 hours (quick testing)
- **Focus**: Real-time debugging

### **For Production**
- **Interval**: 60-300 seconds (balanced performance)
- **Duration**: Continuous (24/7 monitoring)
- **Focus**: Long-term trends and alerts

### **For Analysis**
- **Interval**: 300 seconds (minimal overhead)
- **Duration**: Days/weeks (historical analysis)
- **Focus**: Capacity planning and optimization

## 🎉 **Getting Started**

1. **Open your dashboard**: Navigate to your domain
2. **Log in**: Use admin/admin or your credentials
3. **Start monitoring**: Click "Start Monitoring" in sidebar
4. **Watch live data**: See real-time metrics and charts
5. **Ask AI questions**: Use the AI assistant with live data
6. **Stop when done**: Click "Stop Monitoring" to end

Your observability dashboard is now a **real-time monitoring powerhouse**! 🚀

**Start monitoring now and watch your system come to life!** 