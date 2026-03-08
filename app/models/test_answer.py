from app.extensions import db
import uuid

class TestAnswer(db.Model):
    __tablename__ = "test_answers"

    # String(36) pour correspondre au CHAR(36) MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Toutes les clés étrangères doivent passer en String(36)
    test_session_id = db.Column(
        db.String(36),
        db.ForeignKey("test_sessions.id"),
        nullable=False
    )

    test_question_id = db.Column(
        db.String(36),
        db.ForeignKey("test_questions.id"),
        nullable=False
    )

    # Important : nullable=True est correct ici pour votre logique de score direct
    answer_option_id = db.Column(
        db.String(36),
        db.ForeignKey("answer_options.id"),
        nullable=True
    )

    score = db.Column(db.Integer, nullable=True)