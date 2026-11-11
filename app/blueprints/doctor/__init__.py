from flask import Blueprint

doctor_bp = Blueprint("doctor", __name__)

from app.blueprints.doctor import routes