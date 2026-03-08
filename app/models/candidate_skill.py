from app.extensions import db
import uuid

class CandidateSkill(db.Model):
    __tablename__ = "candidate_skills"

    # Utilisation de String(36) pour le CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # La clé étrangère doit être du même type que l'id de candidate_profiles
    candidate_profile_id = db.Column(
        db.String(36),
        db.ForeignKey("candidate_profiles.id"),
        nullable=False
    )

    target_industry = db.Column(db.String(150), nullable=True)
    languages = db.Column(db.String(255), nullable=True)
    target_job_title = db.Column(db.String(150), nullable=True)
    target_job_level = db.Column(db.String(100), nullable=True)
    expected_salary_min = db.Column(db.Integer, nullable=True)
    work_mode = db.Column(db.String(50), nullable=True)
    
    # TINYINT(1) dans MySQL
    open_to_relocation = db.Column(db.Boolean, nullable=True)
    
    current_location = db.Column(db.String(150), nullable=True)
    nationality = db.Column(db.String(100), nullable=True)
    
    # Correspond au VARCHAR(255) de votre schéma SQL
    availability_date = db.Column(db.String(255), nullable=True)