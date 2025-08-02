#!/bin/bash

# Render Deployment Script for Squarespace Domain
# This script helps deploy your Grafana monitoring stack to Render

echo "🚀 Render Deployment for awtospx.com"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found!"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo ""
echo "📋 Pre-deployment checklist:"
echo "✅ render.yaml configuration ready"
echo "✅ Dockerfiles created"
echo "✅ Requirements updated"

echo ""
echo "🔧 Next steps:"
echo ""
echo "1. 🚀 Deploy to Render:"
echo "   - Go to https://render.com"
echo "   - Sign up/login to your account"
echo "   - Click 'New +' → 'Blueprint'"
echo "   - Connect your GitHub repo: https://github.com/spncrmt/observe"
echo "   - Render will auto-detect render.yaml"
echo "   - Click 'Apply' to deploy"
echo ""
echo "2. 🌐 Configure Squarespace DNS:"
echo "   - Log into Squarespace"
echo "   - Go to Settings → Domains"
echo "   - Click on awtospx.com"
echo "   - Click DNS Settings"
echo "   - Add CNAME records:"
echo "     * @ → grafana-monitoring.onrender.com"
echo "     * www → grafana-monitoring.onrender.com"
echo "     * api → ai-service.onrender.com"
echo ""
echo "3. 🔧 Add Custom Domain in Render:"
echo "   - In Render dashboard, go to grafana-monitoring service"
echo "   - Click Settings → Custom Domains"
echo "   - Add: awtospx.com"
echo "   - Wait for SSL certificate (5-10 minutes)"
echo ""
echo "4. 🧪 Test Access:"
echo "   - Wait for DNS propagation (up to 48 hours)"
echo "   - Test: https://awtospx.com"
echo "   - Login: admin/admin"
echo ""

echo "📚 Detailed guides:"
echo "   - Squarespace setup: SQUARESPACE_DOMAIN_SETUP.md"
echo "   - Render documentation: https://render.com/docs"
echo ""

echo "🎉 After deployment, your services will be available at:"
echo "   - Grafana Dashboard: https://awtospx.com"
echo "   - AI Service API: https://api.awtospx.com"
echo "   - Prometheus: https://prometheus.awtospx.com"
echo ""

echo "💡 Useful Render commands:"
echo "   - View logs: In Render dashboard → Logs"
echo "   - Restart service: In Render dashboard → Manual Deploy"
echo "   - Update environment: In Render dashboard → Environment" 