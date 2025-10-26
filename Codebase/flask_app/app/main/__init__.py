"""
Main Blueprint
This blueprint contains the main application routes.
"""
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
