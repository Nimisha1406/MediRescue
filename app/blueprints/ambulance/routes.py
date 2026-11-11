from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from extensions import db

from app.blueprints.ambulance import ambulance_bp
from app.models.ambulance import Ambulance
from app.models.booking import Booking


@ambulance_bp.route("/")
@login_required
def available_ambulances():

    ambulances = Ambulance.query.filter_by(
        status="available"
    ).all()

    return render_template(
        "ambulance/available.html",
        ambulances=ambulances
    )


@ambulance_bp.route("/book", methods=["GET", "POST"])
@login_required
def book_ambulance():

    ambulances = Ambulance.query.filter_by(
        status="available"
    ).all()

    if request.method == "POST":

        pickup = request.form.get("pickup_location")
        destination = request.form.get("destination")

        emergency_type = request.form.get(
            "emergency_type",
            "General"
        )

        if not pickup or not destination:
            flash(
                "Please enter pickup and destination.",
                "danger"
            )
            return redirect(url_for("ambulance.book_ambulance"))

        try:
            pickup_latitude = float(
                request.form.get("pickup_latitude")
            )

            pickup_longitude = float(
                request.form.get("pickup_longitude")
            )

            destination_latitude = float(
                request.form.get("destination_latitude")
            )

            destination_longitude = float(
                request.form.get("destination_longitude")
            )

        except (TypeError, ValueError):

            flash(
                "Please select valid pickup and destination coordinates.",
                "danger"
            )

            return redirect(url_for("ambulance.book_ambulance"))

        if not ambulances:

            flash(
                "No ambulances are currently available.",
                "warning"
            )

            return redirect(url_for("ambulance.book_ambulance"))

        # Select an available ambulance
        selected_ambulance = ambulances[0]

        booking = Booking(
            patient_id=current_user.id,
            ambulance_id=selected_ambulance.id,
            pickup_location=pickup,
            destination=destination,
            pickup_latitude=pickup_latitude,
            pickup_longitude=pickup_longitude,
            destination_latitude=destination_latitude,
            destination_longitude=destination_longitude,
            emergency_type=emergency_type,
            status="pending"
        )

        selected_ambulance.status = "booked"

        db.session.add(booking)
        db.session.commit()

        flash(
            "Ambulance booking created successfully!",
            "success"
        )

        return redirect(
            url_for("ambulance.my_bookings")
        )

    return render_template(
        "ambulance/book.html",
        ambulances=ambulances
    )


@ambulance_bp.route("/my-bookings")
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        patient_id=current_user.id
    ).order_by(
        Booking.created_at.desc()
    ).all()

    return render_template(
        "ambulance/my_bookings.html",
        bookings=bookings
    )