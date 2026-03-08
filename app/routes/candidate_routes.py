import os
from werkzeug.utils import secure_filename
from app.models.candidate_document import CandidateDocument
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.candidate_account import CandidateAccount
from app.models.candidate_document import CandidateDocument
from app.models.candidate_profile import CandidateProfile
from app.models.candidate_education import CandidateEducation
from app.models.candidate_experience import CandidateExperience
from app.models.candidate_skill import CandidateSkill
from app.models.personality_profile import PersonalityProfile
from app.extensions import db
from app.models.test_session import TestSession

candidate_bp = Blueprint("candidate", __name__, url_prefix="/candidates")


@candidate_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()

    account = CandidateAccount.query.get(user_id)

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    education = CandidateEducation.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    experience = CandidateExperience.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    preferences = CandidateSkill.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    cv = CandidateDocument.query.filter_by(
        candidate_profile_id=profile.id,
        document_type="CV",
        is_active=True
    ).first()

    return jsonify({

        "first_name": account.first_name,
        "last_name": account.last_name,
        "email": account.email,
        "phone_number": account.phone_number,

        "city": profile.city,
        "country": profile.country,

        "education": {
            "education_level": education.education_level,
            "institution_name": education.institution_name
        } if education else None,

        "experience": {
            "has_prior_experience": experience.has_prior_experience,
            "industry": experience.industry,
            "years_of_experience": experience.years_of_experience,
            "specialization": experience.specialization
        } if experience else None,

        "preferences": {
            "target_industry": preferences.target_industry,
            "languages": preferences.languages,
            "target_job_title": preferences.target_job_title,
            "target_job_level": preferences.target_job_level,
            "expected_salary_min": preferences.expected_salary_min,
            "work_mode": preferences.work_mode,
            "open_to_relocation": preferences.open_to_relocation,
            "current_location": preferences.current_location,
            "nationality": preferences.nationality,
            "availability_date": preferences.availability_date
        } if preferences else None,

        "cv": {
            "file_name": cv.file_name,
            "storage_path": cv.storage_path
        } if cv else None

    })

@candidate_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()
    data = request.json

    account = CandidateAccount.query.get(user_id)

    account.first_name = data.get("first_name")
    account.last_name = data.get("last_name")
    account.phone_number = data.get("phone_number")

    db.session.commit()

    return jsonify({"message": "Profil mis à jour"})

@candidate_bp.route("/education", methods=["GET"])
@jwt_required()
def get_education():

    user_id = get_jwt_identity()

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({})

    education = CandidateEducation.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if not education:
        return jsonify({})

    return jsonify({
        "education_level": education.education_level,
        "institution_name": education.institution_name
    })

@candidate_bp.route("/education", methods=["PUT"])
@jwt_required()
def update_education():

    user_id = get_jwt_identity()
    data = request.json

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    education = CandidateEducation.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if not education:

        education = CandidateEducation(
            candidate_profile_id=profile.id,
            education_level=data.get("education_level"),
            institution_name=data.get("institution_name")
        )

        db.session.add(education)

    else:

        education.education_level = data.get("education_level")
        education.institution_name = data.get("institution_name")

    db.session.commit()

    return jsonify({"message": "Education mise à jour"})

@candidate_bp.route("/experiences", methods=["GET"])
@jwt_required()
def get_experiences():

    user_id = get_jwt_identity()

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({})

    experience = CandidateExperience.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if not experience:
        return jsonify({})

    return jsonify({
        "has_prior_experience": experience.has_prior_experience,
        "industry": experience.industry,
        "years_of_experience": experience.years_of_experience,
        "specialization": experience.specialization
    })

@candidate_bp.route("/experiences", methods=["PUT"])
@jwt_required()
def update_experiences():

    user_id = get_jwt_identity()

    data = request.json

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    experience = CandidateExperience.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if not experience:

        experience = CandidateExperience(
            candidate_profile_id=profile.id,
            has_prior_experience=data.get("has_prior_experience"),
            industry=data.get("industry"),
            years_of_experience=data.get("years_of_experience"),
            specialization=data.get("specialization")
        )

        db.session.add(experience)

    else:

        experience.has_prior_experience = data.get("has_prior_experience")
        experience.industry = data.get("industry")
        experience.years_of_experience = data.get("years_of_experience")
        experience.specialization = data.get("specialization")

    db.session.commit()

    return jsonify({"message": "Experience mise à jour"})

@candidate_bp.route("/documents/upload-cv", methods=["POST"])
@jwt_required()
def upload_cv():

    user_id = get_jwt_identity()

    file = request.files.get("cv")

    if not file:
        return jsonify({"error": "Aucun fichier"}), 400

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    filename = secure_filename(file.filename)

    upload_folder = "uploads/cv"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    # désactiver l'ancien CV
    old_docs = CandidateDocument.query.filter_by(
        candidate_profile_id=profile.id,
        document_type="CV",
        is_active=True
    ).all()

    for doc in old_docs:
        doc.is_active = False

    document = CandidateDocument(
        candidate_profile_id=profile.id,
        document_type="CV",
        file_name=filename,
        storage_path=file_path,
        mime_type=file.mimetype,
        file_size_bytes=os.path.getsize(file_path),
        is_active=True
    )

    db.session.add(document)

    db.session.commit()

    return jsonify({"message": "CV uploadé avec succès"})

@candidate_bp.route("/cv", methods=["GET"])
@jwt_required()
def get_cv():

    user_id = get_jwt_identity()

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    document = CandidateDocument.query.filter_by(
        candidate_profile_id=profile.id,
        document_type="CV",
        is_active=True
    ).first()

    if not document:
        return jsonify({})

    return jsonify({
        "file_name": document.file_name,
        "storage_path": document.storage_path
    })

@candidate_bp.route("/personality", methods=["GET"])
@jwt_required()
def get_personality_profile():

    user_id = get_jwt_identity()

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({})

    personality = PersonalityProfile.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if not personality:
        return jsonify({})

    return jsonify({
        "ouverture_curiosite": personality.ouverture_curiosite,
        "discipline_fiabilite": personality.discipline_fiabilite,
        "influence_presence": personality.influence_presence,
        "cooperation": personality.cooperation,
        "resilience_stress": personality.resilience_stress,
        "drive_motivation": personality.drive_motivation,
        "style_action": personality.style_action,
        "alignement_strategique": personality.alignement_strategique
    })

@candidate_bp.route("/preferences", methods=["GET"])
@jwt_required()
def get_preferences():

    user_id = get_jwt_identity()

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({})

    skill = CandidateSkill.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if not skill:
        return jsonify({})

    return jsonify({
        "target_industry": skill.target_industry,
        "languages": skill.languages,
        "target_job_title": skill.target_job_title,
        "target_job_level": skill.target_job_level,
        "expected_salary_min": skill.expected_salary_min,
        "work_mode": skill.work_mode,
        "open_to_relocation": skill.open_to_relocation,
        "current_location": skill.current_location,
        "nationality": skill.nationality,
        "availability_date": skill.availability_date
    })

@candidate_bp.route("/preferences", methods=["PUT"])
@jwt_required()
def update_preferences():

    user_id = get_jwt_identity()

    data = request.json

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    skill = CandidateSkill.query.filter_by(
        candidate_profile_id=profile.id
    ).first()

    if not skill:

        skill = CandidateSkill(
            candidate_profile_id=profile.id,
            target_industry=data.get("target_industry"),
            languages=data.get("languages"),
            target_job_title=data.get("target_job_title"),
            target_job_level=data.get("target_job_level"),
            expected_salary_min=data.get("expected_salary_min"),
            work_mode=data.get("work_mode"),
            open_to_relocation=data.get("open_to_relocation"),
            current_location=data.get("current_location"),
            nationality=data.get("nationality"),
            availability_date=data.get("availability_date")
        )

        db.session.add(skill)

    else:

        skill.target_industry = data.get("target_industry")
        skill.languages = data.get("languages")
        skill.target_job_title = data.get("target_job_title")
        skill.target_job_level = data.get("target_job_level")
        skill.expected_salary_min = data.get("expected_salary_min")
        skill.work_mode = data.get("work_mode")
        skill.open_to_relocation = data.get("open_to_relocation")
        skill.current_location = data.get("current_location")
        skill.nationality = data.get("nationality")
        skill.availability_date = data.get("availability_date")

    db.session.commit()

    return jsonify({"message": "Préférences mises à jour"})

