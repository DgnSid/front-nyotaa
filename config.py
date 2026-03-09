import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def _build_database_config():
    default_url = "mysql+pymysql://root:@localhost:3306/nyota"
    raw_url = os.getenv("DATABASE_URL", default_url)

    if raw_url.startswith("mysql://"):
        raw_url = "mysql+pymysql://" + raw_url[len("mysql://"):]

    parsed = urlsplit(raw_url)
    query_params = parse_qsl(parsed.query, keep_blank_values=True)

    ssl_mode = None
    filtered_params = []
    for key, value in query_params:
        lowered = key.lower()
        if lowered in {"ssl-mode", "ssl_mode"}:
            ssl_mode = value.upper()
            continue
        filtered_params.append((key, value))

    normalized_url = urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urlencode(filtered_params, doseq=True),
            parsed.fragment,
        )
    )

    engine_options = {}
    if ssl_mode in {"REQUIRED", "VERIFY_CA", "VERIFY_IDENTITY"}:
        engine_options["connect_args"] = {"ssl": {}}

    return normalized_url, engine_options

class Config:
    # Clé secrète pour Flask (sessions, etc.)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_NYOTA_2026")

    # Configuration JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_super_secret_key_NYOTA")

    # Configuration Base de données — MySQL via phpMyAdmin
    SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ENGINE_OPTIONS = _build_database_config()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration Emails (Resend ou SMTP Gmail)
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "tonemail@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "onzb xnat ifew svwc")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "tonemail@gmail.com")
