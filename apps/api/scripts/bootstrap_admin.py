import os

from app.db.session import SessionLocal
from app.deploy.bootstrap_admin import bootstrap_admin_user


def main() -> None:
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    full_name = os.getenv("ADMIN_FULL_NAME", "Admin Harmoniza")

    with SessionLocal() as db:
        result = bootstrap_admin_user(
            db,
            email=email,
            password=password,
            full_name=full_name,
        )

    if result is True:
        print(f"Created admin user: {email}")
    elif result is False:
        print(f"Updated admin user: {email}")
    else:
        print("Skipped admin bootstrap: ADMIN_EMAIL/ADMIN_PASSWORD not set")


if __name__ == "__main__":
    main()
