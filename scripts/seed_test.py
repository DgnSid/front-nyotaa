import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db

from app.models.personality_test import PersonalityTest
from app.models.test_question import TestQuestion
from app.models.answer_option import AnswerOption

from app.utils.test_config import NYOTA_QUESTIONS, LIKERT_OPTIONS


app = create_app()


def get_step(question_id):

    if question_id <= 30:
        return 1
    elif question_id <= 46:
        return 2
    elif question_id <= 58:
        return 3
    else:
        return 4


with app.app_context():

    print("Seeding NYOTA personality test...")

    existing = PersonalityTest.query.first()

    if existing:
        print("Test already exists")
        exit()

    test = PersonalityTest(
        name="NYOTA Personality Test",
        version="v1",
        description="Test de personnalité NYOTA"
    )

    db.session.add(test)
    db.session.flush()

    for q in NYOTA_QUESTIONS:

        step = get_step(q["id"])

        question = TestQuestion(
            personality_test_id=test.id,
            question_text=q["text"],
            step=step,
            order_index=q["id"]
        )

        db.session.add(question)
        db.session.flush()

        for opt in LIKERT_OPTIONS:

            option = AnswerOption(
                test_question_id=question.id,
                label=opt["label"],
                score_value=opt["score"],
                order_index=opt["order"]
            )

            db.session.add(option)

    db.session.commit()

    print("72 questions inserted")
    print("360 answer options inserted")