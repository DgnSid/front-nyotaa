import os
import uuid

from werkzeug.utils import secure_filename
from flask import current_app

from app.extensions import db
from app.models.candidate_document import CandidateDocument

# Liste des formats autorisés
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
ALLOWED_MIMETYPES = {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}

class DocumentService:
    @staticmethod
    def is_allowed_file(file):
        # Vérification de l'extension
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        # Vérification du type MIME
        return ext in ALLOWED_EXTENSIONS and file.mimetype in ALLOWED_MIMETYPES

class DocumentService:

    @staticmethod
    def save_cv(file, candidate_profile_id):
        if not DocumentService.is_allowed_file(file):
            return {"error": "Format de fichier non autorisé"}, 400

        filename = secure_filename(file.filename)

        unique_name = f"{uuid.uuid4()}_{filename}"

        # 1. On définit le dossier de destination (ex: uploads/cv)
        # Assure-toi que UPLOAD_FOLDER dans config.py est "uploads"
        directory = os.path.join(current_app.config["UPLOAD_FOLDER"], "cv")

        # 2. CRUCIAL : Crée le dossier s'il n'existe pas physiquement
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # 3. On définit le chemin complet du fichier
        upload_path = os.path.join(directory, unique_name)

        # 4. Sauvegarde physique sur le disque
        file.save(upload_path)

        document = CandidateDocument(
            candidate_profile_id=candidate_profile_id,
            document_type="CV",
            file_name=filename,
            storage_path=os.path.join("cv", unique_name),
            file_size_bytes=os.path.getsize(upload_path),
            mime_type=file.mimetype
        )

        db.session.add(document)
        db.session.commit()

        return document