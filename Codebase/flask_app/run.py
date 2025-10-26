#!/usr/bin/env python3
"""
Flask Application Entry Point
This file serves as the entry point for the Flask application.
Run this file to start the development server.
"""

import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the Flask app instance
app = create_app()

# Import routes to ensure they are registered
from app.main import routes as main_routes
from app.auth import routes as auth_routes

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    print(f"Starting Flask development server...")
    print(f"Server will be available at: http://{host}:{port}")
    
    # Run the development server
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG']
    )