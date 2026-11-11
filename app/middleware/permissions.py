from functools import wraps
from flask import abort
from flask_login import current_user, login_required


def role_required(*allowed_roles):
    """
    Restrict access to users with specific roles.
    Example: @role_required("admin")
    """

    def decorator(func):

        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):

            if current_user.role not in allowed_roles:
                abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def admin_required(func):
    """Allow access only to administrators."""
    return role_required("admin")(func)


def doctor_required(func):
    """Allow access only to doctors."""
    return role_required("doctor")(func)


def patient_required(func):
    """Allow access only to patients."""
    return role_required("patient")(func)