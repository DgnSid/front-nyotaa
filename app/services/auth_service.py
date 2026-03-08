from app.models.candidate_account import CandidateAccount
from app.extensions import db
from app.extensions import bcrypt
from app.models.candidate_profile import CandidateProfile


class AuthService:

    @staticmethod
    def register(data):

        existing_user = CandidateAccount.query.filter_by(
            email=data["email"]
        ).first()

        if existing_user:
            return None, "Email already exists"

        password_hash = bcrypt.generate_password_hash(
            data["password"]
        ).decode("utf-8")

        user = CandidateAccount(
            email=data["email"],
            password_hash=password_hash,
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone_number=data.get("phone_number")
        )

        db.session.add(user)
        db.session.flush()   # important pour récupérer user.id

        # création automatique du profil
        profile = CandidateProfile(
            candidate_account_id=user.id
        )

        db.session.add(profile)

        db.session.commit()

        return user, None

    @staticmethod
    def login(email, password):

        user = CandidateAccount.query.filter_by(email=email).first()

        if not user:
            return None

        if not bcrypt.check_password_hash(user.password_hash, password):
            return None

        return user