import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    # Sécurité Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Base de données
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Upload fichiers
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB max

    # Types fichiers autorisés
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

    # URL du frontend (pour liens envoyés par email)
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
