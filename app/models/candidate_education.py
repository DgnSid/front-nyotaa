from app.extensions import db
import uuid

class CandidateEducation(db.Model):
    __tablename__ = "candidate_educations"

    # Changement en String(36) pour correspondre au CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # La clé étrangère doit aussi être un String(36) pour correspondre à candidate_profiles.id
    candidate_profile_id = db.Column(
        db.String(36),
        db.ForeignKey("candidate_profiles.id"),
        nullable=False
    )

    education_level = db.Column(db.String(100), nullable=False)
    institution_name = db.Column(db.String(255), nullable=False)