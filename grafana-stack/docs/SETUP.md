# Grafana + AI Stack Setup Guide

## 🐳 Install Docker

### **macOS:**
```bash
# Install Docker Desktop
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop
```

### **Linux (Ubuntu/Debian):**
```bash
# Install Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

### **Windows:**
Download Docker Desktop from: https://www.docker.com/products/docker-desktop

## 🚀 Start the Stack

Once Docker is installed:

```bash
# Navigate to the grafana-stack directory
cd grafana-stack

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## 🌐 Access Services

After starting the stack:

- **Grafana Dashboard**: http://localhost:3000
  - Username: `admin`
  - Password: `admin`

- **Prometheus**: http://localhost:9090

- **AI Service API**: http://localhost:5000

## 📊 What You'll See

### **Grafana Dashboard:**
- Real-time CPU, Memory, Disk, Network metrics
- Beautiful visualizations and graphs
- AI-powered insights panel
- Anomaly detection indicators

### **AI Service Features:**
- ML-based anomaly detection
- Root cause analysis
- Natural language queries
- System health scoring

## 🔧 Troubleshooting

### **If Docker isn't running:**
```bash
# macOS: Start Docker Desktop app
# Linux: sudo systemctl start docker
```

### **If ports are in use:**
```bash
# Check what's using the ports
lsof -i :3000
lsof -i :9090
lsof -i :5000

# Stop conflicting services or change ports in docker-compose.yml
```

### **If services fail to start:**
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose down && docker-compose up -d --build
```

## 🎯 Next Steps

1. **Explore Grafana**: Navigate through the dashboard
2. **Test AI Service**: Try the API endpoints
3. **Customize**: Add your own dashboards and metrics
4. **Scale**: Add more data sources and AI capabilities

---

**Ready to experience enterprise-grade monitoring with AI!** 🚀 