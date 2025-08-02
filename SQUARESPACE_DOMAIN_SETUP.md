# Squarespace Domain Setup with Render

This guide will help you configure your Squarespace domain `awtospx.com` to work with your Render-deployed Grafana monitoring stack.

## 🎯 Overview

Since you're using Squarespace for domain management, we'll need to:
1. Deploy your services to Render
2. Configure Squarespace DNS settings
3. Set up custom domain in Render
4. Configure SSL certificates

## 🚀 Step 1: Deploy to Render

### 1.1 Connect Your Repository
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository: `https://github.com/spncrmt/observe`
4. Render will automatically detect the `render.yaml` file

### 1.2 Deploy Services
1. Render will create three services:
   - **grafana-monitoring**: Your main Grafana dashboard
   - **ai-service**: AI monitoring service
   - **prometheus**: Metrics collection service
2. Click "Apply" to start deployment
3. Wait for all services to deploy (5-10 minutes)

### 1.3 Get Your Render URLs
After deployment, note your service URLs:
- Grafana: `https://grafana-monitoring.onrender.com`
- AI Service: `https://ai-service.onrender.com`
- Prometheus: `https://prometheus.onrender.com`

## 🌐 Step 2: Configure Squarespace DNS

### 2.1 Access Squarespace DNS Settings
1. Log into your Squarespace account
2. Go to **Settings** → **Domains**
3. Click on `awtospx.com`
4. Click **DNS Settings**

### 2.2 Get Render IP Addresses
**Important**: You need to get the IP addresses from Render support or use a DNS lookup tool.

**Option A: Contact Render Support**
1. After deploying to Render, contact Render support
2. Ask for the IP addresses for your custom domains
3. They will provide you with the specific IP addresses

**Option B: Use DNS Lookup (Temporary)**
```bash
# Look up the IP addresses for Render services
nslookup grafana-monitoring.onrender.com
nslookup ai-service.onrender.com
nslookup prometheus.onrender.com
```

**Option C: Use Render's IP Range**
Render typically uses these IP ranges:
- `76.76.19.0/24` (76.76.19.x)
- `76.76.20.0/24` (76.76.20.x)

### 2.3 Add DNS Records
Add these records in your Squarespace DNS settings:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | RENDER_IP_ADDRESS | 300 |
| A | www | RENDER_IP_ADDRESS | 300 |
| CNAME | api | ai-service.onrender.com | 300 |
| CNAME | prometheus | prometheus.onrender.com | 300 |

**Example with placeholder IP:**
- Type: A, Name: @, Value: 76.76.19.123
- Type: A, Name: www, Value: 76.76.19.123
- Type: CNAME, Name: api, Value: ai-service.onrender.com
- Type: CNAME, Name: prometheus, Value: prometheus.onrender.com

### 2.4 Alternative: Use Squarespace Domain Forwarding
If you can't get the exact IP addresses:
1. In Squarespace DNS, set up **Domain Forwarding**
2. Forward `awtospx.com` to `https://grafana-monitoring.onrender.com`
3. Enable **301 Redirect** and **SSL**

## 🔧 Step 3: Configure Custom Domain in Render

### 3.1 Add Custom Domain to Grafana Service
1. In Render dashboard, go to your `grafana-monitoring` service
2. Click **Settings** → **Custom Domains**
3. Click **Add Domain**
4. Enter: `awtospx.com`
5. Click **Add Domain**

### 3.2 Add Subdomains (Optional)
You can also add subdomains:
- `api.awtospx.com` → `ai-service.onrender.com`
- `prometheus.awtospx.com` → `prometheus.onrender.com`

## 🔒 Step 4: SSL Certificate Setup

### 4.1 Automatic SSL (Recommended)
Render automatically provides SSL certificates for custom domains:
1. After adding your domain, Render will provision an SSL certificate
2. This may take 5-10 minutes
3. You'll see a green checkmark when SSL is active

### 4.2 Manual SSL (If Needed)
If automatic SSL fails:
1. Contact Render support for manual SSL setup
2. Or use a third-party SSL provider like Cloudflare

## ⏱️ Step 5: DNS Propagation

After updating DNS settings:
- **Immediate**: Some users may see changes within minutes
- **Typical**: Most users will see changes within 2-24 hours
- **Maximum**: Can take up to 48 hours for global propagation

## 🧪 Step 6: Testing

### 6.1 Test DNS Propagation
```bash
# Test from your local machine
nslookup awtospx.com
dig awtospx.com

# Online DNS checkers
# https://whatsmydns.net
# https://dnschecker.org
```

### 6.2 Test Access
Once DNS has propagated:
- **Main Dashboard**: https://awtospx.com
- **AI Service**: https://api.awtospx.com (if configured)
- **Prometheus**: https://prometheus.awtospx.com (if configured)

## 🔍 Step 7: Troubleshooting

### DNS Issues
**Problem**: Domain doesn't resolve to Render
**Solutions**:
1. Check DNS propagation with online tools
2. Verify A records in Squarespace (must use IP addresses for @ and www)
3. Contact Render support for correct IP addresses
4. Contact Squarespace support if needed

### SSL Issues
**Problem**: SSL certificate not working
**Solutions**:
1. Wait for automatic SSL provisioning (5-10 minutes)
2. Check Render service logs
3. Contact Render support

### Service Not Accessible
**Problem**: 404 or connection errors
**Solutions**:
1. Check if Render services are running
2. Verify custom domain configuration in Render
3. Check service logs in Render dashboard

## 📊 Step 8: Monitoring Your Deployment

### Render Dashboard
- Monitor service health in Render dashboard
- Check logs for any errors
- Monitor resource usage

### Grafana Dashboard
- Access your monitoring dashboard at https://awtospx.com
- Login with admin/admin
- Configure data sources and dashboards

## 🔄 Step 9: Updates and Maintenance

### Automatic Deployments
- Render automatically deploys when you push to GitHub
- Monitor deployment status in Render dashboard

### Manual Updates
1. Make changes to your code
2. Push to GitHub
3. Render automatically redeploys

### Environment Variables
Update environment variables in Render dashboard:
1. Go to your service in Render
2. Click **Environment**
3. Add/modify environment variables
4. Redeploy service

## ✅ Success Checklist

- [ ] Services deployed to Render successfully
- [ ] DNS A records configured in Squarespace (using IP addresses)
- [ ] Custom domain added to Render
- [ ] SSL certificate provisioned
- [ ] DNS propagation completed
- [ ] Can access https://awtospx.com
- [ ] Grafana login works (admin/admin)
- [ ] AI service responds
- [ ] Monitoring data is being collected

## 🎉 Congratulations!

Your Grafana monitoring stack is now accessible at **https://awtospx.com** with:
- ✅ Render cloud hosting
- ✅ Squarespace domain integration
- ✅ Automatic SSL certificates
- ✅ Professional domain name
- ✅ Scalable cloud infrastructure

## 📞 Support Resources

- **Render Support**: [help.render.com](https://help.render.com)
- **Squarespace Support**: [support.squarespace.com](https://support.squarespace.com)
- **DNS Propagation**: [whatsmydns.net](https://whatsmydns.net)
- **SSL Checker**: [sslshopper.com](https://sslshopper.com) 