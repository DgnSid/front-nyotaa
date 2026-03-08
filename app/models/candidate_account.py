from app.extensions import db
import uuid
from datetime import datetime

class CandidateAccount(db.Model):
    __tablename__ = "candidate_accounts"

    # Changement en String(36) pour correspondre au CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # SQLAlchemy gérera automatiquement le Boolean vers TINYINT(1) pour MySQL
    email_verified = db.Column(db.Boolean, nullable=False, default=False)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Utilisation de datetime.now pour éviter les décalages si votre serveur MySQL est en local
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.now, 
        onupdate=datetime.now
    )