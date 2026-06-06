from sqlalchemy.orm import Session

from app.models.user import User
from app.services.auth_service import AuthService


def bootstrap_admin_user(
    db: Session,
    *,
    email: str | None,
    password: str | None,
    full_name: str | None = None,
) -> bool | None:
    """Create/update the Railway bootstrap admin user.

    Returns:
        True when a new user was created.
        False when an existing user was updated.
        None when bootstrap credentials were not provided.
    """
    if not email or not password:
        return None

    user = db.query(User).filter(User.email == email).first()
    password_hash = AuthService.hash_password(password)

    if user is None:
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name or "Admin Harmoniza",
            role="admin",
        )
        db.add(user)
        db.commit()
        return True

    user.password_hash = password_hash
    if full_name:
        user.full_name = full_name
    user.role = user.role or "admin"
    db.commit()
    return False
