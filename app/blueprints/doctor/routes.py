from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from extensions import db

from app.blueprints.doctor import doctor_bp
from app.models.doctor import Doctor
from app.models.appointment import Appointment


@doctor_bp.route("/")
@login_required
def doctor_list():

    doctors = Doctor.query.all()

    return render_template(
        "doctor/list.html",
        doctors=doctors
    )


@doctor_bp.route("/book/<int:doctor_id>", methods=["GET", "POST"])
@login_required
def book_appointment(doctor_id):

    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == "POST":

        appointment_date = request.form.get(
            "appointment_date"
        )

        appointment_time = request.form.get(
            "appointment_time"
        )

        reason = request.form.get("reason")

        if not appointment_date or not appointment_time:

            flash(
                "Please select an appointment date and time.",
                "danger"
            )

            return redirect(
                url_for(
                    "doctor.book_appointment",
                    doctor_id=doctor_id
                )
            )

        try:
            date_value = datetime.strptime(
                appointment_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            flash(
                "Invalid appointment date.",
                "danger"
            )

            return redirect(
                url_for(
                    "doctor.book_appointment",
                    doctor_id=doctor_id
                )
            )

        if date_value < datetime.today().date():

            flash(
                "Please select a future date.",
                "danger"
            )

            return redirect(
                url_for(
                    "doctor.book_appointment",
                    doctor_id=doctor_id
                )
            )

        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor.id,
            appointment_date=date_value,
            appointment_time=appointment_time,
            reason=reason,
            status="pending"
        )

        db.session.add(appointment)
        db.session.commit()

        flash(
            "Appointment request submitted successfully!",
            "success"
        )

        return redirect(
            url_for("doctor.my_appointments")
        )

    return render_template(
        "doctor/book.html",
        doctor=doctor,
        today=datetime.today().strftime("%Y-%m-%d")
    )


@doctor_bp.route("/my-appointments")
@login_required
def my_appointments():

    appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).order_by(
        Appointment.created_at.desc()
    ).all()

    return render_template(
        "doctor/appointments.html",
        appointments=appointments
    )