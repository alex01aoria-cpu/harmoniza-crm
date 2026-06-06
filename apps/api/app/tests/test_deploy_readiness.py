from app.core.config import Settings
from app.deploy.bootstrap_admin import bootstrap_admin_user
from app.models.user import User
from app.services.auth_service import AuthService


def test_settings_parses_comma_separated_cors_origins() -> None:
    settings = Settings(cors_origins="https://crm.harmoniza.com.br, https://app.railway.app")

    assert settings.cors_origins_list == [
        "https://crm.harmoniza.com.br",
        "https://app.railway.app",
    ]


def test_settings_normalizes_wrapped_quotes_in_database_url() -> None:
    settings = Settings(database_url='"postgresql://user:pass@db.railway.internal:5432/harmoniza"')

    assert settings.database_url == "postgresql://user:pass@db.railway.internal:5432/harmoniza"


def test_settings_normalizes_wrapped_quotes_in_secret_key() -> None:
    settings = Settings(secret_key='"short-prod-key-2026-railway-ready-45chars"')

    assert settings.secret_key == "short-prod-key-2026-railway-ready-45chars"


def test_bootstrap_admin_creates_user_when_env_values_are_present(db_session) -> None:
    created = bootstrap_admin_user(
        db_session,
        email="admin@harmoniza.com",
        password="SenhaForte123!",
        full_name="Admin Harmoniza",
    )

    assert created is True
    user = db_session.query(User).filter(User.email == "admin@harmoniza.com").one()
    assert user.full_name == "Admin Harmoniza"
    assert user.role == "admin"
    assert AuthService.verify_password("SenhaForte123!", user.password_hash)


def test_bootstrap_admin_updates_existing_user_password(db_session) -> None:
    db_session.add(
        User(
            email="admin@harmoniza.com",
            password_hash=AuthService.hash_password("senha-antiga"),
            full_name="Nome Antigo",
            role="admin",
        )
    )
    db_session.commit()

    created = bootstrap_admin_user(
        db_session,
        email="admin@harmoniza.com",
        password="SenhaNova123!",
        full_name="Admin Novo",
    )

    assert created is False
    user = db_session.query(User).filter(User.email == "admin@harmoniza.com").one()
    assert user.full_name == "Admin Novo"
    assert AuthService.verify_password("SenhaNova123!", user.password_hash)
