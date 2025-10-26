"""
Flask Application Factory
This module contains the application factory function.
"""
import os
from flask import Flask


def create_app():
    """Create and configure the Flask application."""
    # Get the base directory (flask_app folder)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Configure Flask to look for templates and static files in the correct location
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app
