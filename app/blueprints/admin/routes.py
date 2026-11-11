from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.blueprints.admin import admin_bp

from app.models.user import User
from app.models.ambulance import Ambulance
from app.models.doctor import Doctor
from app.models.booking import Booking
from app.models.appointment import Appointment


def admin_required():
    return (
        current_user.is_authenticated
        and current_user.role == "admin"
    )


@admin_bp.route("/dashboard")
@login_required
def dashboard():

    if not admin_required():
        flash(
            "You are not authorized to access the admin dashboard.",
            "danger"
        )
        return redirect(url_for("main.dashboard"))

    total_users = User.query.filter_by(
        role="patient"
    ).count()

    total_ambulances = Ambulance.query.count()

    available_ambulances = Ambulance.query.filter_by(
        status="available"
    ).count()

    total_doctors = Doctor.query.count()

    total_bookings = Booking.query.count()

    total_appointments = Appointment.query.count()

    recent_bookings = Booking.query.order_by(
        Booking.created_at.desc()
    ).limit(5).all()

    recent_appointments = Appointment.query.order_by(
        Appointment.created_at.desc()
    ).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_ambulances=total_ambulances,
        available_ambulances=available_ambulances,
        total_doctors=total_doctors,
        total_bookings=total_bookings,
        total_appointments=total_appointments,
        recent_bookings=recent_bookings,
        recent_appointments=recent_appointments
    )