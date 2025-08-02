# DNS Setup Guide for awtospx.com

This guide will help you configure your DNS settings to point your domain to your Grafana monitoring stack.

## 🎯 Overview

You need to configure your domain registrar's DNS settings to point `awtospx.com` to your server's IP address.

## 📋 Prerequisites

1. **Domain Registrar Access**: You need access to your domain registrar's DNS management panel
2. **Server IP Address**: Your server's public IP address where Grafana will be hosted
3. **Domain Ownership**: You must own `awtospx.com`

## 🔍 Find Your Server IP

### If you're hosting on a cloud provider:

**AWS EC2:**
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

**Google Cloud:**
```bash
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip
```

**DigitalOcean:**
```bash
curl http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address
```

**VPS/Home Server:**
```bash
curl ifconfig.me
```

## 🌐 DNS Configuration

### Step 1: Access Your Domain Registrar

Log into your domain registrar's website (e.g., GoDaddy, Namecheap, Cloudflare, etc.)

### Step 2: Find DNS Management

Look for:
- "DNS Management"
- "DNS Settings"
- "Domain Management" → "DNS"
- "Nameservers" or "DNS Records"

### Step 3: Add DNS Records

Add these **A records**:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_SERVER_IP | 300 |
| A | www | YOUR_SERVER_IP | 300 |

**Example:**
- If your server IP is `203.0.113.1`:
  - Type: A, Name: @, Value: 203.0.113.1
  - Type: A, Name: www, Value: 203.0.113.1

### Step 4: Optional - CNAME Records

You can also add CNAME records for subdomains:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | grafana | awtospx.com | 300 |
| CNAME | monitoring | awtospx.com | 300 |

## 🔧 Popular Domain Registrars

### GoDaddy
1. Log into GoDaddy
2. Go to "My Products" → "DNS"
3. Click "Manage" next to your domain
4. Scroll to "DNS Records"
5. Click "Add" to create new records

### Namecheap
1. Log into Namecheap
2. Go to "Domain List" → "Manage"
3. Click "Advanced DNS"
4. Add A records in the "Host Records" section

### Cloudflare
1. Log into Cloudflare
2. Select your domain
3. Go to "DNS" → "Records"
4. Click "Add record"
5. Set Type to "A" and enter your server IP

### Google Domains
1. Log into Google Domains
2. Select your domain
3. Go to "DNS" → "Synthetic records"
4. Add A records with your server IP

## ⏱️ DNS Propagation

After updating DNS records:

- **Immediate**: Some users may see changes within minutes
- **Typical**: Most users will see changes within 2-24 hours
- **Maximum**: Can take up to 48 hours for global propagation

## 🧪 Testing DNS Configuration

### Test from your server:
```bash
nslookup awtospx.com
dig awtospx.com
```

### Test from your local machine:
```bash
nslookup awtospx.com
ping awtospx.com
```

### Online DNS checkers:
- [whatsmydns.net](https://whatsmydns.net)
- [dnschecker.org](https://dnschecker.org)
- [mxtoolbox.com](https://mxtoolbox.com)

## 🔒 Security Considerations

### Firewall Configuration
Ensure your server allows incoming traffic on these ports:
- **Port 80**: HTTP (for SSL redirect)
- **Port 443**: HTTPS (for secure access)

### Example UFW Commands (Ubuntu):
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Example iptables Commands:
```bash
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## 🚨 Troubleshooting

### DNS Not Propagating
1. **Wait longer**: DNS changes can take up to 48 hours
2. **Clear DNS cache**: `sudo systemctl restart systemd-resolved`
3. **Use different DNS**: Try 8.8.8.8 or 1.1.1.1
4. **Check registrar**: Ensure changes were saved

### Can't Access Grafana
1. **Check server**: Ensure Grafana is running
2. **Check firewall**: Verify ports 80/443 are open
3. **Check SSL**: Ensure certificates are valid
4. **Check logs**: `docker-compose -f docker-compose.prod.yml logs`

### SSL Certificate Issues
1. **Domain mismatch**: Ensure certificate matches domain
2. **DNS not ready**: Wait for DNS propagation before getting certificates
3. **Port 80 blocked**: Let's Encrypt needs port 80 for verification

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your DNS settings match the examples
3. Test with online DNS checkers
4. Contact your domain registrar's support

## ✅ Verification Checklist

- [ ] DNS A records added for `@` and `www`
- [ ] Server IP address is correct
- [ ] Firewall allows ports 80 and 443
- [ ] SSL certificates are installed
- [ ] Grafana stack is running
- [ ] DNS propagation completed (tested with online tools)
- [ ] Can access https://awtospx.com 