# Getting Render IP Addresses for DNS Configuration

Since Squarespace requires IP addresses for root domain (@) records, you'll need to get the specific IP addresses from Render.

## 🔍 Method 1: Contact Render Support (Recommended)

1. **After deploying to Render**, contact Render support
2. **Ask for IP addresses** for your custom domains
3. **Provide your domain**: `awtospx.com`
4. **They will give you** the exact IP addresses to use

## 🔍 Method 2: DNS Lookup (Temporary)

After your services are deployed, you can look up the IP addresses:

```bash
# Look up the IP addresses for your Render services
nslookup grafana-monitoring.onrender.com
nslookup ai-service.onrender.com
nslookup prometheus.onrender.com
```

**Example output:**
```
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
Name:	grafana-monitoring.onrender.com
Address: 76.76.19.123
```

## 🔍 Method 3: Render's IP Ranges

Render typically uses these IP ranges:
- `76.76.19.0/24` (76.76.19.x)
- `76.76.20.0/24` (76.76.20.x)

**Note**: This is a general range and may not be accurate for your specific deployment.

## 📋 DNS Configuration Example

Once you have the IP addresses, configure your Squarespace DNS like this:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 76.76.19.123 | 300 |
| A | www | 76.76.19.123 | 300 |
| CNAME | api | ai-service.onrender.com | 300 |
| CNAME | prometheus | prometheus.onrender.com | 300 |

## ⚠️ Important Notes

- **Root domain (@) requires IP address**, not CNAME
- **Contact Render support** for the most accurate IP addresses
- **IP addresses may change** if you redeploy or restart services
- **Use the same IP** for both @ and www records

## 🚨 Troubleshooting

### IP Address Not Working
1. **Contact Render support** for the correct IP
2. **Check if services are running** in Render dashboard
3. **Verify custom domain** is configured in Render

### DNS Not Propagating
1. **Wait up to 48 hours** for full propagation
2. **Use online DNS checkers**: whatsmydns.net
3. **Clear your DNS cache**: `sudo dscacheutil -flushcache` (macOS)

## 📞 Support Contacts

- **Render Support**: help.render.com
- **Squarespace Support**: support.squarespace.com 