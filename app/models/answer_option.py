from app.extensions import db
import uuid

class AnswerOption(db.Model):
    __tablename__ = "answer_options"

    # On utilise String(36) pour correspondre au CHAR(36) de votre schéma MySQL
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    test_question_id = db.Column(
        db.String(36),
        db.ForeignKey("test_questions.id"),
        nullable=False
    )

    label = db.Column(db.String(255), nullable=False)
    score_value = db.Column(db.Integer, nullable=False)
    order_index = db.Column(db.Integer, nullable=False)

    # Optionnel : Ajouter une relation pour faciliter les requêtes
    # question = db.relationship('TestQuestion', backref=db.backref('options', lazy=True))