from app import create_app
from database import init_database

app = create_app()

if __name__ == "__main__":

    init_database(app)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )