from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.services.test_service import TestService
from flask import request
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
import uuid
from app.extensions import db
from app.models.test_session import TestSession
from app.models.test_answer import TestAnswer
from app.models.personality_profile import PersonalityProfile
from app.models.candidate_profile import CandidateProfile
from app.models.personality_test import PersonalityTest
from app.services.scoring_service import ScoringService

test_bp = Blueprint(
    "test",
    __name__,
    url_prefix="/test"
)

@test_bp.route("/step/<int:step>", methods=["GET"])
@jwt_required()
def get_step(step):
    questions = TestService.get_questions_by_step(step)
    return jsonify({
        "step": step,
        "questions": questions
    })

@test_bp.route("/start", methods=["GET"])
@jwt_required()
def start_test():
    questions = TestService.get_all_questions()
    return jsonify({
        "questions": questions
    })

@test_bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_test():
    data = request.get_json()
    answers = data.get("answers")

    if not answers:
        return jsonify({"message": "Aucune réponse reçue"}), 400

    user_id = get_jwt_identity()
    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    # Empêcher de refaire le test
    existing = TestSession.query.filter_by(
        candidate_profile_id=profile.id,
        status="completed"
    ).first()
    if existing:
        return jsonify({"message": "Test already completed"}), 400

    test = PersonalityTest.query.filter_by(is_active=True).first()
    if not test:
        return jsonify({"message": "Aucun test actif trouvé"}), 404

    session = TestSession(
        candidate_profile_id=profile.id,
        personality_test_id=test.id,
        status="completed",
        completed_at=datetime.utcnow()
    )
    db.session.add(session)
    db.session.flush()

    # Sauvegarde des réponses AVEC le score
    for q_id, score in answers.items():
        answer = TestAnswer(
            test_session_id=session.id,
            test_question_id=uuid.UUID(q_id),
            answer_option_id=None,
            score=score  # ← CORRECTION : score était manquant
        )
        db.session.add(answer)

    # Calcul du score de personnalité
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
        alignement_strategique=scores.get("Alignement stratégique")
    )
    db.session.add(profile_result)
    db.session.commit()

    return jsonify({"message": "Test completed"}), 200

@test_bp.route("/status", methods=["GET"])
@jwt_required()
def get_test_status():
    user_id = get_jwt_identity()
    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({"status": "no_profile"}), 404

    session = TestSession.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if not session:
        return jsonify({"status": "not_started"})

    if session.status == "in_progress":
        return jsonify({"status": "in_progress"})

    result = PersonalityProfile.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if result:
        return jsonify({"status": "completed"})

    return jsonify({"status": "unknown"})
