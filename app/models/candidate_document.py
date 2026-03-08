from app.extensions import db
import uuid
from datetime import datetime

class CandidateDocument(db.Model):
    __tablename__ = "candidate_documents"

    # Changement en String(36) pour le CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # La clé étrangère doit aussi être un String(36)
    candidate_profile_id = db.Column(
        db.String(36),
        db.ForeignKey("candidate_profiles.id"),
        nullable=False
    )

    document_type = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.String(500), nullable=False)
    
    file_size_bytes = db.Column(db.Integer, nullable=True)
    mime_type = db.Column(db.String(100), nullable=True)

    # TINYINT(1) dans MySQL
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, default=datetime.now)