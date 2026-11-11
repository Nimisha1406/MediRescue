from app import create_app
from extensions import db
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():

    inspector = inspect(db.engine)

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    new_columns = {
        "is_email_verified": 
            "BOOLEAN NOT NULL DEFAULT 0",

        "otp_hash": 
            "VARCHAR(256)",

        "otp_expires_at": 
            "DATETIME",

        "otp_purpose": 
            "VARCHAR(20)"
    }

    with db.engine.begin() as connection:

        for column_name, column_type in new_columns.items():

            if column_name not in existing_columns:

                connection.execute(
                    text(
                        f"ALTER TABLE users "
                        f"ADD COLUMN {column_name} {column_type}"
                    )
                )

                print(f"Added column: {column_name}")

            else:
                print(f"Already exists: {column_name}")

    print("\nOTP database migration completed!")