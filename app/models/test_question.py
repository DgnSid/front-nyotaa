from app.extensions import db
import uuid
from datetime import datetime

class TestQuestion(db.Model):
    __tablename__ = "test_questions"

    # String(36) pour correspondre au CHAR(36) de MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # La clé étrangère doit aussi être une chaîne pour correspondre à personality_tests.id
    personality_test_id = db.Column(
        db.String(36),
        db.ForeignKey("personality_tests.id"),
        nullable=False
    )

    question_text = db.Column(db.Text, nullable=False)
    step = db.Column(db.Integer, nullable=False)
    order_index = db.Column(db.Integer, nullable=False)

    # Ajout d'une valeur par défaut pour la date de création
    created_at = db.Column(db.DateTime, default=datetime.now)