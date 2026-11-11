from flask import Blueprint

ambulance_bp = Blueprint("ambulance", __name__)

from app.blueprints.ambulance import routes