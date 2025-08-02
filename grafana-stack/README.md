# Grafana + AI Monitoring Stack

A production-ready monitoring solution combining Grafana's powerful visualization capabilities with AI-powered intelligent insights.

## 🚀 Features

### **Grafana Stack:**
- **Grafana** - Beautiful dashboards and visualizations
- **Prometheus** - Time-series database for metrics
- **Node Exporter** - System metrics collection
- **cAdvisor** - Container metrics monitoring

### **AI Service:**
- **Anomaly Detection** - ML-based pattern recognition
- **Root Cause Analysis** - Intelligent issue diagnosis
- **Predictive Analytics** - Trend forecasting
- **Natural Language Queries** - Ask questions about your system
- **Health Scoring** - Overall system health assessment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Grafana UI    │    │   Prometheus    │    │   AI Service    │
│   (Port 3000)   │◄──►│   (Port 9090)   │◄──►│   (Port 5000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Node Exporter  │    │    cAdvisor     │    │  ML Models      │
│  (Port 9100)    │    │   (Port 8080)   │    │  (Isolation     │
└─────────────────┘    └─────────────────┘    │  Forest, etc.)  │
                                              └─────────────────┘
```

## 🛠️ Quick Start

### 1. Prerequisites
```bash
# Install Docker and Docker Compose
# macOS: brew install docker docker-compose
# Linux: Follow Docker installation guide
```

### 2. Clone and Setup
```bash
cd grafana-stack
docker-compose up -d
```

### 3. Access Services
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **AI Service**: http://localhost:5000

### 4. Import Dashboard
1. Open Grafana at http://localhost:3000
2. Login with admin/admin
3. The system monitoring dashboard will be automatically loaded
4. Navigate to Dashboards → System Monitoring Dashboard

## 📊 Dashboard Features

### **Real-time Metrics:**
- **CPU Usage** - Live CPU utilization with anomaly detection
- **Memory Usage** - Memory consumption trends
- **Disk I/O** - Storage performance monitoring
- **Network Traffic** - Network bandwidth analysis
- **System Load** - Load average statistics

### **AI Insights Panel:**
- **Anomaly Detection** - Automatic pattern recognition
- **Root Cause Analysis** - Intelligent issue diagnosis
- **Predictive Analytics** - Trend forecasting
- **Recommendations** - Actionable optimization suggestions

## 🤖 AI Service API

### **Endpoints:**

#### **Get AI Insights**
```bash
curl http://localhost:5000/api/insights
```
Returns comprehensive system analysis including health score, anomalies, and recommendations.

#### **Get Anomalies**
```bash
curl http://localhost:5000/api/anomalies
```
Returns detected anomalies with severity levels and timestamps.

#### **Natural Language Query**
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is CPU usage high?"}'
```
Ask questions about your system in natural language.

#### **Health Check**
```bash
curl http://localhost:5000/health
```
Service health status.

#### **Prometheus Metrics**
```bash
curl http://localhost:5000/metrics
```
Custom metrics for monitoring the AI service itself.

## 🔧 Configuration

### **Environment Variables:**
Create a `.env` file in the root directory:
```bash
# AI Service Configuration
OPENAI_API_KEY=your_openai_api_key_here
PROMETHEUS_URL=http://prometheus:9090

# Grafana Configuration
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin
```

### **Custom Dashboards:**
Add custom dashboards to `grafana/dashboards/` and they'll be automatically loaded.

### **Prometheus Rules:**
Add alerting rules to `prometheus/rules/` for custom alerts.

## 📈 Monitoring Your Mac

The stack automatically monitors your Mac system through:

- **Node Exporter** - Collects system metrics (CPU, memory, disk, network)
- **cAdvisor** - Container and process monitoring
- **AI Service** - Provides intelligent insights and anomaly detection

### **Key Metrics Collected:**
- CPU utilization per core
- Memory usage and availability
- Disk I/O and space usage
- Network traffic and bandwidth
- System load averages
- Process statistics

## 🎯 AI Capabilities

### **Anomaly Detection:**
- Uses Isolation Forest algorithm
- Detects unusual patterns in metrics
- Provides severity levels (high/medium)
- Real-time scoring

### **Root Cause Analysis:**
- Correlates anomalies across metrics
- Identifies affected system components
- Generates actionable recommendations
- Historical pattern analysis

### **Predictive Analytics:**
- Trend analysis for key metrics
- Forecast potential issues
- Capacity planning insights
- Performance optimization suggestions

### **Natural Language Interface:**
- Ask questions about system health
- Get explanations in plain English
- Query specific metrics
- Receive actionable insights

## 🔍 Troubleshooting

### **Common Issues:**

#### **Services not starting:**
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

#### **No metrics in Grafana:**
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Verify Node Exporter is running
curl http://localhost:9100/metrics
```

#### **AI service errors:**
```bash
# Check AI service logs
docker-compose logs ai-service

# Verify Prometheus connectivity
curl http://localhost:5000/health
```

### **Useful Commands:**
```bash
# View all logs
docker-compose logs -f

# Restart specific service
docker-compose restart grafana

# Update configuration
docker-compose down && docker-compose up -d

# Clean up volumes
docker-compose down -v
```

## 🚀 Production Deployment

### **For Production Use:**
1. **Change default passwords**
2. **Set up proper authentication**
3. **Configure SSL/TLS**
4. **Set up backup strategies**
5. **Configure alerting rules**
6. **Scale services as needed**

### **Docker Compose Override:**
Create `docker-compose.override.yml` for production settings:
```yaml
version: '3.8'
services:
  grafana:
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secure_password_here
    volumes:
      - ./ssl:/etc/grafana/ssl
```

## 📚 Next Steps

### **Enhancements:**
1. **Add more data sources** (Elasticsearch, InfluxDB)
2. **Implement custom dashboards** for specific use cases
3. **Set up alerting** with Slack/email notifications
4. **Add more AI models** for different types of analysis
5. **Implement automated remediation** actions

### **Integration:**
1. **Connect to your existing monitoring** infrastructure
2. **Add custom metrics** from your applications
3. **Set up CI/CD** for dashboard versioning
4. **Implement multi-tenancy** for team access

## 🤝 Contributing

This is a demonstration of Grafana + AI integration. Feel free to:
- Add new AI capabilities
- Create custom dashboards
- Improve the monitoring stack
- Share your enhancements

---

**Enjoy your intelligent monitoring stack!** 🎉 