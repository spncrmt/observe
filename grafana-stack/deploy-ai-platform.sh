#!/bin/bash

# AI-Integrated Observability Platform Deployment Script
# ===================================================

set -e

echo "🚀 Deploying AI-Integrated Observability Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_status "Checking Docker installation..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Build and start the stack
deploy_stack() {
    print_status "Building and starting the AI observability stack..."
    
    # Stop existing containers
    docker-compose down 2>/dev/null || true
    
    # Build and start
    docker-compose up -d --build
    
    print_success "Stack deployment initiated"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for Prometheus
    print_status "Waiting for Prometheus..."
    until curl -s http://localhost:9090/api/v1/query?query=up > /dev/null 2>&1; do
        sleep 2
    done
    print_success "Prometheus is ready"
    
    # Wait for Grafana
    print_status "Waiting for Grafana..."
    until curl -s http://localhost:3000/api/health > /dev/null 2>&1; do
        sleep 2
    done
    print_success "Grafana is ready"
    
    # Wait for AI Service
    print_status "Waiting for AI Service..."
    until curl -s http://localhost:5001/health > /dev/null 2>&1; do
        sleep 2
    done
    print_success "AI Service is ready"
}

# Test AI service capabilities
test_ai_service() {
    print_status "Testing AI service capabilities..."
    
    # Test health endpoint
    if curl -s http://localhost:5001/health | grep -q "healthy"; then
        print_success "AI service health check passed"
    else
        print_warning "AI service health check failed"
    fi
    
    # Test capabilities endpoint
    if curl -s http://localhost:5001/api/capabilities > /dev/null; then
        print_success "AI service capabilities endpoint working"
    else
        print_warning "AI service capabilities endpoint failed"
    fi
    
    # Test demo endpoint
    if curl -s -X POST http://localhost:5001/api/demo \
        -H "Content-Type: application/json" \
        -d '{"type":"create_panel"}' > /dev/null; then
        print_success "AI service demo endpoint working"
    else
        print_warning "AI service demo endpoint failed"
    fi
}

# Import dashboards
import_dashboards() {
    print_status "Importing dashboards..."
    
    # Wait a bit more for Grafana to be fully ready
    sleep 5
    
    # Import the working dashboard
    if [ -f "working-dashboard.json" ]; then
        print_status "Importing working dashboard..."
        # Note: Manual import required through Grafana UI
        print_warning "Please manually import working-dashboard.json through Grafana UI"
    fi
    
    # Import AI assistant dashboard
    if [ -f "ai-assistant-panel.json" ]; then
        print_status "Importing AI assistant dashboard..."
        # Note: Manual import required through Grafana UI
        print_warning "Please manually import ai-assistant-panel.json through Grafana UI"
    fi
}

# Display access information
show_access_info() {
    echo ""
    echo "🎉 AI-Integrated Observability Platform is ready!"
    echo ""
    echo "📊 Access Points:"
    echo "  • Grafana Dashboard: http://localhost:3000 (admin/admin)"
    echo "  • Prometheus: http://localhost:9090"
    echo "  • AI Service: http://localhost:5001"
    echo ""
    echo "🤖 AI Assistant Features:"
    echo "  • Natural language panel creation"
    echo "  • Query explanation and analysis"
    echo "  • Anomaly detection"
    echo "  • Context-aware responses"
    echo ""
    echo "📋 Next Steps:"
    echo "  1. Open Grafana at http://localhost:3000"
    echo "  2. Login with admin/admin"
    echo "  3. Import dashboards manually:"
    echo "     - working-dashboard.json"
    echo "     - ai-assistant-panel.json"
    echo "  4. Test AI features by asking questions like:"
    echo "     - 'Create a panel showing CPU usage'"
    echo "     - 'Explain this query'"
    echo "     - 'Check for anomalies in memory'"
    echo ""
    echo "🔧 AI Service Endpoints:"
    echo "  • Health: http://localhost:5001/health"
    echo "  • Capabilities: http://localhost:5001/api/capabilities"
    echo "  • Process Request: http://localhost:5001/ai/api/process"
    echo ""
    echo "📈 Monitor the stack:"
    echo "  • docker-compose ps"
    echo "  • docker-compose logs -f ai-service"
    echo ""
}

# Main deployment
main() {
    echo "🤖 AI-Integrated Observability Platform"
    echo "======================================"
    echo ""
    
    check_docker
    deploy_stack
    wait_for_services
    test_ai_service
    import_dashboards
    show_access_info
    
    print_success "Deployment completed successfully!"
}

# Run main function
main "$@" 