from app.extensions import db
import uuid

class CandidateExperience(db.Model):
    __tablename__ = "candidate_experiences"

    # Changement en String(36) pour correspondre au CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # La clé étrangère doit correspondre au type de l'ID de candidate_profiles
    candidate_profile_id = db.Column(
        db.String(36),
        db.ForeignKey("candidate_profiles.id"),
        nullable=False
    )

    # SQLAlchemy convertira automatiquement le Boolean en TINYINT(1) pour MySQL
    has_prior_experience = db.Column(db.Boolean, nullable=True)

    industry = db.Column(db.String(150), nullable=True)
    years_of_experience = db.Column(db.Integer, nullable=True)
    specialization = db.Column(db.String(150), nullable=True)