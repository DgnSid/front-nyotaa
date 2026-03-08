from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.document_service import DocumentService
from app.models.candidate_profile import CandidateProfile

document_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/documents"
)


@document_bp.route("/upload-cv", methods=["POST"])
@jwt_required()
def upload_cv():

    user_id = get_jwt_identity()

    profile = CandidateProfile.query.filter_by(
        candidate_account_id=user_id
    ).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    file = request.files.get("file")

    if not file:
        return jsonify({"error": "File missing"}), 400

    document = DocumentService.save_cv(file, profile.id)

    return jsonify({
        "message": "CV uploaded",
        "document_id": str(document.id)
    })