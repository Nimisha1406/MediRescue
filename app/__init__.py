from flask import Flask

from config import Config
from extensions import db, login_manager, csrf, mail


def create_app():

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    # Import models
    from app.models.user import User

    # Configure user loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Import blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.patient import patient_bp
    from app.blueprints.ambulance import ambulance_bp
    from app.blueprints.doctor import doctor_bp
    from app.blueprints.admin import admin_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(
        patient_bp,
        url_prefix="/patient"
    )
    app.register_blueprint(
        ambulance_bp,
        url_prefix="/ambulance"
    )
    app.register_blueprint(
        doctor_bp,
        url_prefix="/doctor"
    )
    app.register_blueprint(
        admin_bp,
        url_prefix="/admin"
    )

    return app