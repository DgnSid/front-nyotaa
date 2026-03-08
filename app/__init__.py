import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from app.config import Config
from app.extensions import db, mail, bcrypt, migrate

def create_app():
    app = Flask(__name__)

    # Chargement de la configuration
    app.config.from_object(Config)

    # Configuration JWT (sécurité)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    # CORS — autoriser le frontend React (Vite sur 5173 et production)
    CORS(
        app,
        origins=["http://localhost:5173", "http://localhost:3000", "https://nyota-front-fin-master.vercel.app", "https://www.nyota.co", "https://nyota.co"],  # Remplacez par l'URL Vercel
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=True,
        vary_header=True
    )

    # Initialisation JWT
    jwt = JWTManager(app)

    # Gestion des erreurs JWT
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({"message": "Token manquant"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({"message": "Token invalide"}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token expiré"}), 401

    # Initialisation des extensions
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Import des Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.test_routes import test_bp
    from app.routes.candidate_routes import candidate_bp

    # Enregistrement des routes
    # Les blueprints portent deja leur propre url_prefix dans leurs fichiers routes.
    app.register_blueprint(auth_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(candidate_bp)

    return app
