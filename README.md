# Observe AI - Grafana Monitoring Stack

A production-ready AI-enhanced monitoring solution combining Grafana's powerful visualization capabilities with intelligent AI insights, deployed on Render with custom domain support.

## 🚀 Features

### **Grafana Stack:**
- **Grafana** - Beautiful dashboards and visualizations
- **Prometheus** - Time-series database for metrics
- **AI Service** - Intelligent monitoring and analysis
- **Custom Domain** - Professional domain integration

### **AI-Powered Monitoring:**
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
│  Custom Domain  │    │  Time Series    │    │  ML Models      │
│  awtospx.com    │    │  Database       │    │  (Anomaly      │
└─────────────────┘    └─────────────────┘    │  Detection)     │
                                              └─────────────────┘
```

## 🛠️ Quick Start

### 1. Deploy to Render
```bash
# Clone the repository
git clone https://github.com/spncrmt/observe.git
cd observe

# Deploy to Render
# 1. Go to https://render.com
# 2. Connect your GitHub repository
# 3. Render will auto-detect render.yaml
# 4. Click "Apply" to deploy
```

### 2. Configure Domain
```bash
# Run the deployment guide
./deploy-render.sh
```

### 3. Access Services
- **Grafana Dashboard**: https://awtospx.com
- **AI Service API**: https://api.awtospx.com
- **Prometheus Admin**: https://prometheus.awtospx.com

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
curl https://api.awtospx.com/insights
```
Returns comprehensive system analysis including health score, anomalies, and recommendations.

#### **Get Anomalies**
```bash
curl https://api.awtospx.com/anomalies
```
Returns detected anomalies with severity levels and timestamps.

#### **Natural Language Query**
```bash
curl -X POST https://api.awtospx.com/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is CPU usage high?"}'
```
Ask questions about your system in natural language.

## 🔧 Configuration

### **Environment Variables:**
- `OPENAI_API_KEY` - Your OpenAI API key for AI features
- `GF_SECURITY_ADMIN_USER` - Grafana admin username
- `GF_SECURITY_ADMIN_PASSWORD` - Grafana admin password

### **Custom Domain Setup:**
See `SQUARESPACE_DOMAIN_SETUP.md` for detailed domain configuration.

## 📁 Project Structure

```
observe_ai/
├── grafana-stack/           # Grafana monitoring stack
│   ├── ai-service/         # AI monitoring service
│   ├── grafana/            # Grafana configuration
│   ├── prometheus/         # Prometheus configuration
│   └── docker-compose.yml  # Local development
├── render.yaml             # Render deployment config
├── deploy-render.sh        # Deployment script
└── SQUARESPACE_DOMAIN_SETUP.md  # Domain configuration
```

## 🚀 Deployment

### **Render Deployment:**
1. Connect GitHub repository to Render
2. Render auto-detects `render.yaml`
3. Deploy with one click
4. Configure custom domain

### **Local Development:**
```bash
cd grafana-stack
docker-compose up -d
```

## 📚 Documentation

- **Domain Setup**: `SQUARESPACE_DOMAIN_SETUP.md`
- **Render IP Guide**: `RENDER_IP_GUIDE.md`
- **Deployment Guide**: `deploy-render.sh`

## 🎯 Use Cases

- **System Monitoring** - Real-time infrastructure monitoring
- **Performance Analysis** - AI-powered performance insights
- **Anomaly Detection** - Automatic issue detection
- **Capacity Planning** - Predictive resource planning
- **Root Cause Analysis** - Intelligent problem diagnosis

## 🔒 Security

- **HTTPS/SSL** - Automatic SSL certificates
- **Authentication** - Grafana user management
- **Internal Networking** - Services not exposed externally
- **Secure Headers** - XSS protection and security headers

## 📞 Support

- **Render Support**: [help.render.com](https://help.render.com)
- **Grafana Docs**: [grafana.com/docs](https://grafana.com/docs)
- **Prometheus Docs**: [prometheus.io/docs](https://prometheus.io/docs)

## 🎉 Getting Started

1. **Deploy to Render** using the provided configuration
2. **Configure your domain** following the setup guide
3. **Access your dashboard** at https://awtospx.com
4. **Login with admin/admin** and start monitoring!

---

**Built with ❤️ using Grafana, Prometheus, and AI**