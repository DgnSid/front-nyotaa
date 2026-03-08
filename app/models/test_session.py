from app.extensions import db
import uuid
from datetime import datetime

class TestSession(db.Model):
    __tablename__ = "test_sessions"

    # Changement en String(36) pour correspondre au CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Les clés étrangères doivent impérativement être des String(36)
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

    # VARCHAR(50) NOT NULL DEFAULT 'in_progress' dans votre schéma
    status = db.Column(db.String(50), nullable=False, default="in_progress")

    started_at = db.Column(db.DateTime, default=datetime.now)
    completed_at = db.Column(db.DateTime, nullable=True)