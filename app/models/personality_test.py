from app.extensions import db
import uuid
from datetime import datetime

class PersonalityTest(db.Model):
    __tablename__ = "personality_tests"

    # Changement en String(36) pour correspondre au CHAR(36) de MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # TINYINT(1) NOT NULL DEFAULT 1 dans votre schéma SQL
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Utilisation de datetime.now pour la cohérence avec le serveur local
    created_at = db.Column(db.DateTime, default=datetime.now)