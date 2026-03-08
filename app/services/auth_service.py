from app.models.candidate_account import CandidateAccount
from app.extensions import db
from app.extensions import bcrypt
from app.models.candidate_profile import CandidateProfile


class AuthService:

    @staticmethod
    def register(data):
        try:
            if not data:
                return None, "Request body is required"

            required_fields = ["email", "password", "first_name", "last_name"]
            missing = [
                field for field in required_fields
                if not str(data.get(field, "")).strip()
            ]
            if missing:
                return None, f"Missing required fields: {', '.join(missing)}"

            email = data["email"].strip().lower()

            existing_user = CandidateAccount.query.filter_by(
                email=email
            ).first()

            if existing_user:
                return None, "Email already exists"

            password_hash = bcrypt.generate_password_hash(
                data["password"]
            ).decode("utf-8")

            user = CandidateAccount(
                email=email,
                password_hash=password_hash,
                first_name=data["first_name"],
                last_name=data["last_name"],
                phone_number=data.get("phone_number")
            )

            db.session.add(user)
            db.session.flush()   # important pour récupérer user.id

            valid_genders = {"Homme", "Femme", "Autre"}
            gender = data.get("gender")
            if gender not in valid_genders:
                gender = None

            # création automatique du profil
            profile = CandidateProfile(
                candidate_account_id=user.id,
                gender=gender
            )

            db.session.add(profile)

            db.session.commit()

            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def login(email, password):

        user = CandidateAccount.query.filter_by(email=email).first()

        if not user:
            return None

        if not bcrypt.check_password_hash(user.password_hash, password):
            return None

        return user
