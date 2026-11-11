MediRescue – Ambulance Booking & Doctor Consultancy System

About the Project

MediRescue is a web-based healthcare assistance platform developed using Python Flask. It provides patients with a convenient way to book ambulances, access doctor consultancy services, and manage their healthcare activities through a single platform.

The system also includes email OTP verification for secure user registration and login.

Features

- User Authentication: Registration, login, logout and password hashing.
- Email OTP Verification: Six-digit OTP verification during registration and login, with expiry and resend functionality.
- Ambulance Booking: Book available ambulances by entering pickup and destination details.
- Location & Maps: Select pickup locations using an interactive map and browser geolocation.
- Ambulance Routing: Calculate routes and distances using OSRM and geographical distance calculations.
- Doctor Consultancy: View available doctors and book appointments.
- Patient Dashboard: Access healthcare services and manage profile information.
- Admin Dashboard: View application statistics and recent records.
- Role-Based Access: Separate access permissions for patients and administrators.

Technologies Used

Technology| Purpose
Python| Backend programming
Flask| Web framework
SQLite| Database
Flask-SQLAlchemy| Database management
Flask-Login| Authentication
Flask-Mail| Email OTP verification
Flask-WTF| CSRF protection
HTML, CSS, JavaScript| Frontend
Bootstrap 5| Responsive design
Leaflet.js| Interactive maps
OSRM| Road route calculation

Project Structure

MediRescue/
│
├── app/
│   ├── blueprints/
│   │   ├── admin/
│   │   ├── ambulance/
│   │   ├── auth/
│   │   ├── doctor/
│   │   ├── main/
│   │   └── patient/
│   │
│   ├── middleware/
│   ├── models/
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   ├── tests/
│   ├── utils/
│   └── __init__.py
│
├── config.py
├── database.py
├── extensions.py
├── migrate_otp.py
├── requirements.txt
├── run.py
├── .env.example
├── .gitignore
└── README.md

How It Works

1. Registration: A patient creates an account by providing their details.
2. Email Verification: A six-digit OTP is sent to the registered email address. The account becomes verified after successful OTP entry.
3. Login: Users enter their credentials and verify the login OTP before accessing the dashboard.
4. Ambulance Booking: Patients enter pickup and destination details and submit an ambulance booking request.
5. Routing: The system uses geographical coordinates and routing services to calculate routes and distances.
6. Doctor Consultancy: Patients can browse doctors and schedule appointments.
7. Administration: Administrators access a separate dashboard to monitor application information.

Installation and Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd MediRescue

2. Create and activate a virtual environment

python -m venv .venv
.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a ".env" file in the project root:

SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///medirescue.db

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

5. Run the application

python run.py

Open your browser and visit:

http://127.0.0.1:5000/

Database

MediRescue uses SQLite to store user accounts, ambulance details, booking records, doctor information, appointments and email verification data.

Future Enhancements

- Real-time ambulance tracking.
- Automatic nearest-ambulance allocation.
- Online payment integration.
- Video consultation with doctors.
- Emergency notifications.
- Prescription management.
