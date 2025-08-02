#!/bin/bash

# SSL Certificate Setup Script for awtospx.com
# This script helps you set up SSL certificates for your Grafana domain

DOMAIN="awtospx.com"
EMAIL="your-email@example.com"  # Change this to your email

echo "🔐 SSL Certificate Setup for $DOMAIN"
echo "======================================"

# Create SSL directory
mkdir -p ssl

echo ""
echo "📋 Choose your SSL certificate method:"
echo "1. Let's Encrypt (Free, automatic renewal)"
echo "2. Self-signed certificate (Development only)"
echo "3. Upload your own certificate"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🔧 Setting up Let's Encrypt certificate..."
        
        # Check if certbot is installed
        if ! command -v certbot &> /dev/null; then
            echo "❌ Certbot not found. Installing..."
            if [[ "$OSTYPE" == "darwin"* ]]; then
                brew install certbot
            else
                sudo apt-get update
                sudo apt-get install -y certbot
            fi
        fi
        
        # Get certificate
        sudo certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive
        
        # Copy certificates to ssl directory
        sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ssl/$DOMAIN.crt
        sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ssl/$DOMAIN.key
        sudo chown $USER:$USER ssl/$DOMAIN.crt ssl/$DOMAIN.key
        
        echo "✅ Let's Encrypt certificate installed!"
        echo "📅 Certificate will auto-renew. Add to crontab:"
        echo "0 12 * * * /usr/bin/certbot renew --quiet"
        ;;
        
    2)
        echo "🔧 Creating self-signed certificate..."
        
        # Generate self-signed certificate
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ssl/$DOMAIN.key \
            -out ssl/$DOMAIN.crt \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
        
        echo "✅ Self-signed certificate created!"
        echo "⚠️  Note: Self-signed certificates will show browser warnings"
        ;;
        
    3)
        echo "📁 Please place your certificate files in the ssl/ directory:"
        echo "   - Certificate file: ssl/$DOMAIN.crt"
        echo "   - Private key file: ssl/$DOMAIN.key"
        echo ""
        echo "Then run this script again to verify the files."
        
        if [ -f "ssl/$DOMAIN.crt" ] && [ -f "ssl/$DOMAIN.key" ]; then
            echo "✅ Certificate files found!"
        else
            echo "❌ Certificate files not found in ssl/ directory"
            exit 1
        fi
        ;;
        
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🔍 Verifying certificate files..."
if [ -f "ssl/$DOMAIN.crt" ] && [ -f "ssl/$DOMAIN.key" ]; then
    echo "✅ Certificate files are ready!"
    echo "📄 Certificate details:"
    openssl x509 -in ssl/$DOMAIN.crt -text -noout | grep -E "(Subject:|Not Before:|Not After:)"
else
    echo "❌ Certificate files not found!"
    exit 1
fi

echo ""
echo "🚀 Next steps:"
echo "1. Update your DNS to point awtospx.com to your server IP"
echo "2. Run: docker-compose -f docker-compose.prod.yml up -d"
echo "3. Access your Grafana at: https://awtospx.com"
echo ""
echo "📚 For DNS setup, add these records:"
echo "   Type: A"
echo "   Name: awtospx.com"
echo "   Value: YOUR_SERVER_IP"
echo ""
echo "   Type: A" 
echo "   Name: www.awtospx.com"
echo "   Value: YOUR_SERVER_IP" 