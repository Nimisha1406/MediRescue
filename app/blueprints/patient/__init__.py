from flask import Blueprint

patient_bp = Blueprint("patient", __name__)

from app.blueprints.patient import routes