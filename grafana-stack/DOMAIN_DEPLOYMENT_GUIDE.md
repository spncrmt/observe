# Domain Deployment Guide: Local Grafana → awtospx.com

This guide will help you move your locally hosted Grafana monitoring stack to your domain `awtospx.com`.

## 🎯 What We're Doing

1. **Set up SSL certificates** for secure HTTPS access
2. **Configure Nginx reverse proxy** to serve Grafana on your domain
3. **Update DNS settings** to point your domain to your server
4. **Deploy the production stack** with proper security

## 📋 Prerequisites

- ✅ Domain ownership (`awtospx.com`)
- ✅ Server with Docker and Docker Compose
- ✅ Public IP address for your server
- ✅ Access to your domain registrar's DNS panel

## 🚀 Quick Deployment Steps

### Step 1: Navigate to Grafana Stack Directory
```bash
cd grafana-stack
```

### Step 2: Set Up SSL Certificates
```bash
# Make the script executable
chmod +x setup-ssl.sh

# Run the SSL setup
./setup-ssl.sh
```

Choose option 1 for Let's Encrypt (recommended) or option 2 for self-signed.

### Step 3: Update Your DNS Settings
Follow the detailed guide in `DNS_SETUP_GUIDE.md` to:
1. Log into your domain registrar
2. Add A records pointing `awtospx.com` to your server IP
3. Wait for DNS propagation (up to 48 hours)

### Step 4: Deploy to Production
```bash
# Make the deployment script executable
chmod +x deploy-to-domain.sh

# Run the deployment
./deploy-to-domain.sh
```

### Step 5: Test Access
Once DNS has propagated, test access at:
- **Grafana Dashboard**: https://awtospx.com
- **AI Service API**: https://awtospx.com/api/
- **Prometheus Admin**: https://awtospx.com/prometheus/

## 🔧 Detailed Configuration

### SSL Certificate Options

#### Option 1: Let's Encrypt (Recommended)
- **Free**: No cost for certificates
- **Auto-renewal**: Certificates renew automatically
- **Trusted**: Widely accepted by browsers
- **Requirements**: Domain must be publicly accessible

#### Option 2: Self-Signed Certificate
- **Development only**: Will show browser warnings
- **Quick setup**: Good for testing
- **No external dependencies**: Works offline

#### Option 3: Upload Your Own Certificate
- **Custom certificates**: Use your own CA-signed certificates
- **Full control**: Complete certificate management
- **Requirements**: Valid SSL certificate files

### Production vs Development

#### Development (Current Setup)
- **Access**: http://localhost:3000
- **Security**: Basic authentication
- **SSL**: None (HTTP only)
- **Ports**: Exposed directly

#### Production (Domain Setup)
- **Access**: https://awtospx.com
- **Security**: HTTPS with SSL certificates
- **SSL**: Let's Encrypt or custom certificates
- **Ports**: Only 80/443 exposed, others internal

## 🔒 Security Enhancements

### Firewall Configuration
```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

### Grafana Security Settings
The production configuration includes:
- **Secure cookies**: HTTPS-only cookies
- **SameSite**: Strict cookie policy
- **Security headers**: XSS protection, frame options
- **Internal networking**: Services not exposed externally

## 📊 Service Architecture

```
Internet → Nginx (Port 80/443) → Grafana (Port 3000)
                    ↓
              AI Service (Port 5000)
                    ↓
              Prometheus (Port 9090)
```

## 🛠️ Management Commands

### Start Services
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Stop Services
```bash
docker-compose -f docker-compose.prod.yml down
```

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f grafana
```

### Restart Services
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Update Configuration
```bash
# Stop services
docker-compose -f docker-compose.prod.yml down

# Update configuration files
# Edit nginx.conf, docker-compose.prod.yml, etc.

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 Monitoring and Troubleshooting

### Check Service Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

### Test SSL Certificate
```bash
openssl s_client -connect awtospx.com:443 -servername awtospx.com
```

### Check Nginx Configuration
```bash
docker exec nginx-proxy nginx -t
```

### View Nginx Logs
```bash
docker logs nginx-proxy
```

## 🚨 Common Issues

### SSL Certificate Issues
**Problem**: Certificate not trusted or expired
**Solution**: 
1. Check certificate validity: `openssl x509 -in ssl/awtospx.com.crt -text -noout`
2. Renew Let's Encrypt: `sudo certbot renew`
3. Restart Nginx: `docker-compose -f docker-compose.prod.yml restart nginx`

### DNS Not Working
**Problem**: Domain doesn't resolve to your server
**Solution**:
1. Check DNS propagation: [whatsmydns.net](https://whatsmydns.net)
2. Verify A records in your domain registrar
3. Wait up to 48 hours for full propagation

### Can't Access Grafana
**Problem**: 502 Bad Gateway or connection refused
**Solution**:
1. Check if services are running: `docker ps`
2. Check logs: `docker-compose -f docker-compose.prod.yml logs`
3. Verify firewall settings
4. Check SSL certificate validity

### Port Already in Use
**Problem**: Port 80 or 443 already occupied
**Solution**:
1. Find what's using the port: `sudo lsof -i :80`
2. Stop conflicting service
3. Or change ports in docker-compose.prod.yml

## 📈 Performance Optimization

### Nginx Optimization
```nginx
# Add to nginx.conf for better performance
client_max_body_size 100M;
proxy_buffering on;
proxy_buffer_size 128k;
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;
```

### Grafana Optimization
```yaml
# Add to docker-compose.prod.yml grafana environment
- GF_SERVER_MAX_CONCURRENT_SNAPSHOT_RENDERS=5
- GF_SERVER_MAX_CONCURRENT_QUERIES=10
- GF_DATABASE_MAX_OPEN_CONN=100
```

## 🔄 Backup and Recovery

### Backup Data
```bash
# Backup Grafana data
docker run --rm -v grafana-stack_grafana_data:/data -v $(pwd):/backup alpine tar czf /backup/grafana_backup_$(date +%Y%m%d).tar.gz -C /data .

# Backup Prometheus data
docker run --rm -v grafana-stack_prometheus_data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus_backup_$(date +%Y%m%d).tar.gz -C /data .
```

### Restore Data
```bash
# Restore Grafana data
docker run --rm -v grafana-stack_grafana_data:/data -v $(pwd):/backup alpine tar xzf /backup/grafana_backup_YYYYMMDD.tar.gz -C /data

# Restore Prometheus data
docker run --rm -v grafana-stack_prometheus_data:/data -v $(pwd):/backup alpine tar xzf /backup/prometheus_backup_YYYYMMDD.tar.gz -C /data
```

## ✅ Success Checklist

- [ ] SSL certificates installed and valid
- [ ] DNS A records configured correctly
- [ ] Firewall allows ports 80 and 443
- [ ] Production stack deployed successfully
- [ ] Can access https://awtospx.com
- [ ] Grafana login works (admin/admin)
- [ ] AI service API responds
- [ ] Monitoring data is being collected
- [ ] SSL certificate auto-renewal configured (if using Let's Encrypt)

## 🎉 Congratulations!

Your Grafana monitoring stack is now accessible at **https://awtospx.com** with:
- ✅ Secure HTTPS access
- ✅ Professional domain name
- ✅ SSL certificates
- ✅ Reverse proxy protection
- ✅ Production-ready configuration

You can now share your monitoring dashboard with others using your professional domain! 