from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

# Database
db = SQLAlchemy()

# Login manager
login_manager = LoginManager()

login_manager.login_view = "auth.login"

login_manager.login_message = (
    "Please login to access this page."
)

login_manager.login_message_category = "warning"

# CSRF protection
csrf = CSRFProtect()

# Email service
mail = Mail()