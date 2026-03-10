from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.models.candidate_account import CandidateAccount
from flask_mail import Message
from app.extensions import mail
from app.utils.token import generate_reset_token
from app.utils.token import verify_reset_token
from werkzeug.security import generate_password_hash
from app.services.email_service import EmailService
from app.extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user, error = AuthService.register(data)
    if error:
        return jsonify({"error": error}), 400
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Account created successfully",
        "access_token": access_token
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = AuthService.login(data["email"], data["password"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "access_token": access_token
    })

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = CandidateAccount.query.get(user_id)
    return jsonify({
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    })

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    user = CandidateAccount.query.filter_by(email=email).first()
    if not user:
        return {"message": "User not found"}, 404
    token = generate_reset_token(email)
    frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:3000")
    reset_url = f"{frontend_url}/reset-password/{token}"
    msg = Message(
        "Réinitialisation du mot de passe",
        recipients=[email]
    )
    msg.body = f"""
Bonjour,
Pour réinitialiser votre mot de passe cliquez sur ce lien :
{reset_url}
Ce lien expire dans 1 heure.
"""
    EmailService.send_password_reset(email, reset_url)
    return {"message": "Password reset email sent"}

@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        return {"message": "Invalid or expired token"}, 400
    data = request.get_json()
    new_password = data.get("password")
    user = CandidateAccount.query.filter_by(email=email).first()
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return {"message": "Password updated successfully"}
