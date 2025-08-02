#!/bin/bash

# Deploy Grafana Stack to Domain Script
# This script helps deploy your Grafana monitoring stack to awtospx.com

DOMAIN="awtospx.com"
CURRENT_DIR=$(pwd)

echo "🚀 Deploying Grafana Stack to $DOMAIN"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "❌ Error: docker-compose.prod.yml not found!"
    echo "Please run this script from the grafana-stack directory"
    exit 1
fi

# Check if SSL certificates exist
if [ ! -f "ssl/$DOMAIN.crt" ] || [ ! -f "ssl/$DOMAIN.key" ]; then
    echo "❌ SSL certificates not found!"
    echo "Please run ./setup-ssl.sh first to set up SSL certificates"
    exit 1
fi

echo ""
echo "🔍 Pre-deployment checks:"
echo "✅ SSL certificates found"
echo "✅ Production docker-compose file found"

# Stop existing containers
echo ""
echo "🛑 Stopping existing containers..."
docker-compose down

# Backup existing data
echo ""
echo "💾 Backing up existing data..."
if [ -d "grafana_data" ]; then
    tar -czf "grafana_backup_$(date +%Y%m%d_%H%M%S).tar.gz" grafana_data/
    echo "✅ Grafana data backed up"
fi

if [ -d "prometheus_data" ]; then
    tar -czf "prometheus_backup_$(date +%Y%m%d_%H%M%S).tar.gz" prometheus_data/
    echo "✅ Prometheus data backed up"
fi

# Start production stack
echo ""
echo "🚀 Starting production stack..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to start
echo ""
echo "⏳ Waiting for services to start..."
sleep 30

# Check service status
echo ""
echo "🔍 Checking service status..."
docker-compose -f docker-compose.prod.yml ps

# Test connectivity
echo ""
echo "🧪 Testing connectivity..."
if curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN | grep -q "200\|302"; then
    echo "✅ Grafana is accessible at https://$DOMAIN"
else
    echo "⚠️  Grafana may not be accessible yet. Please check:"
    echo "   1. DNS is pointing to your server IP"
    echo "   2. Ports 80 and 443 are open on your server"
    echo "   3. Firewall allows incoming traffic"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📊 Access your services:"
echo "   Grafana Dashboard: https://$DOMAIN"
echo "   AI Service API: https://$DOMAIN/api/"
echo "   Prometheus (admin): https://$DOMAIN/prometheus/"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "   Stop services: docker-compose -f docker-compose.prod.yml down"
echo "   Restart services: docker-compose -f docker-compose.prod.yml restart"
echo ""
echo "📚 Next steps:"
echo "   1. Update your DNS settings to point $DOMAIN to your server IP"
echo "   2. Configure your domain registrar's DNS settings"
echo "   3. Wait for DNS propagation (can take up to 48 hours)"
echo "   4. Test access at https://$DOMAIN" 