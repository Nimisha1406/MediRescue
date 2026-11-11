import pytest

from app import create_app
from extensions import db
from app.models.user import User


@pytest.fixture
def app():
    """Create a temporary application for testing."""

    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""

    return app.test_client()


def test_home_page_redirects(client):
    response = client.get("/")

    assert response.status_code == 302


def test_user_registration(client):
    response = client.post(
        "/register",
        data={
            "name": "Test Patient",
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "Test@123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    user = User.query.filter_by(
        email="test@example.com"
    ).first()

    assert user is not None
    assert user.name == "Test Patient"
    assert user.role == "patient"


def test_user_login(client):
    with client.application.app_context():
        user = User(
            name="Login Patient",
            email="login@example.com",
            phone="9876543210",
            role="patient"
        )

        user.set_password("Test@123")
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "email": "login@example.com",
            "password": "Test@123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Logout" in response.data


def test_invalid_login(client):
    response = client.post(
        "/login",
        data={
            "email": "wrong@example.com",
            "password": "wrongpassword"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid" in response.data or b"incorrect" in response.data.lower()