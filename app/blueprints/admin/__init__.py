from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

from app.blueprints.doctor import routes