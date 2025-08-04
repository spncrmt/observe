from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "service": "AI Observability Platform",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "test": "/test",
            "chat": "/chat"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "AI Observability Platform",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({
        "status": "running",
        "message": "AI service is working!",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/chat', methods=['GET'])
def chat():
    """Simple chat interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Chat Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1e1e1e; color: white; }
            .chat { max-width: 600px; margin: 0 auto; }
            .message { background: #2d2d2d; padding: 15px; margin: 10px 0; border-radius: 8px; }
            .user { background: #0066cc; }
            .ai { background: #00cc66; }
        </style>
    </head>
    <body>
        <div class="chat">
            <h1>🤖 AI Chat Test</h1>
            <div class="message ai">
                <strong>AI:</strong> Hello! I'm your AI assistant. The service is working correctly.
            </div>
            <div class="message user">
                <strong>You:</strong> Great! The AI service is responding.
            </div>
            <div class="message ai">
                <strong>AI:</strong> Yes! This means the deployment is successful. You can now use the full chat interface.
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 