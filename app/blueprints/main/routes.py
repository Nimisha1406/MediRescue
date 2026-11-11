from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.blueprints.main import main_bp


@main_bp.route("/")
def home():

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("main.dashboard"))

    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role == "admin":
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "main/dashboard.html",
        user=current_user
    )