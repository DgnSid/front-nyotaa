from app.extensions import db
import uuid
from datetime import datetime

class PersonalityProfile(db.Model):
    __tablename__ = "personality_profiles"

    # String(36) pour correspondre au CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Clés étrangères : doivent correspondre aux types String(36) des tables parentes
    candidate_profile_id = db.Column(
        db.String(36),
        db.ForeignKey("candidate_profiles.id"),
        nullable=False
    )

    personality_test_id = db.Column(
        db.String(36),
        db.ForeignKey("personality_tests.id"),
        nullable=False
    )

    # Scores des 8 traits (correspondent aux colonnes INT de votre schéma SQL)
    ouverture_curiosite = db.Column(db.Integer, nullable=True)
    discipline_fiabilite = db.Column(db.Integer, nullable=True)
    influence_presence = db.Column(db.Integer, nullable=True)
    cooperation = db.Column(db.Integer, nullable=True)
    resilience_stress = db.Column(db.Integer, nullable=True)
    drive_motivation = db.Column(db.Integer, nullable=True)
    style_action = db.Column(db.Integer, nullable=True)
    alignement_strategique = db.Column(db.Integer, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now)