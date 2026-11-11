from extensions import db
from app.models.user import User
from app.models.ambulance import Ambulance
from app.models.doctor import Doctor
from app.models.booking import Booking
from app.models.appointment import Appointment


def init_database(app):

    with app.app_context():

        db.create_all()

        # Create administrator

        admin = User.query.filter_by(
            email="admin@medirescue.local"
        ).first()

        if admin is None:

            admin = User(
                name="MediRescue Admin",
                email="admin@medirescue.local",
                phone="0000000000",
                role="admin"
            )

            admin.set_password("Admin@123")

            db.session.add(admin)

        # Sample ambulance fleet

        if Ambulance.query.count() == 0:

            ambulances = [

                Ambulance(
                    vehicle_no="WB-38A-1001",
                    driver_name="Rakesh Kumar",
                    phone="9000000001",
                    latitude=23.6889,
                    longitude=86.9661,
                    status="available"
                ),

                Ambulance(
                    vehicle_no="WB-38A-1002",
                    driver_name="Amit Singh",
                    phone="9000000002",
                    latitude=23.6730,
                    longitude=86.9520,
                    status="available"
                ),

                Ambulance(
                    vehicle_no="WB-38A-1003",
                    driver_name="Suman Das",
                    phone="9000000003",
                    latitude=23.7050,
                    longitude=86.9900,
                    status="available"
                )
            ]

            db.session.add_all(ambulances)

        # Sample doctors

        if Doctor.query.count() == 0:

            doctors = [

                Doctor(
                    name="Dr. Ananya Sen",
                    specialty="General Physician",
                    qualification="MBBS, MD",
                    phone="9000010001",
                    consultation_fee=400
                ),

                Doctor(
                    name="Dr. Rahul Roy",
                    specialty="Cardiologist",
                    qualification="MBBS, DM Cardiology",
                    phone="9000010002",
                    consultation_fee=800
                ),

                Doctor(
                    name="Dr. Priya Das",
                    specialty="Pediatrician",
                    qualification="MBBS, MD Pediatrics",
                    phone="9000010003",
                    consultation_fee=500
                ),

                Doctor(
                    name="Dr. Arjun Sharma",
                    specialty="Orthopedic",
                    qualification="MBBS, MS Orthopedics",
                    phone="9000010004",
                    consultation_fee=600
                )
            ]

            db.session.add_all(doctors)

        db.session.commit()

        print("MediRescue database initialized!")