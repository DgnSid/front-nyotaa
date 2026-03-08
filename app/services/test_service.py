import uuid
from datetime import datetime
from typing import Dict, Any

from app.extensions import db
from app.models.candidate_profile import CandidateProfile
from app.models.personality_test import PersonalityTest
from app.models.test_session import TestSession
from app.models.test_answer import TestAnswer
from app.models.personality_profile import PersonalityProfile
from app.services.scoring_service import ScoringService
from app.models.test_question import TestQuestion


class TestService:
    """Service layer for personality test operations."""

    @staticmethod
    def submit_test(user_id: uuid.UUID, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Persist a completed test session and compute/store the personality profile.

        Params:
            user_id: CandidateAccount UUID retrieved from JWT in the route layer.
            answers: mapping of question_id (as string UUID) -> numeric score or option.
        Returns:
            dict payload with success message and created ids.
        Raises:
            ValueError if profile or active test not found, or invalid payload.
        """
        if not answers or not isinstance(answers, dict):
            raise ValueError("Invalid answers payload")

        profile = CandidateProfile.query.filter_by(candidate_account_id=user_id).first()
        if not profile:
            raise ValueError("Profile not found")

        test = PersonalityTest.query.filter_by(is_active=True).first()
        if not test:
            raise ValueError("Active personality test not found")

        session = TestSession(
            candidate_profile_id=profile.id,
            personality_test_id=test.id,
            status="completed",
            completed_at=datetime.utcnow(),
        )
        db.session.add(session)
        db.session.flush()  # to get session.id

        for q_id, _score in answers.items():
            answer = TestAnswer(
                test_session_id=session.id,
                test_question_id=uuid.UUID(q_id),
                answer_option_id=None,
            )
            db.session.add(answer)

        scores = ScoringService.calculate_scores(answers)

        profile_result = PersonalityProfile(
            candidate_profile_id=profile.id,
            personality_test_id=test.id,
            ouverture_curiosite=scores.get("Ouverture & Curiosité"),
            discipline_fiabilite=scores.get("Discipline & Fiabilité"),
            influence_presence=scores.get("Influence & Présence"),
            cooperation=scores.get("Coopération"),
            resilience_stress=scores.get("Résilience & Stress"),
            drive_motivation=scores.get("Drive & Motivation"),
            style_action=scores.get("Style d'action"),
            alignement_strategique=scores.get("Alignement stratégique"),
        )
        db.session.add(profile_result)

        db.session.commit()

        return {"message": "Test completed", "session_id": str(session.id), "profile_result_id": str(profile_result.id)}
    
    




    @staticmethod
    def get_all_questions():

        questions = TestQuestion.query.order_by(TestQuestion.order_index).all()

        return [
            {
                "id": str(q.id),
                "question_text": q.question_text,
                "step": q.step
            }
            for q in questions
        ]