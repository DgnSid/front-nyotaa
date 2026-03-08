from app.extensions import db
import uuid
from datetime import datetime

class CandidateProfile(db.Model):
    __tablename__ = "candidate_profiles"

    # Changement en String(36) pour le CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # La clé étrangère doit correspondre au type String(36) du compte
    candidate_account_id = db.Column(
        db.String(36),
        db.ForeignKey("candidate_accounts.id"),
        nullable=False,
        unique=True
    )

    # L'Enum doit correspondre exactement aux valeurs de votre script SQL
    gender = db.Column(
        db.Enum("Homme", "Femme", "Autre"),
        nullable=True
    )

    birth_date = db.Column(db.Date, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    main_field = db.Column(db.String(150), nullable=True)
    short_bio = db.Column(db.Text, nullable=True)

    # Utilisation de datetime.now pour la cohérence locale
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )